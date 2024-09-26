import pandas as pd
import numpy as np
import math
def calculate_percentual_change(df_prices, steps=1):
    """
    function to calculate the percentual change. Comparison is between df_prices 
    and these prices with an offset of 'steps'
    """
    column_headers = df_prices.columns.tolist()

    if len(column_headers) > 1:
        raise ValueError(f'Too many columns. Epexted 1, got {len(column_headers)}.')
    else:
        df_prices[f'shifted_{steps}']                   = df_prices.shift(-steps)
        df_prices[f'percentual_change_{steps}_steps']   = (df_prices[f'shifted_{steps}'] - df_prices[column_headers[0]])/df_prices[f'shifted_{steps}']*100
        #df_prices[['Open']].assign(lambda x: (x[f'shifted_{steps}'] - x[column_headers[0]])/x[f'shifted_{steps}'] if not math.isnan(x[f'shifted_{steps}']) else 0)
    return df_prices[f'percentual_change_{steps}_steps']

def bucketting_prices(df_prices,bins=[-100,-2,-1,1,2,100],labels = [-2,-1,0,1,2]):# labels=['Very bad', 'bad', 'neutral', 'good', 'very good']):
    """This function buckets prices into bins.
        df_prices should be a dataframe with only one column, values are percentual changes
    """
    df_prices['binned'] = pd.cut(df_prices, bins,labels=labels)
    return df_prices['binned']