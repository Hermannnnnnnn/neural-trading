import os
import pandas as pd
import numpy as np
from helper_raw_data import raw_data
import matplotlib.pyplot as plt
from helper_neural_network import my_NNM

pd.set_option('display.max_rows', None)
##############################################################
#VARIABLES
##############################################################
#for fetching historical stock data
ticker              = 'MSFT'
start_date          = '2022-01-01'
end_date            = '2024-01-24'
interval            = '1d'
start_date_for_pred = '2024-01-24'
end_date_for_pred   = '2024-10-01'
#for percentual increase calculations and bucketting
field               = 'Close'
steps_perc_change   = 5
stop_loss           = -1.0
bins                = [-100,2,100]#[-100,-2,-1,1,2,100] #percentual gain is classified into bins: [-100,-2], [-2, -1], etc
labels              = [0,1] #[-2,-1,0,1,2]       #These bins are then labels: [-100,-2] becomes -2, etc.

##for stock indicators
fast_periods    = 5
slow_periods    = 13
signal_periods  = 6
ema_periods     = 26

#For neural network model
number_of_stacks        = 5 # we take the macd signals of, for instance, the last 5 moments as input for neural network.
frac                    = .6 # tells how to divide data between training and validation sets
tuning_number_of_epochs = 20 #is how many iterations we let the model fit to the training set


##############################################################
def make_figure(raw_data_inst):
    dates    = raw_data_inst.df_prices['Date']#.to_numpy()
    y_prices = raw_data_inst.df_prices['Close']#.to_numpy()
    y_macd   = raw_data_inst.df_prices[f'macd_{fast_periods}_{slow_periods}_{signal_periods}']#.to_numpy()
    y_binned = raw_data_inst.df_prices[f'perc_ch_{steps_perc_change}_steps_binned'].fillna(0)#.to_numpy()

    fig, (ax1, ax2, ax3) = plt.subplots(3,1)
    ax1.plot( y_prices.head(100))
    ax2.plot( y_macd.head(100))
    ax2.axhline(y=0, xmin=0, xmax=1)
    ax3.plot( y_binned.head(100))

    ax1.sharex(ax2)
    ax3.sharex(ax2)
    ax1.set(xlabel='time (s)', ylabel='price Close',)
    ax2.set(xlabel='time (s)', ylabel='macd',)
    ax3.set(xlabel='time (s)', ylabel='bins',)

    plt.savefig(os.path.join("results","pictures", "myprices.png"))
##############################################################
#fetching historical data and transforms
##############################################################
raw_data_inst = raw_data(ticker,start_date, end_date, interval,stop_loss)
raw_data_inst.download_data()
raw_data_inst.calculate_percentual_change(field=field,steps=steps_perc_change)#calculates new columns f'perc_ch_{ind}_steps', ind is value between 0 and steps
raw_data_inst.df_prices[f'perc_ch_{steps_perc_change}_steps_binned']            = raw_data_inst.bucketting_prices(bins=bins, labels=labels)
raw_data_inst.df_prices[f'macd_{fast_periods}_{slow_periods}_{signal_periods}'] = raw_data_inst.gimme_macd(fast_periods=fast_periods, slow_periods=slow_periods, signal_periods=signal_periods)
raw_data_inst.df_prices.dropna(how='any', inplace=True)

# raw_data_inst.df_prices[f'ema_{ema_periods}'] = raw_data_inst.gimme_ema(ema_periods=ema_periods)

raw_data_inst.stack_input_data(fields=[f'macd_{fast_periods}_{slow_periods}_{signal_periods}', 'Volume'], number_of_stacks=number_of_stacks)

raw_data_inst.df_prices.to_csv(os.path.join('results','data','df_prices_with_indicators.csv'))
make_figure(raw_data_inst)
##############################################################
#fetching historical data and transforms
##############################################################
# Looking for name of bin column, calculated in previous steps
my_bin_column = ""
columns = raw_data_inst.df_prices.columns.tolist()
for column in columns:
    if "steps_binned" in column:
        my_bin_column = column

my_NNM_inst = my_NNM(raw_data_inst.df_prices,label_fields=[f'macd_{fast_periods}_{slow_periods}_{signal_periods}', "Volume"], target_field=my_bin_column)
my_NNM_inst.prep_data(frac = frac)
my_NNM_inst.tune_model(epochs=tuning_number_of_epochs)
my_NNM_inst.train_model()


###########################################################
#Now, let's make predictions

raw_data_inst_2 = raw_data(ticker,start_date_for_pred, end_date_for_pred, interval,stop_loss)
raw_data_inst_2.download_data()
raw_data_inst_2.calculate_percentual_change(field=field,steps=steps_perc_change)#calculates new columns f'perc_ch_{ind}_steps', ind is value between 0 and steps
raw_data_inst_2.df_prices[f'perc_ch_{steps_perc_change}_steps_binned']            = raw_data_inst_2.bucketting_prices(bins=bins, labels=labels)
raw_data_inst_2.df_prices[f'macd_{fast_periods}_{slow_periods}_{signal_periods}'] = raw_data_inst_2.gimme_macd(fast_periods=fast_periods, slow_periods=slow_periods, signal_periods=signal_periods)
# raw_data_inst_2.df_prices[f'ema_{ema_periods}'] = raw_data_inst_2.gimme_ema(ema_periods=ema_periods)
raw_data_inst_2.stack_input_data(fields=[f'macd_{fast_periods}_{slow_periods}_{signal_periods}', 'Volume'], number_of_stacks=number_of_stacks)

y_prediction = my_NNM_inst.predict_my_model(raw_data_inst_2.df_prices)
# raw_data_inst_2.df_prices =pd.concat([raw_data_inst_2.df_prices, pd.DataFrame(y_prediction)], axis=1)
pd.concat([raw_data_inst_2.df_prices.reset_index(), pd.DataFrame(y_prediction)], axis=1).to_csv(os.path.join('results','data','df_prices_prediction.csv'))
