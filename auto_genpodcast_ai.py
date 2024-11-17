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


# load_dotenv(DOTENVPATH)
# Load the environment variables from the .env file
load_dotenv(".env")
DESTINATAIRES_TECH = os.environ.get("DESTINATAIRES_TECH")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
ACAST_API_KEY = os.environ.get("ACAST_API_KEY")
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
            response = client.chat.completions.create(
                model=model,
                temperature=0.01,
                max_tokens=max_tokens,
                messages=[
                    {'role': 'user', 'content': execprompt},
                    {'role': 'system', 'content': system}
                ]
            )
            message = response.choices[0].message.content
            print(str(datetime.now()) + " : " + "Réponse : " + str(message) + "\n\n")
            return message.strip()

        except Exception as e:
            error_code = type(e).__name__
            error_reason = str(e)
            attempts += 1
            print(f"Erreur : {error_code} - {error_reason}. Nouvel essai dans {str(attempts * 2)} secondes...")
            time.sleep(attempts * 2)

    print("Erreur : Echec de la création de la completion après 10 essais")
    sys.exit()




from pydub import AudioSegment
import os

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





## PODCAST VEILLE #1 ##
# Génération d'une liste de livres pour veille podcast
url_list = ["https://www.artificialintelligence-news.com/"
            , "https://venturebeat.com/category/ai/"
            , "https://www.wired.com/tag/artificial-intelligence/"
            , "https://www.forbes.com/ai/"
            , "https://www.theguardian.com/technology/artificialintelligenceai"
            , "https://www.nature.com/natmachintell/"
            , "https://towardsdatascience.com/"
            , "https://openai.com/news/"
            , "https://neurips.cc/"
            , "https://www.theverge.com/ai-artificial-intelligence"
            , "https://techcrunch.com/tag/artificial-intelligence/"]


# Setting the locale to French
#locale.setlocale(locale.LC_TIME, 'fr_FR')

# Getting the current date
current_date = datetime.now()



# Formatting the date as "dd month yyyy"
formatted_date = current_date.strftime("%d %B %Y")
        
command = "Nous sommes le " + formatted_date + "\nA partir du texte suivant entre ___ , contenant les derniers articles sur l'IA, \
        extraire TOUS les articles datant d'il y a moins de 24 heures et les traduire en français. \
        La traduction doit avoir pour longueur le nombre de signes approximatif de l'article source. \
        Commencer par le titre traduit en français et la date de l'article. Citer la source. \
        Toujours utiliser la forme d'un contenu journalistique pour la traduction. \
        N'hésite pas à développer si besoin afin d'expliquer les termes techniques ou jargonneux à une audience grand public \
        Aucun article datant de moins de 24 heures ne doit etre oublié. Ne converse pas. Ne conclue pas. \
        Ne pas générer d'introduction ni de conclusion, juste l'articke traduit'. \
        Si il n'y a pas d'article, ne pas dire qu'il n'y pas d'article, renvoyer une chaine vide.\
        Ne pas commencer par Voici le compte rendu de l'artcie... Mais directement démarrer par l'article'. Respecter ces consignes strictement. "
     
#generation de la veille
model=DEFAULT_MODEL
responses = [process_url(command, url, model,"","") for url in url_list]
res = "<br><br>".join(responses)

text_veille = str(res.replace("```html", "")).replace("```", "")

print(text_veille)



prompt =    "A partir du texte suivant générer un script de podcast en français d'au moins 30000 signes, \
            pret à etre lu par Michel Lévy Provençal le host de //L'IA aujourd'hui : le podcast de l'IA par l'IA qui vous permet de rester à la page !// \
            Chaque news doit etre assez développée au moins 6000 signes, elle doit contenr les détails, exemples, sources contenues dans l'a news originale pour être pertinente et compréhensible par un auditeur non expert. Si besoin expliquer les acronymes ou les termes techniques sans résumer chaque article. \
            Si tu n'as pas assez d'info sur un article, le zapper. Attention si la news n'est pas originale, c'est à dire qu'elle traite d'information générique, la zapper. \
            Toujours démarrer par cette petite introduction, puis enchainer tout de suite aprés sur le script. Attention, ne jamais démarrer en disant, voici le script du podcast. toujours démarrer directement. \
            La conclusion du script doit etre courte et toujours sous cette forme : //Voilà qui conclut notre épisode d'aujourd'hui. Merci de nous avoir rejoints et n'oubliez pas de vous abonner pour ne manquer aucune de nos discussions passionnantes. À très bientôt dans L'IA aujourd'hui !// \
            "

#text_final = lib__agent_buildchronical.execute(prompt, '', text_veille, model)
text_final = call_llm(prompt, text_veille, "", model, 14000)

print(text_final)


#envoi de la newsletter
#title = "AI PODCAST : veille sur l'IA"
#email = "contact@brightness.fr"
#lib__agent_buildchronical.mail_html(title, text_final, email)


# Task : task7

# Appeler l'API elevenLabs et construire un podcast



# text_final = "Bienvenue dans //L'IA aujourd'hui : le podcast de l'IA par l'IA qui vous permet de rester à la page !// Aujourd'hui, nous allons explorer deux sujets fascinants et d'actualité : l'incertitude des travailleurs étrangers dans le secteur technologique américain face aux politiques d'immigration, et la question de savoir si l'intelligence artificielle peut remplacer les traducteurs humains."
# creation de l'audio
voice_id = "FL36qzLoYbdCLMM5R9rF" # MLP FL36qzLoYbdCLMM5R9rF
# voice_id = "TxGEqnHWrfWFTfGW9XjX" # Josh
# randint = randint(0, 100000)
# filename = PODCASTS_PATH + "podcast" + str(randint) + ".mp3"
# texttospeech(text, voice_id, filename)

randint = random.randint(0, 100000)
final_filename = PODCASTS_PATH + "final_podcast" + str(randint) + str(date.today()) + ".mp3"

# gestion des intonations.
lib__agent_buildchronical.split_text(text_final, limit=300)
lib__agent_buildchronical.convert_and_merge(text_final, voice_id, final_filename)

# titre = "Dailywatch \n du \n" + str(date.today())
# input_audiofile = filename
# output_videofile = "datas/podcast" + str(randint) + ".mp4"

## creation de la video avec les fichiers d'entrée appropriés
# create_video_with_audio(input_audiofile, titre, output_videofile)


titre = "L'IA aujourd'hui épisode du " + str(date.today())
text = text_final
audio = final_filename
email = "michel@brightness.fr"  # Remplacez 'destinataire' par 'email'
subtitle = "L'IA aujourd'hui : le podcast de l'IA par l'IA qui vous permet de rester à la page !"
# Appel de la fonction mailaudio
lib__agent_buildchronical.mailaudio(titre, audio, text, email)



# Conversion d'un fichier audio au format Acast
input_file = audio
output_file = input_file
#output_file = "datas/podcasts/datas_podcasts_final_podcast451932024-11-16_acast.mp3"

# Appel de la fonction de Conversion
#converted_file = convert_audio_to_acast_format(input_file, output_file)


#POST D'UN EPISODE SUR ACAST
print(f"Clé API utilisée : {ACAST_API_KEY}")
print("\n\n\n")
headers = {
    "x-api-key": ACAST_API_KEY
}

# URL de l'API Acast
url = "https://open.acast.com/rest/shows/67328a919e7b27e0ac078578/episodes"

response = requests.get("https://open.acast.com/rest/shows/67328a919e7b27e0ac078578", headers=headers)
print(response.status_code, response.text)
print("/n/n/n")


# Charge utile
payload = {
    'title': titre,
    'subtitle': subtitle,
    'status': 'published',
    'summary': text,    
}




# Fichier audio à envoyer (fichier converti)
file_path = output_file

if not os.path.exists(file_path):
    raise FileNotFoundError(f"Le fichier {file_path} n'existe pas ou le chemin est incorrect.")
else: 
    print(f"Le fichier {file_path} existe.")
    print("\n\n\n")
    
if os.path.getsize(file_path) == 0:
    raise ValueError(f"Le fichier {file_path} est vide.")
else:
    print(f"Le fichier {file_path} existe et a une taille de {os.path.getsize(file_path)} octets.") 
    print("\n\n\n")
# Préparez les fichiers à envoyer

files = [
    ('audio', (os.path.basename(file_path), open(file_path, 'rb'), 'audio/mpeg'))
]

# Effectuez la requête
response = requests.post(url, headers=headers, data=payload, files=files)

# Affichez la réponse
print(f"Statut : {response.status_code}")
print("\n\n\n")
print(f"En-têtes de la réponse : {response.headers}")
print("\n\n\n")
print(f"Réponse : {response.text}")



