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


"""
# Formatting the date as "dd month yyyy"
formatted_date = current_date.strftime("%d %B %Y")
        
command = "Nous sommes le " + formatted_date + "\nA partir du texte suivant entre ___ , contenant des listes et descriptions des derniers articles sur l'IA. \
        Extraire TOUS les articles datant d'il y a moins de 24 heures et générer un compte rendu traitant de l'article. Chaque compte rendu doit contenir au moins 6000 signes. N'hésite pas à développer si besoin afin d'expliquer les termes techniques ou jargonneux à une audience grand public\
        Aucun article datant de moins de 24 heures ne doit etre oublié. Ne converse pas. Ne conclue pas. Ne pas générer d'introduction ni de conclusion, juste le compte rendu traitant de l'article. Si il n'y a pas d'article, ne pas dire qu'il n'y pas d'article, renvoyer une chaine vide.Ne pas commencer par Voici le compte rendu de l'artcie... Mais directement démarrer par le compte rendu. \
        "
     
#generation de la veille
model=DEFAULT_MODEL
responses = [process_url(command, url, model,"","") for url in url_list]
res = "<br><br>".join(responses)

text_veille = str(res.replace("```html", "")).replace("```", "")





prompt =    "A partir du texte suivant générer un script de podcast en français d'au moins 20 000 signes, \
            pret à etre lu par Michel Levy Provencal le host de //L'IA aujourd'hui : le podcast de l'IA par l'IA qui vous permet de rester à la page !// \
            Chaque news doit etre assez développée au moins 3000 signes, pour être pertinente et compréhensible par un auditeur non expert. Si besoin expliquer les acronymes ou les termes techniques. Ne pas trop résumer chaque article. \
            Si tu n'as pas assez d'info sur un article, le zapper. Attention si la news n'est pas originale, c'est à dire qu'elle traite d'information générique, la zapper. \
            Toujours démarrer par cette petite introduction, puis enchainer tout de suite aprés sur le script. Attention, ne jamais démarrer en disant, voici le script du podcast. toujours démarrer directement. \
            La conclusion du script doit etre courte et toujours sous cette forme : //Voilà qui conclut notre épisode d'aujourd'hui. Merci de nous avoir rejoints et n'oubliez pas de vous abonner pour ne manquer aucune de nos discussions passionnantes. À très bientôt dans L'IA aujourd'hui !// \
            "

text_final = lib__agent_buildchronical.execute(prompt, '', text_veille, model)

#envoi de la newsletter
title = "AI PODCAST : veille sur l'IA"
email = "contact@brightness.fr"
lib__agent_buildchronical.mail_html(title, text_final, email)


# Task : task7

# Appeler l'API elevenLabs et construire un podcast

"""

text_final = "Bienvenue dans //L'IA aujourd'hui : le podcast de l'IA par l'IA qui vous permet de rester à la page !// Aujourd'hui, nous allons explorer deux sujets fascinants et d'actualité : l'incertitude des travailleurs étrangers dans le secteur technologique américain face aux politiques d'immigration, et la question de savoir si l'intelligence artificielle peut remplacer les traducteurs humains. Plongeons directement dans ces discussions captivantes. Commençons par le premier sujet : l'incertitude qui plane sur les travailleurs étrangers dans le secteur technologique aux États-Unis à l'approche de l'inauguration de Donald Trump. Cet article, écrit par Amy Feldman, met en lumière une problématique cruciale pour de nombreux professionnels du secteur technologique. Avec l'élection de Trump, connu pour ses positions strictes sur l'immigration, les travailleurs étrangers se retrouvent dans une situation précaire, cherchant désespérément à sécuriser leurs visas avant que de nouvelles politiques potentiellement restrictives ne soient mises en place. Les avocats spécialisés en immigration sont submergés de demandes de renseignements de la part de travailleurs étrangers inquiets. Ces travailleurs, souvent détenteurs de visas H-1B, sont essentiels à l'industrie technologique américaine. Le visa H-1B est un visa non-immigrant qui permet aux entreprises américaines d'employer temporairement des travailleurs étrangers dans des professions spécialisées nécessitant des compétences théoriques ou techniques. Les entreprises technologiques dépendent fortement de ce programme pour recruter des talents internationaux. Cependant, le programme a souvent été critiqué pour être utilisé pour remplacer des travailleurs américains par des étrangers à moindre coût, ce qui a conduit à des appels à la réforme. L'article souligne également l'impact potentiel sur l'innovation et la compétitivité des États-Unis. Les travailleurs étrangers apportent non seulement des compétences techniques, mais aussi des perspectives diversifiées qui stimulent l'innovation. En restreignant l'accès à ces talents, les États-Unis risquent de perdre leur avantage concurrentiel dans le secteur technologique mondial. En outre, l'article aborde les implications personnelles pour les travailleurs concernés. Beaucoup d'entre eux ont construit leur vie aux États-Unis, avec des familles et des enfants scolarisés dans le pays. L'incertitude quant à leur statut d'immigration crée une anxiété considérable, non seulement pour leur avenir professionnel, mais aussi pour leur vie personnelle. Les avocats en immigration conseillent à leurs clients de préparer leurs documents et de soumettre leurs demandes de renouvellement de visa le plus tôt possible. Cependant, même avec une préparation minutieuse, l'avenir reste incertain. Les changements de politique peuvent survenir rapidement, et les travailleurs étrangers doivent être prêts à s'adapter à de nouvelles réalités. Passons maintenant à notre deuxième sujet : l'intelligence artificielle peut-elle remplacer les traducteurs humains ? Cette question est au cœur des débats actuels, alors que les technologies de traduction automatique continuent de progresser à un rythme effréné. Les systèmes de traduction automatique, tels que Google Translate ou DeepL, utilisent des algorithmes d'apprentissage automatique pour analyser et traduire des textes d'une langue à une autre. Ces systèmes s'appuient sur des réseaux de neurones artificiels, qui sont des modèles mathématiques inspirés du fonctionnement du cerveau humain. Grâce à l'apprentissage profond, ces réseaux peuvent traiter d'énormes quantités de données linguistiques pour améliorer la précision des traductions. Cependant, malgré ces avancées, les systèmes d'IA rencontrent encore des difficultés lorsqu'il s'agit de traduire des textes complexes ou nuancés. Les subtilités culturelles, les jeux de mots, et les expressions idiomatiques posent souvent problème aux machines, car elles nécessitent une compréhension contextuelle que les algorithmes peinent à acquérir. Par exemple, une phrase humoristique ou un jeu de mots peut être difficile à traduire correctement sans une compréhension approfondie du contexte culturel. Les traducteurs humains, en revanche, possèdent une compréhension innée des nuances linguistiques et culturelles, ce qui leur permet de produire des traductions plus précises et adaptées au contexte. Ils peuvent également faire preuve de créativité et d'intuition, des qualités qui font souvent défaut aux machines. De plus, les traducteurs humains sont capables de s'adapter rapidement aux changements de contexte ou aux nouvelles informations, ce qui est essentiel dans des domaines tels que la traduction littéraire ou la localisation de contenu. En conclusion, bien que l'IA ait fait des progrès significatifs dans le domaine de la traduction, elle ne peut pas encore remplacer complètement les traducteurs humains. Les machines peuvent être utiles pour des traductions simples ou pour aider les traducteurs humains à gagner du temps, mais elles ne peuvent pas reproduire la finesse et la sensibilité nécessaires pour traduire des textes complexes ou nuancés. Voilà qui conclut notre épisode d'aujourd'hui. Merci de nous avoir rejoints et n'oubliez pas de vous abonner pour ne manquer aucune de nos discussions passionnantes. À très bientôt dans L'IA aujourd'hui !"

# creation de l'audio
#voice_id = "DnF3PZl1PUQOKY4LvcUl" # MLP
voice_id = "TxGEqnHWrfWFTfGW9XjX" # Josh
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
destinataire = "michel@brightness.fr"

## envoyer par email
lib__agent_buildchronical.mailaudio(titre, audio, destinataire, text)


