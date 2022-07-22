from final_function import meths
import pandas as pd
import datetime

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

months_df = pd.DataFrame(columns=res_df['Stock Name'].tolist())

a = pd.DataFrame()
a['val'] = [0,0]
a.index = [datetime.datetime(1995, 3, 10),datetime.datetime(2022, 3, 10)]
a['dates'] = a.index
months_df['test'] = (a.groupby(pd.Grouper(key='dates', axis=0,freq='M')).sum())['val']


##################

print(months_df)

for i in range(0,len(res_df)):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(res_df.iloc[i,0])

    dict,df_gr = meths.ema_two_overlay(ticker=res_df.iloc[i,0], per1 = '20y',
                         int1 = '1wk',
                         short1 = 9,
                         long1 = 26,
                         morethan2months = True,
                         int2 = '1d',
                         per2 = '20y',
                         start2 = datetime.datetime(2022, 3, 10),
                         short2 = 9,
                         long2 = 26,
                        path_for_file = r"C:\Users\Admin\Documents\stock_data")
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

    months_df[res_df.iloc[i,12]] = df_gr['%gain']



small_df = res_df[['Stock Name','Net return','return percent(2 months)']]

#print(months_df)


with pd.ExcelWriter(r"C:\Users\Admin\Documents\stock_data\top50_wkly_daily.xlsx") as writer:
    res_df.to_excel(writer, sheet_name='result')
    small_df.to_excel(writer,sheet_name= 'concise results')
    months_df.to_excel(writer,sheet_name= 'Months results')


