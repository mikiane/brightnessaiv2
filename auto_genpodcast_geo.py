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
url_list = ["https://atlas-report.com/"
            , "https://www.foreignaffairs.com/"
            , "https://thediplomat.com/"
            , "https://foreignpolicy.com/"
            , "https://worldview.stratfor.com/"
            , "https://nationalinterest.org/"
            , "https://www.chathamhouse.org/"
            , "https://hir.harvard.edu/"
            , "https://www.worldpoliticsreview.com/"
            , "https://www.the-american-interest.com/"
            , "https://www.e-ir.info/"
            , "https://www.globalpolicyjournal.com/"]


# Setting the locale to French
#locale.setlocale(locale.LC_TIME, 'fr_FR')

# Getting the current date
current_date = datetime.now()



# Formatting the date as "dd month yyyy"
formatted_date = current_date.strftime("%d %B %Y")
        
command = "Nous sommes le " + formatted_date + "\nA partir du texte suivant entre ___ , contenant les derniers articles sur la géopolitique, \
        extraire TOUS les articles datant d'il y a moins de 48 heures. \
        Commencer par le titre traduit en français et la date de l'article.  \
        N'hésite pas à développer si besoin afin d'expliquer les termes techniques ou jargonneux à une audience grand public \
        Aucun article datant de moins de 48 heures ne doit etre oublié. Ne converse pas. Ne conclue pas. \
        Ne pas générer d'introduction ni de conclusion, juste l'article'. \
        Si il n'y a pas d'article, ne pas dire qu'il n'y pas d'article, renvoyer une chaine vide.\
        Ne pas commencer par Voici l'artcie... Mais directement démarrer par l'article'. Respecter ces consignes strictement. "
     
#generation de la veille
model=DEFAULT_MODEL

responses = [lib_genpodcasts.process_url(command, url, model,"","") for url in url_list]
res = "<br><br>".join(responses)

text_veille = str(res.replace("```html", "")).replace("```", "")

print(text_veille)

"""

prompt =    "A partir du texte suivant générer un script de podcast en français d'au moins 30000 signes, \
            pret à etre lu par le host de //Dans le monde aujourd'hui : le podcast géopolitique par l'IA qui vous permet de rester à la page !// \
            Chaque news doit etre assez développée au moins 6000 signes, elle doit contenir les détails, exemples, contenues dans la news originale pour être pertinente et compréhensible par un auditeur non expert. Si besoin expliquer les acronymes ou les termes techniques sans résumer chaque article. \
            Si tu n'as pas assez d'info sur un article, le zapper. Attention si la news n'est pas originale, c'est à dire qu'elle traite d'information générique, la zapper. \
            Toujours démarrer par cette petite introduction, puis enchainer tout de suite aprés sur le script. Attention, ne jamais démarrer en disant, voici le script du podcast. toujours démarrer directement. \
            La conclusion du script doit etre courte et toujours sous cette forme : //Voilà qui conclut notre épisode d'aujourd'hui. Merci de nous avoir rejoints et n'oubliez pas de vous abonner pour ne manquer aucune de nos discussions passionnantes. À très bientôt dans Le monde aujourd'hui !// \
            "
"""

"""
# version askolovitch
prompt = 
À partir du texte fourni, générer un script de podcast en français d'au moins 30000 signes pour 'L'IA aujourd'hui', présenté par Michel Lévy Provençal, avec l'introduction standard 'Bienvenue dans L'IA aujourd'hui : le podcast de l'IA par l'IA qui vous permet de rester à la page !...' proposer une phrase qui resume les sujets traités dans cette épisode. Attention l'intro doit etre courte. PLutot que "Aujourd'hui, un menu varié et captivant : des décisions politiques influencées par des hallucinations d’IA, l’expansion audacieuse de GitHub vers des outils multi-modèles, l’épineuse question de la gouvernance de l’IA ignorée par la plupart des entreprises, et des tensions au sein de grandes entreprises technologiques. Nous explorerons également les impacts sociétaux de l'IA, ses limites éthiques et sa place croissante dans nos vies. Préparez-vous à plonger dans l’univers fascinant et complexe de l’intelligence artificielle !" dire par exemple  "Aujourd'hui : des décisions politiques influencées par des hallucinations d’IA, l’expansion audacieuse de GitHub vers des outils multi-modèles, l’épineuse question de la gouvernance de l’IA ignorée par la plupart des entreprises, et des tensions au sein de grandes entreprises technologiques. C'est parti !" La conclusion standard doit etre 'Voilà qui conclut notre épisode d'aujourd'hui. Merci de nous avoir rejoints et n'oubliez pas de vous abonner. À très bientôt dans L'IA aujourd'hui !'. 
Adopter un style de revue de presse dynamique avec un ton journalistique caractéristique de Claude Askolovitch sur France Inter (ne jamais citer cet élément). Chaque news doit être développée sur au moins 6000 signes, incluant contexte, détails et implications, en expliquant les termes techniques sans simplification excessive. Établir des liens pertinents entre les actualités pour créer une narration fluide. Ignorer les articles trop génériques ou manquant d'informations substantielles. Utiliser des transitions naturelles entre les sujets, des questions pour engager l'audience sur certains sujets qui s'y pretent. Ne pas le faire systematiquement. Le contenu doit être informatif et accessible, équilibrant faits techniques et analyse approfondie, en gardant toujours à l'esprit qu'il s'agit d'une revue de presse destinée à être écoutée. Le style de la revue de presse doit etre le suivant : 
Respecter le style et le format specifiés
<style>
Je vous parle d'une prison...
Ouverte aux quatre vents et pourtant elle n'a que trois ans la prison de Mulhouse dont les portes du parking du personnel sont régulièrement ouverte, et dont le chemin de ronde n'est protégé que par une grille d'un mètre vingt de hauteur. Elle manque aussi de barreaux aux fenêtres du quartier des femmes, cette prison de Mulhouse, et les carreaux de ses fenêtres se descellent au coupe-ongle et au couteau, ce qui permet d'alimenter les détenus en cannabis et en smartphones livrés par drone dans les cellules...
Je vous passe le béton imbibé d'eau, mais bref, voici tel que le raconte le figaro, sourcé aux personnel pénitentiaire, le paysage d'un ratage d'Etat... car la République que le président Macron voulait doter de 15000 places de prison supplémentaire, n'a pas toujours eu la main heureuse en choisissant les entreprises qui construiraient les nouvelles prisons... l'Etat s'est fait avoir par des mercenaires de la construction...
Elle me laisse rêveur, cette naïveté de la République, tant nous aurions besoin de réassurances quand nos vies se disjoignent.
Dans le même Figaro, l'historien Pierre Vermeren, livre un texte habité, sur "le suicide en cours de notre modèle social et politique", que porte notre incapacité à créer des richesses et la persistance d'un chômage de masse que les discours officiels prétendaient avoir contenu...
Vermeren oppose les élites des grandes agglomérations au peuple "qui mesure tous les jours la régression économique dans laquelle il se débat", il passe par la Lorraine dont la population régresse pour illustrer le péril. "La Meuse avait 215 000 habitants en 1962, elle n'en a plus que 180 000. L'abandon par la France des activités de production est la cause directe de cet effondrement sans précédent depuis la guerre de Trente Ans (au XVIIe siècle). Entre 1990 et 2022, la Lorraine a perdu 100 000 emplois industriels, et autant dans le secteur primaire. Sans la béquille du travail frontalier ce serait la catastrophe".. Je vous laisse lire les conséquences politiques de la catastrophe -sommes-nous si loin de l'Amérique...
Ce texte de Pierre Vermeren recoupe la tribune d'un économiste américain, Anton Brender, au Monde, qui décrit Donald Trump comme un homme qui menace la démocratie mais promet de faire baisser le prix des oeufs... Et recoupe aussi l'interview d'une femme de gauche radicale dans un journal de gauche, Libération, où Naomi Klein, canadienne essayiste altermondialiste dit écouter avec attention le podcast de l'idéologue trumpiste Steve Bannon, qui lui en apprend plus que les media amis…
Elle dit que Bannon voit dans l'expulsion de masse des immigrés un sujet économique, pour rendre des emplois aux américains, et cette manière de voir peut rendre le projet attrayant... Elle dit que l’extrême-droite se nourrit de la misère sociale et économique mais aussi de la souffrance des classes populaires jugées et menacées dans leurs mode de vie...
Elle dit enfin, Naomi Klein, que le complotisme s'appuie sur un sentiment légitime, tant les gens « ressentent profondément que le système est monté contre eux ».
« Ils entendent parler du Forum économique mondial à Davos, d'une jolie montagne en Suisse où les gens se retrouvent pour prendre des grandes décisions, et se mettent à imaginer quelque chose qui n'est pas tout à fait de l'ordre de la réalité. Leur diagnostic est faux. Mais leur sentiment est fondé. »
Et on parle donc du bon usage du complotisme!
Mais oui... Car cet éloge du complotisme se poursuit, je dis cela en souriant, dans un texte brillant d'un journal libéral rationnel, l'Opinion, signé d'un jeune essayiste, Raphael Llorca,qui voit dans les mensonges, la post-vérité, les outrances de Donald Trump, un placebo politique... Un discours qui ne parle pas de la réalité mais entre en phase avec un ressenti, donne un effet de sens, une illusion de certitude, participe d'une compréhension du monde, d'une guérison?
Llorca cite un roman américain, "Bien-être" de Nathan Hill, et aussi une interview puissante, qu'un philosophe français, François Noudelman, défenseur attristé, désespéré, de la vérité, a donné au site de Philosophie magazine après l'élection de Trump... Quand Trump ou les siens mentent, explique en substance Noudelman, même son électorat ne le croit pas, mais cela n’est pas le sujet. Dire que les migrants mangent des chats ou que l'on tue des bébés à la naissance dans les états démocrates, devient dit, Noudelman, une fiction assumée, un moyen d'attirer l'attention sur des choses supposées vraies -la coupure ici entre l'élite libérale et un peuple en déshérence...
On peut s'abandonner au vertige du mensonge tentateur - en réalité, Noudelman est horrifié... Mais il n'est pas absurde de se souvenir qu'au commencement est la souffrance sociale. Je lis dans le Dauphiné libéré que ce week end, des gilets jaunes sont venus à Davezieux, au rond-point de la croix de justice, célébrer les 6 ans de leur combat -ils viennent encore, chaque samedi, quand nous parlons désormais d'autre chose.... Ils parlent de révolte d'injustice de retraite de travailleurs pauvres du cout de la vie et du fossé entre les citoyens et le pouvoir et rien n'a changé, ils ont des banderoles où ils réclament la destitution du Président, la sortie de l'Union européenne et « pas un euro à l’Ukraine", comme si l'Ukraine y était pour quelque chose...
L'Opinion à sa une se demande si Trump sera pour l'Ukraine un président de la paix. Je vois dans cette question un hommage à la confusion des temps.
Je vous parle enfin d'un homard...
Pêché il y a trois mois, le 9 aout à Ouessant dans le Finistère et que depuis on entoure de soin, il est hébergé à Tregastel dans les Côtes d'Armor, hébergé dans un vivier de 600 litres d'eau pour lui tout seul, câliné bichonné nourri.... lui qui était né pour passer à la casserole remonté des casiers de Jean-Denis Le Pape... Oui lais ce homard bleu, est doré, couleur si rare qu'elle est un mystère et la passion des scientifiques, et lui donne le droit au traitement de faveur, au luxe, et la carapace de ce homard, quand il aura mué, sera expédiée aux États-Unis pour qu'on l'étudie...
je me suis demandé pourquoi tant d'attention pour animal rare et parfois si peu aux hommes...
Allons. Dans le Figaro (encore!) vous verrez une grand mère... Cheveux bouclés gris-bleu lunettes téléphone à la main, un ancien téléphone, noir en bakélite... Et forcément vous aller l'aimer cette mamie anglaise prénommée Daisy, pourtant agaçante, parce qu'elle est bavarde, ne comprend pas très bien ce que vous lui dite au téléphone, parle lentement, dit un peu n'importe quoi, tiens, par exemple, dans une conversation elle va vous proposer des photos de son chat...
Miaou...
Mais ne lui en voulez pas à Daisy, c’est pour la bonne cause qu'elle papote... Et puis elle n'existe pas vraiment... Elle a été inventée par l'opérateur téléphonique Virgin Media, à grand renfort d'intelligence artificielle, pour faire tourner en bourrique les brouteurs, comme on appelle les escrocs qui par téléphone vous arnaquent vous escroquent et qui sont une plaie -un britannique sur 5 dit etre sollicité par ces bandits une fois par semaine..... Daisy désormais, par les algorithmes sera leur leur chemin, elle peut les retenir avec son bavardage quarante minutes, et c'est du temps pendant lequel ils n'iront pas arnaquer quelqu'un d'autre... Thank you Miss Daisy!</style>
<style>
Je vous parle de sang…
Qu’un soldat sentait couler de son corps mais il ne le voyait pas ce sang, nul le voyait, me sang invisible dont il se vidait… Ce soldat, il s’appelait Eliron Mizrahi, qui avait combattu 186 jours à Gaza, conduisant un bulldozer de l’armée israélienne, s’est tué au mois de juin dernier, et le Monde qui me dit son histoire m’apprend que son ami Guy Zaken qui était le copilote de leur bulldozer, a témoigné ensuite devant une commission parlementaire, et a dit qu’à Gaza, les soldats israeliens avaient du écraser des palestiniens morts ou vivants par centaines…
Le Monde ne précise pas que Guy Zaken dans son témoignage, ne disait pas « écraser des palestiniens », mais « des terroristes », le mot n’est pas indifférent pour cet homme… Il disait aussi, Guy Zaken, je l’ai lu sur le site de CNN, ne plus pouvoir manger de la viande qui lui rappelait trop ce qu’il avait vu à Gaza, employant ce même mot, « viande », pour décrire les corps le sang des victimes de la guerre, « les nôtres et les leurs », ajoutait-il…
Et je pourrais m’excuser de nous imposer cela un début de semaine où j’aurais pu gambader avec de joyeux footballeurs, en Une de l’Equipe Rabiot et Digne de l’équipe de france qui a vaincu l’Italie, ou pas moins beaux, en une du Courrier picard, les héros de Liancourt-Clermont, vainqueurs de Brétigny en Coupe de France, qui au tour suivant iront c’est prestigieux jouer Rouen-Quevilly…
Mais le football ne change rien aux guerres… Et sur le site de Haaretz qui est un journal gardien de la conscience israélienne et qui ne fait pas de gros titre sur la victoire d’Israel contre la Belgique, je vois un ado farouche et fier en tenue de football qui s’appelait Naji, qui jouait défenseur dans le club de son village en Cisjordanie, qui rêvait d’aller faire un stage de foot en Jordanie comme son grand frère avant lui, mais qui un jour a quitté son match pour aller jeter des pierres et des soldats israeliens l’ont tué au lieu de l’arrêter, puis ont cassé le bras de son père Nidal qui voulait s’avancer vers le corps de son fils…
Je me demande ce que change dans l’opinion israélienne l’article de Haaretz -que changeons-nous, journalistes. Je me demande aussi ce que pensent les jeunes soldats qui ont tiré sur Naji et frappé Nidal…
Le site du Monde répond partiellement à cette question, en racontant donc le suicide d’un conducteur de bulldozer, et en rencontrant deux soldats israéliens, revenus de Gaza, victimes de stress post-traumatique, qui réapprennent à vivre, à drainer leur peur et la violence, dans un ranch près de Tel Aviv, créé par un israelien d’origine argentine, au contact de chevaux. Ils racontent une guerre où le danger est partout, l’ennemi n’a pas d’uniforme, et les gamins, les gamins de Gaza dont on ne comprend pas s’ils les prennent en pitié ou s’ils en avaient peur, et qui disent, « pour vous nous sommes des monstres, n’est-ce pas ? ». Et le journal, et des psys, nous expliquent comment on peut être à la fois victime et bourreau.
On parle aussi d’un moustique…
Un moustique mutant, attention, un moustique humanoïde, un enfant-dengue (dengue comme la maladie, pas la folie), qui survit et joue à un jeu video dans un bidonville deux siècles et demi après nous, 2272, dans ce qui fut l’argentine et qui est devenu un archipel d’ilots chétifs après que les eaux libérées par la fonte des glaces ont englouti Buenos Aires et la Patagonie… C’est Mediapart qui m’évoque cette aventure de science-fiction drôle absurde imprégnée d’esprit gaucho-punk, a dit le journal espagnol El Païs, gaucho n’étant pas une catégorie politique mais le cavalier mythique de la culture argentine… Le roman s’appelle « L’enfance du monde », traduit chez Christian Bourgois, son auteur Michel Nieva, argentin vivant aux Etats-Unis, traducteur d’Héraclite du grec et de Faulkner de Dixie, et aussi concepteur à l’occasion de jeux vidéos…
Mais ce qui me rend cette histoire curieuse, intrigante, c’est que Nieva accompagne son roman d’un essai, qui le suit, un roman et un essai dans un même volume, il y voit une cohérence… L’essai est titré « La Science-Fiction capitaliste », Nieva y dénonce l’appropriation de son art littéraire par des milliardaires qui y piochent l’argumentaire des technologies qu’ils concoctent, Nieva, cible Elon Musk, qui aurait trouvé chez Asimov l’idée de nous faire migrer dans l’espace, et qui sur cette terre contribue à ravager les sols pour ses véhicules électriques. Nieva veut témoigner des territoires qui disparaissent et veut nous suggérer d’autres utopies…
Nous le retrouvons Monsieur Musk, cible de deux tribunes de Libération, où deux têtes bien faites du CNRS, le mathématicien David Chavalarias et la chercheuse en biologie Florence Debarre, nous invitent à organiser notre départ de X, ex twitter le réseau social qui fut pourtant dit Florence Debarre un précieux outil de travail, mais que Elon Musk a asservi à ses causes et au triomphe de Donald Trump…
La lettre X me revient dans son autre acception, la nôtre, qui désigne l’Ecole polytechnique qui manque de sous et de femmes pour assurer son avenir… Les filles ne sont plus que 16% des admises et il va falloir recruter en contournant les prépas traditionnelles, s’ouvrir encore, les sciences de la vie, la médecine, les doubles licences de la fac… Quant aux sous, et bien, pour tenir son rang et sécuriser notamment un chouette batiment pour les maths, X s’en va chercher 200 millions chez ses donateurs, son réseau des anciens…
Et on parle enfin d’une fougère…
Une fougère capillaire d’une espèce rare trouvée au Bois Bryat à Revin, et dont la présence me dit l’Ardennais, retarde les travaux d’une déchetterie espérée planifiée -il va falloir déplacer la fougère avant de construire l’avenir…
Pourra-t-s’il s’inspirer de cette patience, Frédéric Douchet maire de Grandvilliers dans l’Oise dont le Courrier picard me dit qu’il veut déplacer le grand marché de sa ville du lundi au samedi, afin que les gens qui travaillent puissent s’y rendre, au marché… Pas bête mais…
Mais le lundi c’est le jour où vient de Rouen le Marché royal, qui vend des fruits et légumes et qui le samedi est a Elbeuf, alors il ne viendrait plus… Le le lundi c’est le jour des personnes âgées des retraités auxquels les commerçants apportent le panier a domicile, le marché du lundi, c’est Grandvilliers lui-même. La ville a été créée en 1212 par l’abbaye de Saint-Lucien et le marché le lundi a commencé en 1213, peut-on ainsi abolir 812 ans d’histoire?
J’ai lu dans le Bonhomme picard que Frédéric Douchet, donc le maire, est d’une dynastie politique, son oncle Arthur fut maire de Thieuloy-Saint-Antoine pendant quarante-sept ans, lui Frédéric est née à Thieuloy-Saint-Antoine mais a étudié de la maternelle au collège a Grandvilliers, puis il a vadrouillé pour les études et le boulot en Normandie et en région parisienne, il a été de la fonction publique et a monté des boites de conseil, il est revenu se faire élire dans le bourg de son enfance, je me demande si le guette la tentation d’entrer dans l’histoire…
</style>
<format>
Toujours rédiger la revue de presse comme un script complet à lire, sans titre, sous titre ou bullet point. Cela doit etre un texte pret à être lu. Ne pas marquer dans le script des éléments de forme (ex: transition, titre ou silence).Evite la succession d'adjectifs, va droit au but. Le podcast ne cessessite pas une intro longue mais direct.
</format>"""



prompt = """

Contexte : Vous êtes chargé(e) d’écrire un script en français complet pour un podcast quotidien de revue de presse sur la géopolitique intitulé Le monde Aujourd’hui. Ce podcast doit être informatif, factuel et engageant, conçu pour un auditoire curieux mais non-expert. L’objectif est de fournir un contenu captivant et accessible tout en restant rigoureux.

Consignes spécifiques :

- Structure du script :
  - Introduction :
    - Courte et percutante, introduire le podcast avec la phrase standard :  
      "Bonjour et bienvenue dans Le monde Aujourd’hui, le podcast quotidien de géopolitique par l’IA!"  
    - Suivre par une phrase résumant les sujets du jour, concise et dynamique :  
      "Aujourd’hui : [grandes thématiques du jour]."
  - Les grandes actualités du jour :  
    Développez chaque actualité en au moins 6000 signes, en incluant :
    - Contexte détaillé : origine, évolution du sujet.
    - Détails et implications : chiffres, exemples, conséquences.
    - Etre précis dans le compte rendu des infos. Pas d'information générique ou vague.
    - Évitez les actualités génériques ou redondantes, en privilégiant les informations originales et significatives.
    
  - Focus thématique (facultatif) :  
    Si un sujet particulier se prête à une analyse approfondie, développez un segment dédié (par exemple : un événement spécifique, une décision réglementaire majeure, ou une avancée géopolitique remarquable). Ce segment doit être construit comme une mini-enquête journalistique.
  - Transitions :  
    Utilisez des transitions naturelles entre les sujets, en assurant une narration fluide. Variez les styles pour éviter la répétition, mais restez sobre : pas d’abus de questions rhétoriques ou d’effets de style inutiles.
  - Conclusion :  
    Ne pas faire de récapitulatif court. Tout de suite après la dernière actualité, conclure avec la phrase standard :  
      "Voilà qui conclut notre épisode d’aujourd’hui. Merci de nous avoir rejoints, et n’oubliez pas de vous abonner pour ne manquer aucune de nos discussions passionnantes. À très bientôt dans Le monde Aujourd’hui !"

- Ton et style :
  - Utiliser un français litteraire, n'buse pas des adjectifs, soit simple et direct
- Accessible mais rigoureux : Évitez un ton trop technique ou professoral. Expliquez les concepts sans les simplifier à outrance.
  - Engageant et fluide : Adoptez un style journalistique équilibré, dynamique mais sans excès d’emphase.
  - Informé et crédible : Appuyez-vous sur des faits solides, sourcés et vérifiés, en évitant les conjectures.
  - Sans redondance : Limitez les répétitions ou les apartés trop longs.
  - Unifier les thématiques : Lorsque possible, établissez des liens entre les sujets pour créer une narration cohérente et captivante.
  - N"utilise pas de titre pour chaque news.
  - N'insiste pas sur les questions rhétoriques pour chaque news et n'abuse pas des commentaires génériques relatifs à des questions, ethiques, philosophiques ou politiques liées à ces news. 
  - Contente toi de donner les faits.
  - Eviter les mots comme : "crucial", "important", "essentiel", "fondamental", "révolutionnaire", "extraordinaire", "incroyable", "exceptionnel", "fantastique", "génial", "fabuleux", "merveilleux", "formidable", "superbe", "extraordinaire", "époustouflant", "étonnant", "impressionnant", "phénoménal", "stupéfiant", "miraculeux", "prodigieux", "sensationnel", "sublime", "grandiose", "majestueux", "magnifique", "splendide", "éblouissant", "éclatant", "radieux", "rayonnant", "resplendissant", "scintillant", "étincelant", "chatoyant", "coloré", "vif", "éclatant" et éviter les superlatifs.

Objectif final : Produire un script détaillé, prêt à être lu, d’une durée de **10 à 15 minutes**, soit environ **30 000 signes**, en intégrant les actualités fournies de manière exhaustive et captivante.

Instructions pour les actualités fournies :
1. Développez chaque sujet avec rigueur en exploitant les détails, les chiffres et les exemples fournis dans les sources.
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
# voice_id = "1e772jvf7it56XMrbdci" # Marco
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


titre = "Le monde aujourd'hui épisode du " + str(date.today())
text = text_final
audio = final_filename
email = "michel@brightness.fr"  # Remplacez 'destinataire' par 'email'
subtitle = "Le monde aujourd'hui : le podcast géopolitique par l'IA qui vous permet de rester à la page !"
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
url = "https://open.acast.com/rest/shows/677268f0310557bf4f6d31a6/episodes"
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



