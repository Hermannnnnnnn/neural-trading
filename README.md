# NEURAL-TRADING
This project is an on-the-fly try-out of the combination of 
- binance (REST API usage for downloading trade historical data) <- Nope became yfinance for the time being.
- tensorflow (to apply the neural network model for optimization)
- price indices (using these as input for the neural network model)
- some old thoughts on which factors correlate to movement of prices (just like people, there is the person itself determining behavioral aspects e.g. personality, character, stress etc. . This person however is influenced in some degree by society.)

# Historical data
## Binance API
We will be using the BINANCE API. Other platforms are possible as well, meh. This choice was based on the fact that a colleague of mine used BINANCE.
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
