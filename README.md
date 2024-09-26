# Neural trading
1. [Introduction](1-introduction)
2. [Historical data](2-historical-data-)
    1. [yfinance](21-yfinance)
    2. [binance](22-binance)
3. [ML model tools](3-ml-model-tools)
    1. [stockpy](31-stockpy)
    2. [tensorflow](32-tensorflow)
4. [Stock indicator tools](4-stock-indicators-tools)
5. [Neural network model design](5-neural-network-model-design)
    1.  [Input](51-input)
    2.  [Outcome](51-outcome)


# 1. Introduction
In this project we try to apply neural network learning models to the field of the stock market (how original :)). To do so, we'll need:
- **historical stock data**,
- **Stock indicators**,
- **ML modeling tool**,
- Lastly and most importantly, a **conceptual base model for the neural network**.

Hereunder we'll give a short explanation about some of the choices we made regarding tools and model. You'll find each of these requirements in their respective helper file. These will be used in the main.py file.

# 2. Historical data
At the moment we're using **yfinance** because it's the easiest to use. Long term this is probably not the right choice for us, once we'll try building our own auto-trading bot. Then other platforms will be better, like **binance** or others [link](https://github.com/DaveSkender/Stock.Indicators/discussions/579).

## 2.1 yfinance
yfinance is open source :+1:. You can easily fetch historical data no prob. Simply install the requirements.txt and look at test_file.py

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
Stockpy is a python package offering a lot of tools for machine learning. Key point of interest of mine is neural networks. At the moment I stepped down from this tool because the last commit to the package was a year ago and I can't find much usefull documentation :-1:.
## 3.2 Tensorflow
Tensorflow however... is a very popular tool and it would seem very user-friendly :+1:.

# 4. Stock indicator tools
## stock-indicators
There's a variety of stock indicators, some of which we'll need for our neural network. How convenient that there's a python package called stock-indicators that holds the functions capable of calculating these indices on stock data.
Tool works with so-called quotes meh. To use it you'll need to have python duh, but also .NET. See [link](https://python.stockindicators.dev/guide/).

# 5. Neural network model design
## 5.1 Input
We'll use at this moment of writing the following as our N-dimensional input:
- a set of 5 concurrent MACD data points,
- combined with the respective trading volumes.
## 5.2 Outcome
One key part of neural networks is that you associate a certain input with an outcome. This outcome should belong to a **limited set of possibilities**!!

We will implement this as follows:
*A data point will be classified as either Very good, good, neutral, bad, very bad (values 2,1,0,-1,-2). The criteria is by looking a number n data points further in time and observing the percentual increase. This increase is then bucketted.
For instance (but this can be parametrized), with p as percentual change:
- if p > 2% then result is very good.
- if 2%  > p > 1% then good.
- if 1%  > p > -1% then neutral.
- if -1% > p > -2% then bad.
- if -2% > p then very bad.
