# imports
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# app
TITLE = "Sentiment analysis of tweets on US Airlines"
st.title(TITLE)
st.sidebar.title(TITLE)

DESCRIPTION = "This application is a streamlit dashboard to make easier the visualization of sentiment analysis of tweets 🐦"
st.markdown(DESCRIPTION)
st.sidebar.markdown(DESCRIPTION)

def split_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """splits the values from the tweet_coords column to two new columns called Latitude and Longitude"""
    coords_df = df['tweet_coord'].str.strip('[]').str.split(', ', expand=True).rename(columns={0:'lat', 1:'lon'})
    st.write(coords_df)
    coords_df.lat = coords_df.lat.astype('float128', copy=False)
    coords_df.lon = coords_df.lon.astype('float128', copy=False)
    df = pd.concat([df, coords_df], axis=1, sort=False)
    return df
    
DATA_PATH = "Tweets.csv"
@st.cache(persist=True)
def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data.tweet_created = pd.to_datetime(data.tweet_created)
    data = split_coordinates(data)
    return data
data = load_data()
st.write(data)

st.sidebar.subheader("Show random tweet.")
random_tweet = st.sidebar.radio("Sentiment", ('positive', 'neutral', 'negative'))
# displaying the tweet as md text and using .sample(n=1) to get only one tweet:
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0, 0])

st.sidebar.markdown("### Number of tweets by sentiment")
select_visual = st.sidebar.selectbox('Visualization type', ['Bars', 'Pie'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 
                               'Tweets': sentiment_count.values})

if st.sidebar.checkbox("Hide", True) == False:
    st.markdown("### Number of tweets by sentiment")
    if select_visual == 'Bars':
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

st.write(data.dtypes)
st.map(data)




