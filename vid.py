# -*- coding: utf-8 -*-

import streamlit as st
import numpy as np
import pandas as pd
from utils import *

st.title("Video Transcript, version 0.1")
st.caption("A demonstration of the best available products")

scp_video_source = "https://s3-eu-west-1.amazonaws.com/connectedviews-vod01/406ff546-3bc6-43f0-8142-06dd768a873d/en/406ff546-3bc6-43f0-8142-06dd768a873d_1200.mp4"
video_source = "https://www.youtube.com/watch?v=SCnnTvk7PTg"

st.subheader("Malaysia joins Marrakesh, March 2022")
st.video(video_source)

vid_title, save_location = download_audio(video_source)
st.header(vid_title)
st.audio(save_location)

ai_url = submit_transcription(save_location)
speakers_df = pd.DataFrame()
speakers_df = do_transcription(ai_url)

st.subheader("Index of Speakers")

for index, row in speakers_df.iterrows() :
    with st.expander(row['speaker']) :
        st.write(row['text'])
#        st.button(row['start'])
