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
import google.generativeai as genai
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
    
    genai.configure(api_key=GEMINI_API_KEY)

    # Create the model
    generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": max_tokens,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-thinking-exp-1219",
        generation_config=generation_config,
        system_instruction="À partir de maintenant, réponds directement à ma question sans introduction.\"",
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message("Context : " + context + "\n" + input_data + "\n" + "Query : " + prompt)

    for content in response:
        print(content)
        yield content



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
    token_nb = 2000
    
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
                
                
                if model == "o1-preview":
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
                        
