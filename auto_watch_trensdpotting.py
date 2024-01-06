import lib__agent_buildchronical



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
url_list = ["https://www.hachette.fr/a-paraitre/histoire-et-actualite"
            ,"https://www.grasset.fr/a-paraitre/"
            ,"https://www.diateino.com/nouveautes.php"
            ,"https://www.belin-editeur.com/sciences-belin"
            ,"https://editions.flammarion.com/Catalogue/(parution)/a-paraitre/(domaine)/Sciences humaines"
            ,"https://editions.flammarion.com/Catalogue/(parution)/a-paraitre/(domaine)/Essais et documents"
            ,"https://www.actes-sud.fr/recherche/catalogue/rayon/1198?keys="
            ,"https://www.albin-michel.fr/essais-docs"
            ,"https://www.albin-michel.fr/sciences-humaines"
            ,"https://www.seuil.com/a-paraitre"
            ,"https://www.dunod.com/recherche/etat/Nouveaut%C3%A9"
            ,"https://www.puf.com/search?search_api_fulltext=&f%5B0%5D=discipline%3A593"
            ,"https://www.puf.com/search?search_api_fulltext=&f%5B0%5D=discipline%3A561"
            ,"https://www.puf.com/search?search_api_fulltext=&f%5B0%5D=discipline%3A541"
            ,"https://www.odilejacob.fr/catalogue/"
            ,"https://www.fayard.fr/a-paraitre/"
            ,"http://editions.ehess.fr/a-paraitre/"]

command = "A partir du texte suivant entre ___ , contenant des listes et descriptions de livres, extraire et générer la liste exhaustive des livres mentionnés dans le texte.\
        La liste doit comprendre les informations suivantes : \
            Titre de l'ouvrage \
            <br>Auteur de l'ouvrage \
            <br>Éditeur \
            <br>URL associée au livre. \
            Ne pas générer d'introduction ni de conclusion, juste la liste. \
            Toujours utiliser un modele de page HTML fond blanc, avec Titre en rouge en <h3>, description en <p> noir sur fond bleu clair, lien vers le livre derriere un Read More.\
            Démarrer la liste avec le titre de la source."
            
model="gpt-4-1106-preview"


responses = [process_url(command, url, model,"","") for url in url_list]
res = "<br><br>".join(responses)


text = str(res.replace("```html", "")).replace("```", "")
title = "TRENDSPOTTING : veille livres à paraître"
email = "michel@brightness.fr"
lib__agent_buildchronical.mail_html(title, text, email)

