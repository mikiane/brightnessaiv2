import requests
from dotenv import load_dotenv
import os
# load_dotenv(DOTENVPATH)
# Load the environment variables from the .env file
load_dotenv(".env")
VECTORIZE_TOKEN = os.environ.get("VECTORIZE_TOKEN")
import json


# Extrait le text de JSON

def extract_and_concatenate_texts(json_input):
    try:
        # Charger les données JSON
        data = json.loads(json_input)
        # Extraire la valeur de 'record' et la décoder
        value = json.loads(data['record']['value'])
        
        # Vérifier si 'related_documents' existe et contient des éléments
        if 'related_documents' in value and value['related_documents']:
            # Extraire les documents relatifs et leurs textes
            texts = [doc['text'] for doc in value['related_documents']]
            # Concaténer les textes avec deux sauts de ligne entre chacun
            concatenated_texts = "\n\n".join(texts)
        else:
            concatenated_texts = "Aucun contxte trouvé."
    
    except json.JSONDecodeError:
        concatenated_texts = "Erreur dans le format."
    except KeyError:
        concatenated_texts = "Données manquantes."
    
    return concatenated_texts

# Exemple d'utilisation de la fonction


# Appelle Vectorize

def retrieve_and_concatenate_texts(endpoint, question, token, num_results=5):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    data = {
        "question": question,
        "numResults": num_results,
        "rerank": True
    }
    
    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()  # Cela lève une exception si la réponse n'est pas un succès
        json_response = response.text
        return extract_and_concatenate_texts(json_response)
    except requests.exceptions.RequestException as e:
        return f"Erreur de requête: {e}"
    except Exception as e:
        return f"Erreur inattendue: {e}"



# Exemple d'utilisation de la fonction
# Remplacez par votre token réel
question = "Parle moi de scenario planning"
retrieval_endpoint = "https://client.app.vectorize.io/api/gateways/service/o38d-e267e6a43523/peb269e55/retrieve"

result = retrieve_and_concatenate_texts(retrieval_endpoint, question, VECTORIZE_TOKEN)
print(result)

