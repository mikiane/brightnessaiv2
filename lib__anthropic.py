from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import os
from dotenv import load_dotenv
import requests
import anthropic



load_dotenv('.env')


# Environment Variables
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")
SENDGRID_KEY = os.environ.get("SENDGRID_KEY")
SENDGRID_KEY = os.environ['SENDGRID_KEY']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
REGION_NAME = os.environ['REGION_NAME']
ANTHROPIC_API_KEY = os.environ['ANTHROPIC_API_KEY']

# Assurez-vous d'avoir défini votre clé API comme variable d'environnement
api_key = ANTHROPIC_API_KEY



def generate_chat_completion_anthropic_api_2(consigne, texte, model="claude-3-opus-20240229"):
    

    # Construct the prompt from the given consigne and texte
    prompt = f"{HUMAN_PROMPT} {consigne} : {texte}{AI_PROMPT}"

    # Create an Anthropic client
    client = Anthropic()
    
    # Create a stream completion using the Anthropic API
    stream = client.completions.create(
        prompt=prompt,
        model=model,
        stream=True,
        temperature=0.05,
        # Set any other desired parameters here, for example:
        max_tokens_to_sample=99000
    )

    # Iterate over the stream completions and yield the results
    for completion in stream:
        yield completion.completion
        
        

def generate_chat_completion_anthropic_req(consigne, texte, model="claude-3-opus-20240229"):
    # Construct the prompt from the given consigne and texte
    prompt = f"{HUMAN_PROMPT} {consigne} : {texte}{AI_PROMPT}"
    
    # Set the API endpoint URL
    url = "https://api.anthropic.com/v1/messages"
    
    # Set the headers
    headers = {
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "messages-2023-12-15",
        "content-type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY
    }
    
    # Set the request data
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 99000,
        "stream": True
    }
    
    # Send the POST request to the API endpoint
    response = requests.post(url, headers=headers, json=data, stream=True)
    
    # Iterate over the stream completions and yield the results
    for line in response.iter_lines():
        if line:
            yield line.decode('utf-8')






def generate_chat_completion_anthropic(consigne, texte, model="claude-3-opus-20240229"):
    client = anthropic.Anthropic(
        api_key=ANTHROPIC_API_KEY
    )

    with client.messages.stream(
        model=model,
        max_tokens=99000,
        temperature=0,
        system=consigne,
        messages=[
            {
                "role": "user",
                "content": texte
            }
        ]
    ) as stream:
        for text in stream.text_stream:
            yield text