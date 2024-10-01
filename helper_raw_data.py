import yfinance as yf
import pandas as pd
import numpy as np
import re
from stock_indicators import Quote, indicators


"""
This file contains some functions to download historical prices for stocks and to apply some basic transformations.
--------------------
DOWNLOAD DATA:
--------------------
- yfinance
--------------------
TRANSORMING DATA:
--------------------
- calculating price movements in percentage
- calculating labeled buckets for these percentages.

With stock_indicators we calculate .. stock indicators ;)
"""

class raw_data:
  def __init__(self, ticker, start_date, end_date, interval,stop_loss):
    self.ticker     = ticker
    self.start_date = start_date # of form 2024-01-30
    self.end_date   = end_date# of form 2024-01-30
    self.interval   = interval
    self.stop_loss  = stop_loss
    #for stock indicators 
    
  def download_data(self) -> None:
    self.df_prices = yf.download(self.ticker, start=self.start_date, end=self.end_date, interval=self.interval).reset_index()
    return
  
  def calculate_percentual_change(self, field: str ='Close', steps: int =1) -> None:
      """
      This function calculates the percentual change over a number of steps. Defaults to the 'Close' column of the raw downloaded data.
      --------------------
      INPUT
      --------------------
      field:      This string is the column name in self.df_prices, holding price data for which we want to calculate percentual changes.
      steps:      This integer tells how many steps in the future we go to compare prices with and calculate the percentual change. 
      --------------------
      OUTCOME
      --------------------
      Two added columns to self.df_prices.
      - First is f'shifted_{steps}' which is the {field} column, shifted {steps} steps.
      - Second is f'perc_ch_{steps}_steps'. It contains the percentual change between f'shifted_{steps}' and {field}
      """
      column_headers = self.df_prices.columns.tolist()
      if field not in column_headers:
          raise NameError(f'Wrong field. {field} does not match the column headers {column_headers}')
      else:
          for ind in range(steps):
            self.df_prices[f'shifted_{ind}']       = self.df_prices[field].shift(-ind)
            self.df_prices[f'perc_ch_{ind}_steps'] = (self.df_prices[f'shifted_{ind}'] - self.df_prices[field])/self.df_prices[f'shifted_{ind}']*100
      return
  def bucketting_prices(self,smoothen: bool = True, steps: int =1, bins: list =[-100,-2,-1,1,2,100],labels: list = [-2,-1,0,1,2]) -> None:# labels=['Very bad', 'bad', 'neutral', 'good', 'very good']):
      """
      This function buckets price movements (in percentages) into bins.
      Hence you have to run calculate_percentual_change first.
      ---------------------
      INPUT
      ---------------------
      smoothen: At the moment, OBSOLETE. Funcionality replaced by taking the max percentual increase over a period of time. #if true, then the percentual changes are averaged out a bit, in case we have an extremely volatile market.
      steps:    the same value as used in calculate_percentual_change() and tells the range for which we take the max increase as percentual change.
      bins:     list determining boundaries for buckets
      labels:   list for the labels ie values of the buckets
      ---------------------
      OUTCOME
      ---------------------
      Adds a column to self.df_prices. Column is named f'perc_ch_{steps}_steps_binned'
      """
      columns = [x for x in self.df_prices.columns.tolist() if re.search(r'perc_ch_[\d]+_steps', x) is not None]
      def min_max_function(row):
         if np.min(row)< self.stop_loss:#row[columns].min(axis=1) 
            return np.min(row)# row[columns].min(axis=1)
         else:
            return np.max(row)# row[columns].max(axis=1)
      # self.df_prices[f'perc_ch_{steps}_steps_binned'] = pd.cut(self.df_prices[columns].apply(min_max_function, axis=1), bins=bins,labels=labels)#self.df_prices[columns].max(axis=1)

      # self.df_prices[f'perc_ch_{steps}_steps_binned'] = pd.cut((self.df_prices[f'perc_ch_{steps}_steps']+self.df_prices[f'perc_ch_{steps}_steps'].shift(1))/2, bins=bins,labels=labels)
      return pd.cut(self.df_prices[columns].apply(min_max_function, axis=1), bins=bins,labels=labels)#self.df_prices[columns].max(axis=1)

  
  def gimme_macd(self, fast_periods=12, slow_periods=26, signal_periods=9):
      self.quotes_list = [
                          Quote(d,o,h,l,c,v) 
                          for d,o,h,l,c,v 
                          in zip(self.df_prices['Date'], self.df_prices['Open'], self.df_prices['High'], self.df_prices['Low'], self.df_prices['Close'], self.df_prices['Volume'])
                          ]

      # self.df_prices[f'macd_{fast_periods}_{slow_periods}_{signal_periods}'] = [x.macd for x in indicators.get_macd(self.quotes_list, fast_periods=fast_periods, slow_periods=slow_periods, signal_periods=signal_periods)]
      return  [x.macd for x in indicators.get_macd(self.quotes_list, fast_periods=fast_periods, slow_periods=slow_periods, signal_periods=signal_periods)]
  
  def stack_input_data(self, fields = ['macd_12_26_9', 'Volume'], number_of_stacks=5):
    for field in fields:
      for stack in range(number_of_stacks):
          self.df_prices[f'{field}_shifted_{stack}']       = self.df_prices[field].shift(-stack)
    self.df_prices.dropna(how='any', inplace=True)
    return
