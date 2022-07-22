import yfinance as yf

relian = yf.Ticker('RELIANCE.NS')

# get stock info
info = relian.info

# get historical market data
hist = relian.history(period="max")

# show actions (dividends, splits)
actions = relian.actions

# show dividends
div = relian.dividends

# show splits
splits = relian.splits

# show financials
fin = relian.financials
quart = relian.quarterly_financials

# show major holders
major_holders = relian.major_holders

# show institutional holders
inst_holders = relian.institutional_holders

# show balance sheet
balance_sheet = relian.balance_sheet
quart_bal_sheet = relian.quarterly_balance_sheet

# show cashflow
cahsflow = relian.cashflow
quart_cash = relian.quarterly_cashflow

# show earnings
earnings = relian.earnings
quart_earn = relian.quarterly_earnings

# show sustainability
sus = relian.sustainability

# show analysts recommendations
rec = relian.recommendations

# show next event (earnings, etc)
calen = relian.calendar

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
isin = relian.isin

# show options expirations
opts = relian.options

# show news
news = relian.news

# get option chain for specific expiration
opt = relian.option_chain('YYYY-MM-DD')
# data available via: opt.calls, opt.puts