# brightnessaiv2
 **BrightnessAI: An Overview**  
 
 **Chat Completion Project** 
 BrightnessAI's Chat Completion Project is a cutting-edge implementation leveraging OpenAI's GPT-4 for server-side response generation. Written in Python and Flask, this project features a server with two main endpoints (/stream_chat and /chat) to process user inputs. It intricately uses OpenAI’s API to generate intelligent responses, offering flexibility in choosing models like GPT-4. The server manages prompt creation, API requests, and response parsing, delivering these as a text stream to the client. The client, a simplistic web interface, interacts with the server through a form, showcasing responses in real-time. This project requires an OpenAI API key and can be started with a few simple commands, as detailed in the repository. 
 
 
  **Text Transformers API** 
  Another facet of BrightnessAI is the Text Transformers API, housed in a Flask framework. This versatile API offers services like summarization, custom text transformation, and podcast generation from text. Key features include summarization with variable factors, text transformation based on specific instructions, and the ability to turn text into podcasts. Users need to install necessary Python packages and can start the server with straightforward commands. This API is user-friendly, accepting POST requests with specific parameters, and is capable of handling files up to 50 MB.  
  
  **Extended LLM (Alter Brain)** 
  Lastly, the Extended LLM (Alter Brain) project is a work-in-progress, representing a simplified 'second brain' for neural language models. Utilizing the OpenAI Embedding API, it creates semantic indexes from text embeddings stored in CSV files. This system enhances information retrieval, pivoting from traditional keyword searches to a more nuanced semantic approach. Users can index text files, build and query the index, and adapt the code for extended functionalities. This project is compatible with GPT-4 and soon with LLAMA, signifying its forward-thinking design.  Overall, BrightnessAI is a comprehensive suite of tools on GitHub, showcasing innovative uses of AI in text processing and response generation. Each project under this umbrella demonstrates a unique aspect of AI's potential in enhancing digital communication and information processing.

## Gmail Sent Contacts Export
This repository now includes a script to extract recipient information from your Gmail sent mail. Run `python gmail_sent_contacts_to_csv.py` after configuring OAuth credentials to generate a `sent_contacts.csv` file containing the names and email addresses found in your sent messages.
