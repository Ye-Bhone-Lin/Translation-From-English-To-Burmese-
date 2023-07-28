import streamlit as st
import assemblyai as aai
from deep_translator import GoogleTranslator
from io import BytesIO
from streamlit_lottie import st_lottie
import tempfile
import os
import requests
#from PIL import Image
st.set_page_config(page_title='Translation from English to Burmese', page_icon='🌐')

aai.settings.api_key = "19781e777c8b4b9f9923352489c3ab02"
transcriber = aai.Transcriber()
def lottie_codingurl(url):
    animations = requests.get(url)
    if animations.status_code !=200:
        return None
    return animations.json()
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
left_column,right_column = st.columns(2)
with right_column:
    #gif_path = "bf082f30bac907f854a3e00a5ad3505f.gif"
    #gif_img = Image.open(gif_path)
    #st.image(gif_img, use_column_width=True)
    lottie_coding = lottie_codingurl('https://assets3.lottiefiles.com/packages/lf20_biekfbpy.json')
    st_lottie(lottie_coding,height=150,key='coding')
with left_column:
    st.title('Translation from English To Burmese 🗣️')
test = st.text_area('Write text; it will translate from English to Burmese')
burmese_text = translate_to_burmese(test)
if st.button('Click here to translate'):
    st.write(burmese_text)

st.divider() 
st.header('You can add Videos or Audio files that you want to translate 🎥')
uploaded_file = st.file_uploader('Choose a video or audio file', type=["mp4", "mp3", "mov"])
if uploaded_file is not None:
    st.video(uploaded_file)
    temp_file_path = save_uploaded_file(uploaded_file)
    English,Burmese = st.columns(2)

    try:
        transcript = transcriber.transcribe(temp_file_path)
        result_text = transcript.text
        with English:
            st.caption('_English_')
            st.write(result_text)

        with Burmese:
            st.caption('_Burmese_')
            st.write(translate_to_burmese(result_text))
    finally:
        os.remove(temp_file_path)
else:
    st.warning('You need to upload a video file.')




    

else:
    st.warning('You need to upload a video file.')

