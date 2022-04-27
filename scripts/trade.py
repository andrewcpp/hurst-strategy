import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import yfinance as yf

import sma
import bollinger

nano = pd.read_csv('data/nasdaq_nano.csv')
micro = pd.read_csv('data/nasdaq_micro.csv')
small = pd.read_csv('data/nasdaq_small.csv')
medium = pd.read_csv('data/nasdaq_medium.csv')
large = pd.read_csv('data/nasdaq_large.csv')
mega = pd.read_csv('data/nasdaq_mega.csv')

yf_data = yf.download('MANU', start='2019-07-01', end='2020-12-31')
yf_data = yf_data.reset_index()

date = np.array(yf_data['Date'].tolist())
date = np.array([str(date[i])[:10] for i in range(0, len(date))])
closings = np.array(yf_data['Close'].tolist())

momentum = sma.SMA(closings, date, 100000)
balance, yields, buys, sells = momentum.run()
print((sells - buys) / buys * 100)
momentum.graph()

reversion = bollinger.Bollinger(closings, date, 100000)
balance, yields, buys, sells = reversion.run()
print((sells - buys) / buys * 100)
reversion.graph()
