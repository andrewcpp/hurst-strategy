import pandas as pd
import yfinance as yf

import random
from cmath import nan

# Acquiring random symbols to test
# Source: https://www.nasdaq.com/market-activity/stocks/screener

'''
nano = pd.read_csv('data/nasdaq_nano.csv')
micro = pd.read_csv('data/nasdaq_micro.csv')
small = pd.read_csv('data/nasdaq_small.csv')
'''
medium = pd.read_csv('data/nasdaq_medium.csv')
large = pd.read_csv('data/nasdaq_large.csv')
mega = pd.read_csv('data/nasdaq_mega.csv')

'''
nano = nano['Symbol'].tolist()
micro = micro['Symbol'].tolist()
small = small['Symbol'].tolist()
'''
medium = medium['Symbol'].tolist()
large = large['Symbol'].tolist()
mega = mega['Symbol'].tolist()

'''
random.shuffle(nano)
random.shuffle(micro)
random.shuffle(small)
random.shuffle(medium)
random.shuffle(large)
random.shuffle(mega)

nano = nano[:10]
micro = micro[:10]
small = small[:20]
medium = medium[:50]
large = large[:50]
mega = mega[:40]
'''

symbols = medium
symbols.extend(large)
symbols.extend(mega)
symbols.append('MANU')

for s in symbols:
  yf_data = yf.download(s, start='2021-01-01', end='2021-12-31')
  yf_data = yf_data.reset_index()
  yf_data = yf_data.drop(columns=['Open', 'High', 'Low', 'Adj Close', 'Volume'])
  yf_data.to_csv('stocks/' + s + '.csv')