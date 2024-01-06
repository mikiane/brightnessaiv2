# ----------------------------------------------------------------------------
# Project: Semantic Search Module for the Alter Brain project
# File:    lib__search_source.py
#  Uses Feedly to fiond RSS feeds based on a topic
# 
# Author:  Michel Levy Provencal
# Brightness.ai - 2023 - contact@brightness.fr
# ----------------------------------------------------------------------------


import requests
from dotenv import load_dotenv
import os
from lib__env import *
from googlesearch import search
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

#Récupération des sites de veille via Feedly
load_dotenv(DOTENVPATH)

#load_dotenv(".env") # Load the environment variables from the .env file.
api_token = os.environ.get("FEEDLY_API_TOKEN")
g_api_key = os.environ.get("GOOGLE_API_TOKEN")
cse_id = os.environ.get("CSE_ID")

# Function to get the feedly feeds (n = number of feeds, topic = topic to search)
def get_feedly_feeds(topic, n=3):
    url = 'https://cloud.feedly.com/v3/search/feeds'
    headers = {'Authorization': 'OAuth ' + api_token}
    params = {'query': topic, 'count': n}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f'Error with status code: {response.status_code}')
        return []
    
    data = response.json()
    feeds = []
    
    for result in data.get('results', []):
        title = result.get('title')
        feed_url = result.get('feedId', '').replace('feed/', '')
        feeds.append([title, feed_url])
    #print (str(feeds))
    return feeds
    
    


def google_search(search_term, api_key=g_api_key, cse_id=cse_id, num_results=5):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, num=num_results).execute()
    
    # Vérifie si 'items' existe dans la réponse
    if 'items' in res:
        return res['items']
    else:
        # Gérez l'absence de 'items' comme vous le jugez approprié
        print("Aucun résultat trouvé")
        return []

