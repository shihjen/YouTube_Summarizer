# import essential libraries
import streamlit as st
import streamlit_lottie as st_lottie
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Streamlit page configuration
st.set_page_config(page_title = 'Youtube Summarizer',
                   page_icon = ' ',
                   layout = 'centered',
                   initial_sidebar_state = 'auto')

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt = '''
You are a Youtube summarizer.
You will be given with YouTube transcript text.
Your task is to summarize the entire video based on the transcript given and providing the video summary in bullet points within 250 words. 
Please provide the summary of the text given here: 
'''

description = '''
Video content has become a dominant medium for information dissemination and entertainment. 
YouTube, as one of the largest video-sharing platforms, hosts an immense variety of content ranging from educational lectures, news, and tutorials to entertainment. 
However, the sheer volume of content can be overwhelming for users who may not have the time to watch lengthy videos. 
A solution to this problem is a web application that leverages the capabilities of large language models to generate concise summaries of YouTube video transcripts. 
This application aims to provide users with quick, comprehensive overviews of video content, saving them time and enhancing their content consumption experience.
'''

# function to load the lottie file
def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

# function to extract the Youtube video transcript
def extract_transcript(url):
    try:
        video_id = url.split('=')[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ''
        for i in transcript_text:
            script = ' ' + i['text']
            transcript += script
        return transcript
    except Exception as e:
        st.write('Unexpected Error(s) Occured!')
    
# function to generate the Youtube video summary using llm
def generate_video_summary(transcript_text, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt + transcript_text)
    return response.text

st.title('YouTube Summarizer')
cover_pic = load_lottiefile('img/youtube.json')
st.lottie(cover_pic, speed=0.5, reverse=False, loop=True, quality='low', height=400, key='first_animate')
st.write(description)
st.subheader('Video URL')
url = st.text_input('Enter the YouTube video link:')

container = st.container(border=True)

if url:
    try:
        video_id = url.split('=')[1]
        container.subheader('Content Summary')
        transcript_text = extract_transcript(url)
        response_text = generate_video_summary(transcript_text, prompt)
        container.write(response_text)
        container.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
        container.markdown(f'#### Video ID: {video_id}')
    except:
        st.write('Unexpected Error(s) Occured!')