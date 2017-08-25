"""
Title:  Basic Momentum
Desc:   Apply a simple momentum strategy to 2hr candle stick data
Author: Yassin Eltahir
Date:   2017-08-24
"""

import pandas as pd
import numpy as np
from tqdm import tqdm
import seaborn as sns
%matplotlib inline

# Source Historical Data
dat_loc = '/Users/yassineltahir/Downloads/poloniex_crypto_pairs_price_history.csv'
hist_ohlc = pd.read_csv(dat_loc)

# Convert Date to timestamp and assign an index
hist_ohlc.index = pd.DatetimeIndex(hist_ohlc.date)

# Available Tickers
tickers = hist_ohlc.ticker.unique().tolist()

# Select a Ticker & Subset
ticker = tickers[12]
tick_df = hist_ohlc[hist_ohlc.ticker==ticker].copy(deep=True)


# Calculate the return & log return for the close price
tick_df['return'] = tick_df.close/tick_df.close.shift(1)
tick_df['log_return'] = np.log(tick_df['return'])


# Define Momentum as the average return over the last N candles
num_candles = [1,5,12,24]

mom_names = []
mom_log_names = []
for period in num_candles:
    
    # Calc rolling regular returns
    col = 'rolling_return_{}'.format(period)
    mom_names.append(col)
    tick_df[col] = tick_df['return'].rolling(period).mean()
    
    # Calc rolling log returns
    col_log = 'rolling_return_log_{}'.format(period)
    mom_log_names.append(col_log)
    tick_df[col_log] = tick_df['log_return'].rolling(period).mean()


plot_df = tick_df[mom_log_names].dropna()
plot_df.plot()
# sns.tsplot(data=plot_df)


"""
Strategy:
    If the rolling returns > 1 then buy/hold
    If the rolling returns = 0 then hold
    If the rolling returns < 1 then sell
"""

# Calculate strategy flag
strat_names = []
strat_log_names = []
for i in range(0,len(num_candles)):
    
    # Calculate regular strategy
    strat = "strategy_{}".format(num_candles[i])
    tick_df[strat] = np.sign(tick_df[mom_names[i]])
    strat_names.append(strat)
    
    # Calculate log regular strategy
    strat_log = "strategy_log_{}".format(num_candles[i])
    tick_df[strat_log] = np.sign(tick_df[mom_log_names[i]])
    strat_log_names.append(strat_log)
    
   
# View Strategy Decisions
tick_df[strat_log_names].dropna().plot()



# # Calculate Actual Returns
# act_names = []
# act_log_names = []
# for i in range(0,len(num_candles)):
    
#     # Calculate regular strategy
#     strat = "strategy_{}".format(num_candles[i])
#     tick_df[strat] = np.sign(tick_df[mom_names[i]])
#     strat_names.append(strat)
    
#     # Calculate log regular strategy
#     strat_log = "strategy_log_{}".format(num_candles[i])
#     tick_df[strat_log] = np.sign(tick_df[mom_log_names[i]])
#     strat_log_names.append(strat_log)
    
   
# # View Strategy Decisions
# tick_df[strat_log_names].dropna().plot()