import quandl

tsla = quandl.get('WIKI/TSLA', start_date = "2010-06-29", end_date = "2018-03-27")

print(tsla)


