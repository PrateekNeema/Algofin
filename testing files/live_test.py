# Raw Package
import numpy as np
import pandas as pd
import datetime
#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go

#Interval required 5 minutes
data = yf.download(tickers='ADANIGREEN.NS',start = datetime.datetime(2020, 3, 1),end=datetime.datetime(2022, 4, 1), interval='1d')
d1 = yf.download(tickers='PVR.NS', period='1mo', interval='15m')
#Print data
a = data.index[1]
b = data.index[2]
c = d1.index[5]

#print(a,b,c)




#print(c.date())

#print(a<c<b)
print(data)

