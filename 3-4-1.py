from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

sec = pdr.get_data_yahoo('005930.KS', start = '2018-05-04')
msft = pdr.get_data_yahoo('MSFT', start = '2018-05-04')
a = pdr.get_data_yahoo('MSFT', start = '2018-05-04')
b = pdr.get_data_yahoo('sbux', start = '2018-05-04')
c = pdr.get_data_yahoo('ba', start = '2018-05-04')
d = pdr.get_data_yahoo('o', start = '2018-05-04')


print(sec.head(10))
print(msft.tail(10))

tmp_msft = msft.drop(columns = 'Volume')
print(tmp_msft.tail())

print(sec.index)
print(sec.columns)

import matplotlib.pyplot as plt

plt.plot(sec.index, sec.Close, 'b', label = 'Samsung Electronics')
plt.plot(msft.index, msft.Close, 'r--', label = 'Microsoft')
plt.legend(loc = 'best')
plt.show()

sec_dpc = (sec['Close'] / sec['Close'].shift(1) - 1) * 100
sec_dpc.iloc[0] = 0
plt.hist(sec_dpc, bins = 18)
plt.grid(True)
plt.show()
print(sec_dpc.describe())

sec_dpc_cs = sec_dpc.cumsum()
print(sec_dpc_cs)

msft_dpc = (msft['Close'] / msft['Close'].shift(1) - 1) * 100
msft_dpc.iloc[0] = 0
msft_dpc_cs = msft_dpc.cumsum()
print(msft_dpc.head())

plt.plot(sec.index, sec_dpc_cs, 'b', label = 'Samsung Electronics')
plt.plot(msft.index, msft_dpc_cs, 'r--', label = 'Microsoft')
plt.ylabel('Change %')
plt.grid(True)
plt.legend(loc = 'best')
plt.show()