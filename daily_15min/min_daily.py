import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import yfinance as yf
from tabulate import tabulate
import warnings
warnings.filterwarnings('ignore')

#ticker = 'RELIANCE.NS'


def daily_15min_overlay(ticker):
    ser = yf.download(tickers=ticker,start = datetime.datetime(2022, 3, 2), interval='1d')

    df1 = pd.DataFrame({'Close daily': ser['Close']})

    short_window = 9
    long_window = 26
    short_window_name = '9_daily'
    long_window_name = '26_daily'

    # Create short exponential moving average column
    df1[short_window_name] = df1['Close daily'].ewm(span=short_window, adjust=False).mean()

    # Create a long exponential moving average column
    df1[long_window_name] = df1['Close daily'].ewm(span=long_window, adjust=False).mean()

    # create a new column 'Signal' such that if faster moving average is greater than slower moving average
    # then set Signal as 1 else 0.
    df1['gap_daily'] = 0
    df1.loc[df1[short_window_name] > df1[long_window_name],'gap_daily'] = 1.0
    df1.loc[df1[short_window_name] <= df1[long_window_name],'gap_daily'] = -1.0



    #print(df1)


    ###############################
    ser1 = yf.download(tickers=ticker, start = datetime.datetime(2022, 3, 2), interval='15m')

    df2 = pd.DataFrame({'Close_15min': ser1['Close']})

    short_window_name2 = '9_15min'
    long_window_name2 = '26_15min'

    # Create short exponential moving average column
    df2[short_window_name2] = df2['Close_15min'].ewm(span=short_window, adjust=False).mean()

    # Create a long exponential moving average column
    df2[long_window_name2] = df2['Close_15min'].ewm(span=long_window, adjust=False).mean()

    # create a new column 'Signal' such that if faster moving average is greater than slower moving average
    # then set Signal as 1 else 0.
    df2['gap_15min'] = 99
    df2.loc[df2[short_window_name2] > df2[long_window_name2],'gap_15min'] = 1.0
    df2.loc[df2[short_window_name2] <= df2[long_window_name2],'gap_15min'] = -1.0

    # create a new column 'Position' which is a day-to-day difference of the 'Signal' column.
    df2['action_15min'] = df2['gap_15min'].diff()
    df3_mini = df2[(df2['action_15min'] == 2) | (df2['action_15min'] == -2)]   ##=2 means buy and -2 means sell

    df3_mini['daily_status'] = 999

    for i in range(0,len(df3_mini)):   ###not optimiseed but okay for this much data
        for j in range(0,len(df1)-1):
            if df1.index[j] <= df3_mini.index[i].date() < df1.index[j+1]:
                df3_mini.iloc[i,5] = df1.iloc[j,3]


    df3_mini['Final call'] = 0
    df3_mini['Action'] = 'oo'

    for i in range(0,len(df3_mini)):

        if (df3_mini.iloc[i,4]+df3_mini.iloc[i,5]) == 3:
            df3_mini.iloc[i,6] = 1
            df3_mini.iloc[i,7] = 'Long'
        elif (df3_mini.iloc[i,4]+df3_mini.iloc[i,5]) == -1:
            df3_mini.iloc[i,6] = 0
            df3_mini.iloc[i, 7] = 'Neutral'
        elif (df3_mini.iloc[i, 4] + df3_mini.iloc[i, 5]) == -3:
            df3_mini.iloc[i, 6] = -1
            df3_mini.iloc[i, 7] = 'Short'
        elif (df3_mini.iloc[i, 4] + df3_mini.iloc[i, 5]) == 1:
            df3_mini.iloc[i, 6] = 0
            df3_mini.iloc[i, 7] = 'Neutral'


    df3_mini['Gains'] = 0

    for i in range(0,len(df3_mini)):

        if df3_mini.iloc[i,6] == 0 and df3_mini.iloc[i-1,6] == 1 and i!=0:   #long then now neutral
            df3_mini.iloc[i, 8] = df3_mini.iloc[i,0] - df3_mini.iloc[i-1,0]
        elif df3_mini.iloc[i,6] == 0 and df3_mini.iloc[i-1,6] == -1 and i!=0 :  # short then now neutral
            df3_mini.iloc[i, 8] = df3_mini.iloc[i-1, 0] - df3_mini.iloc[i, 0]


    df_gains = df3_mini[(df3_mini['Gains'] !=0)]
    df_only_gains = df_gains['Gains']
    stats_gains = df_gains['Gains'].describe()
    stats_gains['Net Gain'] = df_gains.sum()['Gains']

    print(df3_mini)
    #print(stats_gains)

    #df3_mini.to_csv('15min_weekly_overlay_new.csv')

    df3_mini.index = df3_mini.index.tz_localize(None)
    df_gains.index = df_gains.index.tz_localize(None)
    df_only_gains.index = df_only_gains.index.tz_localize(None)
    #df2.index = df2.index.tz_localize(None)

    with pd.ExcelWriter(r"C:\Users\Admin\Documents\stock_data\daily_15min\!" + ticker[0:(len(ticker)-3)] + ".xlsx") as writer:
        df3_mini.to_excel(writer, sheet_name='Calls')
        df_gains.to_excel(writer, sheet_name='Nonzero Gain rows')
        stats_gains.to_excel(writer, sheet_name='Stats')
        df1.to_excel(writer,sheet_name="daily_EMA_status")

    positive_gains = df_gains['Gains'][(df_gains['Gains'] > 0)]
    negative_gains = df_gains['Gains'][(df_gains['Gains'] < 0)]

    #print(positive_gains)

    result_dict = {'No of trades': stats_gains['count'],
                   'Positive trades': positive_gains.count(),
                   'Negative trades': negative_gains.count(),
                    'Average Postive trade' : positive_gains.mean(),
                   'Average Negative trade' : negative_gains.mean(),
                   'Max Postive trade': positive_gains.max(),
                   'Max Negative trade': negative_gains.min(),
                   'Min positive trade': positive_gains.min(),
                   'Min negative trade': negative_gains.max(),
                    'Net return' : stats_gains['Net Gain']
                   }

    return result_dict

#print(daily_15min_overlay('HINDUNILVR.NS'))






