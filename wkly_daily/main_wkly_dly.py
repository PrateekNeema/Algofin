import weekly_daily

companies = ['RELIANCE.NS','TCS.NS','HDFC.NS','INFY.NS','HINDUNILVR.NS','ADANIGREEN.NS']


for company in companies:
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(company)
    weekly_daily.daily_weekly_overlay(company)