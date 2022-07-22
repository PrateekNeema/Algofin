import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import yfinance as yf
from tabulate import tabulate
import warnings

warnings.filterwarnings('ignore')


class stock:

    def __init__(self, stk_ticker):
        self.ticker = stk_ticker
        self.main_df = pd.DataFrame()

    def EMA_strat(self, period, interval, short_window=9, long_window=26,layer_name = "A"):

        signal = 'Signal_'+ layer_name
        postion = 'Position_' + layer_name
        close = 'Close price_' + layer_name

        ser = yf.download(tickers=self.ticker, period=period, interval=interval)  # timeseries
        self.df_full = pd.DataFrame({'Open': ser['Open'], 'High': ser['High'], 'Low': ser['Low'], 'Close': ser['Close'],
                                     'Adj Close': ser['Adj Close'], 'Volume': ser['Volume']})
        self.df1 = pd.DataFrame({close: ser['Close']})

        short_window_name = str(short_window) + '_' + str(interval) + '_' + layer_name
        long_window_name = str(long_window) + '_' + str(interval) + '_' + layer_name

        # Create short exponential moving average column
        self.df1[short_window_name] = self.df1[close].ewm(span=short_window, adjust=False).mean()

        # Create a long exponential moving average column
        self.df1[long_window_name] = self.df1[close].ewm(span=long_window, adjust=False).mean()

        # create a new column 'Signal' such that if faster moving average is greater than slower moving average
        # then set Signal as 1 else 0.
        self.df1[signal] = 0.0
        self.df1[signal] = np.where(self.df1[short_window_name] > self.df1[long_window_name], 1.0, 0.0)

        # create a new column 'Position' which is a day-to-day difference of the 'Signal' column.
        self.df1[postion] = self.df1[signal].diff()
        self.df_EMA_actions = self.df1[(self.df1[postion] == 1) | (self.df1[postion] == -1)]

        print(self.df_EMA_actions)

    # def get_EMA_profits(self, buysell=True, sellbuy=True):
    #
    #     self.df_EMA_actions['Buy/Sell Pair'] = 0
    #     self.df_EMA_actions['Sell/Buy Pair'] = 0
    #
    #     for i in range(0, len(self.df_EMA_actions)):
    #
    #         if buysell:
    #             if self.df_EMA_actions.iloc[i, 4] == -1:  ##buy thensell
    #                 self.df_EMA_actions.iloc[i, 5] = self.df_EMA_actions.iloc[i, 0] - self.df_EMA_actions.iloc[i - 1, 0]
    #
    #         if sellbuy:
    #             if self.df_EMA_actions.iloc[i, 4] == 1 and i != 0:  ##sell then buy
    #                 self.df_EMA_actions.iloc[i, 6] = self.df_EMA_actions.iloc[i-1, 0] - self.df_EMA_actions.iloc[i, 0]
    #
    #     df_buysell = self.df_EMA_actions[(self.df1['Position'] == -1)]
    #     print(df_buysell.describe())
    #
    #     df_sellbuy = self.df_EMA_actions[(self.df1['Position'] == 1)]
    #     print(df_sellbuy.describe())
    #
    #     print(tabulate(self.df_EMA_actions, headers='keys', tablefmt='psql'))


def performace_calc(df):
    profit = df['Buy/Sell Pair'].sum() + df['Sell/Buy Pair'].sum()
    print("Profit : Rs " + str(profit))


HDFC = stock('TATAMOTORS.NS')
HDFC.EMA_strat(period='10y', interval='1wk', short_window=9, long_window=26,layer_name='weekly')
HDFC.EMA_strat(period='10y', interval='1d', short_window=9, long_window=26,layer_name='daily')

print("Done")
#performace_calc(HDFC.df_EMA_actions)
