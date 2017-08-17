"""
Title:  Get All Historical Poliniex Data
Desc:   For the currency pairs traded in the last 24hrs, aim to get as much of the
        historical data as possible at the most granular level
Author: Yassin Eltahir
Date:   2017-08-17
"""

import pandas as pd
import poloniex as px
from datetime import datetime
import time
from tqdm import tqdm


# Get all the currency pairs
print "{}: Getting Currency Pairs... ".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
currency_pairs = px.return24hVolume('pairs')
print "{}: Getting Currency Pairs... Done".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Get the current time as pretty string
right_now = datetime.now().strftime("%Y-%m-%d")

# Get as much historical data as exists for each traded currency pair
print "{}: Getting Historical Prices... ".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

exch_price_hist = []
for pair in tqdm(currency_pairs):
    
    # Incase the connection fails, retry the request
    while True:
        try:
            exch_price_hist.append(px.returnChartData(
                                      currency_pair = pair,
                                      start_date = '2000-01-01',    # As early as possible
                                      end_date = right_now ,        # Today
                                      period = 7200,                 # 2hr candlestick periods
                                      out = 'df',                   
                                      include_ticker = True
                                      )
                                )
        except:
            # Sleep for 1 sec before retrying
            time.sleep(1)
            continue
        break

print "{}: Getting Historical Prices... Done".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Combine into a single df & dump as a CSV
print "{}: Writing To CSV...".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
exch_price_hist_flat = pd.concat(exch_price_hist)
exch_price_hist_flat.to_csv('poloniex_crypto_pairs_price_history.csv',index = False, float_format='%.9f')
print "{}: Writing To CSV... Done".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))