# Imports the Google Cloud Translation library
from google.cloud import translate
import os
from googletrans import Translator

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tts.json'
#PROJECT_ID = "lustrous-maxim-424207-h0"
#location = "us-central1"

# Initialize Translation client
def translate_text(pdf , target_lang:str):

    #client = translate.TranslationServiceClient()
    translator = Translator()

    #parent = f"projects/{PROJECT_ID}/locations/{location}"

    # response = client.translate_text(
    #     request={
    #         "parent": parent,
    #         "contents": [pdf],
    #         "mime_type": "text/plain",  # mime types: text/plain, text/html
    #         "source_language_code": "en-US",
    #         "target_language_code": target_lang,
    #     }
    # )

    response = translator.translate(pdf, dest=target_lang)

    # Display the translation for each input text provided

    return response.text
