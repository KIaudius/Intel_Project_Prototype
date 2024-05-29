#a streamlit app to browse pdf and flow in the pipeline

import streamlit as st
from pathlib import Path
import base64
from PyPDF2 import PdfReader

from functions.TTS_Google_API import tts_google
from functions.summarizer_Google_API import summarizer
from functions.translator_Google_API import translate_text


# Set the page configuration
st.set_page_config(page_title="Project 1 - Alpha", page_icon="📄")

#Language Codes
LANGUAGE_CODES = {
    'Afrikaans': 'af',
    'Albanian': 'sq',
    'Amharic': 'am',
    'Arabic': 'ar',
    'Armenian': 'hy',
    'Azerbaijani': 'az',
    'Basque': 'eu',
    'Belarusian': 'be',
    'Bengali': 'bn',
    'Bosnian': 'bs',
    'Bulgarian': 'bg',
    'Catalan': 'ca',
    'Cebuano': 'ceb',
    'Chichewa': 'ny',
    'Chinese (Simplified)': 'zh-cn',
    'Chinese (Traditional)': 'zh-tw',
    'Corsican': 'co',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Esperanto': 'eo',
    'Estonian': 'et',
    'Filipino': 'tl',
    'Finnish': 'fi',
    'French': 'fr',
    'Frisian': 'fy',
    'Galician': 'gl',
    'Georgian': 'ka',
    'German': 'de',
    'Greek': 'el',
    'Gujarati': 'gu',
    'Haitian Creole': 'ht',
    'Hausa': 'ha',
    'Hawaiian': 'haw',
    'Hebrew': 'iw',
    'Hindi': 'hi',
    'Hmong': 'hmn',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Igbo': 'ig',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Javanese': 'jw',
    'Kannada': 'kn',
    'Kazakh': 'kk',
    'Khmer': 'km',
    'Kinyarwanda': 'rw',
    'Korean': 'ko',
    'Kurdish': 'ku',
    'Kyrgyz': 'ky',
    'Lao': 'lo',
    'Latin': 'la',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Luxembourgish': 'lb',
    'Macedonian': 'mk',
    'Malagasy': 'mg',
    'Malay': 'ms',
    'Malayalam': 'ml',
    'Maltese': 'mt',
    'Maori': 'mi',
    'Marathi': 'mr',
    'Mongolian': 'mn',
    'Burmese': 'my',
    'Nepali': 'ne',
    'Norwegian': 'no',
    'Odia': 'or',
    'Pashto': 'ps',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Punjabi': 'pa',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Samoan': 'sm',
    'Scots Gaelic': 'gd',
    'Serbian': 'sr',
    'Sesotho': 'st',
    'Shona': 'sn',
    'Sindhi': 'sd',
    'Sinhala': 'si',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Somali': 'so',
    'Spanish': 'es',
    'Sundanese': 'su',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Tajik': 'tg',
    'Tamil': 'ta',
    'Tatar': 'tt',
    'Telugu': 'te',
    'Thai': 'th',
    'Turkish': 'tr',
    'Turkmen': 'tk',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Uyghur': 'ug',
    'Uzbek': 'uz',
    'Vietnamese': 'vi',
    'Welsh': 'cy',
    'Xhosa': 'xh',
    'Yiddish': 'yi',
    'Yoruba': 'yo',
    'Zulu': 'zu'
}


# Get a list of PDF files in the current directory
pdf_files = [f for f in Path(".").glob("*.pdf")]

# Create a sidebar
st.sidebar.title("Choose Your PDF File")

# Display the list of PDF files in the sidebar
selected_pdf = st.sidebar.selectbox("Select a PDF file", pdf_files, index=0)

#Get the value to be summarized
num_tokens = st.number_input("Number of words for summary", min_value=10, max_value= 2056, step=10)

#Get the language to be translated to
language_options = list(LANGUAGE_CODES.keys())
target_lang = st.selectbox("Select target language for translation", language_options, index=language_options.index('English'))
lang = LANGUAGE_CODES[target_lang]


# Display the selected PDF file path
if selected_pdf:
    st.write(f"Selected PDF file: {selected_pdf}")
else:
    st.write("No PDF file selected.")

# Add a section to apply functions to the selected PDF file
st.header("This Application will Summarize, Translate and Convert it to Audio For People to Understand.")

if selected_pdf:
    # Add your functions here

    if st.button("START"):
        text = ''
        reader  = PdfReader(selected_pdf)
        num_pages = len(reader.pages)

        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()

        st.spinner(text='This may take a moment...')
        summary = summarizer(text, num_tokens)
        st.write(summary)
        translated_text = translate_text(summary, lang)
        st.write(translated_text)
        final_audio_output = tts_google(translated_text, lang)

st.header("The Audio File : ")

source = [f for f in Path(".").glob("*.mp3")]

selected_audio = st.selectbox("The audio file is", source , index=0)

if selected_audio:
    # Open the audio file and read its contents
    with open(selected_audio, "rb") as audio_file:
        audio_data = audio_file.read()

    # Encode the audio data as base64
    audio_base64 = base64.b64encode(audio_data).decode("utf-8")

    # Create an HTML audio element to play the audio
    audio_html = f"""
        <audio controls autoplay>
            <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
else:
    st.write("No audio file selected.")