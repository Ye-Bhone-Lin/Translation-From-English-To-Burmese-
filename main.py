import streamlit as st
import assemblyai as aai
from deep_translator import GoogleTranslator
from io import BytesIO
from streamlit_lottie import st_lottie
import tempfile
import os
import requests
import webbrowser
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

#from PIL import Image
st.set_page_config(page_title='Translation from English to Burmese', page_icon='🌐')

aai.settings.api_key = "19781e777c8b4b9f9923352489c3ab02"
transcriber = aai.Transcriber()
add_selectbox = st.sidebar.selectbox(
    "How would you like to translate?",
    ("Translate Text Directly", "Videos and Audio Translate", "YouTube Videos (in case they don't have transcipt)","YouTube Videos with their transcriptions"))
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
def translate_to_chinese(text):
    translator = GoogleTranslator(source='en', target='chinese (simplified)') 
    result = translator.translate(text)
    return result
def translate_to_korean(text):
    translator = GoogleTranslator(source='en', target='ko') 
    result = translator.translate(text)
    return result
def stream_youtube_video(youtube_url):
    yt = YouTube(youtube_url)
    video_stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
    return video_stream
left_column,right_column = st.columns(2)
if add_selectbox == "Translate Text Directly":
    with right_column:
        #gif_path = "bf082f30bac907f854a3e00a5ad3505f.gif"
        #gif_img = Image.open(gif_path)
        #st.image(gif_img, use_column_width=True)
        lottie_coding = lottie_codingurl('https://assets3.lottiefiles.com/packages/lf20_biekfbpy.json')
        st_lottie(lottie_coding,height=150,key='coding')
    with left_column:
        st.title('Translation from English To Burmese 🗣️')
    test = st.text_area('Write text; it will translate English to Burmese or Chinese')
    option = st.selectbox(
        'Which languages do you want to translate',
        ('Burmese', 'Chinese','Korean'))
    st.write('You selected:', option)
    if option == 'Burmese':
        burmese_text = translate_to_burmese(test)
        if st.button('Click here to translate'):
            st.write(burmese_text)
    elif option == "Chinese":
        chinese_text = translate_to_chinese(test)
        if st.button('Click here to translate'):
            st.write(chinese_text)
    elif option == "Korean":
        korean = translate_to_korean(test)
        if st.button('Click here to translate'):
            st.write(korean)

elif add_selectbox == 'Videos and Audio Translate':
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

elif add_selectbox == "YouTube Videos with their transcriptions":

    st.header('Translate the YouTube Videos with their transcriptions')
    youtube_url = st.text_input('Paste the Youtube Link in here')
    if st.button('Click here to translate'):        
        video_stream = stream_youtube_video(youtube_url)
        st.components.v1.iframe(video_stream.url, width=800, height=500)
        
        if "v=" in youtube_url:
            youtube_url = youtube_url.split("v=")[1]
            st.write(youtube_url)
            transcript_list = YouTubeTranscriptApi.list_transcripts(youtube_url)
            language_list = []
            target_lan = []
            for transcript in transcript_list:
                language_list.append(transcript.language)
            for tar in language_list:
                if tar in ["English", "English - en", "English (auto-generated)"]:
                    target_lan.append(tar)
                if tar in ["Chinese", "Chinese (China) - zh_CN", "Chinese (auto-generated)", "Chinese (Simplified)"]:
                    target_lan.append(tar)
                if tar in ["Korean","Korean (auto-generated)"]:
                    target_lan.append(tar)
                if tar in ["Indonesian","Indonesian (auto-generated)","Indonesian - id"]:
                    target_lan.append(tar)

            choose = st.selectbox("Which Languages do you want to choose in order to translate",(target_lan))
            oldtext,finaltext = st.columns(2)

            if choose in ["English", "English - en", "English (auto-generated)"]:
                t = YouTubeTranscriptApi.get_transcript(youtube_url, languages=['en'])
                with oldtext:
                    st.write(' '.join(script["text"] for script in t))
                with finaltext:
                    translator = GoogleTranslator(source='en', target='my')
                    translated_text = (' '.join(script["text"] for script in t))
                    st.write(translator.translate(translated_text))
            elif choose in ["Korean", "Korean (auto-generated)"]:
                t = YouTubeTranscriptApi.get_transcript(youtube_url, languages=['ko'])
                with oldtext:
                    st.write(' '.join(script["text"] for script in t))
                with finaltext:
                    translator = GoogleTranslator(source='ko', target='my')
                    translated_text = (' '.join(script["text"] for script in t))
                    st.write(translator.translate(translated_text))
            elif choose in ["Indonesian", "Indonesian (auto-generated)", "Indonesian - id"]:
                t = YouTubeTranscriptApi.get_transcript(youtube_url, languages=['id'])
                with oldtext:
                    st.write(' '.join(script["text"] for script in t))
                with finaltext:
                    translator = GoogleTranslator(source='id', target='my')
                    translated_text = (' '.join(script["text"] for script in t))
                    st.write(translator.translate(translated_text))
            elif choose in ["Chinese", "Chinese (China) - zh_CN", "Chinese (auto-generated)", "Chinese (Simplified)"]:
                t = YouTubeTranscriptApi.get_transcript(youtube_url, languages=['zh-Hans', 'zh-CN','zh'])
                with oldtext:
                    st.write(' '.join(script["text"] for script in t))
                with finaltext:
                    translator = GoogleTranslator(source='zh-CN', target='my')
                    translated_text = (' '.join(script["text"] for script in t))
                    st.write(translator.translate(translated_text))
        else:
            video_id = youtube_url.split("/")[-1]
elif add_selectbox == "YouTube Videos (in case they don't have transcipt)":
    st.header('You can paste a YouTube Link in this part :pushpin:')
    youtube_url = st.text_input('Paste the Youtube Link in here(:red[It can only translate English videos])')
    st.caption('Example: https://www.youtube.com/watch?v=NgEaOJ7lRWY')
    if st.button('Click here to translate'):        
       video_stream = stream_youtube_video(youtube_url)
       st.components.v1.iframe(video_stream.url, width=800, height=500)

       English1,Burmese1 = st.columns(2)
       transcript = transcriber.transcribe(video_stream.url)
       with English1:
           st.caption('_English_')
           st.write(transcript.text)
       with Burmese1:
           st.caption('_Burmese_')
           st.write(translate_to_burmese(transcript.text))
st.divider() 
