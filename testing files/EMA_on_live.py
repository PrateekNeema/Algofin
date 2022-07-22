import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
#Data viz
import plotly.graph_objs as go

#Data Source
import yfinance as yf


# import package
import pandas_datareader.data as web
# set start and end dates
# set start and end dates
start = datetime.datetime(2018, 2, 1)
end = datetime.datetime(2020, 2, 1)
# extract the daily closing price data
data_df = yf.download(tickers='HDFC.NS', period='1d', interval='1m')
data_df = pd.DataFrame({'Open': data_df['Open'],'High': data_df['High'],'Low': data_df['Low'],'Close':data_df['Close']})


#data_df[]
#data_df.columns = {'Close Price'}
# Create 20 days exponential moving average column
data_df['20_EMA'] = data_df['Close'].ewm(span=9, adjust=False).mean()
# Create 50 days exponential moving average column
data_df['50_EMA'] = data_df['Close'].ewm(span=26, adjust=False).mean()
# create a new column 'Signal' such that if 20-day EMA is greater   # than 50-day EMA then set Signal as 1 else 0

data_df['Signal'] = 0.0
data_df['Signal'] = np.where(data_df['20_EMA'] > data_df['50_EMA'], 1.0, 0.0)
# create a new column 'Position' which is a day-to-day difference of # the 'Signal' column
data_df['Position'] = data_df['Signal'].diff()
plt.figure(figsize=(20, 10))
# plot Close, short-term and long-term moving averages
data_df['Close'].plot(color='k', lw=1, label='Close')
data_df['20_EMA'].plot(color='b', lw=1, label='20-day EMA')
data_df['50_EMA'].plot(color='g', lw=1, label='50-day EMA')
print(data_df.columns.tolist())
"""
# plot 'buy' and 'sell' signals
plt.plot(data_df[data_df['Position'] == 1].index,data_df['20_EMA'][data_df['Position'] == 1],'^', markersize = 15, color = 'g', label = 'buy')
plt.plot(data_df[data_df['Position'] == -1].index,data_df['20_EMA'][data_df['Position'] == -1],'v', markersize = 15, color = 'r', label = 'sell')
plt.ylabel('Price in Rupees', fontsize=15)
plt.xlabel('Time', fontsize=15)
plt.title('ULTRACEMCO - EMA Crossover', fontsize=20)
plt.legend()
plt.grid()
plt.show()
"""
#declare figure
fig = go.Figure()

#Candlestick
fig.add_trace(go.Candlestick(x=data_df.index,
                open=data_df['Open'],
                high=data_df['High'],
                low=data_df['Low'],
                close=data_df['Close'], name = 'market data'))

# Add titles
fig.update_layout(
    title='HDFC live share price evolution',
    yaxis_title='Stock Price (Rupees per share)')

# X-Axes
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=15, label="15m", step="minute", stepmode="backward"),
            dict(count=45, label="45m", step="minute", stepmode="backward"),
            dict(count=1, label="HTD", step="hour", stepmode="todate"),
            dict(count=3, label="3h", step="hour", stepmode="backward"),
            dict(step="all")
        ])
    )
)

#Show
fig.show()
