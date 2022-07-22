import min_wkly
import pandas as pd

df = pd.read_csv('ind_nifty50list.csv')
df.iloc[:,2] += '.NS'

res_df = pd.DataFrame()

res_df['Ticker'] = df.iloc[:,2]

res_df['Net return'] = 0
res_df['No of trades'] = 0
res_df['+ve trades'] = 0
res_df['-ve trades'] = 0
res_df['Avg +ve trade'] = 0
res_df['Avg -ve trade'] = 0
res_df['Max +ve trade'] = 0
res_df['Max -ve trade'] = 0
res_df['Min +ve trade'] = 0
res_df['Min -ve trade'] = 0
res_df['return percent(2 months)'] = 0

res_df['Stock Name'] = df.iloc[:,0]

#print(res_df)

for i in range(0,len(res_df)):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(res_df.iloc[i,0])

    dict = min_wkly.weekly_15min_overlay(res_df.iloc[i,0])
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
    res_df.iloc[i,11] = dict['%return']

small_df = res_df[['Stock Name','Net return','return percent(2 months)']]

with pd.ExcelWriter(r"C:\Users\Admin\Documents\stock_data\Final_res_wkly_15.xlsx") as writer:
    res_df.to_excel(writer, sheet_name='result')
    small_df.to_excel(writer,sheet_name= 'concise results')


