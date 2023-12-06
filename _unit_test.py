import lib__agent_buildchronical
import lib__anthropic
import os
import random
import lib__embedded_context
import PyPDF2
import docx
import lib__hfmodels
import os  # Import os module for interacting with the operating system
from dotenv import load_dotenv  # Import dotenv module for loading .env files
import lib__env
import lib__script_tasks
import lib__transformers
import generatechatcompletion

load_dotenv(lib__env.DOTENVPATH)
hf_token = os.environ.get("HF_API_TOKEN")
hf_url = os.environ.get("MODEL_URL")

"""

####################################################################################################
# Testing : lib__agent_buildchronical
####################################################################################################
 
print("\n\n###############################################\n\n")

print("testing : lib__agent_buildchronical.generate_image")
lib__agent_buildchronical.generate_image("un chat sur une fenetre", "tests/chat.jpg")


print("\n\n###############################################\n\n")

def test_mailaudio():
    print("testing: lib__agent_buildchronical.mailaudio")
    try:
        lib__agent_buildchronical.mailaudio(
            title="Test Email",
            audio="path/to/audio.mp3",
            text="Ceci est un test.",
            email="example@example.com"
        )
        print("mailaudio executed without errors.")
    except Exception as e:
        print(f"Erreur dans mailaudio: {e}")

def test_mail_nofile():
    print("testing: lib__agent_buildchronical.mail_nofile")
    try:
        lib__agent_buildchronical.mail_nofile(
            title="Test Email",
            text="Ceci est un test sans fichier.",
            email="example@example.com"
        )
        print("mail_nofile executed without errors.")
    except Exception as e:
        print(f"Erreur dans mail_nofile: {e}")

# Exécution des tests
test_mailaudio()
test_mail_nofile()
print("\n\n")


print("\n\n###############################################\n\n")

def test_replace_numbers_with_text():
    print("testing: lib__agent_buildchronical.replace_numbers_with_text")
    try:
        result = lib__agent_buildchronical.replace_numbers_with_text("Il y a 5 pommes et 20% de réduction.")
        print(result)
        print("replace_numbers_with_text executed without errors.")
    except Exception as e:
        print(f"Erreur dans replace_numbers_with_text: {e}")

test_replace_numbers_with_text()
print("\n\n")

print("\n\n###############################################\n\n")

def test_split_text():
    print("testing: lib__agent_buildchronical.split_text")
    try:
        chunks = lib__agent_buildchronical.split_text("a" * 1500, limit=1000)
        print(chunks)
        print("split_text executed without errors.")
    except Exception as e:
        print(f"Erreur dans split_text: {e}")

test_split_text()
print("\n\n")


print("\n\n###############################################\n\n")

def test_texttospeech():
    print("testing: lib__agent_buildchronical.texttospeech")
    voice_id = "TxGEqnHWrfWFTfGW9XjX" # Josh
    try:
        lib__agent_buildchronical.texttospeech("Bonjour", voice_id, "tests/bonjour.mp3")
        print("texttospeech executed without errors.")
    except Exception as e:
        print(f"Erreur dans texttospeech: {e}")

test_texttospeech()

print("\n\n###############################################\n\n")

def test_convert_and_merge():
    print("testing: lib__agent_buildchronical.convert_and_merge")
    voice_id = "TxGEqnHWrfWFTfGW9XjX" # Josh
    try:
        lib__agent_buildchronical.convert_and_merge("Bonjour", voice_id, "tests/merged.mp3")
        print("convert_and_merge executed without errors.")
    except Exception as e:
        print(f"Erreur dans convert_and_merge: {e}")

test_convert_and_merge()


print("\n\n###############################################\n\n")


def test_extract_first_link():
    print("testing: lib__agent_buildchronical.extract_first_link")
    try:
        first_link = lib__agent_buildchronical.extract_first_link("https://rss.app/feeds/ts7TBAc6R3BNeWTU.xml")
        print("extract_first_link executed without errors.")
        print(first_link)
    except Exception as e:
        print(f"Erreur dans extract_first_link: {e}")


print("\n\n###############################################\n\n")

def test_extract_n_links():
    print("testing: lib__agent_buildchronical.extract_n_links")
    try:
        links = lib__agent_buildchronical.extract_n_links("https://rss.app/feeds/ts7TBAc6R3BNeWTU.xml", 5)
        print("extract_n_links executed without errors.")
        print(links)
    except Exception as e:
        print(f"Erreur dans extract_n_links: {e}")

test_extract_first_link()
test_extract_n_links()


print("\n\n###############################################\n\n")


def test_extract_title():
    print("testing: lib__agent_buildchronical.extract_title")
    try:
        title = lib__agent_buildchronical.extract_title("http://mikiane.com")
        print("extract_title executed without errors.")
        print(title)
    except Exception as e:
        print(f"Erreur dans extract_title: {e}")

test_extract_title()


print("\n\n###############################################\n\n")

def test_execute():
    print("testing: lib__agent_buildchronical.execute")
    try:
        result = lib__agent_buildchronical.execute("Bonjour", "https://mikiane.com", "")
        print("execute executed without errors.")
        print(result)
    except Exception as e:
        print(f"Erreur dans execute: {e}")

test_execute()



print("\n\n###############################################\n\n")



def test_create_image_with_text():
    print("testing: lib__agent_buildchronical.create_image_with_text")
    try:
        lib__agent_buildchronical.create_image_with_text("Test", "datas/input.jpg", "datas/output.jpg")
        print("create_image_with_text executed without errors.")
    except Exception as e:
        print(f"Erreur dans create_image_with_text: {e}")

test_create_image_with_text()




####################################################################################################
# Testing : lib__antropic
####################################################################################################

print("\n\n###############################################\n\n")

def test_generate_chat_completion_anthropic():
    # Test inputs
    consigne = "traduire en anglais"
    texte = "Bonjour je m'appelle anthropic"

    try:
        # Attempt to call the function
        results = lib__anthropic.generate_chat_completion_anthropic(consigne, texte)

        # If the function returns a generator, attempt to get the first item
        try:
            first_result = next(results)
            print("Function executed successfully. First result:", first_result)
        except StopIteration:
            print("Function executed, but no items in the generator.")
    except Exception as e:
        # If an error occurs, print the error
        print("Error occurred:", e)

# Call the test function
test_generate_chat_completion_anthropic()



####################################################################################################
# Testing : lib__embedded_context
####################################################################################################

print("\n\n###############################################\n\n")

def test_generate_unique_filename():
    try:
        # Mock inputs
        prefix = "test"
        suffix = "txt"

        # Call the function
        filename = lib__embedded_context.generate_unique_filename(prefix, suffix)
        print(f"Function executed successfully. Generated filename: {filename}")
    except Exception as e:
        print("Error occurred:", e)

test_generate_unique_filename()


print("\n\n###############################################\n\n")


def test_convert_pdf_to_text():
    try:
        # Mock input - Ensure a test PDF file exists at this path
        file_path = "datas/test.pdf"

        # Call the function
        text = lib__embedded_context.convert_pdf_to_text(file_path)
        print(f"Function executed successfully. Extracted text: {text[:100]}...")
    except Exception as e:
        print("Error occurred:", e)

test_convert_pdf_to_text()

print("\n\n###############################################\n\n")



def test_convert_docx_to_text():
    try:
        # Mock input - Ensure a test DOCX file exists at this path
        file_path = "datas/test.docx"

        # Call the function
        text = lib__embedded_context.convert_docx_to_text(file_path)
        print(f"Function executed successfully. Extracted text: {text[:100]}...")
    except Exception as e:
        print("Error occurred:", e)

test_convert_docx_to_text()

print("\n\n###############################################\n\n")


def test_concat_files_in_text():
    try:
        # Mock input - Directory path with some text files
        path = "datas/txt"

        # Call the function
        combined_text = lib__embedded_context.concat_files_in_text(path)
        print(f"Function executed successfully. Combined text: {combined_text[:100]}...")
    except Exception as e:
        print("Error occurred:", e)

test_concat_files_in_text()


print("\n\n###############################################\n\n")

def test_convert_csv_to_text():
    try:
        result = lib__embedded_context.convert_csv_to_text("datas/sample.csv")
        print(f"Function executed successfully. Combined text: {result[:100]}...")

    except Exception as e:
        print(f"Error in convert_csv_to_text: {e}")

# Execute the test
test_convert_csv_to_text()

print("\n\n###############################################\n\n")

def test_convert_json_to_text():
    try:
        result = lib__embedded_context.convert_json_to_text("datas/sample.json")
        print(f"Function executed successfully. Combined text: {result[:100]}...")
    except Exception as e:
        print(f"Error in convert_json_to_text: {e}")

# Execute the test
test_convert_json_to_text()


print("\n\n###############################################\n\n")

def test_convert_excel_to_text():
    try:
        result = lib__embedded_context.convert_excel_to_text("datas/sample.xlsx")
        print(f"Function executed successfully. Combined text: {result[:100]}...")
    except Exception as e:
        print(f"Error in convert_excel_to_text: {e}")

# Execute the test
test_convert_excel_to_text()

print("\n\n###############################################\n\n")

def test_convert_pptx_to_text():
    try:
        result = lib__embedded_context.convert_pptx_to_text("datas/sample.pptx")
        print(f"Function executed successfully. Text content: {result[:100]}...")
    except Exception as e:
        print(f"Error in convert_pptx_to_text: {e}")

# Execute the test
test_convert_pptx_to_text()

print("\n\n###############################################\n\n")

def test_convert_xml_to_text():
    try:
        result = lib__embedded_context.convert_xml_to_text("datas/sample.xml")
        print(f"Function executed successfully. Text content: {result[:100]}...")
    except Exception as e:
        print(f"Error in convert_xml_to_text: {e}")

# Execute the test
test_convert_xml_to_text()

print("\n\n###############################################\n\n")

def test_convert_html_to_text():
    try:
        result = lib__embedded_context.convert_html_to_text("datas/sample.html")
        print(f"Function executed successfully. Text content: {result[:100]}...")
    except Exception as e:
        print(f"Error in convert_html_to_text: {e}")

# Execute the test
test_convert_html_to_text()

print("\n\n###############################################\n\n")

def test_convert_image_to_text():
    try:
        result = lib__embedded_context.convert_image_to_text("datas/sample.jpg")
        print(f"Function executed successfully. Text content: {result[:100]}...")
    except Exception as e:
        print(f"Error in convert_image_to_text: {e}")

# Execute the test
test_convert_image_to_text()

print("\n\n###############################################\n\n")

def test_convert_text_to_text():
    try:
        result = lib__embedded_context.convert_text_to_text("datas/sample.txt")
        print(f"Function executed successfully. Text content: {result[:100]}...")
    except Exception as e:
        print(f"Error in convert_text_to_text: {e}")

# Execute the test
test_convert_text_to_text()



print("\n\n###############################################\n\n")


def test_concat_files_in_text():
    try:
        result = lib__embedded_context.concat_files_in_text("datas/txt")  # Replace 'test_data' with the path to your test directory
        print(f"Function executed successfully. Combined text (sample): {result[:100]}...")
    except Exception as e:
        print(f"Error in concat_files_in_text: {e}")

test_concat_files_in_text()


print("\n\n###############################################\n\n")

def test_split_text_into_blocks():
    test_text = "This is a sample text to test the split_text_into_blocks function." * 100  # Sample text
    try:
        result = lib__embedded_context.split_text_into_blocks(test_text, limit=4000)
        print(f"Function executed successfully. Number of blocks created: {len(result)}")
    except Exception as e:
        print(f"Error in split_text_into_blocks: {e}")

test_split_text_into_blocks()


print("\n\n###############################################\n\n")

def test_write_blocks_to_csv():
    test_blocks = ["Block 1", "Block 2", "Block 3"]  # Sample blocks
    test_path = "./"  # Set the path where you want to save the CSV file
    test_filename = "sample.csv"
    try:
        lib__embedded_context.write_blocks_to_csv(test_blocks, test_path, test_filename)
        print(f"Function executed successfully. Blocks written to {test_path + test_filename}")
    except Exception as e:
        print(f"Error in write_blocks_to_csv: {e}")

test_write_blocks_to_csv()


print("\n\n###############################################\n\n")


def test_get_embedding():
    test_text = "Sample text for testing the embedding function."
    try:
        result = lib__embedded_context.get_embedding(test_text, engine="text-embedding-ada-002")
        print(f"Function executed successfully. Embedding length: {len(result)}")
        print(f"Function executed successfully. Embedding value: {result}")

    except Exception as e:
        print(f"Error in get_embedding: {e}")

test_get_embedding()

print("\n\n###############################################\n\n")


def test_create_embeddings():
    try:
        # Assuming 'datas/sample.csv' is a valid CSV file in the correct format
        result_path = lib__embedded_context.create_embeddings("datas/", "sample_emb.csv")
        print(f"Function executed successfully. Embeddings saved in: {result_path}")
    except Exception as e:
        print(f"Error in create_embeddings: {e}")

# Execute the test
test_create_embeddings()

print("\n\n###############################################\n\n")


def test_query_extended_llm():
    print("testing: query_extended_llm")
    try:
        # Remplacer 'input_text' par un texte de test et 'index_file.csv' par un nom de fichier valide
        response = lib__embedded_context.query_extended_llm("parle moi de hacks et d'attaques cyber", "datas/emb_sample_emb.csv")
        if isinstance(response, str):
            print("query_extended_llm executed without errors and returned a string. : " + response)
        else:
            print("query_extended_llm did not return a string.")
    except Exception as e:
        print(f"Erreur dans query_extended_llm: {e}")

# Exécution du test
test_query_extended_llm()


####################################################################################################
# Testing : lib__hfmodels
####################################################################################################

print("\n\n###############################################\n\n")

# Mock inputs for the test
mock_prompt = "Traduire ce texte en anglais : 'Je veux créer une page web avec des images et des textes. Comment puis-je créer une page web avec des images et des textes ? Vous pouvez utiliser HTML, CSS et JavaScript pour créer une page web avec des images et des textes. HTML est utilisé pour structurer la page web, CSS est utilisé pour définir le style de la page web et JavaScript est utilisé pour ajouter des fonctionnalités interactives à la page web. Vous pouvez utiliser un éditeur de texte pour créer votre page web, puis utiliser un navigateur web pour la visualiser. Il existe de nombr ux ressources en ligne pour aider à apprendre HTML, CSS et JavaScript, tels que des tutorials, des guides et des exemples de code.'"
dummy_token = hf_token
dummy_url = hf_url
max_token = 1024
num_tokens = 300

for result in lib__hfmodels.stream_hfllm(mock_prompt, dummy_token, dummy_url, max_token, num_tokens):
    print(result)
        
    # Since it's a generator, we attempt to get the first item
    # first_response = next(result, "No response")
    # print(f"Function executed successfully. First response: {first_response}")

# Execute the test







    
consigne = "Traduire ce texte en anglais : "
texte = "'Je veux créer une page web avec des images et des textes. Comment puis-je créer une page web avec des images et des textes ? Vous pouvez utiliser HTML, CSS et JavaScript pour créer une page web avec des images et des textes. HTML est utilisé pour structurer la page web, CSS est utilisé pour définir le style de la page web et JavaScript est utilisé pour ajouter des fonctionnalités interactives à la page web. Vous pouvez utiliser un éditeur de texte pour créer votre page web, puis utiliser un navigateur web pour la visualiser. Il existe de nombr ux ressources en ligne pour aider à apprendre HTML, CSS et JavaScript, tels que des tutorials, des guides et des exemples de code.'"
dummy_token = hf_token
dummy_url = hf_url
max_token = 1024
num_tokens = 300
for result in generatechatcompletion.generate_chat(consigne, texte, model="hf", model_url=dummy_url):
    print(result)


"""
from huggingface_hub import InferenceClient

client = InferenceClient(hf_url, token=hf_token)
for token in client.text_generation("How do you make cheese?", max_new_tokens=500, stream=True):
    print(token)

"""
####################################################################################################
# Testing : lib__script_tasks
####################################################################################################
print("\n\n###############################################\n\n")

def test_request_llm():
    prompt_test = "Bonjour je voudrais que tu traduises en anglais"
    context_test = "Cette fonction de test utilise une clé API fictive pour éviter une connexion réelle à l'API OpenAI."
    input_data_test = "Le test se concentre sur la capture des exceptions et l'affichage des messages d'erreur."
    model_test = "gpt-4"

    try:
        # Utilisation de valeurs fictives pour l'API key afin d'éviter une vraie connexion
        result = lib__script_tasks.request_llm(prompt_test, context_test, input_data_test, model_test)
        print(f"Function executed successfully. Result: {result[:100]}...")
    except Exception as e:
        print(f"Error in request_llm: {e}")

# Execute the test
test_request_llm()




print("\n\n###############################################\n\n")


def test_execute_tasks():
    try:
        # Mock tasks and model for testing
        tasks = {
            "task1": {
                "input_data": "Voiture électrique : l'étonnante stratégie de Toyota en Europe Le japonais ne commercialise qu'un seul modèle 100 % à batteries. Il compte sur ses motorisations hybrides pour gagner du temps, au risque de voir la concurrence s'éloigner loin devant… Ajouter à mes articles Commenter Partager Bruxelles Japon Toyota Urban SUV Concept Toyota Urban SUV Concept (Toyota) Par Guillaume Guichard Publié le 4 déc. 2023 à 6:30Mis à jour le 4 déc. 2023 à 6:33 Pour Toyota, la révolution électrique peut attendre. Le constructeur japonais a précisé la semaine dernière à Bruxelles son offensive dans l'électrique en Europe. « Nous nous sentons plus prêts qu'avant pour prendre la place qui est la nôtre sur le marché de l'électrique », mar﻿tèle Andrea Carlucci, vice-président de Toyota Motor Europe. Longtemps rétif à développer une gamme tout électrique, le numéro un mondial du secteur n'aura toutefois pas de gamme complète de voitures à batteries avant 2026. Encore au stade des concepts… Pour faire patienter clients et observateurs, il a présenté aux journalistes européens deux nouveaux « concepts » aux lignes tendues et aux angles acérés. Le premier, le plus éloigné du design final, est un « crossover » sport (soit un croisement entre un SUV et une berline) et ne sera commercialisé qu'en 2025. La deuxième des deux futures voitures dévoilées lundi en Europe, un SUV citadin de segment B, devrait faire son entrée sur le marché l'année prochaine. LIRE AUSSI : Toyota veut casser son image de mauvais élève de la voiture électrique « Nous, nous faisons de la vraie cuisine… » : quand le patron de Toyota s'en prend à Tesla Pour ne pas assommer le consommateur avec un prix trop lourd, le futur SUV de segment C sera proposé avec deux options de batteries. Ce véhicule viendra rejoindre dans les concessions la seule voiture électrique de la marque. A savoir le bZ4x , commercialisé depuis septembre en France et importé du Japon. Pas de voiture électrique pas chère à l'horizon Toyota est le seul grand constructeur à forte présence en Europe à ne pas avoir de gamme plus large. Stellantis en compte aujourd'hui 13 , Volkswagen Group plus d'une dizaine également, Renault une demi-dizaine à partir de l'année prochaine. LIRE AUSSI : DECRYPTAGE - La voiture électrique à 25.000 euros, le nouveau Graal de l'automobile Le constructeur japonais ne semble pas non plus à ce stade miser sur un véhicule électrique à moins de 25.000 euros. Tous les constructeurs européens grand public tablent pourtant sur ce type de modèle pour ouvrir un large marché à l'électrique. « Nous ne sommes pas dans cette course, a reconnu Andrea Carlucci. Mais nous devons nous en préoccuper. » Certes, un jour, le japonais devrait commercialiser une citadine Yaris électrique. « Ce sera tout naturel à un moment donné », a reconnu le dirigeant. Probablement en 2026, pour compléter sa future gamme de six véhicules à batterie. L'hybride pour diminuer les émissions de CO2 En attendant, Toyota renvoie les clients qui veulent des voitures plus accessibles vers les motorisations essence voire hybride. Une autre façon de justifier la stratégie multi-énergie du groupe - thermique, hybrides, et un peu de tout électrique. Si le japonais prend le temps, c'est qu'il peut se le permettre. Grâce à ses modèles hybrides à succès, il fait davantage que remplir les objectifs de diminution des émissions de CO2 imposés aux constructeurs par l'Union européenne. Son mix est « électrifié » - comprendre surtout hybride - à hauteur de 71 %. Il vise 75 % en 2024. LIRE AUSSI : Automobile : l'usine Toyota de Valenciennes devient la première usine française Malgré le peu d'enthousiasme de la direction de Toyota ces dernières années sur les véhicules 100 % électriques, les équipes de R&D du géant automobile planchaient discrètement sur des ruptures technologiques présentées comme majeures. Un domaine que peu de concurrents ont investigué eux-mêmes, se reposant plutôt sur des fournisseurs, ou au mieux sur des coentreprises avec des spécialistes. Toyota porte le fer dans les batteries Toyota vise une industrialisation de ses nouvelles technologies, dévoilées cet été, à horizon 2026. Celles-ci seraient plus denses et moins chères. Cette performance a priori antinomique laisse sceptiques les spécialistes ès batteries de Brass North America, interrogés par les analystes d'UBS. LIRE AUSSI : Voiture électrique : Toyota promet des batteries à faire pâlir d'envie Tesla Mieux, Toyota assure être maintenant très proche du Graal des fabricants de batterie , la batterie solide. Une méthode de production de masse est en cours de développement, précise Toyota, qui vise une commercialisation en 2027-2028. D'après Brass North America, le constructeur a pris une longueur d'avance sur les spécialistes américains du sujet que sont QuantumScape et SolidPower. Toutefois, le japonais n'inondera pas le marché avec ses batteries solides. « Nous les commercialiserons graduellement, à plus petite échelle », précise Andrea Carlucci. Le groupe anticipe une production de « plusieurs dizaines de milliers de voitures » à horizon 2028. Soit quelques dixièmes du marché global de la voiture électrique.",
                "prompt": "traduire en anglais",
                "brain_id": ""
            }
        }
        model = "gpt-4"


        # Execute the function with mock data
        results = list(lib__script_tasks.execute_tasks(tasks, model))
        
        print("Function executed successfully.")
        for result in results:
            print(f"{result}")

    except Exception as e:
        print(f"Error in execute_tasks: {e}")

# Execute the test
test_execute_tasks()



def test_request_llm_stream():
    try:
        # Dummy data for testing
        prompt = "Traduire en anglais"
        context = "Voiture électrique : l'étonnante stratégie de Toyota en Europe Le japonais ne commercialise qu'un seul modèle 100 % à batteries."
        input_data = "Il compte sur ses motorisations hybrides pour gagner du temps, au risque de voir la concurrence s'éloigner loin devant… "
        model = "gpt-4-1106-preview"  # Example model, change as needed

        # Attempt to call the function with dummy data
        response_generator = list(lib__script_tasks.request_llm_stream(prompt, context, input_data, model))

        # Iterate over the response generator and print each result
        # Note: In a real scenario, this would produce outputs from the OpenAI API
        print("\n\nFunction executed successfully.")
        
    except Exception as e:
        print(f"Error in request_llm_stream: {e}")

# Execute the test
test_request_llm_stream()



def test_truncate_strings():
    prompt = "Tradurie en francais ancien"
    context = "Voiture électrique : l'étonnante stratégie de Toyota en Europe Le japonais ne commercialise qu'un seul modèle 100 % à batteries. Il compte sur ses motorisations hybrides pour gagner du temps, au risque de voir la concurrence s'éloigner loin devant… Ajouter à mes articles Commenter Partager Bruxelles Japon Toyota Urban SUV Concept Toyota Urban SUV Concept (Toyota) Par Guillaume Guichard Publié le 4 déc. 2023 à 6:30Mis à jour le 4 déc. 2023 à 6:33 Pour Toyota, la révolution électrique peut attendre. " 
    input_data = "Le constructeur japonais a précisé la semaine dernière à Bruxelles son offensive dans l'électrique en Europe. « Nous nous sentons plus prêts qu'avant pour prendre la place qui est la nôtre sur le marché de l'électrique », mar﻿tèle Andrea Carlucci, vice-président de Toyota Motor Europe. Longtemps rétif à développer une gamme tout électrique, le numéro un mondial du secteur n'aura toutefois pas de gamme complète de voitures à batteries avant 2026. Encore au stade des concepts… Pour faire patienter clients et observateurs, il a présenté aux journalistes européens deux nouveaux « concepts » aux lignes tendues et aux angles acérés. Le premier, le plus éloigné du design final, est un « crossover » sport (soit un croisement entre un SUV et une berline) et ne sera commercialisé qu'en 2025. La deuxième des deux futures voitures dévoilées lundi en Europe, un SUV citadin de segment B, devrait faire son entrée sur le marché l'année prochaine. LIRE AUSSI : Toyota veut casser son image de mauvais élève de la voiture électrique « Nous, nous faisons de la vraie cuisine… » : quand le patron de Toyota s'en prend à Tesla Pour ne pas assommer le consommateur avec un prix trop lourd, le futur SUV de segment C sera proposé avec deux options de batteries. Ce véhicule viendra rejoindre dans les concessions la seule voiture électrique de la marque. A savoir le bZ4x , commercialisé depuis septembre en France et importé du Japon. Pas de voiture électrique pas chère à l'horizon Toyota est le seul grand constructeur à forte présence en Europe à ne pas avoir de gamme plus large. Stellantis en compte aujourd'hui 13 , Volkswagen Group plus d'une dizaine également, Renault une demi-dizaine à partir de l'année prochaine. LIRE AUSSI : DECRYPTAGE - La voiture électrique à 25.000 euros, le nouveau Graal de l'automobile Le constructeur japonais ne semble pas non plus à ce stade miser sur un véhicule électrique à moins de 25.000 euros. Tous les constructeurs européens grand public tablent pourtant sur ce type de modèle pour ouvrir un large marché à l'électrique. « Nous ne sommes pas dans cette course, a reconnu Andrea Carlucci. Mais nous devons nous en préoccuper. » Certes, un jour, le japonais devrait commercialiser une citadine Yaris électrique. « Ce sera tout naturel à un moment donné », a reconnu le dirigeant. Probablement en 2026, pour compléter sa future gamme de six véhicules à batterie. L'hybride pour diminuer les émissions de CO2 En attendant, Toyota renvoie les clients qui veulent des voitures plus accessibles vers les motorisations essence voire hybride. Une autre façon de justifier la stratégie multi-énergie du groupe - thermique, hybrides, et un peu de tout électrique. Si le japonais prend le temps, c'est qu'il peut se le permettre. Grâce à ses modèles hybrides à succès, il fait davantage que remplir les objectifs de diminution des émissions de CO2 imposés aux constructeurs par l'Union européenne. Son mix est « électrifié » - comprendre surtout hybride - à hauteur de 71 %. Il vise 75 % en 2024. LIRE AUSSI : Automobile : l'usine Toyota de Valenciennes devient la première usine française Malgré le peu d'enthousiasme de la direction de Toyota ces dernières années sur les véhicules 100 % électriques, les équipes de R&D du géant automobile planchaient discrètement sur des ruptures technologiques présentées comme majeures. Un domaine que peu de concurrents ont investigué eux-mêmes, se reposant plutôt sur des fournisseurs, ou au mieux sur des coentreprises avec des spécialistes. Toyota porte le fer dans les batteries Toyota vise une industrialisation de ses nouvelles technologies, dévoilées cet été, à horizon 2026. Celles-ci seraient plus denses et moins chères. Cette performance a priori antinomique laisse sceptiques les spécialistes ès batteries de Brass North America, interrogés par les analystes d'UBS. LIRE AUSSI : Voiture électrique : Toyota promet des batteries à faire pâlir d'envie Tesla Mieux, Toyota assure être maintenant très proche du Graal des fabricants de batterie , la batterie solide. Une méthode de production de masse est en cours de développement, précise Toyota, qui vise une commercialisation en 2027-2028. D'après Brass North America, le constructeur a pris une longueur d'avance sur les spécialistes américains du sujet que sont QuantumScape et SolidPower. Toutefois, le japonais n'inondera pas le marché avec ses batteries solides. « Nous les commercialiserons graduellement, à plus petite échelle », précise Andrea Carlucci. Le groupe anticipe une production de « plusieurs dizaines de milliers de voitures » à horizon 2028. Soit quelques dixièmes du marché global de la voiture électrique."
    max_length = 9000

    try:
        truncated_prompt, truncated_context, truncated_input_data = lib__script_tasks.truncate_strings(prompt, context, input_data, max_length)
        print("Function 'truncate_strings' executed successfully.")
        print("Truncated prompt:", truncated_prompt[:5])
        print("Truncated context:", truncated_context[:50])
        print("Truncated input data:", truncated_input_data[:50])
    except Exception as e:
        print(f"Error in 'truncate_strings': {e}")

test_truncate_strings()




def test_transform():
    test_text = "Voiture électrique : l'étonnante stratégie de Toyota en Europe Le japonais ne commercialise qu'un seul modèle 100 % à batteries. Il compte sur ses motorisations hybrides pour gagner du temps, au risque de voir la concurrence s'éloigner loin devant… Ajouter à mes articles Commenter Partager Bruxelles Japon Toyota Urban SUV Concept Toyota Urban SUV Concept (Toyota) Par Guillaume Guichard Publié le 4 déc. 2023 à 6:30Mis à jour le 4 déc. 2023 à 6:33 Pour Toyota, la révolution électrique peut attendre. Le constructeur japonais a précisé la semaine dernière à Bruxelles son offensive dans l'électrique en Europe. « Nous nous sentons plus prêts qu'avant pour prendre la place qui est la nôtre sur le marché de l'électrique », mar﻿tèle Andrea Carlucci, vice-président de Toyota Motor Europe. Longtemps rétif à développer une gamme tout électrique, le numéro un mondial du secteur n'aura toutefois pas de gamme complète de voitures à batteries avant 2026. Encore au stade des concepts… Pour faire patienter clients et observateurs, il a présenté aux journalistes européens deux nouveaux « concepts » aux lignes tendues et aux angles acérés. Le premier, le plus éloigné du design final, est un « crossover » sport (soit un croisement entre un SUV et une berline) et ne sera commercialisé qu'en 2025. La deuxième des deux futures voitures dévoilées lundi en Europe, un SUV citadin de segment B, devrait faire son entrée sur le marché l'année prochaine. LIRE AUSSI : Toyota veut casser son image de mauvais élève de la voiture électrique « Nous, nous faisons de la vraie cuisine… » : quand le patron de Toyota s'en prend à Tesla Pour ne pas assommer le consommateur avec un prix trop lourd, le futur SUV de segment C sera proposé avec deux options de batteries. Ce véhicule viendra rejoindre dans les concessions la seule voiture électrique de la marque. A savoir le bZ4x , commercialisé depuis septembre en France et importé du Japon. Pas de voiture électrique pas chère à l'horizon Toyota est le seul grand constructeur à forte présence en Europe à ne pas avoir de gamme plus large. Stellantis en compte aujourd'hui 13 , Volkswagen Group plus d'une dizaine également, Renault une demi-dizaine à partir de l'année prochaine. LIRE AUSSI : DECRYPTAGE - La voiture électrique à 25.000 euros, le nouveau Graal de l'automobile Le constructeur japonais ne semble pas non plus à ce stade miser sur un véhicule électrique à moins de 25.000 euros. Tous les constructeurs européens grand public tablent pourtant sur ce type de modèle pour ouvrir un large marché à l'électrique. « Nous ne sommes pas dans cette course, a reconnu Andrea Carlucci. Mais nous devons nous en préoccuper. » Certes, un jour, le japonais devrait commercialiser une citadine Yaris électrique. « Ce sera tout naturel à un moment donné », a reconnu le dirigeant. Probablement en 2026, pour compléter sa future gamme de six véhicules à batterie. L'hybride pour diminuer les émissions de CO2 En attendant, Toyota renvoie les clients qui veulent des voitures plus accessibles vers les motorisations essence voire hybride. Une autre façon de justifier la stratégie multi-énergie du groupe - thermique, hybrides, et un peu de tout électrique. Si le japonais prend le temps, c'est qu'il peut se le permettre. Grâce à ses modèles hybrides à succès, il fait davantage que remplir les objectifs de diminution des émissions de CO2 imposés aux constructeurs par l'Union européenne. Son mix est « électrifié » - comprendre surtout hybride - à hauteur de 71 %. Il vise 75 % en 2024. LIRE AUSSI : Automobile : l'usine Toyota de Valenciennes devient la première usine française Malgré le peu d'enthousiasme de la direction de Toyota ces dernières années sur les véhicules 100 % électriques, les équipes de R&D du géant automobile planchaient discrètement sur des ruptures technologiques présentées comme majeures. Un domaine que peu de concurrents ont investigué eux-mêmes, se reposant plutôt sur des fournisseurs, ou au mieux sur des coentreprises avec des spécialistes. Toyota porte le fer dans les batteries Toyota vise une industrialisation de ses nouvelles technologies, dévoilées cet été, à horizon 2026. Celles-ci seraient plus denses et moins chères. Cette performance a priori antinomique laisse sceptiques les spécialistes ès batteries de Brass North America, interrogés par les analystes d'UBS. LIRE AUSSI : Voiture électrique : Toyota promet des batteries à faire pâlir d'envie Tesla Mieux, Toyota assure être maintenant très proche du Graal des fabricants de batterie , la batterie solide. Une méthode de production de masse est en cours de développement, précise Toyota, qui vise une commercialisation en 2027-2028. D'après Brass North America, le constructeur a pris une longueur d'avance sur les spécialistes américains du sujet que sont QuantumScape et SolidPower. Toutefois, le japonais n'inondera pas le marché avec ses batteries solides. « Nous les commercialiserons graduellement, à plus petite échelle », précise Andrea Carlucci. Le groupe anticipe une production de « plusieurs dizaines de milliers de voitures » à horizon 2028. Soit quelques dixièmes du marché global de la voiture électrique."
    test_instruct = "Résumez ce texte."

    try:
        # Appel de la fonction avec un texte et des instructions de test
        result = lib__transformers.transform(test_text, test_instruct)

        # Affichage du résultat complet pour vérification manuelle
        print("Function executed successfully. Result:")
        print(result)
    except Exception as e:
        # Gestion des erreurs et affichage de l'exception
        print(f"Error in transform: {e}")

# Exécutez la fonction de test
test_transform()

def test_summarize():
    test_text = "Voiture électrique : l'étonnante stratégie de Toyota en Europe Le japonais ne commercialise qu'un seul modèle 100 % à batteries. Il compte sur ses motorisations hybrides pour gagner du temps, au risque de voir la concurrence s'éloigner loin devant… Ajouter à mes articles Commenter Partager Bruxelles Japon Toyota Urban SUV Concept Toyota Urban SUV Concept (Toyota) Par Guillaume Guichard Publié le 4 déc. 2023 à 6:30Mis à jour le 4 déc. 2023 à 6:33 Pour Toyota, la révolution électrique peut attendre. Le constructeur japonais a précisé la semaine dernière à Bruxelles son offensive dans l'électrique en Europe. « Nous nous sentons plus prêts qu'avant pour prendre la place qui est la nôtre sur le marché de l'électrique », mar﻿tèle Andrea Carlucci, vice-président de Toyota Motor Europe. Longtemps rétif à développer une gamme tout électrique, le numéro un mondial du secteur n'aura toutefois pas de gamme complète de voitures à batteries avant 2026. Encore au stade des concepts… Pour faire patienter clients et observateurs, il a présenté aux journalistes européens deux nouveaux « concepts » aux lignes tendues et aux angles acérés. Le premier, le plus éloigné du design final, est un « crossover » sport (soit un croisement entre un SUV et une berline) et ne sera commercialisé qu'en 2025. La deuxième des deux futures voitures dévoilées lundi en Europe, un SUV citadin de segment B, devrait faire son entrée sur le marché l'année prochaine. LIRE AUSSI : Toyota veut casser son image de mauvais élève de la voiture électrique « Nous, nous faisons de la vraie cuisine… » : quand le patron de Toyota s'en prend à Tesla Pour ne pas assommer le consommateur avec un prix trop lourd, le futur SUV de segment C sera proposé avec deux options de batteries. Ce véhicule viendra rejoindre dans les concessions la seule voiture électrique de la marque. A savoir le bZ4x , commercialisé depuis septembre en France et importé du Japon. Pas de voiture électrique pas chère à l'horizon Toyota est le seul grand constructeur à forte présence en Europe à ne pas avoir de gamme plus large. Stellantis en compte aujourd'hui 13 , Volkswagen Group plus d'une dizaine également, Renault une demi-dizaine à partir de l'année prochaine. LIRE AUSSI : DECRYPTAGE - La voiture électrique à 25.000 euros, le nouveau Graal de l'automobile Le constructeur japonais ne semble pas non plus à ce stade miser sur un véhicule électrique à moins de 25.000 euros. Tous les constructeurs européens grand public tablent pourtant sur ce type de modèle pour ouvrir un large marché à l'électrique. « Nous ne sommes pas dans cette course, a reconnu Andrea Carlucci. Mais nous devons nous en préoccuper. » Certes, un jour, le japonais devrait commercialiser une citadine Yaris électrique. « Ce sera tout naturel à un moment donné », a reconnu le dirigeant. Probablement en 2026, pour compléter sa future gamme de six véhicules à batterie. L'hybride pour diminuer les émissions de CO2 En attendant, Toyota renvoie les clients qui veulent des voitures plus accessibles vers les motorisations essence voire hybride. Une autre façon de justifier la stratégie multi-énergie du groupe - thermique, hybrides, et un peu de tout électrique. Si le japonais prend le temps, c'est qu'il peut se le permettre. Grâce à ses modèles hybrides à succès, il fait davantage que remplir les objectifs de diminution des émissions de CO2 imposés aux constructeurs par l'Union européenne. Son mix est « électrifié » - comprendre surtout hybride - à hauteur de 71 %. Il vise 75 % en 2024. LIRE AUSSI : Automobile : l'usine Toyota de Valenciennes devient la première usine française Malgré le peu d'enthousiasme de la direction de Toyota ces dernières années sur les véhicules 100 % électriques, les équipes de R&D du géant automobile planchaient discrètement sur des ruptures technologiques présentées comme majeures. Un domaine que peu de concurrents ont investigué eux-mêmes, se reposant plutôt sur des fournisseurs, ou au mieux sur des coentreprises avec des spécialistes. Toyota porte le fer dans les batteries Toyota vise une industrialisation de ses nouvelles technologies, dévoilées cet été, à horizon 2026. Celles-ci seraient plus denses et moins chères. Cette performance a priori antinomique laisse sceptiques les spécialistes ès batteries de Brass North America, interrogés par les analystes d'UBS. LIRE AUSSI : Voiture électrique : Toyota promet des batteries à faire pâlir d'envie Tesla Mieux, Toyota assure être maintenant très proche du Graal des fabricants de batterie , la batterie solide. Une méthode de production de masse est en cours de développement, précise Toyota, qui vise une commercialisation en 2027-2028. D'après Brass North America, le constructeur a pris une longueur d'avance sur les spécialistes américains du sujet que sont QuantumScape et SolidPower. Toutefois, le japonais n'inondera pas le marché avec ses batteries solides. « Nous les commercialiserons graduellement, à plus petite échelle », précise Andrea Carlucci. Le groupe anticipe une production de « plusieurs dizaines de milliers de voitures » à horizon 2028. Soit quelques dixièmes du marché global de la voiture électrique."

    try:
        # Appel de la fonction avec un texte de test
        result = lib__transformers.summarize(test_text)

        # Affichage du résultat complet pour vérification manuelle
        print("Function executed successfully. Result:")
        print(result)
    except Exception as e:
        # Gestion des erreurs et affichage de l'exception
        print(f"Error in summarize: {e}")

# Exécutez la fonction de test
test_summarize()



def test_transcribe_audio():
    try:
        # Remplacez 'path/to/audiofile.mp3' par le chemin d'accès à votre fichier audio
        transcript = lib__transformers.transcribe_audio('tests/stevetest.mp3')
        print("Function executed successfully.")
        print("Transcript:")
        print(transcript)  # Affichage de la transcription complète
    except Exception as e:
        print(f"Error in transcribe_audio: {e}")

# Exécuter le test
test_transcribe_audio()

"""