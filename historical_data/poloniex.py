"""
Title:  Get Poliniex Data
Desc:   Basic mucking around to get Poloniex historical & live data
Author: Yassin Eltahir
Date:   2017-07-07
"""

import requests
import time
import datetime
import pandas as pd



def returnChartData(currency_pair, start_date, end_date, period, out = 'full', include_ticker = False):
    
    """
    Simple function to return historical chart data from Poloniex
    Poloniex Docs: https://poloniex.com/support/api/
    
    Inputs Are:
    currency_pair:   From/To currencies, eg USD/BTC USDT_BTC
    start:           Date as string. Format of YYYY-MM-DD
    end:             Date as string. Format of YYYY-MM-DD
    period:          Candlestick period in seconds (INT)
    out:             How much of the response to return
                          - full (type: response)  = Raw request object
                          - json (type: dict)      = Historical pricing as a json
                          - df   (type: pandas df) = Historical pricing flattened to a pandas df
    include_ticker:  If df, should a column for the ticker be included
    """   
    
    # The entry point to Poloniex's public API
    base_url = "https://poloniex.com/public"
        
    
    # Convert dates to unix time
    start_unix = time.mktime(datetime.datetime.strptime(start_date , "%Y-%m-%d").timetuple())
    end_unix = time.mktime(datetime.datetime.strptime(end_date , "%Y-%m-%d").timetuple())
    
    
    # Check if the period provided is valid
    # Valid period values
    valid_periods = [300, 900, 1800, 7200, 14400,86400]
    if period not in valid_periods:
        raise ValueError('Invalid period provided. Ensure it is in {}'.format(valid_periods))
          
    
    # Build Full URL
    full_url = "{}?command=returnChartData&currencyPair={}&start={}&end={}&period={}".format(base_url,currency_pair,start_unix, end_unix,period)
    
    # Send request
    response = requests.request("GET", full_url)

    # By default only return the json response. If desired, return the full object
    if out == 'full':
        return response
    elif out == 'json':
        return response.json()
    elif out == 'df':
         price_hist = pd.DataFrame(response.json())
         price_hist['date'] = pd.to_datetime(price_hist['date'],unit='s') # Convert UNIX time to human-readable time
         
         if include_ticker:
             price_hist['ticker'] = currency_pair
         
         return price_hist


def return24hVolume(out = 'full'):
    
    """
    Simple function to return the 24h Volume for currency pairs from Poloniex
    Poloniex Docs: https://poloniex.com/support/api/
    
    Inputs Are:
    out:     How much of the response to return
                - full      (type: response) = Raw request object
                - 24hVolume (type: dict)     = Traded currency pairs, volume and currency totals
                - pairs     (type: list)     = Just the currency pairs traded in the last 24hrs

    """  
    
    # The entry point to Poloniex's public API
    base_url = "https://poloniex.com/public"
    
    # Build Full URL
    full_url = "{}?command=return24hVolume".format(base_url)
    
    # Send request
    response = requests.request("GET", full_url)
    
    # Determine how much of the response was asked for
    if out == 'full':
        return response
    elif out == '24hVolume':
        return response.json()
    elif out == 'pairs':
        return [x for x in return24hVolume().json().keys() if 'total' not in x]





