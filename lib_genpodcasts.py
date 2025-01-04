import lib__agent_buildchronical
import random
import datetime
from datetime import date
from datetime import datetime
import locale
import lib__transformers
import json
import lib__embedded_context
import os
import requests
import time
import openai
from urllib.parse import unquote
from queue import Queue
from datetime import *
from lib__env import *
from openai import OpenAI
import sys
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import json
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import requests
from pydub import AudioSegment
import os
import google.generativeai as genai
import anthropic


# load_dotenv(DOTENVPATH)
# Load the environment variables from the .env file
load_dotenv(".env")
DESTINATAIRES_TECH = os.environ.get("DESTINATAIRES_TECH")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
ACAST_API_KEY = os.environ.get("ACAST_API_KEY")
XAI_KEY = os.environ.get("XAI_KEY")
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
model = DEFAULT_MODEL


def upload_and_get_public_url(service, file_path, file_name=None):
    """
    Uploads a file to Google Drive and returns its public URL.
    
    Parameters:
        service: The Google Drive API service instance.
        file_path: The local path to the file to upload.
        file_name: Optional. The name to use for the file in Google Drive. If not provided, the original file name is used.
    
    Returns:
        str: The public URL of the uploaded file.
    """
    # Use the original file name if no custom name is provided
    if not file_name:
        file_name = file_path.split("/")[-1]

    # Metadata for the file
    file_metadata = {'name': file_name}

    # Prepare the file for upload
    media = MediaFileUpload(file_path, resumable=True)

    try:
        # Upload the file to Google Drive
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        # Get the file ID of the uploaded file
        file_id = file.get('id')

        # Set the file to be publicly accessible
        service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        # Generate the public URL
        public_url = f"https://drive.google.com/uc?id={file_id}&export=download"
        return public_url

    except Exception as e:
        raise Exception(f"An error occurred: {e}")






def process_url(command, url, model, site="", input_data=""):
    """
    This function takes a command, a url and a model as input and generates a response based on the command and the content of the url
    """
    content = lib__agent_buildchronical.fetch_and_parse_urls(url)
    content = content.replace('\n', '')
    prompt = command + "\n ___ " + content + "\n ___ \n"
    # print("Prompt : " + prompt)
    input_data = ""
    site = ""
    model=model
    res = lib__agent_buildchronical.execute(prompt, site, input_data, model)
    return res



def call_llm(prompt, context, input_data, model=DEFAULT_MODEL, max_tokens=10000):

    attempts = 0
    execprompt = "Context : " + context + "\n" + input_data + "\n" + "Query : " + prompt
    system = "Je suis un assistant parlant parfaitement le français et l'anglais."

    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    while attempts < 10:
        try:
            if model=="gpt-4o":
                response = client.chat.completions.create(
                model=model,
                temperature=0.01,
                max_tokens=max_tokens,
                messages=[
                    {'role': 'user', 'content': execprompt},
                    {'role': 'system', 'content': system}
                ]
            )
            else:
                response = client.chat.completions.create(
                model=model,
                messages=[
                    {'role': 'user', 'content': execprompt}
                ]
            )
            message = response.choices[0].message.content
            #print(str(datetime.now()) + " : " + "Réponse : " + str(message) + "\n\n")
            return message.strip()

        except Exception as e:
            error_code = type(e).__name__
            error_reason = str(e)
            attempts += 1
            print(f"Erreur : {error_code} - {error_reason}. Nouvel essai dans {str(attempts * 2)} secondes...")
            time.sleep(attempts * 2)

    print("Erreur : Echec de la création de la completion après 10 essais")
    sys.exit()


def call_deepseek_llm(prompt, context, input_data, model=DEFAULT_MODEL, max_tokens=10000):

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
    return message.strip()


def call_grok_llm(prompt, context, input_data, model="grok-2-latest", max_tokens=8192):
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
    response_content = completion.choices[0].message.content
    return str(response_content)


def call_google_llm(prompt, context, input_data, model="gemini-2.0-flash-thinking-exp-1219", max_tokens=8192):
    
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

    print(response.text)
    return response.text



def call_anthropic_llm(prompt, context, input_data, model="claude-3-5-sonnet-20241022", max_tokens=8192):

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
    
    return message.content[0].text



def convert_audio_to_acast_format(input_file, output_file):
    """
    Convert an audio file to the Acast-compatible format.
    
    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to save the converted audio file.

    Returns:
        str: Path to the converted audio file.
    """
    try:
        # Charger le fichier audio
        audio = AudioSegment.from_file(input_file)

        # Convertir avec les paramètres requis
        audio.export(
            output_file,
            format="mp3",
            parameters=["-ar", "44100", "-b:a", "128k"]
        )
        print(f"Fichier converti avec succès : {output_file}")
        return output_file
    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")
        return None
