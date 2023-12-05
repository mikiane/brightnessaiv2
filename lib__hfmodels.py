import requests
import openai


def query(payload, headers, api_url):
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()


"""
#### NE FONCTIONNE PAS/ A DEBUGUER ####
def stream_mistral(prompt, api_token="none", max_tokens=1024):
    client = openai.OpenAI(api_key=api_token)  # Create an OpenAI client with the API key

    response = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.1",
        messages=[
            {'role': 'system', 'content': "Je suis un assistant"},
            {'role': 'user', 'content': prompt}
        ],
        temperature=0,
        max_tokens=max_tokens,
        stream=True
    )

    # For each part of the response
    for chunk in response:
        # If the part contains a 'delta' and the 'delta' contains 'content'
        if 'delta' in chunk['choices'][0] and 'content' in chunk['choices'][0]['delta']:
            content = chunk['choices'][0]['delta']['content']  # Extract the content
            print(content)
            yield f"{content}"  # Yield the content as a string

"""
#############################################################################################################################
##### NE FONCTIONNE PAS/ A DEBUGUER ####

def stream_hfllm(prompt, api_token, api_url, max_token, num_tokens=300):
    # Créer un pipeline pour la génération de texte avec le modèle spécifié

    input0 = prompt
    n = num_tokens * 3 # Number of iterations * 15 = Nb Tokens
    headers = {\
        "Authorization": f"Bearer {api_token}",\
        "max_tokens": str(max_token), \
        "presence_penalty": "0",\
        "frequency_penalty": "0",\
        "temperature" : "0"}

    i=0
    data = query({"inputs": input0}, headers, api_url)
    input = str(data[0]['generated_text'])
    new_characters = input[len(prompt):]
    yield f"{new_characters}"
    #print(input)  # Print initial output
    previous_input = input  # Store the initial input
    while (i < n):
        #print(i)
        data = query({"inputs": input}, headers, api_url)
        new_input = str(data[0]['generated_text'])
        if new_input == input[len(new_input):]: break
        
        # Find and print only the new part of the generated text
        new_characters = new_input[len(previous_input):]
        #print(new_characters,end='\n')
        yield f"{new_characters}"
        
        if len(new_characters) == 0: break
        # Update the previous_input and input variables
        previous_input = new_input
        input = new_input
        i += 1

#############################################################################################################################

