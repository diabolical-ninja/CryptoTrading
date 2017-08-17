"""
Title:  Get CryptoCompare Data
Desc:   Basic mucking around to get CryptoCompare historical & live data
Author: Yassin Eltahir
Date:   2017-07-23
"""

import requests
import time
import datetime
import pandas as pd


def get_cointlist(data_as_df = False):

    '''
    Get general info for all the coins available on the CryptoCompare website.
    Docs at https://www.cryptocompare.com/api/#-api-data-coinlist
    '''

    url = "https://www.cryptocompare.com/api/data/coinlist/"
    response = requests.request("GET", url)

    # By default return the response payload. Not interested in the status, cookie, etc
    if data_as_df:
        return pd.DataFrame(response.json()['Data']).transpose()
    else:
        return response.json()



# Sample Use
get_cointlist_as_json = get_cointlist()
get_cointlist_as_df = get_cointlist(data_as_df=True)
