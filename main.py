import os
import pandas as pd
import numpy as np
from helper_raw_data import raw_data
from helper_stock_indicators import my_indicators
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)

##############################################################
#VARIABLES
##############################################################
#for fetching historical stock data
ticker              = 'MSFT'
start_date          = '2024-01-01'
end_date            = '2024-08-24'
interval            = '1d'
#for percentual increase calculations and bucketting
field               = 'Close'
steps_perc_change   = 5
bins                = [-100,-2,-1,1,2,100] #percentual gain is classified into bins: [-100,-2], [-2, -1], etc
labels              = [-2,-1,0,1,2]       #These bins are then labels: [-100,-2] becomes -2, etc.

##for macd
fast_periods    = 12
slow_periods    = 26
signal_periods  = 9

#For neural network model
##############################################################
#fetching historical data
##############################################################
raw_data_inst = raw_data(ticker,start_date, end_date, interval)
raw_data_inst.download_data()
raw_data_inst.calculate_percentual_change(field=field,steps=steps_perc_change)
raw_data_inst.bucketting_prices(steps=steps_perc_change, bins=bins, labels=labels)
print(raw_data_inst.df_prices.head())
##############################################################
#Adding stock indicators
##############################################################
my_indicators_inst = my_indicators(raw_data_inst.df_prices)
my_indicators_inst.gimme_macd(fast_periods=fast_periods, slow_periods=slow_periods, signal_periods=signal_periods)
print(my_indicators_inst.df_prices.head())
#############################################################
#Making figure
##############################################################
dates    = my_indicators_inst.df_prices['Date'].to_numpy()
y_prices = my_indicators_inst.df_prices['High'].to_numpy()
y_macd   = my_indicators_inst.df_prices[f'macd_{fast_periods}_{slow_periods}_{signal_periods}'].to_numpy()
y_binned = my_indicators_inst.df_prices[f'perc_ch_{steps_perc_change}_steps_binned'].fillna(0).to_numpy()

fig, (ax1, ax2, ax3) = plt.subplots(3,1)
ax1.plot(dates   , y_prices)
ax2.plot(dates   , y_macd)
ax2.axhline(y=0, xmin=0, xmax=1)
ax3.scatter(dates, y_binned)

ax1.sharex(ax2)
ax3.sharex(ax2)

ax2.set(xlabel='time (s)', ylabel='macd',)

plt.savefig(os.path.join("results","pictures", "mygraph.png"))