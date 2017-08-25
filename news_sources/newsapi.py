"""
Title:  newsapi package
Desc:   Class to access the newsapi (https://newsapi.org/)
Author: Yassin Eltahir
Date:   2017-08-19
"""

import requests
import pandas as pd


class NewsApi:
    '''
    News API: https://newsapi.org/

    Each instance must be provided:
        - X-Token: Authentication Token From
    '''

    def __init__(self):
        self.url = 'https://newsapi.org/v1/'
        self.token = None


    # Sources
    def sources(self, category=None, language=None, country=None, out='full'):
        """
        Provides a list of the news sources and blogs available on News API

        :param category: The category you would like to get sources for
               Possible options: business, entertainment, gaming, general, music, politics, science-and-nature, sport, technology

        :param language: The 2-letter ISO-639-1 code of the language you would like to get sources for
               Possible options: en, de, fr

        :param country:  The 2-letter ISO 3166-1 code of the country you would like to get sources for
               Possible options: au, de, gb, in, it, us

        :param: out: How much of the response to return
                      - full (type: response)  = Raw request object
                      - json (type: dict)      = Sources as JSON
                      - df   (type: pandas df) = Sources flattened to a pandas df
        """


        # Collect the optional parameters & build out the request URL
        params = []
        if category:
            params.append("category=" + category)
        if language:
            params.append("language=" + language)
        if country:
            params.append("country=" + country)

        params = '&'.join(params)
        url = self.url + "/sources?" + params

        # Attempt the request & return in n
        try:
            response = requests.request("GET", url)
            if out == 'full':
                return response
            elif out == 'json':
                return response.json()
            elif out == 'df':
                return pd.DataFrame(response.json()['sources'])

        except Exception as ex:
            print "Oh No! Something went wrong collecting news sources..."
            print ex




    # Articles
    def articles(self, source, sortby=None, out='full'):
        """
        Provides a list of live article metadata from a news source or blog

        :param source: The identifer for the news source or blog you want headlines from

        :param sortby: Specify which type of list you want
               Possible options: top, latest and popular

        :param out: How much of the response to return
                      - full (type: response)  = Raw request object
                      - json (type: dict)      = Sources as JSON
                      - df   (type: pandas df) = Sources flattened to a pandas df
        """

        header = {
            'x-api-key': self.token
        }

        # Build out the request url
        url = self.url + "/articles?source=" + source

        if sortby:
            url += "&sortBy=" + sortby

        # Attempt the request & return in n
        try:
            response = requests.request("GET", url, headers = header)
            if out == 'full':
                return response
            elif out == 'json':
                return response.json()
            elif out == 'df':
                return pd.DataFrame(response.json()['articles'])

        except Exception as ex:
            print "Oh No! Something went wrong collecting news articles..."
            print ex