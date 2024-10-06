#  Neural trading
1. [Introduction](#1-introduction)
2. [Run the project](#2-runn-the-project)
    1. [Prerequisites](#21-prerequisites)
    2. [Running the project](#22-running-the-project)
3. [Historical data](#3-historical-data)
    1. [yfinance](#31-yfinance)
    2. [binance](#32-binance)
4. [ML model tools](#4-ml-model-tools)
    1. [Stockpy](#41-stockpy)
    2. [Tensorflow](#42-tensorflow)
5. [Stock indicator tools](#5-stock-indicator-tools)
    1. [Stock-indicators](#51-stock-indicators)
6. [Neural network model design](#6-neural-network-model-design)
    1.  [Input](#61-input)
    2.  [Outcome](#62-outcome)


# 1. Introduction
In this project we try to apply neural network learning models to the field of the stock market (how original :blush:). To do so, we'll need:
- **historical stock data**,
- **Stock indicators**,
- **ML modeling tool**,
- **a model for the neural network**. 

How convenient that there are python packages enabling these requirements!!

Hereunder we'll
- first describe how to run the project, 
- then we explain some of the package choices available,which ones we chose and why we did so.
- The last section describes how we've applied our data to neural networks.

# 2. Run the project
## 2.1 Prerequisites
1. Have python installed (latest version should be enough lol)
2. Have .NET installed (see [4.1 Stock-indicators](#41-stock-indicators))
3. Run `python -m venv .venv` in the project folder
4. Activate the venv by executing `source .venv/bin/activate` for linux or `source .venv/bin/activate.ps1` for windows
4. Run `pip install -r requirements.txt`

## 2.2 Running the project

At the moment, you run the project by 
- running the *main.py* file. This will perform all the data transformations/manipulations/predictions.
- running the *draw_results.py*, which will generate a picture in *results/pictures/mypredictions.png*, visualizing the results.

# 3. Historical data
At the moment we're using **yfinance** because it's the easiest to use. Long term this is probably not the right choice for us, once we decide to try building our own auto-trading bot. Then other platforms will be better, like **binance** or others [see here](https://github.com/DaveSkender/Stock.Indicators/discussions/579).

## 3.1 yfinance
yfinance is open source, no registration required and very easy to fetch data :+1:. Simply install the requirements.txt and look at the helper module for its usage.

## 3.2 Binance
We first tried out binance, stepped away from it since you'll need an acount, deposit some money and get validated :-1:. In any case:

**Step I**
go to [this link](https://www.binance.com/en).

**Step II**
sign up or log in.

**Step III**
wait until approved and deposit money :/


# 4. ML model tools
My partner's computer is too slow :worried:. I wanted to use **tensorflow** since it's easy to implement and seemingly the most very popular package for ML. ML packages however are very large and will perform optimization algorithms, so I've ordered a new computer... .

## 4.1 Stockpy
We tried **Stockpy** first, after a quick google search. However, the last change was a year ago and I can't find much usefull documentation :-1:.
## 4.2 Tensorflow
Tensorflow however... **is a very popular tool** and it would seem very user-friendly :+1:.
- [Here](https://www.geeksforgeeks.org/implementing-neural-networks-using-tensorflow/)'s an easy example of applying neural networking to some data. 
- And [here](https://keras.io/guides/keras_tuner/getting_started/)'s a page showcasing the usage of the **keras tuner**. The keras tuner optimizes the hyperparameters for a neural network. Hyperparameters are external parameters, like number of nodes, number of layers, learning speed, activation function, etc. 
After this optimization, you can optimize the inner parameters (the weights). And after that, you are ready to make predictions.

We have implemented a similar setup as the second example.

# 5. Stock indicator tools
Why re-invent the wheel right (I did that some years back for these indicators :disappointed:). Of course there are packages available that calculate stock indicators! We tried out **stock-indicators**, happy so far with the results.

## 5.1 stock-indicators
**Stock-indicators** works with so-called `quotes` meh. To use it you'll need to have python duh, but also .NET. [See link](https://python.stockindicators.dev/guide/).

# 6. Neural network model design
## 6.1 Input
We'll use at this moment of writing the following as our N-dimensional input:
- a set of N concurrent MACD data points,
- combined with the respective trading volumes and
- the SMA or EMA, meant to incorporate the signal of a bullish or bearish market. (not yet implemented)

So our input incorporate the local behaviour of the stock price plus a global signal.

## 6.2 Outcome
The outcome of a NNM for the set data has to be **a limited set of possibilities**!! We will implement this as follows:

*The N-dimensional input is associated with an outcome classified by possibilities "Very good, good, neutral, bad, very bad" (values 2,1,0,-1,-2). We will apply this classification on the percentual increase that **will** happen in the near future*.

For instance, with p as the upcoming percentual change:
- if p > 2% then result is *very good*.
- if 2%  > p > 1% then *good*.
- if 1%  > p > -1% then *neutral*.
- if -1% > p > -2% then *bad*.
- if -2% > p then very bad.

Added to this we apply the logic that, if there's a decrease in price beyond the stop loss **before** there is a *good* increase, then we associate the outcom immediately with *bad*.

After the model is trained and used for predictions, you'll see that these predictions give probabilistic outcomes. You'll see this in the mypredictions.png after you run the project.