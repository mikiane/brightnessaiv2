import lib__agent_buildchronical

from datetime import datetime
import locale

# Load the environment variables from the .env file
from dotenv import load_dotenv
import os
load_dotenv(".env")

DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
model = DEFAULT_MODEL

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


# Génération d'une liste de talks TED
rss_list = ["https://rss.app/feeds/tZTJRd8QbKQoXf6q.xml"]


# Setting the locale to French
#locale.setlocale(locale.LC_TIME, 'fr_FR')

# Getting the current date
current_date = datetime.now()

# Formatting the date as "dd month yyyy"
formatted_date = current_date.strftime("%d %B %Y")


#Commande pour générer la veille
command = "Nous sommes le " + formatted_date + "\nA partir du texte suivant entre ___ , contenant des listes et descriptions des derniers articles sur le thème du Public Speaking. \
        Extraire tous les articles datant d'il y a moins d'une semaine et générer la liste exhaustive des informations récentes mentionnés dans le texte. \
        Aucun article datant de moins d'une semaine doit etre oublié. La liste doit comprendre les informations suivantes : \
            Titre de l'article \
            <br>Description / résumé de la video dans la langue originelle de l'article\
            <br>URL associée à l'article. La liste générée doit etre au format magazine, synthétique et simple. \
            <br>pour chaque article, génerer un tweet en français en utilisant le titre, la description et en citant l'url associée. Utiliser un ton neutre. \
        Le format du texte produit doit etre HTML. \
        Ne pas générer d'introduction ni de conclusion, juste la liste. \
        Toujours utiliser un modele de page HTML fond blanc, avec Titre en rouge en <h3>, description en <p> noir, tweet en <p> sur fond bleu clair, lien vers l'article derriere un Read More.\
        Démarrer la liste avec le titre de la source."
     

#génération de la veille
model=DEFAULT_MODEL
responses = [process_rss(command, rss, model,"","") for rss in rss_list]
res = "<br><br>".join(responses)
text_veille = str(res.replace("```html", "")).replace("```", "")



#envoi de la newsletter
title = "Public Speaking WATCH : veille sur Public Speaking"
email = "contact@brightness.fr"
lib__agent_buildchronical.mail_html(title, text_veille, email)

