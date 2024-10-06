#  Neural trading
1. [Introduction](1-introduction)
2. [Running the project](2-running-the-project)
    1. [Prerequisites](21-prerequisites)
    2. [Running the project](22-run-the-project)
3. [Historical data](3-historical-data)
    1. [yfinance](31-yfinance)
    2. [binance](32-binance)
4. [ML model tools](4-ml-model-tools)
    1. [stockpy](41-stockpy)
    2. [tensorflow](42-tensorflow)
5. [Stock indicator tools](5-stock-indicator-tools)
    1. [Stock-indicators](51-stock-indicators)
6. [Neural network model design](6-neural-network-model-design)
    1.  [Input](61-input)
    2.  [Outcome](62-outcome)


# 1. Introduction
In this project we try to apply neural network learning models to the field of the stock market (how original :blush:). To do so, we'll need:
- **historical stock data**,
- **Stock indicators**,
- **ML modeling tool**,
- **a model for the neural network**. 

How convenient that there are python packages enabling these requirements!!

# 2. Running the project
## 2.1 Prerequisites
1. Have python installed (latest version should be enough lol)
2. Have .NET installed (see [4.1 Stock-indicators](#41-stock-indicators))
3. Run `python -m venv .venv` in the project folder
4. Activate the venv by executing `source .venv/bin/activate` for linux or `source .venv/bin/activate.ps1` for windows
4. Run `pip install -r requirements.txt`

## 2.2 Run the project

At the moment, you run the project by 
- running the *main.py* file. This will make all the data transformations run.
- For visualising the *predictions* you run the *draw_results.py*, which will generate a picture in *results/pictures/mypredictions.png*.
 
The *main.py* contains three important parts:
1. In part I we set **variables** specifying which historical data we'll take and how the macd will be taken.
2. In part II the **data transformations** happen. First we preprocess the raw stock trade data, then we feed it into our machine learning set up. This machine learning does two things, based on the feed:
    - first it will try to find the *best* **hyperparameters** setting for the neural network (how many layers, how many nodes per layer, which activation function).
    - Then, with these hyperparameters, the *best* **weights** are calculated ie the neural network model itself will be optimized. 
3. Lastly, in part III, we download some new data, feed it into our neural network which gives *predictions* for price movements.

The *draw_results.py* builds upon part III. Herein we generate a figure showing three things:
1. the prices in function of time.
2. Bins: these are classifications of future price movements. A value 0 would mean a movement that indicates a bad opportunity to buy. The value 1 (or 2, 3,... for higer order of classifications) would mean a good opportunity to buy.

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
Tensorflow however... **is a very popular tool** and it would seem very user-friendly :+1:. On [this link](https://www.geeksforgeeks.org/implementing-neural-networks-using-tensorflow/) you can find an easy example of applying neural networking to some data.

# 5. Stock indicator tools
Why re-invent the wheel right (I did that some years back for these indicators :disappointed:). Of course there are packages available that calculate stock indicators! We tried out **stock-indicators**, happy so far with the results.

## 5.1 stock-indicators
**Stock-indicators** works with so-called `quotes` meh. To use it you'll need to have python duh, but also .NET. [See link](https://python.stockindicators.dev/guide/).

# 6. Neural network model design
## 6.1 Input
We'll use at this moment of writing the following as our N-dimensional input:
- a set of N concurrent MACD data points,
- combined with the respective trading volumes.

So this means that we postulate that not only the MACD signal and volume traded are correlated with the price movement, but also the MACD signals and volumes leading up to the moment.

## 6.2 Outcome
The outcome of a NNM is supposed to be a **limited set of possibilities**!! We will implement this as follows:

*The N-dimensional input is associated with an outcome classified by possibilities "Very good, good, neutral, bad, very bad" (values 2,1,0,-1,-2). We will apply this classification on the percentual increase that **will** happen in the near future*.

For instance, with p as the upcoming percentual change:
- if p > 2% then result is *very good*.
- if 2%  > p > 1% then *good*.
- if 1%  > p > -1% then *neutral*.
- if -1% > p > -2% then *bad*.
- if -2% > p then very bad.
