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
In this project we try to apply neural network learning models to the field of the stock market (how original :blush:). To do so, we'll need:
- **historical stock data**,
- **Stock indicators**,
- **ML modeling tool**,
- **a model for the neural network**.

You'll find each of these requirements wrapped in its own *helper* module. They are called in the *main.py* which you simply need to run in order to run the project.

**Prerequisites to run this project**:
1. Have python installed (latest version to be safe)
2. Have .NET installed see [41-stock-indicators]
3. Run `python -m venv .venv` in the project folder
4. Activate the venv, for instance by executing `source .venv/bin/activate`
4. Run `pip install -r requirements.txt`

Hereunder we'll give a short explanation about some of the choices we made regarding tools and model. 

# 2. Historical data
At the moment we're using **yfinance** because it's the easiest to use. Long term this is probably not the right choice for us, once we decide to try building our own auto-trading bot. Then other platforms will be better, like **binance** or others [link](https://github.com/DaveSkender/Stock.Indicators/discussions/579).

## 2.1 yfinance
yfinance is open source, no registration required and very easy to fetch data :+1:. Simply install the requirements.txt and look at the helper module for its usage.

## 2.2 Binance
We first tried out binance, stepped away from it since you'll need an acount, deposit some money and get validated :-1:. In any case:

**Step I**
go to (https://www.binance.com/en)[https://www.binance.com/en].

**Step II**
sign up or log in.

**Step III**
wait until approved and deposit money :/


# 3. ML model tools
My computer is too slow :worried:. I want to use **tensorflow** since it's easy to implement and a very popular package. ML packages however are very large and so I've ordered a new computer, let's wait and see what it can do hohohoho.

## 3.1 Stockpy
We tried **Stockpy** first, after a quick google search. However, there seems to be little support left for this package since the last change was a year ago and I can't find much usefull documentation :-1:.
## 3.2 Tensorflow
Tensorflow however... is a very popular tool and it would seem very user-friendly :+1:. On (https://www.geeksforgeeks.org/implementing-neural-networks-using-tensorflow/)[https://www.geeksforgeeks.org/implementing-neural-networks-using-tensorflow/] you can find an easy example of applying neural networking to some data.

# 4. Stock indicator tools
Why re-invent the wheel right (I did that some years back for these indicators :disappointed:). Of course there are packages available that calculate stock indicators! We tried out **stock-indicators**, happy so far with the results.

## 4.1 stock-indicators
**Stock-indicators** works with so-called `quotes` meh. To use it you'll need to have python duh, but also .NET. See [link](https://python.stockindicators.dev/guide/).

# 5. Neural network model design
## 5.1 Input
We'll use at this moment of writing the following as our N-dimensional input:
- a set of N concurrent MACD data points,
- combined with the respective trading volumes.
## 5.2 Outcome
The outcome of a NNM is a **limited set of possibilities**!! We will implement this as follows:

*A data point will be classified as either Very good, good, neutral, bad, very bad (values 2,1,0,-1,-2). The criteria is by looking a number n data points further in time and observing the percentual increase. This increase is then bucketted.*

For instance (but this can be parametrized), with p as percentual change:
- if p > 2% then result is very good.
- if 2%  > p > 1% then good.
- if 1%  > p > -1% then neutral.
- if -1% > p > -2% then bad.
- if -2% > p then very bad.
