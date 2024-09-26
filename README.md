# Overview
1. [Introduction](1-introduction)
2. [Fetching historical data - packages](2-fetching-historical-data-packages)
    1. [yfinance](21-yfinance)
    2. [binance](22-binance)

3. [ML model packages](3-ml-model-packages)
4. [Stock indicators](4-stock-indicators)
5. [Neural network model](5-neural-network-model)
    1.  [Bucketing](51-bucketing)
# 1. Introduction
In this project we try to apply neural network models on stock indicators. We use:
- **yfinance**, since its open source and very quickly set up.
- **tensorflow or stockpy** to apply the neural network model for optimization.
- **stock-indicators** for calculating, well, stock indicators.
- Lastly and most importantly, a **base model for the neural network**. Some correlation should exist between a future price movement and:
    - the degree of bull/bear market generally (SPY500 for example)
    - the degree of bull/bear market locally (the stock being processed)
    - the local behaviour of price movement (the last few data points)
    - the volumes traded and those points.


# 2. Fetching historical data - packages
At the moment we're using yfinance because it's the easiest to use. On this [link](https://github.com/DaveSkender/Stock.Indicators/discussions/579) you'll find a discussion about which tools are available.

## 2.1 yfinance
yfinance however is open source :+1:. You can easily fetch historical data no prob. Simply install the requirements.txt and look at test_file.py

## 2.2 Binance
To use the binance python package you'll need
Hereunder a short how-to to get the API token en username. You'll store these in de .env file (see .env_template for namegivings).
HOWEVER: you have to deposit some money and your account needs to be verified :-1:.

**Step I**
go to (https://www.binance.com/en)[https://www.binance.com/en] . Easy right :? ?

**Step II**
sign up or log in.

**Step III**
wait until approved and deposit money :/


# 3. ML model packages
## stockpy
Stockpy is a python package offering a lot of tools for machine learning. Key point of interest of mine is neural networks. Let's see if it works applying it to stock indicators.

# 4. Stock indicators
## stock-indicators
There's a variety of stock indicators. How convenient that there's a python package called stock-indicators that holds the functions capable of calculating these indices on stock data.

# 5. Neural network model
## 5.1 bucketing
One key part of neural networks is that you associate a certain input with an outcome. This outcome should belong to a **limited set of possibilities**!!

We will do this as follows:
*A data point will be classified as either Very good, good, neutral, bad, very bad. The criteria is by looking x data points further and classifying by percentual increase/decrease. For instance (but this can be parametrized), with x as percentual change:
- if x > 2% then result is very good.
- if 2%  > x > 1% then good.
- if 1%  > x > -1% then neutral.
- if -1% > x > -2% then bad.
- if -2% > x then very bad.
