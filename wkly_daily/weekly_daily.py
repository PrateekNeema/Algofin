import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import yfinance as yf
from tabulate import tabulate
import warnings
warnings.filterwarnings('ignore')

#ticker = 'RELIANCE.NS'

def daily_weekly_overlay(ticker):

    ser = yf.download(tickers=ticker, period='20y', interval='1wk')

    df1 = pd.DataFrame({'Close wkly': ser['Close']})

    short_window = 9
    long_window = 26
    short_window_name = '9_wkly'
    long_window_name = '26_wkly'

    # Create short exponential moving average column
    df1[short_window_name] = df1['Close wkly'].ewm(span=short_window, adjust=False).mean()

    # Create a long exponential moving average column
    df1[long_window_name] = df1['Close wkly'].ewm(span=long_window, adjust=False).mean()

    # create a new column 'Signal' such that if faster moving average is greater than slower moving average
    # then set Signal as 1 else 0.
    df1['gap_wkly'] = 99
    df1.loc[df1[short_window_name] > df1[long_window_name],'gap_wkly'] = 1.0
    df1.loc[df1[short_window_name] <= df1[long_window_name],'gap_wkly'] = -1.0

    print(df1)


    ###############################
    ser1 = yf.download(tickers=ticker, period='20y', interval='1d')

    df2 = pd.DataFrame({'Close_daily': ser1['Close']})

    short_window_name2 = '9_daily'
    long_window_name2 = '26_daily'

    # Create short exponential moving average column
    df2[short_window_name2] = df2['Close_daily'].ewm(span=short_window, adjust=False).mean()

    # Create a long exponential moving average column
    df2[long_window_name2] = df2['Close_daily'].ewm(span=long_window, adjust=False).mean()

    # create a new column 'Signal' such that if faster moving average is greater than slower moving average
    # then set Signal as 1 else 0.
    df2['gap_daily'] = 99
    df2.loc[df2[short_window_name2] > df2[long_window_name2],'gap_daily'] = 1.0
    df2.loc[df2[short_window_name2] <= df2[long_window_name2],'gap_daily'] = -1.0

    # create a new column 'Position' which is a day-to-day difference of the 'Signal' column.
    df2['action_dly'] = df2['gap_daily'].diff()
    df3_mini = df2[(df2['action_dly'] == 2) | (df2['action_dly'] == -2)]   ##=2 means buy and -2 means sell

    df3_mini['weekly_status'] = 999

    for i in range(0,len(df3_mini)):   ###not optimiseed but okay for this much data
        for j in range(0,len(df1)-1):
            if df1.index[j] <= df3_mini.index[i] < df1.index[j+1]:
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

        if df3_mini.iloc[i,6] == 0 and df3_mini.iloc[i-1,6] == 1 :   #long then now neutral
            df3_mini.iloc[i, 8] = df3_mini.iloc[i,0] - df3_mini.iloc[i-1,0]
        elif df3_mini.iloc[i,6] == 0 and df3_mini.iloc[i-1,6] == -1 :  # short then now neutral
            df3_mini.iloc[i, 8] = df3_mini.iloc[i-1, 0] - df3_mini.iloc[i, 0]

    df_gains = df3_mini[(df3_mini['Gains'] !=0)]
    df_only_gains = df_gains['Gains']
    stats_gains = df_gains['Gains'].describe()
    stats_gains['Net Gain'] = df_gains.sum()['Gains']

    # req_stats = {'No of trades(pairs)': stats_gains['count'],
    #              'Positive trades': df_only_gains[(df_only_gains['Gains'] > 0)].count(),
    #              'Negative trades': df_only_gains[(df_only_gains['Gains'] > 0)].count(),
    #              'Max positive trade' : 0,
    #              'Max '}

    print(df3_mini)
    print(stats_gains)

    #df3_mini.to_csv('daily_weekly_overlay_new.csv')

    with pd.ExcelWriter(ticker+'_dly_wkly_overlay.xlsx') as writer:
        df3_mini.to_excel(writer, sheet_name='Calls')
        df_gains.to_excel(writer, sheet_name='Nonzero Gain rows')
        stats_gains.to_excel(writer, sheet_name='Stats')
        df1.to_excel(writer, sheet_name="weekly_EMA_status")










