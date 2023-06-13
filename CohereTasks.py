import os
from dotenv import load_dotenv
import cohere

# Set the client
load_dotenv()
co = cohere.Client(os.environ.get("COHERE_API_KEY")) # This is a trial API key

def generate_summary(messages, note):
    # Call the summarize endpoint and
    response = co.summarize( 
    text= messages,
    length='medium',
    format='bullets',
    model='command-light',
    additional_command=note,
    temperature=0.3,
    ) 
    return response.summary