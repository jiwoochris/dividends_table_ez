import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests

url = 'https://www.investing.com/equities/starbucks-corp-dividends'

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

with urlopen(req) as doc:
    html = BeautifulSoup(doc, 'lxml')
    pgrr = html.find(class_='left first')
    # s = str(pgrr.a['href']).split('=')
    # last_page = s[-1]
    print(pgrr)