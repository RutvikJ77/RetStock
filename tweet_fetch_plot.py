from config import create_api
from main import selected_company
import tweepy as tp
import re
import itertools
import collections
import pandas as pd
import nltk
from nltk.corpus import stopwords
import seaborn as sns
import matplotlib.pyplot as plt



api = create_api()

def remove_url(txt):
    """Replace URLs found in a text string with nothing 
    (i.e. it will remove the URL from the string).

    Parameters
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())







search_term = selected_company

tweets = tp.Cursor(api.search,q=search_term,lang="en").items(10)
all_tweets = [tweet.text for tweet in tweets]
all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]
words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]

all_words_no_urls = list(itertools.chain(*words_in_tweet))

counts_no_urls = collections.Counter(all_words_no_urls)

print(counts_no_urls.most_common(15))



