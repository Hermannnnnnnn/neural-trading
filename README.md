# Neural trading
1. [Introduction](1-introduction)
2. [Historical data](2-historical-data-)
    1. [yfinance](21-yfinance)
    2. [binance](22-binance)
3. [ML model tools](3-ml-model-tools)
    1. [stockpy](31-stockpy)
    2. [tensorflow](32-tensorflow)
4. [Stock indicator tools](4-stock-indicators-tools)
5. [Neural network model](5-neural-network-model)
    1.  [Input](51-input)
    2.  [Outcome](51-outcome)


# 1. Introduction
In this project we try to apply neural network models on stock indicators. For this we need:
- **historical stock data**,
- **Stock indicators**,
- **ML modeling tool**,
- Lastly and most importantly, a **conceptual base model for the neural network**.

Hereunder we'll give a short explanation about some of the choices we made regarding tools and model.

# 2. Historical data
At the moment we're using **yfinance** because it's the easiest to use. Long term this is probably not the right choice for us, once we'll try building our own auto-trading bot. Then other platforms will be better, like **binance** or others [link](https://github.com/DaveSkender/Stock.Indicators/discussions/579).

## 2.1 yfinance
yfinance however is open source :+1:. You can easily fetch historical data no prob. Simply install the requirements.txt and look at test_file.py

## 2.2 Binance
We tried out binance, stepped away from it since you'll need an acount, deposit some money and get validated :-1:. In any case:

**Step I**
go to (https://www.binance.com/en)[https://www.binance.com/en].

**Step II**
sign up or log in.

**Step III**
wait until approved and deposit money :/


# 3. ML model tools
## 3.1 Stockpy
Stockpy is a python package offering a lot of tools for machine learning. Key point of interest of mine is neural networks. Let's see if it works applying it to stock indicators.
## 3.2 Tensorflow
to explore...

# 4. Stock indicator tools
## stock-indicators
There's a variety of stock indicators. How convenient that there's a python package called stock-indicators that holds the functions capable of calculating these indices on stock data.
Tool works with so-called quotes meh. To use it you'll need to have python duh, but also .NET. See [link](https://python.stockindicators.dev/guide/).

# 5. Neural network model
## 5.1 Input
We'll use at this moment of writing the following as our N-dimensional input:
- a set of 5 concurrent MACD data points,
- combined with the respective trading volumes.
## 5.2 Outcome
One key part of neural networks is that you associate a certain input with an outcome. This outcome should belong to a **limited set of possibilities**!!

We will do this as follows:
*A data point will be classified as either Very good, good, neutral, bad, very bad. The criteria is by looking N data points further and classifying by percentual increase/decrease. For instance (but this can be parametrized), with x as percentual change:
- if x > 2% then result is very good.
- if 2%  > x > 1% then good.
- if 1%  > x > -1% then neutral.
- if -1% > x > -2% then bad.
- if -2% > x then very bad.
