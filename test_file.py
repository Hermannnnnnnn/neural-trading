from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
#import mplfinance as mpf
from datetime import datetime#, timedeltamsft 
from stock_indicators import Quote, indicators
pd.set_option('display.max_rows', None)
##############################################################
#VARIABLES
##############################################################
ticker_symbol       ='MSFT'
start_date          = '2024-01-01'
end_date            ='2024-08-24'
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

results = indicators.get_sma(quotes_list, 20)
#print(results)
#print(type(results))
print([f"sma on date {x.date.date()} was {x.sma}" for x in results])