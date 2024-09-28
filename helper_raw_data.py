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
          self.df_prices[f'shifted_{steps}']       = self.df_prices[field].shift(-steps)
          self.df_prices[f'perc_ch_{steps}_steps'] = (self.df_prices[f'shifted_{steps}'] - self.df_prices[field])/self.df_prices[f'shifted_{steps}']*100

  def bucketting_prices(self,smoothen: bool = True, steps: int =1, bins: list =[-100,-2,-1,1,2,100],labels: list = [-2,-1,0,1,2]) -> None:# labels=['Very bad', 'bad', 'neutral', 'good', 'very good']):
      """
      This function buckets price movements (in percentages) into bins.
      Hence you have to run calculate_percentual_change first.
      ---------------------
      INPUT
      ---------------------
      smoothen: if true, then the percentual changes are averaged out a bit, in case we have an extremely volatile market.
      steps:    the same value as used in calculate_percentual_change() and tells for how many steps we look in the future to calculate the percentual increase
      bins:     list determining boundaries for buckets
      labels:   list for the labels ie values of the buckets
      ---------------------
      OUTCOME
      ---------------------
      Adds a column to self.df_prices. Column is named f'perc_ch_{steps}_steps_binned'
      """

      self.df_prices[f'perc_ch_{steps}_steps_binned'] = pd.cut((self.df_prices[f'perc_ch_{steps}_steps']+self.df_prices[f'perc_ch_{steps}_steps'].shift(1))/2, bins=bins,labels=labels)
