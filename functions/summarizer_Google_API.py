import vertexai
from vertexai.language_models import TextGenerationModel
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tts.json'

PROJECT_ID = "lustrous-maxim-424207-h0"

def summarizer(PDF, numtokens):

    vertexai.init(project=PROJECT_ID, location = "us-central1")

    parameters = {
    "temperature": 0,
    "max_output_tokens": numtokens,
    "top_p": 0.95,
    "top_k": 40,
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")

    prompt = f"""Provide a summary for the following + {PDF} """

    response = model.predict(prompt,**parameters,)

    return response.text

