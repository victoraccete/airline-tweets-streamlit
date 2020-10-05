import streamlit as st
import pandas as pd
import numpy as np

title = "Sentiment analysis of tweets on US Airlines"
st.title(title)
st.sidebar.title(title)

description = "This application is a streamlit dashboard to make easier the visualization of sentiment analysis of tweets 🐦"
st.markdown(description)
st.sidebar.markdown(description)
"""
DATA_PATH = "Tweets.csv"
def load_data():
    data = pd.read_csv(DATA_PATH)"""