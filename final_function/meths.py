import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import yfinance as yf
from tabulate import tabulate
import warnings
warnings.filterwarnings('ignore')



def ema_two_overlay(ticker,
                         per1 = '20y',
                         int1 = '1wk',
                         short1 = 9,
                         long1 = 26,
                         morethan2months = False,
                         int2 = '15m',
                         per2 = '1mo',
                         start2 = datetime.datetime(2022, 3, 10),
                         short2 = 9,
                         long2 = 26,
                        path_for_file = r"C:\Users\Admin\Documents\stock_data"):
    ser = yf.download(tickers=ticker, period = per1, interval=int1)   #period = '10y'

    close1 = 'Close ' + str(int1)
    gap1 = 'gap ' + str(int1)

    df1 = pd.DataFrame({close1: ser['Close']})

    short_window = short1
    long_window = long1
    short_window_name = str(short1) + '_'+ str(int1)
    long_window_name = str(long1) + '_'+ str(int1)

    # Create short exponential moving average column
    df1[short_window_name] = df1[close1].ewm(span=short_window, adjust=False).mean()

    # Create a long exponential moving average column
    df1[long_window_name] = df1[close1].ewm(span=long_window, adjust=False).mean()

    # create a new column 'Signal' such that if faster moving average is greater than slower moving average
    # then set Signal as 1 else 0.
    df1[gap1] = 99
    df1.loc[df1[short_window_name] > df1[long_window_name],gap1] = 1.0
    df1.loc[df1[short_window_name] <= df1[long_window_name],gap1] = -1.0

    #print(df1)


    ###############################
    if morethan2months:
        ser1 = yf.download(tickers=ticker, period=per2, interval=int2)
    else:
        ser1 = yf.download(tickers=ticker, start= start2, interval=int2)

    close2 = 'Close ' + str(int2)
    gap2 = 'gap ' + str(int2)
    action2 = 'action '+ str(int2)

    df2 = pd.DataFrame({close2: ser1['Close']})

    short_window2 = short2
    long_window2 = long2
    short_window_name2 = str(short2) + '_' + str(int2)
    long_window_name2 = str(long2) + '_' + str(int2)

    # Create short exponential moving average column
    df2[short_window_name2] = df2[close2].ewm(span=short_window2, adjust=False).mean()

    # Create a long exponential moving average column
    df2[long_window_name2] = df2[close2].ewm(span=long_window2, adjust=False).mean()

    # create a new column 'Signal' such that if faster moving average is greater than slower moving average
    # then set Signal as 1 else 0.
    df2[gap2] = 99
    df2.loc[df2[short_window_name2] > df2[long_window_name2],gap2] = 1.0
    df2.loc[df2[short_window_name2] <= df2[long_window_name2],gap2] = -1.0

    # create a new column 'Position' which is a day-to-day difference of the 'Signal' column.
    df2[action2] = df2[gap2].diff()

    df2.iloc[0:50,4] = 0

    #print("#############################")
    #print(df2.columns.tolist())

    df3_mini = df2[(df2[action2] == 2) | (df2[action2] == -2)]   ##=2 means buy and -2 means sell

    df3_mini[str(int1)+'_status'] = 999

    for i in range(0,len(df3_mini)):   ###not optimiseed but okay for this much data
        for j in range(0,len(df1)-1):
            if df1.index[j] <= df3_mini.index[i].date() < df1.index[j+1]:
                df3_mini.iloc[i,5] = df1.iloc[j,3]



    df3_mini['Final call'] = 0
    df3_mini['Final Action'] = 'oo'

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

        if df3_mini.iloc[i,6] == 0 and df3_mini.iloc[i-1,6] == 1 and i!=0 :   #long then now neutral
            df3_mini.iloc[i, 8] = df3_mini.iloc[i,0] - df3_mini.iloc[i-1,0]
        elif df3_mini.iloc[i,6] == 0 and df3_mini.iloc[i-1,6] == -1 and i!=0 :  # short then now neutral
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

    df_gains_and_dates = pd.DataFrame()
    df_gains_and_dates['Gains'] = df_gains['Gains']
    df_gains_and_dates['Date,time'] = df_gains.index
    #print(df_gains_and_dates)
    df_grouped_by_months = df_gains_and_dates.groupby(pd.Grouper(key='Date,time', axis=0,freq='M')).sum()
    #print(df_grouped_by_months)

    df_gains['Date,time'] = df_gains.index

    df_grouped_by_months['avg close'] = (df_gains.groupby(pd.Grouper(key='Date,time', axis=0,freq='M')).mean())[close2]
    df_grouped_by_months['%gain'] = (df_grouped_by_months['Gains'])/(df_gains.groupby(pd.Grouper(key='Date,time', axis=0,freq='M')).mean())[close2]

    #print(df_grouped_by_months)

    #print(df3_mini)
    #print(stats_gains)

    #df3_mini.to_csv('15min_weekly_overlay_new.csv')

    #print(df3_mini.index)

    df3_mini.index = df3_mini.index.tz_localize(None)
    df_gains.index = df_gains.index.tz_localize(None)
    df_only_gains.index = df_only_gains.index.tz_localize(None)
    df_grouped_by_months.index = df_grouped_by_months.index.tz_localize(None)
    #df2.index = df2.index.tz_localize(None)

    with pd.ExcelWriter(path_for_file + "\$"+ str(int1) +"_"+str(int2) +"\$"+ ticker+".xlsx") as writer:
        df3_mini.to_excel(writer, sheet_name='Calls')
        df_gains.to_excel(writer, sheet_name='Nonzero Gain rows')
        stats_gains.to_excel(writer, sheet_name='Stats')
        df_grouped_by_months.to_excel(writer,sheet_name='Grouped by Months')
        #df1.to_excel(writer,sheet_name="weekly_EMA_status")
        #df2.to_excel(writer,sheet_name="all 15min data")

    positive_gains = df_gains['Gains'][(df_gains['Gains'] > 0)]
    negative_gains = df_gains['Gains'][(df_gains['Gains'] < 0)]


    # print(positive_gains)

    ret_percent = (stats_gains['Net Gain'])/(df3_mini[close2].mean())

    result_dict = {'No of trades': stats_gains['count'],
                   'Positive trades': positive_gains.count(),
                   'Negative trades': negative_gains.count(),
                   'Average Postive trade': positive_gains.mean(),
                   'Average Negative trade': negative_gains.mean(),
                   'Max Postive trade': positive_gains.max(),
                   'Max Negative trade': negative_gains.min(),
                   'Min positive trade': positive_gains.min(),
                   'Min negative trade': negative_gains.max(),
                   'Net return': stats_gains['Net Gain'],
                   '%return' : ret_percent
                   }


    return result_dict,df_grouped_by_months

# print(ema_two_overlay(ticker='RELIANCE.NS', per1 = '20y',
#                          int1 = '1wk',
#                          short1 = 9,
#                          long1 = 26,
#                          morethan2months = True,
#                          int2 = '1d',
#                          per2 = '20y',
#                          start2 = datetime.datetime(2022, 3, 10),
#                          short2 = 9,
#                          long2 = 26,
#                         path_for_file = r"C:\Users\Admin\Documents\stock_data"))










