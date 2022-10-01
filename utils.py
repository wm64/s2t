# -*- coding: utf-8 -*-
import pandas as pd
import os
from pytube import YouTube
import streamlit as st
import requests
from time import sleep

ai_auth_key="fc18a8029ffd47faa4e5b972b591ba1b"
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

headers = {
    'authorization' : ai_auth_key,
    'content_type' : 'application/json'
    }

@st.cache()
def download_audio(vid_url) :
    yt = YouTube(vid_url)
    audio = yt.streams.filter(only_audio=True).first()
    out = audio.download()
    base, ext = os.path.splitext(out)
    out_file = base + '.mp3'
    os.rename(out, out_file)
    return yt.title, out_file


#@st.cache()
def submit_transcription(save_location) :
    
    def read_file(save_location, chunk_size=5242880):
        with open(save_location, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    response = requests.post(upload_endpoint,
                            headers=headers,
                            data=read_file(save_location))
    return response.json()['upload_url'] # URL to the uploaded file

#@st.cache()
def do_transcription(ai_url):
    transcript_task = {
        'audio_url' : ai_url ,
        'word_boost' : ["WIPO", "Wipo"] ,
        'boost_param' : 'high' ,
        'speaker_labels' : True 
        }
    response = requests.post(transcript_endpoint,
                             headers=headers,
                             json=transcript_task)

    transcript_id = response.json()['id']
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    
    speakers_df = pd.DataFrame()
    while True :
        transcript_task = {
            'audio_url' : ai_url
            }
        poll = requests.get(polling_endpoint, headers=headers, json=transcript_task)
        status = poll.json()['status']
        print(status) 

        if status == 'submitted' or status == 'processing' :
            sleep(2)
        elif status == 'completed' :
            speakers = poll.json()['utterances']
            speakers_df = pd.DataFrame(speakers)
            break
        elif status == 'error' :
            print(poll.json()['error'])
            break
        else :
            print('Unexpected exit status')
            print(status)
            break
    return speakers_df
        
