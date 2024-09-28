import pytest
import pandas as pd
from helper_raw_data import raw_data

@pytest.fixture(scope='module', autouse=True)  
def my_test_df_prices() -> pd:dataframe:
    """
    Making a custom test dataframe
    """
    data = {
        'Volume':[0,100,200]

    }

def test_raw_data_download_data:
    data = raw_data.download_data()