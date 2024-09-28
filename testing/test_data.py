import pytest
import random
import numpy as np
import pandas as pd
from helper_raw_data import raw_data
import datetime

@pytest.fixture(scope='module', autouse=True)  
def raw_test_data():
    """
    Making a custom test dataframe
    """
    size = 5
    start = datetime.datetime.today()

    prices = {
                'Volume':random.sample([i for i in np.arange(10, 200, 1 )],size ),  
                'Close': random.sample([i for i in np.arange(100, 120, 1 )],size ),                  
                'Open': random.sample([i for i in np.arange(100, 120, 1 )],size),
                'Date': [start.date() + datetime.timedelta(days=x) for x in range(size)]
            }
    raw_data_inst = raw_data('TEST', min(prices['Date']), max(prices['Date']),'1d')
    raw_data_inst.df_prices = pd.DataFrame(prices)
    return raw_data_inst

def test_helper_raw_data():
    ticket = 'MSFT'
    assert 1==1