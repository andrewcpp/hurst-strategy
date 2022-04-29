import csv
import os
import math
from cmath import nan

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
# matplotlib.use('PDF')

from statsmodels.tsa.stattools import adfuller
from hurst import compute_Hc

import sma
import bollinger

csv_header = ['stock', 'adf', 'hurst', 'momentum returns', 'reversion returns']
csv_data = []

directory = 'stocks'

for stock in os.listdir(directory):
  f = 'stocks/' + stock
  stock = stock[:-4]
  print(stock)
  df = pd.read_csv(f)
  df = df.dropna()

  if len(df) < 200:
    continue

  train = df[:math.floor(len(df) / 2)]
  test = df[math.floor(len(df) / 2):]

  prices = np.array(train['Close'].tolist())

  adf = 0 # Stationary is 0, Non-Stationary is 1
  hurst_exp = 0

  result = adfuller(prices, autolag='AIC')
  if result[0] < result[4]["5%"]:
      adf = 0
  else:
      adf = 1

  H, c, vak = compute_Hc(prices)
  hurst_exp = H

  test = test.reset_index()
  dates = np.array(test['Date'].tolist())
  dates = np.array([str(dates[i])[:10] for i in range(0, len(dates))])
  prices = np.array(test['Close'].tolist())

  momentum = sma.SMA(prices, dates, 100000)
  balance, yields, buys, sells = momentum.run()
  if buys == 0:
    momentum_return = nan
  else:
    momentum_return = (sells - buys) / buys * 100
  print(hurst_exp)
  # momentum.graph()

  reversion = bollinger.Bollinger(prices, dates, 100000)
  balance, yields, buys, sells = reversion.run()
  if buys == 0:
    reversion_return = nan
  else:
    reversion_return = (sells - buys) / buys * 100
  reversion.graph()

  row = [stock, adf, hurst_exp, momentum_return, reversion_return]
  csv_data.append(row)

with open('data/results.csv', 'w', encoding='utf-8', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(csv_header)
  writer.writerows(csv_data)

data = pd.read_csv('data/results.csv')
data = data.dropna()

adf = data['adf'].to_numpy()
hurst = data['hurst'].to_numpy()
sma_returns = data['momentum returns'].to_numpy()
bollinger_returns = data['reversion returns'].to_numpy()

balanced_returns = []

for i in range(len(data)):
  if hurst[i] <= 0.5:
    balanced_returns.append(bollinger_returns[i])
  else:
    balanced_returns.append(sma_returns[i])

balanced_returns = np.array(balanced_returns)

print("Momentum mean: " + str(np.mean(sma_returns)))
print("Momentum median: " + str(np.median(sma_returns)))
print("Momentum standard deviation: " + str(str(np.std(sma_returns))))

print("Reversion mean: " + str(np.mean(bollinger_returns)))
print("Reversion median: " + str(np.median(bollinger_returns)))
print("Reversion standard deviation: " + str(np.std(bollinger_returns)))

plt.hist(sma_returns, bins=15)
plt.hist(balanced_returns, bins=15)
plt.title("Momentum vs Balanced")
plt.legend(['Momentum', 'Balanced'])
plt.xlabel("Returns (%)")
plt.ylabel("Frequency")
plt.show()

plt.clf()

plt.hist(bollinger_returns, bins=100)
plt.hist(balanced_returns, bins=100)
plt.title("Reversion vs Balanced")
plt.legend(['Reversion', 'Balanced'])
plt.xlabel("Returns (%)")
plt.ylabel("Frequency")
plt.show()