import tensorflow as tf
from tensorflow import keras
import keras
from keras import layers
from keras_tuner.tuners import RandomSearch#,BayesianOptimization #doesn't work, to research
# from kerastuner.tuners import BayesianOptimization

from keras_tuner.engine.hyperparameters import HyperParameters
from tensorflow.keras.utils import to_categorical #function to transform for instance [1,2,3] into [[1,0,0],[0,1,0], [0,0,1]]. The latter is the format for output of neural network
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Activation
import re
import pandas as pd
import os
import matplotlib.pyplot as plt
import time
from datetime import datetime
# import np_utils
class my_NNM:
    def __init__(self, df_prices, label_fields = ['macd_12_26_9', 'Volume'], target_field = 'some_bin_column'):
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
        self.df_prices                  = df_prices
        self.label_fields               = label_fields
        self.target_field               = target_field
        if not os.path.exists(os.path.join('results','data', datetime.now().strftime("%Y-%m-%d")) ):
            os.mkdir(os.path.join('results','data', datetime.now().strftime("%Y-%m-%d")) )
        self.output_folder              = os.path.join('results','data', datetime.now().strftime("%Y-%m-%d"),datetime.now().strftime("%H-%M-%S.%f"))
    
    def prep_data(self, frac=0.70):
        """
        Function that preps the data for input into the Neural Network:
        --------------
        ACTIONS:
        ---------------
        - divide the data into layer (= input) and output
        - further divide into training and validation set, based on frac
        - Normalize the input ie make sure values are between 0 and 1 for better behaviour
        - Categorize output. Ex: outputs [0,1,2] become [[1,0,0], [0,1,0], [0,0,1]]
        --------------
        OUTPUT:
        --------------
        new dfs:
        - self.X_train
        - self.X_val
        - self.y_train
        - self.y_val
        """
        labels = []
        #identifying the labels
        for column in self.df_prices.columns.tolist():
            for my_label in self.label_fields:
                if re.search(rf'{my_label}_shifted_[\d]+', column):
                    labels.append(column)
        #dividing data into its training set and validation set and into labels and target
        count_rows = self.df_prices.shape[0]
        self.X_train = self.df_prices[labels ][:(round(count_rows*frac))]
        self.X_val = self.df_prices[labels ][( round(count_rows*frac)):count_rows]
        self.y_train = self.df_prices[self.target_field ][:(round(count_rows*frac))]
        self.y_val = self.df_prices[self.target_field ][( round(count_rows*frac)):count_rows]
        #scaling sets to range of [0,1]
        max_val = self.X_train.max(axis= 0)
        min_val = self.X_train.min(axis= 0)    
        range = max_val.sub(min_val)
        print(range)
        # range = max_val - min_val
        self.X_train = (self.X_train - min_val)/range
        self.X_val =  (self.X_val- min_val)/range

        number_of_classes = self.y_train.nunique()
        self.y_train    = to_categorical(self.y_train, number_of_classes)
        self.y_val      = to_categorical(self.y_val, number_of_classes)
        return


    def build_model(self,hp):
        def call_code(units, activation, dropout, lr):#contains code for model, input are hyperparameters to be optimized by keras-tuner
            model = keras.Sequential()
            model.add(layers.Flatten())
            model.add(layers.Dense(units=units, activation=activation))
            if dropout:
                model.add(layers.Dropout(rate=0.25))
            model.add(layers.Dense(2, activation=activation))
            model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=lr),
                loss="binary_crossentropy",#"categorical_crossentropy", #
                metrics=["accuracy"],
            )
            return model

        units = hp.Int("units", min_value=32, max_value=512, step=32)
        # units = 64
        activation = hp.Choice("activation", ["relu", "sigmoid"])
        dropout = hp.Boolean("dropout")
        lr = hp.Float("lr", min_value=1e-4, max_value=1e-2, sampling="log")#learning rate
        # call existing model-building code with the hyperparameter values.
        model = call_code(
            units=units, activation=activation, dropout=dropout, lr=lr
        )
        return model
    

    def tune_model(self):
        tuner = RandomSearch(
        # tuner = BayesianOptimization(
                self.build_model,
                objective='val_accuracy',
                max_trials=3,  # how many model variations to test? Only useful with
                executions_per_trial=3,  # how many trials per variation? (same model could perform differently)
                directory=os.path.join(self.output_folder),
                project_name = 'my_neural_trading_keras'
        )

        tuner.search(x=self.X_train,
                    y=self.y_train,
                    # verbose=2, # just slapping this here bc jupyter notebook. The console out was getting messy.
                    epochs=3,
                    batch_size=64,
                    #callbacks=[tensorboard],  # if you have callbacks like tensorboard, they go here.
                    validation_data=(self.X_val, self.y_val))
        tuner.results_summary()

    # The following is without keras_tuner, but simply code for optimizing a hardcoded model
    def prep_NNM(self, layers):
        input_shape = [self.X_train.shape[1]]       
        print(input_shape)
        self.model = tf.keras.Sequential([        
            tf.keras.layers.Dense(units=64, activation='relu',
                                input_shape=input_shape),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(units=64, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(units=1, activation= 'sigmoid')
        ])
        self.model.summary()
        self.model.compile(optimizer='adam',  
                    
                    # MAE error is good for
                    # numerical predictions
                    loss='mse', metrics=['accuracy'])  #loss: mae = mean absolute error, mse = mean squared error
    def train_NNM(self):
        losses = self.model.fit(self.X_train.to_numpy(), self.y_train,
 
                   validation_data=(self.X_val.to_numpy(), self.y_val),
                    
                   # it will use 'batch_size' number
                   # of examples per example
                   batch_size=256, 
                   epochs=50,  # total epoch
                   )
        print('losses ')
        print(losses.history)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        length = len(losses.history['loss'])
        # loss_df.loc[:,['loss','val_loss']].plot()
        ax.plot(list(range(0, length)), losses.history['loss'],color="red", label = "loss")       
        ax.plot(list(range(0, length)), losses.history['val_loss'], color="blue", label = "val_loss") 
        ax.legend(["loss", "val_loss"])      
        plt.savefig(os.path.join("results","pictures", "myNNM_plot_losses.png"))
    # def predict_NNM(self):
       
    #     # this will pass the first 3 rows of features
    #     # of our data as input to make predictions
    #     self.model.predict(self.X_val.iloc[0:3, :])
    

if __name__ == '__main__':
    df_prices = pd.read_csv(os.path.join('results', 'data', 'df_prices_with_indicators'))
    ###########################
    # Looking for name of bin column
    my_bin_column = ""
    columns = df_prices.columns.tolist()
    for column in columns:
       if "steps_binned" in column:
          my_bin_column = column
    print(my_bin_column)
    ###########################

    my_NNM_inst = my_NNM(df_prices,label_fields=["macd_12_26_9", "Volume"], target_field=my_bin_column)#, number_of_shifts_of_labels=5)

    my_NNM_inst.prep_data()
    my_NNM_inst.tune_model()

    # my_NNM_inst.prep_NNM(3)
    # my_NNM_inst.train_NNM()
