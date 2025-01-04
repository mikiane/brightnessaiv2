from pydub import AudioSegment
import lib_genpodcasts
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

load_dotenv(".env")
DESTINATAIRES_TECH = os.environ.get("DESTINATAIRES_TECH")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
ACAST_API_KEY = os.environ.get("ACAST_API_KEY")
#model = DEFAULT_MODEL


## PODCAST VEILLE #1 ##
# Génération d'une liste de livres pour veille podcast
rss_list = ["https://flint.media/bots/feeds/eyJhbGciOiJIUzI1NiJ9.eyJib3RfaWQiOjEyNzYyLCJlZGl0aW9uIjoibGFzdCJ9.IswPZy0ZFMgrJRIMX21OU_UDnWU7NF-FOf3DCT_8sVQ"]


# Setting the locale to French
#locale.setlocale(locale.LC_TIME, 'fr_FR')

# Getting the current date
current_date = datetime.now()

def process_rss(command, url, model, site="", input_data=""):
    """
    This function takes a command, a url and a model as input and generates a response based on the command and the content of the url
    """
    content = lib__agent_buildchronical.fetch_and_parse_rss_to_string(url)
    content = content.replace('\n', '')
    prompt = command + "\n ___ " + content + "\n ___ \n"
    print("Prompt : " + prompt)
    input_data = ""
    site = ""
    model=model
    res = lib__agent_buildchronical.execute(prompt, site, input_data, model)
    return res


# Formatting the date as "dd month yyyy"
formatted_date = current_date.strftime("%d %B %Y")
        
command = "Nous sommes le " + formatted_date + "\nA partir du texte suivant entre ___ , contenant les derniers articles sur l'IA, \
        extraire TOUS les articles datant d'il y a moins de 48 heures. \
        Commencer par le titre traduit en français et la date de l'article. \
        N'hésite pas à développer si besoin afin d'expliquer les termes techniques ou jargonneux à une audience grand public \
        Aucun article datant de moins de 48 heures ne doit etre oublié. Ne converse pas. Ne conclue pas. \
        Ne pas générer d'introduction ni de conclusion, juste l'article'. \
        Si il n'y a pas d'article, ne pas dire qu'il n'y pas d'article, renvoyer une chaine vide.\
        Ne pas commencer par Voici l'artcie... Mais directement démarrer par l'article'. Respecter ces consignes strictement. "
     
#generation de la veille
model=DEFAULT_MODEL

responses = [process_rss(command, rss, model,"","") for rss in rss_list]

res = "<br><br>".join(responses)

text_veille = str(res.replace("```html", "")).replace("```", "")
print("RESULTAT DE LA VEILLE \n\n\n")
print(text_veille)

prompt = """

Contexte : Vous êtes chargé(e) d’écrire un script en français complet pour un podcast quotidien de revue de presse sur l'Intelligence Artificielle intitulé L'IA Aujourd’hui. Ce podcast doit être informatif, factuel et engageant, conçu pour un auditoire curieux mais non-expert. L’objectif est de fournir un contenu captivant et accessible tout en restant rigoureux.

Consignes spécifiques :

- Structure du script :
  - Introduction :
    - Courte et percutante, introduire le podcast avec la phrase standard :  
      "Bonjour à toutes et à tous, bienvenue dans L'IA Aujourd’hui, le podcast de l'IA par l’IA qui vous permet de rester à la page !"  
    - Suivre par une phrase résumant les sujets du jour, concise et dynamique :  
      "Aujourd’hui : [grandes thématiques du jour]. C’est parti !"
  - Les grandes actualités du jour :  
    Développez chaque actualité en au moins 6000 signes, en incluant :
    - Contexte détaillé : origine, évolution du sujet.
    - Détails et implications : chiffres, exemples, conséquences.
    - Etre précis dans le compte rendu des infos. Pas d'information générique ou vague.
    - Évitez les actualités génériques ou redondantes, en privilégiant les informations originales et significatives.
    - être exhaustif dans la description de l'article (fournir les détails, les chiffres, les exemples, les conséquences cités dans l'article)
  - Transitions :  
    Utilisez des transitions naturelles entre les sujets, en assurant une narration fluide. Variez les styles pour éviter la répétition, mais restez sobre : pas d’abus de questions rhétoriques ou d’effets de style inutiles.
  - Conclusion :  
    Ne pas faire de récapitulatif court. Tout de suite après la dernière actualité, conclure avec la phrase standard :  
      "Voilà qui conclut notre épisode d’aujourd’hui. Merci de nous avoir rejoints, et n’oubliez pas de vous abonner pour ne manquer aucune de nos discussions passionnantes. À très bientôt dans L'IA Aujourd’hui !"

- Ton et style :
  - Utiliser un français journalistique, n'abuse pas des adjectifs, soit simple et direct
- Accessible mais rigoureux : Évitez un ton trop technique ou professoral. Expliquez les concepts sans les simplifier à outrance.
  - Engageant et fluide : Adoptez un style journalistique équilibré, dynamique mais sans excès d’emphase.
  - Informé et crédible : Appuyez-vous sur des faits en évitant les conjectures.
  - Sans redondance : Limitez les répétitions ou les apartés trop longs.
  - Unifier les thématiques : Lorsque possible, établissez des liens entre les sujets pour créer une narration cohérente et captivante.
  - N"utilise pas de titre pour chaque news.
  - N'insiste pas sur les questions rhétoriques pour chaque news et n'abuse pas des commentaires génériques relatifs à des questions, ethiques, philosophiques ou politiques liées à ces news. 
  - Contente toi de donner les faits mais détaille les bien.
  - inutile de citer auteur et source
  - Eviter les mots comme : "crucial", "important", "essentiel", "fondamental", "révolutionnaire", "extraordinaire", "incroyable", "exceptionnel", "fantastique", "génial", "fabuleux", "merveilleux", "formidable", "superbe", "extraordinaire", "époustouflant", "étonnant", "impressionnant", "phénoménal", "stupéfiant", "miraculeux", "prodigieux", "sensationnel", "sublime", "grandiose", "majestueux", "magnifique", "splendide", "éblouissant", "éclatant", "radieux", "rayonnant", "resplendissant", "scintillant", "étincelant", "chatoyant", "coloré", "vif", "éclatant" et éviter les superlatifs.

Objectif final : Produire un script détaillé, prêt à être lu, d’une durée de **10 à 15 minutes**, soit environ **30 000 signes**, en intégrant les actualités fournies de manière exhaustive et captivante.

Instructions pour les actualités fournies :
1. Développez chaque sujet avec rigueur en exploitant les détails, les chiffres et les exemples fournis.
2. Ignorez les actualités génériques ou manquant d’informations pertinentes.
"""




#prompt = "À partir du texte fourni, générer un script de podcast en français d'au moins 30000 signes pour 'L'IA aujourd'hui', présenté par Michel Lévy Provençal, avec l'introduction standard 'Bienvenue dans L'IA aujourd'hui : le podcast de l'IA par l'IA qui vous permet de rester à la page ! Je suis Michel Lévy Provençal, votre hôte' et la conclusion standard 'Voilà qui conclut notre épisode d'aujourd'hui. Merci de nous avoir rejoints et n'oubliez pas de vous abonner pour ne manquer aucune de nos discussions passionnantes. À très bientôt dans L'IA aujourd'hui !'. Adopter un style de revue de presse dynamique avec un ton journalistique engageant caractéristique de Michel Lévy Provençal. Chaque news doit être développée sur au moins 6000 signes, incluant contexte, détails et implications, en expliquant les termes techniques sans simplification excessive. Établir des liens pertinents entre les actualités pour créer une narration fluide. Ignorer les articles trop génériques ou manquant d'informations substantielles. Utiliser des transitions naturelles entre les sujets, des questions rhétoriques pour maintenir l'engagement, et un style narratif incluant le 'nous' inclusif. Le contenu doit être informatif et accessible, équilibrant faits techniques et analyse approfondie, en gardant toujours à l'esprit qu'il s'agit d'une revue de presse destinée à être écoutée."
#text_final = lib__agent_buildchronical.execute(prompt, '', text_veille, model)
text_final = lib_genpodcasts.call_llm(prompt, text_veille, "", model, 14000)

print(text_final)

#envoi de la newsletter
#title = "AI PODCAST : veille sur l'IA"
#email = "contact@brightness.fr"
#lib__agent_buildchronical.mail_html(title, text_final, email)


# Task : task7

# Appeler l'API elevenLabs et construire un podcast


# text_final = "Bienvenue dans //L'IA aujourd'hui : le podcast de l'IA par l'IA qui vous permet de rester à la page !// Aujourd'hui, nous allons explorer deux sujets fascinants et d'actualité : l'incertitude des travailleurs étrangers dans le secteur technologique américain face aux politiques d'immigration, et la question de savoir si l'intelligence artificielle peut remplacer les traducteurs humains."
# creation de l'audio
voice_id = "Fgn8wInzqZU1U5EP2qp0" # MLP   eKZsbKN3buNViPVgJwQr
# voice_id = "TxGEqnHWrfWFTfGW9XjX" # Josh
# randint = randint(0, 100000)
# filename = PODCASTS_PATH + "podcast" + str(randint) + ".mp3"
# texttospeech(text, voice_id, filename)

randint = random.randint(0, 100000)
final_filename = PODCASTS_PATH + "final_podcast" + str(randint) + str(date.today()) + ".mp3"
combined = AudioSegment.from_mp3(str(LOCALPATH) + "sounds/intro.mp3")
# gestion des intonations.
lib__agent_buildchronical.texttospeech(text_final, voice_id, final_filename)
audio_segment = AudioSegment.from_mp3(final_filename)
combined += audio_segment
combined += AudioSegment.from_mp3(str(LOCALPATH) + "sounds/outro.mp3")

# Save the final concatenated audio file
combined.export(final_filename, format='mp3')

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
print("Début de post de podcast")

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


print("début d'envoi de podcast")
# Effectuez la requête
response = requests.post(url, headers=headers, data=payload, files=files)
print("fin d'envoi de podcast")

# Affichez la réponse
print(f"Statut : {response.status_code}")
print("\n\n\n")
print(f"En-têtes de la réponse : {response.headers}")
print("\n\n\n")
print(f"Réponse : {response.text}")



