import streamlit as st
import assemblyai as aai
from deep_translator import GoogleTranslator
from io import BytesIO
import tempfile
import os
aai.settings.api_key = "19781e777c8b4b9f9923352489c3ab02"
transcriber = aai.Transcriber()
def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        return temp_file.name
def translator1(videoaudio):

    transcript = transcriber.transcribe(videoaudio)
    result_text = transcript.text
    return result_text
def translate_to_burmese(text):
    translator = GoogleTranslator(source='en', target='my') 
    result = translator.translate(text)
    return result
st.title('Translation from English To Burmese')
test = st.text_input('Wrtie text')
burmese_text = translate_to_burmese(test)
st.write(burmese_text)
st.header('You can add Videos or Audio files that you want to translate')
uploaded_file = st.file_uploader('Choose a video file', type=["mp4", "mp3", "mov"])
if uploaded_file is not None:
    st.video(uploaded_file)
    temp_file_path = save_uploaded_file(uploaded_file)
    try:
        transcript = transcriber.transcribe(temp_file_path)
        result_text = transcript.text
        st.write(result_text)
        st.write(translate_to_burmese(result_text))
    finally:
        os.remove(temp_file_path)

    

else:
    st.warning('You need to upload a video file.')

