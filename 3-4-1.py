# from pandas_datareader import data as pdr
import yfinance as yf
# yf.pdr_override()
import pprint

msft = yf.Ticker("PEP")

# pprint.pprint(msft.info)

print(msft.info['sector'])
print(msft.info['industry'])
print(msft.info['longName'])
print(msft.info['currentPrice'])


print(msft.dividends[-12:].index)

s.unique()