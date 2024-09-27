import yfinance as yf
import pandas as pd

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
"""

class raw_data:
  def __init__(self, ticker, start_date, end_date, interval):
    self.ticker     = ticker
    self.start_date = start_date # of form 2024-01-30
    self.end_date   = end_date# of form 2024-01-30
    self.interval   = interval 

  def download_data(self) -> None:
    self.df_prices = yf.download(self.ticker, start=self.start_date, end=self.end_date, interval=self.interval).reset_index()

  def calculate_percentual_change(self, field='Close', steps=1) -> None:
      """
      function to calculate the percentual change over a number of steps. Defaults to the 'Close' column of the raw downloaded data.
      """
      column_headers = self.df_prices.columns.tolist()

      if field not in column_headers:
          raise NameError(f'Wrong field. {field} does not match the column headers {column_headers}')
      else:
          self.df_prices[f'shifted_{steps}']       = self.df_prices[field].shift(-steps)
          self.df_prices[f'perc_ch_{steps}_steps'] = (self.df_prices[f'shifted_{steps}'] - self.df_prices[field])/self.df_prices[f'shifted_{steps}']*100

  def bucketting_prices(self,steps=1, bins=[-100,-2,-1,1,2,100],labels = [-2,-1,0,1,2]) -> None:# labels=['Very bad', 'bad', 'neutral', 'good', 'very good']):
      """
      This function buckets price movements (in percentages) into bins.
      Hence you have to run calculate_percentual_change first.
      """
      self.df_prices[f'perc_ch_{steps}_steps_binned'] = pd.cut(self.df_prices[f'perc_ch_{steps}_steps'], bins=bins,labels=labels)
