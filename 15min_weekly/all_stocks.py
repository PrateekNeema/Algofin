import pandas as pd

df = pd.read_csv('ind_nifty50list.csv')

df.iloc[:,2] += '.NS'

print(df.iloc[:,0:3])