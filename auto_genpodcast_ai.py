import lib__agent_buildchronical
import random
import datetime
from datetime import date
from datetime import datetime

import locale
import lib__transformers

# Load the environment variables from the .env file
from dotenv import load_dotenv
import os
load_dotenv(".env")

DESTINATAIRES_TECH = os.environ.get("DESTINATAIRES_TECH")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")


DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
model = DEFAULT_MODEL

def process_url(command, url, model, site="", input_data=""):
    """
    This function takes a command, a url and a model as input and generates a response based on the command and the content of the url
    """
    content = lib__agent_buildchronical.fetch_and_parse_urls(url)
    content = content.replace('\n', '')
    prompt = command + "\n ___ " + content + "\n ___ \n"
    print("Prompt : " + prompt)
    input_data = ""
    site = ""
    model=model
    res = lib__agent_buildchronical.execute(prompt, site, input_data, model)
    return res


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
        extraire TOUS les articles datant d'il y a moins de 24 heures et les traduire en français.  Chaque article doit contenir au moins 6000 signes. N'hésite pas à développer si besoin afin d'expliquer les termes techniques ou jargonneux à une audience grand public\
        Aucun article datant de moins de 24 heures ne doit etre oublié. Ne converse pas. Ne conclue pas. Ne pas générer d'introduction ni de conclusion, juste l'articke traduit'. Si il n'y a pas d'article, ne pas dire qu'il n'y pas d'article, renvoyer une chaine vide.Ne pas commencer par Voici le compte rendu de l'artcie... Mais directement démarrer par l'article'. \
        "
     
#generation de la veille
model=DEFAULT_MODEL
responses = [process_url(command, url, model,"","") for url in url_list]
res = "<br><br>".join(responses)

text_veille = str(res.replace("```html", "")).replace("```", "")


prompt =    "A partir du texte suivant générer un script de podcast en français d'au moins 50 000 signes, \
            pret à etre lu par Michel Lévy Provençal le host de //L'IA aujourd'hui : le podcast de l'IA par l'IA qui vous permet de rester à la page !// \
            Chaque news doit etre assez développée au moins 3000 signes, pour être pertinente et compréhensible par un auditeur non expert. Si besoin expliquer les acronymes ou les termes techniques. Ne pas trop résumer chaque article. \
            Si tu n'as pas assez d'info sur un article, le zapper. Attention si la news n'est pas originale, c'est à dire qu'elle traite d'information générique, la zapper. \
            Toujours démarrer par cette petite introduction, puis enchainer tout de suite aprés sur le script. Attention, ne jamais démarrer en disant, voici le script du podcast. toujours démarrer directement. \
            La conclusion du script doit etre courte et toujours sous cette forme : //Voilà qui conclut notre épisode d'aujourd'hui. Merci de nous avoir rejoints et n'oubliez pas de vous abonner pour ne manquer aucune de nos discussions passionnantes. À très bientôt dans L'IA aujourd'hui !// \
            "

text_final = lib__agent_buildchronical.execute(prompt, '', text_veille, model)

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


titre = 'Daily Watch Generative AI du ' + str(date.today())
text = text_final
audio = final_filename
email = "michel@brightness.fr"  # Remplacez 'destinataire' par 'email'

# Appel de la fonction mailaudio
lib__agent_buildchronical.mailaudio(titre, audio, text, email)

