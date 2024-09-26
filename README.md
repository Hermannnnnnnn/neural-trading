# NEURAL-TRADING
In this project we try to apply neural network models on stock indicators. We use:
- **yfinance**, since its open source and very quickly set up.
- **tensorflow or stockpy** to apply the neural network model for optimization.
- **stock-indicators** for calculating, well, stock indicators.
- Lastly and most importantly, a **base model for the neural network**. Some correlation should exist between a future price movement and:
    - the degree of bull/bear market generally (SPY500 for example)
    - the degree of bull/bear market locally (the stock being processed)
    - the local behaviour of price movement (the last few data points)
    - the volumes traded and those points.


# Historical data
## Binance API
Hereunder a short how-to to get the API token en username. You'll store these in de .env file (see .env_template for namegivings).
HOWEVER: you have to deposit some money and your account needs to be verified :(

### Step I: go to (https://www.binance.com/en)[https://www.binance.com/en] . Easy right :? ?

### Step II: sign up or log in.

### Step III: wait until approved and deposit money :/

## yfinance API
yfinance however is open source :). You can easily fetch historical data no prob. Simply install the requirements.txt and look at test_file.py

# ML model
## stockpy
Stockpy is a python package offering a lot of tools for machine learning. Key point of interest of mine is neural networks. Let's see if it works applying it to stock indicators.

# Stock indicators
## stock-indicators
There's a variety of stock indicators. How convenient that there's a python package called stock-indicators that holds the functions capable of calculating these indices on stock data.

# Neural network model
## bucketing
One key part of neural networks is that you associate a certain input with an outcome. This outcome should belong to a **limited set of possibilities**!!

We will do this as follows:
*A data point will be classified as either Very good, good, neutral, bad, very bad. The criteria is by looking x data points further and classifying by percentual increase/decrease. For instance (but this can be parametrized), with x as percentual change:
- if x > 2% then result is very good.
- if 2%  > x > 1% then good.
- if 1%  > x > -1% then neutral.
- if -1% > x > -2% then bad.
- if -2% > x then very bad.


# Notes
- see https://github.com/DaveSkender/Stock.Indicators/discussions/579 for links to platforms that offer API accesses.