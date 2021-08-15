# from pandas_datareader import data as pdr
import yfinance as yf
import datetime
import pandas as pd
# yf.pdr_override()
import pprint

msft = yf.Ticker("APPL")

# pprint.pprint(msft.info)
print(msft.info['longName'])

print(msft.info)

if msft.info['sector'] == None:
    pprint.pprint(msft.info)
print(msft.info['sector'])
print(msft.info['industry'])

print(msft.info['currentPrice'])


print(msft.dividends[-12:].index)

s = pd.Series(msft.dividends[-12:].index)
print(s.dt.month.unique())

# print(str(msft.dividends[-1]))

print(msft.dividends[-1])

print(pd.Series(msft.dividends[-12:].index).dt.month.nunique())

print(pd.Series(msft.dividends[-4:].index).dt.month.unique())

print(set(pd.Series(msft.dividends[-12:].index).dt.month))


# s.unique()