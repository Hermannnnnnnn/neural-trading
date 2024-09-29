import tensorflow as tf
import re
import pandas as pd
import os

class my_NNM:
    def __init__(self, df_prices, label_fields = ['Close', 'Volume'], target_field = 'some_bin_column', number_of_shifts_of_labels=5):
        """
        -----------
        INPUT
        -----------
        df_prices    = dataframe holding 
                        - stock data 'Date, Close, Open, Volume, etc'
                        - binned percentual changes <- these are the target fields
        label_fields = list of column headers of df_prices. These are the so-called labels ie input for our neural network
        target_field = a column_header of df_prices. This is the target ie output for our neural network.
        number_of_shifts_of_labels = a number telling us how many copies we want of the label_fields, each shifted one more row.
                                     Each of these shifted columns will be taken as input for the NNM.
        """
        self.df_prices = df_prices
        self.label_fields = label_fields
        self.target_field = target_field
        self.number_of_shifts_of_labels = number_of_shifts_of_labels
        self.shift_labels()
    
    def shift_labels(self):
        # if not set(self.label_fields) <=  self.df_prices.columns.tolist():
        #   raise NameError(f'Wrong field. {str(self.label_fields)} does not match the column headers {str(self.df_prices.columns.tolist())}')
        # elif self.number_of_shifts_of_labels <= 0:
        #   raise ValueError(f'Wrong value for number_of_shifts_of_labels. Shoulb be > 0, is {self.number_of_shifts_of_labels}')            
        # else:
        
        for field in self.label_fields:
            for steps in range(self.number_of_shifts_of_labels):
                self.df_prices[f'{field}_shifted_{steps}']       = self.df_prices[field].shift(-steps)
        self.df_prices.dropna(how='any', inplace=True)

    def prep_data(self, frac=0.80):
        labels = []
        #dividing sets into labels and target
        for column in self.df_prices.columns.tolist():
            for my_label in self.label_fields:
                if re.search(rf'{my_label}_shifted_[\d]+', column):
                    labels.append(column)
        # labels = [x for x in self.df_prices.columns.tolist() if re.search(f'{y}\_shifted\_\d', x) for y in self.label_fields]
        #dividing data into its training set and validation set
        count_rows = self.df_prices.shape[0]
        self.train_df_prices = self.df_prices[labels + [self.target_field]][:(round(count_rows*frac))]
        self.val_df_prices = self.df_prices[labels + [self.target_field]][( round(count_rows*frac)):count_rows]
        #scaling sets to range of [0,1]
        max_val = self.train_df_prices.max(axis= 0)
        min_val = self.train_df_prices.min(axis= 0)    
        range = max_val.sub(min_val)
        # range = max_val - min_val
        self.train_df_prices = (self.train_df_prices - min_val)/range
        self.val_df_prices =  (self.val_df_prices- min_val)/range

        self.X_train    = self.train_df_prices[labels]
        self.X_val      = self.val_df_prices[labels]
        self.y_train    = self.train_df_prices[self.target_field]
        self.y_val      = self.val_df_prices[self.target_field]
        print(self.X_train)
        print(self.X_val)
        print(self.y_train)
        print(self.y_val)
    def prep_NNM(self, layers):
        input_shape = [self.X_train.shape[1]]       
        print(input_shape)
        self.model = tf.keras.Sequential([        
            tf.keras.layers.Dense(units=64, activation='relu',
                                input_shape=input_shape),
            tf.keras.layers.Dense(units=64, activation='relu'),
            tf.keras.layers.Dense(units=1)
        ])
        self.model.summary()
        self.model.compile(optimizer='adam',  
                    
                    # MAE error is good for
                    # numerical predictions
                    loss='mae')  
    def train_NNM(self):
       losses = self.model.fit(self.X_train, self.y_train,
 
                   validation_data=(self.X_val, self.y_val),
                    
                   # it will use 'batch_size' number
                   # of examples per example
                   batch_size=256, 
                   epochs=15,  # total epoch
                   )
       
    # def predict_NNM(self):
       
    #     # this will pass the first 3 rows of features
    #     # of our data as input to make predictions
    #     self.model.predict(self.X_val.iloc[0:3, :])


if __name__ == '__main__':
    df_prices = pd.read_csv(os.path.join('results', 'data', 'df_prices_with_indicators'))
    my_bin_column = ""
    columns = df_prices.columns.tolist()
    for column in columns:
       if column.find("steps_binned"):
          my_bin_column = column

    my_NNM_inst = my_NNM(df_prices,label_fields=["Close", "Volume"], target_field=my_bin_column, number_of_shifts_of_labels=5)

    my_NNM_inst.prep_data()
    my_NNM_inst.prep_NNM(3)
    my_NNM_inst.train_NNM()
