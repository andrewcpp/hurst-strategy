import numpy as np
import pandas as pd

import yfinance as yf

'''
Simply long-term momentum strategy using formation period.
Looks back to a certain period of time and calculates returns.
Returns top five performing stocks. Can modify code to return top n stocks.
'''

# Return closing price in top_five
def sort_top_five(element):
  return element[1]

def top_five():
  nasdaq_data = pd.read_csv('data/nasdaq_large.csv')
  ticker_list = nasdaq_data['Symbol'].tolist()

  minint = float('-inf')
  top_five = [('TICKER', minint), ('TICKER', minint), ('TICKER', minint), ('TICKER', minint), ('TICKER', minint)]

  for ticker in ticker_list:
    yf_data = yf.download(ticker, start='2019-07-01', end='2019-12-31')

    if (len(yf_data['Close']) == 0):
      continue

    returnRate = (yf_data['Close'][-1] - yf_data['Close'][0]) / yf_data['Close'][0]

    if (returnRate > top_five[0][1]):
      top_five.pop(0)
      top_five.append((ticker, returnRate))
      top_five.sort(key=sort_top_five)

  return top_five