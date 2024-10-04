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

    df_prices_test = pd.DataFrame({"perc_ch_0_steps":[0.0,-2,2],"perc_ch_1_steps":[  -2.781694,0,4 ],"perc_ch_2_steps":[ 2.238303,0,0],"perc_ch_3_steps":[0.196046 ,0,0 ],"perc_ch_4_steps":[1.153931 ,0,0]})
    raw_data_inst = raw_data('TEST_TICKER', '2000-01-01','2999-12-31', '1d', -1)
    raw_data_inst.df_prices = df_prices_test
    return raw_data_inst

def test_helper_raw_data(raw_test_data):
    print('my bucketted prices are')
    print(pd.DataFrame(raw_test_data.bucketting_prices(bins=[-100,2,3,100], labels=[0,1,2])).values.tolist())
    print('my desired outcome is')
    print([[0],[0],[2]])
    assert all([a[0] == b[0] for a, b in zip(pd.DataFrame(raw_test_data.bucketting_prices(bins=[-100,2,3,100], labels=[0,1,2])).values.tolist(), [[0],[0],[2]])])

    # assert pd.DataFrame(raw_test_data.bucketting_prices(bins=[-100,2,3,100], labels=[0,1,2])).values.tolist() == [[[0],[0],[2]]]