"""
Title:  Reddit Posts
Desc:   Summarised post information from Reddit using PRAW
Author: Yassin Eltahir
Date:   2017-08-19
"""

import praw
from datetime import datetime
import yaml



# Source Credentials
creds = yaml.load(open("creds.yaml",'r'))


# Instantiate authenticated reddit instance
reddit = praw.Reddit(client_id = creds['reddit']['client_id'],
                     client_secret = creds['reddit']['client_secret'],
                     password = creds['reddit']['password'],
                     user_agent = creds['reddit']['user_agent'],
                     username = creds['reddit']['username'])



def submission_data(post):
    """
    For a reddit submission post, extracts a few fields of interest
    :param post:
    :return  dict on post attributes
    """
    data = {
        'created_utc': datetime.utcfromtimestamp(post.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
        'title': post.title,
        'domain': post.domain,
        'url': post.url,
        'votes': post.ups - post.downs
    }

    return data




# Go to the crypto news subreddit and extract post information
crypto_currency_news = reddit.subreddit('Crypto_Currency_News')


ccn_posts = [submission_data(x) for x in crypto_currency_news.top('all')]