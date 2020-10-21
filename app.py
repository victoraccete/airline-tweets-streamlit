import streamlit as st
import pandas as pd
#import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

TITLE = "Sentiment analysis of tweets on US Airlines"
st.title(TITLE)
st.sidebar.title(TITLE)

DESCRIPTION = "This application is a streamlit dashboard to make easier the visualization of sentiment analysis of tweets 🐦"
st.markdown(DESCRIPTION)
st.sidebar.markdown(DESCRIPTION)

def split_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """splits the values from the tweet_coords column to two new columns called Latitude and Longitude"""
    coords_df = df['tweet_coord'].str.strip('[]').str.split(', ', expand=True).rename(columns={0:'lat', 1:'lon'})
    coords_df.lat = coords_df.lat.astype('float')
    coords_df.lon = coords_df.lon.astype('float')
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

st.sidebar.subheader("Show random tweet.")
random_tweet = st.sidebar.radio("Sentiment", ('positive', 'neutral', 'negative'))
# displaying the tweet as md text and using .sample(n=1) to get only one tweet:
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0, 0])

st.sidebar.markdown("### Number of tweets by sentiment")
select_visual = st.sidebar.selectbox('Visualization type', ['Bars', 'Pie'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 
                               'Tweets': sentiment_count.values})

if st.sidebar.checkbox("Show plot", True):
    st.markdown("### Number of tweets by sentiment")
    if select_visual == 'Bars':
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)
#

@st.cache(persist=True)
def remove_na_from_coords(df: pd.DataFrame) -> pd.DataFrame:
    # getting only the rows where the coordinates are not null
    df = df[df['tweet_coord'].notna()]
    return df
map_df = remove_na_from_coords(data)
#

st.sidebar.subheader("When and where are users tweeting from?")
if st.sidebar.checkbox("Show map", False):
    hour = st.sidebar.slider("Hour of day", 0, 23)
    modified_data = data[data['tweet_created'].dt.hour == hour]
    st.markdown("### Tweets locations based on time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, hour+1))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)
        
#
st.sidebar.subheader("Breakdown airline tweets by sentiment")
airlines = ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America')
choice = st.sidebar.multiselect('Pick airlines', airlines)

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, 
                              x='airline', 
                              y='airline_sentiment', 
                              histfunc='count', 
                              color='airline_sentiment', 
                              facet_col='airline_sentiment',
                              labels={'airline_sentiment': 'tweets'},
                              height=600,
                              width=800)
    st.plotly_chart(fig_choice)  
#
st.sidebar.header("Sentiment word cloud")
word_sentiment = st.sidebar.radio('Display wordcloud for which sentiment?', ('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox("Hide wordcloud", True, key='3'):
    #st.set_option('deprecation.showPyplotGlobalUse', False) # removing big warning
    st.header('Word cloud for %s' % (word_sentiment))
    df = data[data.airline_sentiment == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white',height=640, width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    plt.box(False)
    st.pyplot()
#