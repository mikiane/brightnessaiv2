import lib__agent_buildchronical

from datetime import datetime
import locale


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
url_list = ["https://www.technologyreview.com/artificial-intelligence/"
            , "https://www.artificialintelligence-news.com/"
            , "https://rss.app/feeds/v1.1/ts7TBAc6R3BNeWTU.json"
            , "https://www.artificialintelligence-news.com/"
            , "https://venturebeat.com/category/ai/"
            , "https://www.wired.com/tag/artificial-intelligence/"
            , "https://www.forbes.com/ai/"
            , "https://www.theverge.com/ai-artificial-intelligence"
            , "https://www.theguardian.com/technology/artificialintelligenceai"]



# Setting the locale to French
#locale.setlocale(locale.LC_TIME, 'fr_FR')

# Getting the current date
current_date = datetime.now()

# Formatting the date as "dd month yyyy"
formatted_date = current_date.strftime("%d %B %Y")
        
command = "Nous sommes le " + formatted_date + "\nA partir du texte suivant entre ___ , contenant des listes et descriptions des derniers articles sur l'IA. \
        Extraire TOUS les articles datant d'il y a moins d'une semaine et générer la liste exhaustive des informations récentes mentionnés dans le texte. \
        Aucun article datant de moins d'une semaine doit etre oublié. La liste doit comprendre les informations suivantes : \
            Titre de l'article \
            <br>Description / résumé de l'article dans la langue originelle de l'article\
            <br>Pour chaque article genere un tweet en français en utilisant le titre, la description et en citant l'url associée. Utiliser un ton neutre. \
        Répondre directement en générant la liste. Ne converse pas. Ne conclue pas. Ne pas générer d'introduction ni de conclusion, juste la liste. \
        Toujours utiliser un modele de page HTML fond blanc, avec Titre en rouge en <h3>, description en <p> noir, tweet en <p> sur fond bleu clair, lien vers l'article derriere un Read More.\
        Démarrer la liste avec le titre de la source."
     
#generation de la veille
model="gpt-4-1106-preview"
responses = [process_url(command, url, model,"","") for url in url_list]
res = "<br><br>".join(responses)

text_veille = str(res.replace("```html", "")).replace("```", "")


#envoi de la newsletter
title = "AI WATCH : veille sur l'IA"
email = "contact@brightness.fr"
lib__agent_buildchronical.mail_html(title, text_veille, email)
