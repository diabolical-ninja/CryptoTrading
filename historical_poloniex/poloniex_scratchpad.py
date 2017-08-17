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

# Flatten JSON into dataframe
usd_eth_hist = returnChartData('totalXMR','2017-07-01','2017-08-01',14400)
usd_eth_hist = pd.DataFrame(usd_eth_hist)


# Convert UNIX time to human-readable time
usd_eth_hist['date'] = pd.to_datetime(usd_eth_hist['date'],unit='s')


usd_eth_hist.date.min()


currency_pairs = return24hVolume('pairs')


# Test each currency pair
all_pairs_chart_data = [returnChartData(x,'2017-08-16','2017-08-17',86400) for x in currency_pairs]

