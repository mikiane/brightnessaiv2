#################   Agent X   #################
# Agent récupérant les sources de veille sur Feedly, les parsant, les résument et les envoyant par mail sous la forme d'une chronique.
# Auteur : Michel Levy Provencal (Brightness AI)
# Date : 2023-06-07
#  Format : "[['AI Brightness', 'https://flint.media/bots/feeds/eyJhbGciOiJIUzI1NiJ9.eyJib3RfaWQiOjEyNzYxLCJlZGl0aW9uIjoibWF0Y2hfc2FtcGxlcyJ9.9Jha1LyxzzlEzA4xRtJqp1MD323gQZXvENePFMq8ptY']]" topic
################################################
################################################


from lib__agent_buildchronical import *
import lib__search_sources
import sys
import ast
from datetime import *
import random
import argparse
from lib__env import *
from dotenv import load_dotenv
import os

#import streamlit as st
#load_dotenv(".env") # Load the environment variables from the .env file.
#load_dotenv("/home/michel/extended_llm/.env") # Load the environment variables from the .env file.
load_dotenv('.env')
load_dotenv(DOTENVPATH)
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
DESTINATAIRES_TECH = os.environ.get("DESTINATAIRES_TECH")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")
n_feeds = 5 # define the number of feeds to get from Feedly
n_links = 2 # define the number of links to get from each feed

##########################################################################################################################################################################
# Function to get rss feed links from Feedly API by topic
def get_feedly_feeds(topic):
    try:
        array_as_string = lib__search_sources.get_feedly_feeds(topic, n_feeds)
    except Exception as e:
        print(f"Erreur lors de l'appel de 'get_feedly_feeds' : {e}")
        sys.exit(1)

    if not array_as_string:  # c'est-à-dire, si array_as_string est vide
        print("Erreur : 'get_feedly_feeds' a renvoyé une chaîne vide")
        sys.exit(1)

    try:
        array_as_string = repr(array_as_string)  # obtient une représentation de chaîne sûre pour ast.literal_eval
        rss_urls = ast.literal_eval(array_as_string)  # convertit la chaîne en liste
        
    except Exception as e:
        print(f"Erreur lors de la conversion de la chaîne en liste : {e}")
        sys.exit(1)
    return(rss_urls)
    
    
##########################################################################################################################################################################
# Function that parse rss feeds and return a list of links
def parse_feeds(rss_urls):
    
    n = int(n_links)  # define number of links to get from each feed

    ### Récpération des premiers articles des flux.
    rss_urls_transformed = []  # a new list to store the transformed values

    for site_name, rss_url in rss_urls:
        first_n_links = extract_n_links(rss_url, n)  # get the first n links from the RSS feed
        if first_n_links:  # only add the line if the result is not an empty list
            for link in first_n_links:
                link_title = extract_title(link)
                rss_urls_transformed.append([site_name, link, link_title])

    rss_urls = rss_urls_transformed  # replace the original list with the transformed list
    return(rss_urls)
    
##########################################################################################################################################################################
# Function that summarize rss feeds and return a list of summaries
def summarize_feeds(rss_urls, topic):
    ## generer les résumés
    summaries = []
    for site_name, url, link_title in rss_urls:
        print(str(datetime.now()) +  " : Summarization de " + link_title + " : " + url)
        prompt = f"Rédige un résumé de cet article en respectant la complexité du sujet. Agis comme un journaliste spécialisé dans les sujets de {topic}. \nFormat : ne précise jamais qu'il s'agit d'un résumé. Ecrire tous les chiffres, les nombres, les dates en toutes lettres. Le texte ne doit pas comporter de parenthèses ni de tirets. Ne démarre pas le résumé par 'Bonjour' ou une formule de politesse. Entre directement dans le vif du sujet."
        site = url
        input_data = ""
        summary = execute(prompt, site, input_data, "gpt-4")
        prompt = "Rédige un titre pour cet article. Format : Adopter un ton dynamique, style radio. Ecrire tous les chiffres, les nombres, les dates en toutes lettres. Le texte ne doit pas comporter de parenthèses ni de tirets."
        titre = execute(prompt, "", summary, "gpt-4")
        print( str(datetime.now()) +  " : RESUMÉ DE L'ARTICLE : \n\n\n\n" + "" + titre + "" + "\n\n" + summary)
        
        if summary is not None:  # only add the line if the result is not None
            summaries.append([link_title, url, "\n\n\n\n" + "" + titre + "" + "\n\n" + summary])  # replace site_name with link_title

    return(summaries)

##########################################################################################################################################################################
# Function that build a chronicle from a list of summaries
def build_chronicle(summaries, topic):
    # concatener les résumés 
    source = ""
    for summary in summaries:
        source += str(summary[2]) + "\n\n"
    
    # generer la chronique    
    prompt = f"Objectif : obtenir une chronique à diffuser (par email et en audio) signée par l’équipe de Brightness sans préciser la régularité du rendez-vous. \nRôle : Agis comme un rédacteur de chronique, journaliste spécialisé dans les sujets de {topic} qui rédige une chronique à destination du grand public en essayant de vulgariser au mieux, sans dénaturer la complexité du sujet traité.\nTache : Ecrire une chronique à partir des éléments de contexte.\nEtapes : Commencer directement par un des éléments du contexte et développer la chronique en créant des liaisons entre les différents articles traités.\nFormat : Adopter un ton dynamique, style radio. Sauter des lignes entre chaque article traité. Ecrire tous les chiffres, les têtes de chapitre éventuels, les nombres, les dates en toutes lettres. Le texte ne doit pas comporter de parenthèses ni de tirets."
    site = ""
    input_data = source
    chronicle = execute(prompt, site, input_data, model)
     
    return(chronicle)


##########################################################################################################################################################################
# Function that build a chronicle from a list of summaries
def build_large_chronicle(summaries, topic, name):
    # concatener les résumés 
    source = ""
    titres = ""
    for summary in summaries:
        source += str(summary[2]) + "\n\n"
        titres += str(summary[0]) + "\n\n"
        
        
    print(str(datetime.now()) +  " : SOURCES AVANT LA CREATION DES INTROS / CONCLUSIONS : \n\n " + source + "\n\n\n")
          
    ### INTRO
    """Objectif : Ecrire l’introduction d’une chronique radio personnalisée pour {name}. \nRôle : Agis comme un journaliste spécialisé dans les sujets de {topic}. Il vulgarise sans dénaturer la complexité du sujet traité.\nTache : Ecrire une introduction en citant tous les titres des articles contenus dans le contexte.\nFormat : Adopter un ton dynamique, style radio.”
    """
    prompt = f"Objectif : Ecrire l'introduction synthétique d’une chronique personnalisée pour {name} en agissant comme un journaliste spécialisé dans les sujets de {topic}. \nTache : Ecrire tous les titres des articles contenus dans le contexte en sautant une ligne pour chaque titre.\nFormat : Adopter un ton dynamique, style radio. Fais en une introduction dédiée à {name}"
    site = ""
    input_data = titres
    intro = execute(prompt, site, input_data, "gpt-4")
    
    
    print(str(datetime.now()) +  " : INTRO : \n\n " + intro + "\n\n\n")

    
    ### ARTICLES
    articles = source
    
    ### CONCLUSION
    """Objectif : Conclure une chronique radio personnalisée pour {name}. La chronique est signée par l’équipe de Brightness (sans préciser la régularité du rendez-vous). \nRôle : Agis comme un journaliste spécialisé dans les sujets de {topic}. \nFormat : Adopter un ton dynamique, court et style radio.”
    """    
    prompt = f"Objectif : Conclure une chronique radio personnalisée pour {name}. La chronique est signée par l’équipe de Brightness (sans préciser la régularité du rendez-vous). \nRôle : Agis comme un journaliste spécialisé dans les sujets de {topic}. \nFormat : Adopter un ton dynamique, court et style radio."
    site = ""
    input_data = ""
    conclu = execute(prompt, site, input_data, "gpt-4")
    
    print(str(datetime.now()) +  " : CONCLU : \n\n " + conclu + "\n\n\n")
      
    chronicle = str(intro) + "\n\n" + str(articles) + "\n\n" + str(conclu)
    return(chronicle)


def build_large_chronicle_html(summaries, topic, name):
    # concatener les résumés 
    source = ""
    titres = ""
    for summary in summaries:
        source += str(summary[2]) + "\n\n"
        titres += str(summary[0]) + "\n\n"
        
        
    print(str(datetime.now()) +  " : SOURCES AVANT LA CREATION DES INTROS / CONCLUSIONS : \n\n " + source + "\n\n\n")
          
    ### INTRO
    """Objectif : Ecrire l’introduction d’une chronique radio personnalisée pour {name}. \nRôle : Agis comme un journaliste spécialisé dans les sujets de {topic}. Il vulgarise sans dénaturer la complexité du sujet traité.\nTache : Ecrire une introduction en citant tous les titres des articles contenus dans le contexte.\nFormat : Adopter un ton dynamique, style radio.”
    """
    prompt = f"Objectif : Ecrire l'introduction synthétique d’une chronique personnalisée pour {name} en agissant comme un journaliste spécialisé dans les sujets de {topic}. \nTache : Ecrire tous les titres des articles contenus dans le contexte en sautant une ligne pour chaque titre.\nFormat : Adopter un ton dynamique, style radio. Fais en une introduction dédiée à {name}"
    site = ""
    input_data = titres
    intro = execute(prompt, site, input_data, "gpt-4")
    
    
    print(str(datetime.now()) +  " : INTRO : \n\n " + intro + "\n\n\n")

    
    ### ARTICLES
    articles = convert_into_html(source, "gpt-3.5-turbo-16k")
    
    ### CONCLUSION
    """Objectif : Conclure une chronique radio personnalisée pour {name}. La chronique est signée par l’équipe de Brightness (sans préciser la régularité du rendez-vous). \nRôle : Agis comme un journaliste spécialisé dans les sujets de {topic}. \nFormat : Adopter un ton dynamique, court et style radio.”
    """    
    prompt = f"Objectif : Conclure une chronique radio personnalisée pour {name}. La chronique est signée par l’équipe de Brightness (sans préciser la régularité du rendez-vous). \nRôle : Agis comme un journaliste spécialisé dans les sujets de {topic}. \nFormat : Adopter un ton dynamique, court et style radio."
    site = ""
    input_data = ""
    conclu = execute(prompt, site, input_data, "gpt-4")
    
    print(str(datetime.now()) +  " : CONCLU : \n\n " + conclu + "\n\n\n")
      
    chronicle = str(intro) + "\n\n" + str(articles) + "\n\n" + str(conclu)
    return(chronicle)

##########################################################################################################################################################################
# Function that generate a prompte to build an image
def generate_podcast(text, topic):
    # generer titre
    titre = f"Revue de presse {topic} \n du \n" + str(date.today())

    #id_podcast
    randint = random.randint(0, 100000)
    id_podcast = str(randint) + str(date.today())

    # generer image ###############@
    # generation du prompt pour la génération de l'image
    #prompt_image = request_llm("Décrire une illustration pour cette chronique en précisant les détails visuels en moins de 240 caractères", '', text, "gpt-3.5-turbo")
    #output_filename = "img/" + id_podcast + ".png"
    #generate_image(prompt_image, output_filename)
    ############################################

    # creation de l'audio
    #voice_id = "DnF3PZl1PUQOKY4LvcUl" # MLP
    #voice_id = "FL36qzLoYbdCLMM5R9rF" # MLP-PRO
    voice_id = "TxGEqnHWrfWFTfGW9XjX"  # Josh
    final_filename = PODCASTS_PATH + "final_podcast" + id_podcast + ".mp3"

    # gestion des intonations.
    # split_text(text, limit=300)
    convert_and_merge(text, voice_id, final_filename)
    
    return(id_podcast)

    # titre = "Dailywatch \n du \n" + str(date.today())
    # input_audiofile = filename
    # output_videofile = "datas/podcast" + str(randint) + ".mp4"

    ## creation de la video avec les fichiers d'entrée appropriés
    # create_video_with_audio(input_audiofile, titre, output_videofile)


##########################################################################################################################################################################
# Function that generate sources from a list of links
def generate_sources(rss_urls):
    # generer les sources
    sources = "sources: \n"
    for site_name, url, link_title in rss_urls:  # add site_name
        sources += link_title + ": " + url + "\n\n"
    
    return(sources)

##########################################################################################################################################################################
# Function that generate an illustration from a text
def generate_illustration(text, id_podcast):
    # generer image ###############@
    # generation du prompt pour la génération de l'image
    prompt_image = request_llm("Décrire une illustration pour cette chronique en présisant les détails visuels en moins de 240 caractères", '', text, "gpt-3.5-turbo")
    output_filename = "img/" + id_podcast + ".png"
    generate_image(prompt_image, output_filename)
    ############################################

##########################################################################################################################################################################
# Function that send an email with the chronicle and the illustration
def send_email(chronicle, final_filename, topic, sources, email):
    # Votre code pour envoyer le courriel ici
    today = date.today()
    formatted_date = today.strftime('%d/%m/%Y')
    titre =  str(formatted_date) + f' Revue de presse {topic}'
    text = chronicle + "\n\n" + "Aller plus loin :" + "\n\n" + sources
    audio = final_filename
    # destinataires = ["contact@mikiane.com", "michel@brightness.fr" ]
    #image = output_filename

    print("envoi de l'email")
    ## envoyer par email
    mailaudio(titre, audio, text, email)

##########################################################################################################################################################################
# Function that send an email with the chronicle without audio
def send_email_nofile(chronicle, topic, sources, email):
    # Votre code pour envoyer le courriel ici
    today = date.today()
    formatted_date = today.strftime('%d/%m/%Y')
    titre =  str(formatted_date) + f' Revue de presse {topic}'
    text = chronicle + "\n\n" + "Aller plus loin :" + "\n\n" + sources
   
    print("envoi de l'email")
    ## envoyer par email
    mail_nofile(titre, text, email)
    
    
    
    
def send_email_html(chronicle, topic, sources, email):
    # Votre code pour envoyer le courriel ici
    today = date.today()
    formatted_date = today.strftime('%d/%m/%Y')
    titre =  str(formatted_date) + f' Revue de presse {topic}'
    text = chronicle + "\n\n" + "Aller plus loin :" + "\n\n" + sources
   
    print("envoi de l'email")
    ## envoyer par email
    mail_html(titre, text, email)

        

print("""
    Bienvenue dans le générateur de podcasts Brightness AI !
    Ce script va vous permettre de générer un podcast à partir de sources de veille.
    Il va d'abord vous demander de choisir les articles à résumer, puis
    les parser, les résumer et les envoyer par mail sous la forme d'une chronique.
""")


topic = "Intelligence Artificielle"
feed = "https://flint.media/bots/feeds/eyJhbGciOiJIUzI1NiJ9.eyJib3RfaWQiOjEyNzYyLCJlZGl0aW9uIjoibGFzdCJ9.IswPZy0ZFMgrJRIMX21OU_UDnWU7NF-FOf3DCT_8sVQ"
n_links = 3
email = "michel@brightness.fr"
name = "Michel"


##########################################################################################################################################################################
# Créez un parser pour les arguments
parser = argparse.ArgumentParser(description='Script utilisant topic, feed, et n_links comme arguments.')

# Ajoutez les arguments attendus
parser.add_argument('--topic', type=str, required=True, help='Sujet à traiter.')
parser.add_argument('--feed', type=str, required=True, help='Lien vers le flux de données.')
parser.add_argument('--n_links', type=int, required=True, help='Nombre de liens à traiter.')
parser.add_argument('--email', type=str, required=True, help='Adresse email du destinataire.')
parser.add_argument('--name', type=str, required=True, help='Nom du destinataire.')
parser.add_argument('--podcast', type=str, required=False, help='no : if you dont want to generate a podcast')
parser.add_argument('--html', type=str, required=False, help='yes : if you  want to generate an HTML email')

htmlformat = False
genpodcast = True

# Parsez les arguments
args = parser.parse_args()
if args.podcast and args.podcast == "no":
    genpodcast = False
    
if args.html and args.html == "yes":
    htmlformat = True
    
if args.topic and args.feed and args.n_links and args.email and args.name:
    topic = args.topic
    feed = args.feed
    n_links = args.n_links
    email = args.email
    name = args.name
    print(f"Topic: {args.topic}, Feed: {args.feed}, Number of links: {args.n_links}, Email: {args.email}, Name: {args.name}")
else:
    print("Tous les arguments doivent être fournis. Utilisez --help pour plus d'informations.")
    exit(1)

##########################################################################################################################################################################

try:
  
    feeds = [["Feed", feed]]
    
    ##########################################################################################################################################################################
    # on parse les feeds
    parsed_feeds = parse_feeds(feeds)
    ##########################################################################################################################################################################
    ## Demande à l'utilisateur de choisir ses articles
    # Affichez chaque url avec son index
    """
    for i, url in enumerate(parsed_feeds):
        print(f"{i+1}. {url}\n")

    # Demandez à l'utilisateur de sélectionner les indices des urls à conserver
    selected_indices = input("Veuillez entrer les numéros des urls que vous souhaitez conserver, séparés par des virgules : ")

    # Convertissez les indices sélectionnés en une liste d'entiers
    selected_indices = list(map(int, selected_indices.split(',')))

    # Filtrer rss_urls pour ne conserver que les urls sélectionnées
    parsed_feeds = [parsed_feeds[i-1] for i in selected_indices]
    """
    
    
    ## Execution du script
    print(str(datetime.now()) +  " : Summarization des articles...\n")
    summaries = summarize_feeds(parsed_feeds, topic)
    #chronicle = build_chronicle(summaries, topic)
    
    print(str(datetime.now()) +  " : Construction de la chronique...\n")
    if htmlformat:
        chronicle = build_large_chronicle_html(summaries, topic, name)
    else:
        chronicle = replace_numbers_with_text(build_large_chronicle(summaries, topic, name))
    
    print(str(datetime.now()) +  " : Génération des sources...\n")
    sources = generate_sources(parsed_feeds)
        
    if genpodcast:
        print(str(datetime.now()) +  " : Génération du podcast...\n")
        id_podcast = generate_podcast(chronicle, topic)
        final_filename = PODCASTS_PATH + "final_podcast" + id_podcast + ".mp3"

        print(str(datetime.now()) +  " : Envoi de l'email...\n")
        # output_filename = "img/" + id_podcast + ".png"
        send_email(chronicle, final_filename, topic, sources, email)
        print(f"Le podcast pour le sujet '{topic}' a été créé et envoyé par mail.")
        
    else:     
        if htmlformat:
            send_email_html(chronicle, topic, sources, email)
        else:
            send_email_nofile(chronicle, topic, sources, email)
        
except Exception as e:
    print("Une erreur s'est produite: ", e)
    
    
    
    
    
    
    
    