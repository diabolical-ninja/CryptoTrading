"""
Title:  Basic Momentum V2
Desc:   Apply a simple momentum strategy to 2hr candle stick data
Author: Yassin Eltahir
Date:   2017-09-11
"""

# Required Packages
import pandas as pd
import numpy as np
from tqdm import tqdm
import seaborn as sns

# Pretty Up the Plots
%matplotlib inline
sns.set()

# Source Historical Data & Create Timestamp Reference
#dat_loc = '/Users/yassineltahir/Downloads/poloniex_crypto_pairs_price_history.csv'
dat_loc = r'C:\Users\yassin.eltahir\Documents\Data\poloniex_crypto_pairs_price_history.csv'
hist_ohlc = pd.read_csv(dat_loc)

hist_ohlc.index = pd.DatetimeIndex(hist_ohlc.date)


# Determine which Tickers are Available
tickers = hist_ohlc.ticker.unique().tolist()
ticker = tickers[12]
tick_df = hist_ohlc[hist_ohlc.ticker==ticker].copy(deep=True)


# Fn to apply a simple momentum trading strategy to a financial time series
def basic_momentum(df):
    
    # Calculate Log Returns
    df['returns'] = np.log(df['close'] / df['close'].shift(1))
    
    # Calculate Momentum for different periods
    # Periods are independant of the data aggregation level, eg if 2hr then 15 = 30hrs
    cols = []
    for momentum in [15, 30, 60, 120]:
        col = 'position_%s' % momentum 
        df[col] = np.sign(df['returns'].rolling(momentum).mean())
        cols.append(col)   
        
    # Calculate Returns for each period
    strats = ['returns']
    for col in cols:
        strat = 'strategy_%s' % col.split('_')[1]
        df[strat] = df[col].shift(1) * tick_df['returns']
        strats.append(strat)
     
    # The total returns at any point in time are the sum up to that day & undo log transform
    returns_df = df[strats].dropna().cumsum().apply(np.exp)
    return returns_df



# Calculate Momentume Returms for each set of pairs
pairs_momentum_results = [basic_momentum(hist_ohlc[hist_ohlc.ticker==x]) for x in tickers if 'BTC' in x]


# Plot Results for All BTC based Pairs
modelled_tickers = [x for x in tickers if 'BTC' in x]

for i in range(0,len(pairs_momentum_results)):

    if len(pairs_momentum_results[i]) > 0:
        pair_id = i
        
        fig = pairs_momentum_results[pair_id].plot(title = modelled_tickers[pair_id])
        fig = fig.set_ylabel("Return (%)")
        fig = fig.get_figure()
        
        file_name = "C:/Users/yassin.eltahir/Downloads/CryptoPlots/{}_momentum_returns.png".format(modelled_tickers[pair_id])
        fig.savefig(file_name)