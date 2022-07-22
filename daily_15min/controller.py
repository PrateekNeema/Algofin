import min_daily
import pandas as pd

res_df = pd.DataFrame()

res_df['Stock Name'] = ['RELIANCE.NS','TCS.NS','HDFC.NS','INFY.NS','HINDUNILVR.NS','ADANIGREEN.NS']

res_df['Net return'] = 0
res_df['No of trades'] = 0
res_df['Positive trades'] = 0
res_df['Negative trades'] = 0
res_df['Average Postive trade'] = 0
res_df['Average Negative trade'] = 0
res_df['Max Postive trade'] = 0
res_df['Max Negative trade'] = 0
res_df['Min positive trade'] = 0
res_df['Min negative trade'] = 0

for i in range(0,len(res_df)):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(res_df['Stock Name'][i])

    dict = min_daily.daily_15min_overlay(res_df.iloc[i,0])
    res_df.iloc[i,1] = dict['Net return']
    res_df.iloc[i,2] = dict['No of trades']
    res_df.iloc[i,3] = dict['Positive trades']
    res_df.iloc[i,4] = dict['Negative trades']
    res_df.iloc[i,5] =dict['Average Postive trade']
    res_df.iloc[i,6] = dict['Average Negative trade']
    res_df.iloc[i,7] = dict['Max Postive trade']
    res_df.iloc[i,8] = dict['Max Negative trade']
    res_df.iloc[i,9] = dict['Min positive trade']
    res_df.iloc[i,10] = dict['Min negative trade']

with pd.ExcelWriter(r"C:\Users\Admin\Documents\stock_data\Final_res.xlsx") as writer:
    res_df.to_excel(writer, sheet_name='result')


