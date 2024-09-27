from stock_indicators import Quote, indicators


class my_indicators:

    def __init__(self, df_prices) -> None:
        self.df_prices = df_prices
        self.quotes_list = [
                            Quote(d,o,h,l,c,v) 
                            for d,o,h,l,c,v 
                            in zip(df_prices['Date'], df_prices['Open'], df_prices['High'], df_prices['Low'], df_prices['Close'], df_prices['Volume'])
                            ]
        
    def gimme_macd(self, fast_periods=12, slow_periods=26, signal_periods=9):
        self.df_prices[f'macd_{fast_periods}_{slow_periods}_{signal_periods}'] = [x.macd for x in indicators.get_macd(self.quotes_list, fast_periods=fast_periods, slow_periods=slow_periods, signal_periods=signal_periods)]
