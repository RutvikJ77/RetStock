import streamlit as st
import yfinance as yf
import pandas as pd
import tweepy as tp
import re
import itertools
import collections
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from config import create_api


stop_words =set(stopwords.words('english'))
api = create_api()

Tickerdict = {"Gamestop":'GME',"Apple":'AAPL',"AMC Entertainment":'AMC',"Google":'GOOGL',"Microsoft":'MSFT'}
Duration = {"2 Weeks":'2wk',"1 Month":'1mo',"1 Year":'1y',"5 Years":'5y'}
st.title('RetStock 📈')

def remove_url(txt):
    """Replace URLs found in a text string with nothing 
    Parameters txt : string
        A text string that you want to parse and remove urls.
    Returns The same txt string with url's removed.
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

def words_data(select_company,ntweets_fetch):
    """
    Tweets fetch and count analysis
    Parameters - company and number of tweets to be fetched.
    returns cleaned twitter data.
    """
    search_term = select_company + " stock"
    tweets = tp.Cursor(api.search,q=search_term,lang="en").items(ntweets_fetch)
    all_tweets = [tweet.text for tweet in tweets]
    all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]
    words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]
    tweets_nsw = [[word for word in tweet_words if not word in stop_words] for tweet_words in words_in_tweet]

    all_words_nsw = list(itertools.chain(*tweets_nsw))
    counts_nsw = collections.Counter(all_words_nsw)
    clean_tweets_nsw = pd.DataFrame(counts_nsw.most_common(15), columns=['words', 'count'])
    return clean_tweets_nsw

def matplot():
    """
    Creates a Matplot lib chart
    Returns fig object
    """
    data = words_data(selected_company,tweets_fetch)
    fig, ax = plt.subplots(figsize=(8, 8))
    data.sort_values(by='count').plot.barh(x='words', y='count', ax=ax, color="purple")

    ax.set_title("Common Words Found in Tweets (Without Stop Words)")
    return fig

st.markdown("## Retail Investment Analysis")

st.sidebar.header('Choose your company and duration')

selected_company = st.sidebar.selectbox("Select your company for analysis:",["Gamestop","Apple","AMC Entertainment","Google","Microsoft"])
tickerData = yf.Ticker(Tickerdict[selected_company])

day_range = st.sidebar.selectbox("Select Time duration for analysis:",["2 Weeks","1 Month","1 Year","5 Years"])
tweets_fetch = st.sidebar.selectbox("Tweets to fetch:",[50,100,500,1000])

tickerDf = tickerData.history(period=Duration[day_range])
st.write("### " + selected_company + " Closing Price")
st.line_chart(tickerDf.Close)
st.pyplot(fig=matplot())