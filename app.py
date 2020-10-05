import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

TITLE = "Sentiment analysis of tweets on US Airlines"
st.title(TITLE)
st.sidebar.title(TITLE)

DESCRIPTION = "This application is a streamlit dashboard to make easier the visualization of sentiment analysis of tweets 🐦"
st.markdown(DESCRIPTION)
st.sidebar.markdown(DESCRIPTION)

DATA_PATH = "Tweets.csv"

@st.cache(persist=True)
def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data.tweet_created = pd.to_datetime(data.tweet_created)
    return data

data = load_data()

st.sidebar.subheader("Show random tweet.")
random_tweet = st.sidebar.radio("Sentiment", ('positive', 'neutral', 'negative'))
# displaying the tweet as md text and using .sample(n=1) to get only one tweet:
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0, 0])
