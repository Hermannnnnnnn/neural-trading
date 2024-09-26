import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import yfinance as yf
#import mplfinance as mpf
from datetime import datetime#, timedeltamsft 
from stock_indicators import Quote, indicators
pd.set_option('display.max_rows', None)
##############################################################
#VARIABLES
##############################################################
#for fetching historical stock data
ticker_symbol       ='MSFT'
start_date          = '2024-01-01'
end_date            ='2024-08-24'

##for macd
fast_periods    = 12
slow_periods    = 26
signal_periods  = 9

##############################################################
#fetching historical data
##############################################################
df = yf.download(ticker_symbol, start=start_date, end=end_date).reset_index()
print(df.head())
##############################################################
#Adding stock indicators
##############################################################
quotes_list = [
    Quote(d,o,h,l,c,v) 
    for d,o,h,l,c,v 
    in zip(df['Date'], df['Open'], df['High'], df['Low'], df['Close'], df['Volume'])
]
results = indicators.get_macd(quotes_list, fast_periods=fast_periods, slow_periods=slow_periods, signal_periods=signal_periods)

##############################################################
#Making figure
##############################################################
x = np.array([x.date.date() for x in results])
y_macd = np.array([x.macd for x in results])#, df['High'].values)
y_prices = df['High'].to_numpy()
fig, (ax1, ax2) = plt.subplots(2,1)
ax1.plot(x, y_prices)
ax2.plot(x, y_macd)
ax1.sharex(ax2)
ax2.axhline(y=0, xmin=0, xmax=1)
#ax1.set(xlabel='time (s)', ylabel='prices',)
#       title='About as simple as it gets, folks')
ax2.set(xlabel='time (s)', ylabel='macd',)
#       title='About as simple as it gets, folks')

#ax1.grid()
#ax2.grid()
plt.savefig(os.path.join("results","pictures", "mygraph.png"))