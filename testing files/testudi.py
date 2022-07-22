import datetime
import pandas as pd

a = pd.DataFrame([0,0])
a['dates'] = [datetime.datetime(1995, 3, 10),datetime.datetime(2022, 3, 10)]

print(a.groupby(pd.Grouper(key='dates', axis=0,freq='M')).sum())