# -*- coding: utf-8 -*-
'''
Filename: generatechatcompletion.py
Author: Michel Levy Provencal
Description: This file defines two functions, generate_chat_completion and generate_chat, that use OpenAI's API to generate chat responses. It uses environmental variables for API keys and includes a default model of "gpt-4" if no model is specified in the function parameters.
'''

import openai  # Import the openai API package
import os  # Import os module for interacting with the operating system
from dotenv import load_dotenv  # Import dotenv module for loading .env files
import lib__anthropic
import lib__hfmodels
from huggingface_hub import InferenceClient
#from googleapiclient.http import MediaFileUpload
#from google.oauth2.service_account import Credentials
#from googleapiclient.discovery import build
import requests
from pydub import AudioSegment
import os
#import google.generativeai as genai
import anthropic
from openai import OpenAI


# Load the environment variables from the .env file
from dotenv import load_dotenv
import os
load_dotenv(".env")

DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
model = DEFAULT_MODEL

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")
SENDGRID_KEY = os.environ.get("SENDGRID_KEY")
XAI_KEY = os.environ.get("XAI_KEY")
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")


# Set the OpenAI API key from the environment variables
openai.api_key = os.environ['OPEN_AI_KEY']



def streamcall_deepseek_llm(prompt, context, input_data, model=DEFAULT_MODEL, max_tokens=10000):

    execprompt = "Context : " + context + "\n" + input_data + "\n" + "Query : " + prompt
    system = "Je suis un assistant parlant parfaitement le français et l'anglais."

    # Please install OpenAI SDK first: `pip3 install openai`
    client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": execprompt},
            {"role": "user", "content": system},
        ],
        stream=False
    )
    message = response.choices[0].message.content
    for content in message:
        print(content)
        yield content


def streamcall_grok_llm(prompt, context, input_data, model="grok-2-latest", max_tokens=8192):
    from openai import OpenAI
    # Remplacez par votre clé API
    XAI_API_KEY = XAI_KEY
    client = OpenAI(
        api_key=XAI_API_KEY,
        base_url="https://api.x.ai/v1",
    )

    # Exemple d'entrée pour le modèle
    prompt = [
        {"role": "system", "content": "Vous êtes un assistant."},
        {"role": "user", "content": "Context : " + context + "\n" + input_data + "\n" + "Query : " + prompt}
    ]

    # Créez une complétion
    completion = client.chat.completions.create(
        model="grok-2-latest",  # Spécifiez le modèle ici
        messages=prompt,
        max_tokens=max_tokens,  # Limitez le nombre de tokens générés
        temperature=0.2,  # Réglez la créativité du modèle
        top_p=1.0,       # Utilisez la valeur top-p pour contrôler la diversité
        n=1,             # Nombre de réponses à générer
        stop=None        # Optionnel : spécifiez un ou plusieurs arrêts pour le texte
    )

    # Affichez la réponse générée
    response = completion.choices[0].message.content
    for content in response:
            print(content)
            yield content



def streamcall_google_llm(prompt, context, input_data, model="gemini-2.0-flash-thinking-exp-1219", max_tokens=8192):
    """
    Appel de Gemini 2.0 en mode streaming, en reprenant la logique existante dans lib_genpodcasts.py.
    On recrée la structure de streaming manualisé (chunk par chunk), car l’API ne semble
    pas proposer un flux natif comme pour OpenAI/Anthropic/Grok.
    """

    import google.generativeai as genai
    from math import ceil

    # Configuration du modèle (gemini-2.0-flash-thinking-exp-1219, etc.)
    genai.configure(api_key=os.environ.get('GEMINI_API_KEY', None))

    generation_config = {
        "temperature": 0.1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": max_tokens,
        "response_mime_type": "text/plain",
    }

    # Création du modèle
    gemini_model = genai.GenerativeModel(
        model_name=model,
        generation_config=generation_config,
        system_instruction="À partir de maintenant, réponds directement à ma question sans introduction."
    )

    # Ouverture de la session de chat
    chat_session = gemini_model.start_chat(history=[])

    # Construction du prompt
    execprompt = f"Context : {context}\n{input_data}\nQuery : {prompt}"

    # Envoi du message (Gemini ne fournit pas un stream direct, on stream donc manuellement)
    response = chat_session.send_message(execprompt)
    full_text = response.text  # Gemini renvoie la réponse complète

    # On choisit une taille de chunk, par exemple 100 caractères
    chunk_size = 100
    total_chunks = ceil(len(full_text) / chunk_size)

    for i in range(total_chunks):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, len(full_text))
        chunk = full_text[start_idx:end_idx]
        print(chunk, end="", flush=True)
        yield chunk



def streamcall_anthropic_llm(prompt, context, input_data, model="claude-3-5-sonnet-20241022", max_tokens=8192):

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=ANTHROPIC_API_KEY,
    )
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": "Context : " + context + "\n" + input_data + "\n" + "Query : " + prompt}
        ]
    )
    
    
    for content in message.content[0]:
        print(content)
        yield content





def extract_context(text, model):
    """
    Extraire un contexte de 'text' basé sur la limite spécifiée.

    Si la longueur de 'text' est inférieure à 'limit', renvoie le texte complet.
    Sinon, renvoie une combinaison des premiers et derniers caractères de 'text'
    avec ' [...] ' inséré au milieu pour indiquer la coupure.

    :param text: La chaîne de caractères à traiter.
    :param limit: La limite de longueur pour le contexte extrait.
    :return: La chaîne de caractères traitée.
    """
    token_nb = 10000
    
    if model == "claude-2":
        token_nb = 100000 
    if model == "claude-3":
        token_nb = 100000 
    if model == "gpt-4":
        token_nb = 8000
    if model == "gpt-4-turbo-preview":
        token_nb = 128000
    if model == "gpt-4-turbo":
        token_nb = 128000
    if model == DEFAULT_MODEL:
        token_nb = 250000
    if model == "gpt-3.5-turbo-16k": 
        token_nb = 16000
    if model == "hf":
        token_nb = 2000  
    if model == "mistral":
        token_nb = 2000      
    
    if token_nb > 2000:
        limit = (int(token_nb)*2) - 4000
    else:
        limit = int((int(token_nb)*2)/2)
    
    if len(text) < limit:
        return text
    else:
        half_limit_adjusted = limit // 2 - 4
        return text[:half_limit_adjusted] + ' [...] ' + text[-half_limit_adjusted:]


"""
# Function to generate chat completions
def generate_chat_completion(consigne, texte, model=DEFAULT_MODEL, model_url=os.environ['MODEL_URL']):
    texte = extract_context(texte, model)
    client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    prompt = str(consigne + " : " + texte)  # Construct the prompt from the given consigne and texte

     
    if model == "claude-2":
        model = "claude-2.1" #update to claude 2.1
        response = lib__anthropic.generate_chat_completion_anthropic(consigne, texte, model)
        for content in response:
            print(content)
            yield content
            
    else:
        if model == "claude-3":
            model = "claude-3-opus-20240229" #update to claude 3
            response = lib__anthropic.generate_chat_completion_anthropic(consigne, texte, model)
            for content in response:
                print(content)
                yield content
            
        else:
                
            if model == "hf":
                #prompt = str(consigne + "\n Le texte : ###" + texte + " ###\n")  # Construct the prompt from the given consigne and texte
                prompt = str(consigne + "\n" + texte)  # Construct the prompt from the given consigne and texte
                prompt = "<s>[INST]" + prompt + "[/INST]"
                print("Prompt : " + prompt + "\n")
                print("Model URL : " + model_url + "\n" + "HF TOKEN : " + os.environ['HF_API_TOKEN'] + "\n")
                
                client = InferenceClient(model_url, token=os.environ['HF_API_TOKEN'])
                response = client.text_generation(
                    prompt,
                    max_new_tokens=1024,
                    stream=True
                )
                
                for result in response:
                    yield result

            
            else:
                
                # Use OpenAI's Chat Completion API
                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {'role': 'system', 'content': "Je suis un assistant parlant parfaitement le français et l'anglais capable de corriger, rédiger, paraphraser, traduire, résumer, développer des textes."},
                        {'role': 'user', 'content': prompt}
                    ],
                    temperature=0,
                    stream=True
                )
                
                for message in completion:
                # Vérifiez ici la structure de 'chunk' et extrayez le contenu
                # La ligne suivante est un exemple et peut nécessiter des ajustements
                
                    if message.choices[0].delta.content: 
                        text_chunk = message.choices[0].delta.content 
                        print(text_chunk, end="", flush="true")
                        yield text_chunk
                    
"""              


                        
                        
                        
                        
                        
"""
# Function to generate chat
def generate_chat(consigne, texte, system="", model=DEFAULT_MODEL, temperature=1):
    prompt = str(consigne + " : " + texte)  # Construct the prompt from the given consigne and texte
    # Call the OpenAI API to create a chat
    print("Model : " + model + "\n")
    print("Temperature : " + str(temperature) + "\n")
    client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    texte = extract_context(texte, model)
    
    if model == "claude-2":
        model = "claude-2.1" #update to claude 2.1
        response = lib__anthropic.generate_chat_completion_anthropic(consigne, texte, model, temperature)
        for content in response:
            print(content)
            yield content
            
    else:
        if model == "claude-3":
            model = "claude-3-opus-20240229" #update to claude 3
            response = lib__anthropic.generate_chat_completion_anthropic(consigne, texte, model, temperature)
            for content in response:
                print(content)
                yield content
    
        else:
            if model == "hf":
                prompt = str(consigne + "\n" + texte)  # Construct the prompt from the given consigne and texte
                #prompt = str(consigne + "\n Le texte : ###" + texte + " ###\n")  # Construct the prompt from the given consigne and texte
                prompt = "<s>[INST]" + prompt + "[/INST]"
                
                print("Prompt : " + prompt + "\n")
                print("Model URL : " + os.environ['MODEL_URL'] + "\n" + "HF TOKEN : " + os.environ['HF_API_TOKEN'] + "\n")
                
                client = InferenceClient(os.environ['MODEL_URL'], token=os.environ['HF_API_TOKEN'])
                response = client.text_generation(
                    prompt,
                    max_new_tokens=1024,
                    stream=True
                )
                
                for result in response:
                    yield result


            else:   
                
                
                if model == "o1-preview" or model == "o1" or model == "o3-mini":
                    completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": system + "\n" + prompt}
                    ],
                    stream=True
                
)
                else:
                
                    completion = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=temperature, # set to 0.4 for scenario planning
                        stream=True
                    )

                for message in completion:
                # Vérifiez ici la structure de 'chunk' et extrayez le contenu
                # La ligne suivante est un exemple et peut nécessiter des ajustements
                
                    if message.choices[0].delta.content: 
                        text_chunk = message.choices[0].delta.content 
                        print(text_chunk, end="", flush="true")
                        yield text_chunk
                        
    """
    
    
    
    
def generate_chat(consigne, texte, system="", model=DEFAULT_MODEL, temperature=0):
    prompt = str(consigne + " : " + texte)  # Construction du prompt
    print("Model : " + model + "\n")
    print("Temperature : " + str(temperature) + "\n")

    client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    texte = extract_context(texte, model)

    if model == "claude-2":
        model_updated = "claude-2.1"
        response = lib__anthropic.generate_chat_completion_anthropic(
            consigne, texte, model_updated, temperature
        )
        for content in response:
            print(content)
            yield content

    elif model == "claude-3":
        model_updated = "claude-3-opus-20240229"
        response = lib__anthropic.generate_chat_completion_anthropic(
            consigne, texte, model_updated, temperature
        )
        for content in response:
            print(content)
            yield content

    elif model == "hf":
        prompt_hf = str(consigne + "\n" + texte)
        prompt_hf = "<s>[INST]" + prompt_hf + "[/INST]"
        print("Prompt : " + prompt_hf + "\n")
        print("Model URL : " + os.environ['MODEL_URL'] + "\n" + "HF TOKEN : " + os.environ['HF_API_TOKEN'] + "\n")

        client_hf = InferenceClient(os.environ['MODEL_URL'], token=os.environ['HF_API_TOKEN'])
        response = client_hf.text_generation(
            prompt_hf,
            max_new_tokens=1024,
            stream=True
        )
        for result in response:
            yield result

    elif model == "google":
        # Appel au modèle Gemini 2.0
        response_stream = streamcall_google_llm(
            prompt=consigne,
            context="",
            input_data=texte,
            model="gemini-2.0-flash-thinking-exp-1219",
            max_tokens=8192
        )
        for chunk in response_stream:
            yield chunk

    elif model == "grok":
        # Appel au modèle Grok
        response_stream = streamcall_grok_llm(
            prompt=consigne,
            context="",
            input_data=texte,
            model="grok-2-latest",
            max_tokens=8192
        )
        for chunk in response_stream:
            yield chunk

    elif model == "deepseek":
        # Appel au modèle Deepseek
        response_stream = streamcall_deepseek_llm(
            prompt=consigne,
            context="",
            input_data=texte,
            model=DEFAULT_MODEL,  # ou "deepseek-chat" si nécessaire
            max_tokens=10000
        )
        for chunk in response_stream:
            yield chunk

    elif model in ["o1-preview", "o1", "o3-mini"]:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": system + "\n" + prompt}
            ],
            stream=True
        )
        for message in completion:
            if message.choices[0].delta.content:
                text_chunk = message.choices[0].delta.content
                print(text_chunk, end="", flush=True)
                yield text_chunk

    else:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            stream=True
        )
        for message in completion:
            if message.choices[0].delta.content:
                text_chunk = message.choices[0].delta.content
                print(text_chunk, end="", flush=True)
                yield text_chunk