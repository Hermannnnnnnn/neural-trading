import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

df = pd.read_csv(os.path.join('results', 'data', 'df_prices_prediction.csv'))
print(df.head())
my_bin_column = ""
columns = df.columns.tolist()
print(columns)
for column in columns:
    if "steps_binned" in column:
        my_bin_column = column
print(my_bin_column)
my_pred_columns = [ x for x in columns if x.isnumeric()]
# my_perc_ch_columns = [x for x in columns if 'perc_ch' in x and 'steps_binned' not in x]
# print(df[[my_bin_column] + my_perc_ch_columns].head(35))
# exit()
dates    = df['Date']
y_prices = df['Close']
# y_perc   = df[my_perc_ch_columns]
y_pred   = df[my_pred_columns]

y_bins      = df[my_bin_column]

fig,(ax1, ax2,ax4) = plt.subplots(3,1)
ax1.plot(y_prices)#.head(50))
plt.grid()
ax2.plot(y_bins)#.head(50))
plt.grid()
for column in y_pred.columns.tolist():
    ax4.plot(y_pred[column], label=column)#.head(50))
ax4.axhline(y=0.5, xmin=0, xmax=1)

plt.grid()
# ax3.plot(y_perc)#.head(50))
# ax3.set_yticks(np.arange(-1, 4, 1))
# ax3.set_ylim(-2,3)

ax4.grid(axis="x")
ax1.sharex(ax2)
# ax2.sharex(ax3)
ax2.sharex(ax4)

ax1.grid()
ax2.grid()
# ax3.grid()
ax4.grid()

ax1.set(xlabel='time (s)', ylabel='prices',)
ax2.set(xlabel='time (s)', ylabel='bins',)

ax4.set(xlabel='time (s)', ylabel='predictions',)
ax4.legend()
plt.savefig(os.path.join("results","pictures", "mypredictions.png"))
