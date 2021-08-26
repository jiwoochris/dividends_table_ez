import yfinance as yf

samsung = yf.Ticker("005935.KS")
print(samsung.dividends)

hyundai = yf.Ticker("005387.KS")
print(hyundai.dividends)

ktng = yf.Ticker("033780.KS")
print(ktng.dividends)