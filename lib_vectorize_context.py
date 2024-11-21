import requests
from dotenv import load_dotenv
import os
# load_dotenv(DOTENVPATH)
# Load the environment variables from the .env file
load_dotenv(".env")
VECTORIZE_TOKEN = os.environ.get("VECTORIZE_TOKEN")


retrieval_endpoint = "https://client.app.vectorize.io/api/gateways/service/o38d-e267e6a43523/peb269e55/retrieve"
headers = {
    'Content-Type': 'application/json',
    'Authorization': VECTORIZE_TOKEN
}
data = {
    "question": "Parle moi de scenario planning",
    "numResults": 5,
    "rerank": True
}
response = requests.post(retrieval_endpoint, headers=headers, json=data)
response.raise_for_status()
print(response.json())