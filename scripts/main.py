import csv
import os
import math
import random
from cmath import nan

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
# matplotlib.use('PDF')

import scipy.optimize as opt
from statsmodels.tsa.stattools import adfuller
from hurst import compute_Hc

import sma
import bollinger

csv_header = ['stock', 'adf', 'hurst', 'momentum returns', 'reversion returns']
csv_data = []

directory = 'stocks'

momentum_yields = []
reversion_yields = []

'''for stock in os.listdir(directory):
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
  momentum_yields.extend(yields)
  if buys == 0:
    momentum_return = nan
  else:
    momentum_return = (sells - buys) / buys * 100
  # momentum.graph()

  reversion = bollinger.Bollinger(prices, dates, 100000)
  balance, yields, buys, sells = reversion.run()
  reversion_yields.extend(yields)
  if buys == 0:
    reversion_return = nan
  else:
    reversion_return = (sells - buys) / buys * 100
  # reversion.graph()

  row = [stock, adf, hurst_exp, momentum_return, reversion_return]
  csv_data.append(row)

with open('data/results.csv', 'w', encoding='utf-8', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(csv_header)
  writer.writerows(csv_data)'''

data = pd.read_csv('data/results.csv')
data = data.dropna()
data = data.sample(frac = 1)

tickers = data['stock'].tolist()
random.shuffle(tickers)
adf = data['adf'].to_numpy()
hurst = data['hurst'].to_numpy()
sma_returns = data['momentum returns'].to_numpy()
bollinger_returns = data['reversion returns'].to_numpy()

momentum_mean = np.mean(sma_returns) # 0.053323898415951684
momentum_median = np.median(sma_returns) # -0.1566196542532628
momentum_std = np.std(sma_returns)  # 2.8950620055630782

reversion_mean = np.mean(bollinger_returns) # 1.9232573665702308
reversion_median = np.median(bollinger_returns) # 1.638969325808142
reversion_std = np.std(bollinger_returns) # 6.477782335970814

balanced_returns = []
for i in range(len(data)):
  if hurst[i] < 0.5:
    balanced_returns.append(bollinger_returns[i])
  else:
    balanced_returns.append(sma_returns[i])

balanced_returns = np.array(balanced_returns)

plt.hist(sma_returns, range=[-10, 10], bins=30)
plt.hist(bollinger_returns, range=[-10, 10], bins=30)
plt.hist(balanced_returns, range=[-10, 10], bins=30)
plt.title("Returns on SMA vs Bollinger vs Balanced with 0.5 Hurst")
plt.xlabel("Returns")
plt.ylabel("Frequency")
plt.legend(['SMA', 'Bollinger', 'Balanced'])
plt.savefig("img/hurst_default.png")
plt.clf()

x = []
y = []

means = []
medians = []
stds = []

for i in range(0, 100, 1):
  balanced_returns = []
  for j in range(len(data)):
    if hurst[j] <= i / 100:
      balanced_returns.append(bollinger_returns[j])
    elif hurst[j] > i / 100:
      balanced_returns.append(sma_returns[j])
  balanced_returns = np.array(balanced_returns)
  means.append(np.mean(balanced_returns))
  medians.append(np.median(balanced_returns))
  stds.append(np.std(balanced_returns))
  x.append(i / 100)

'''def f(x, a, b, c, d):
  return a / (1. + np.exp(-c * (x - d))) + b

(a_, b_, c_, d_), _ = opt.curve_fit(f, x, stds)

y_fit = f(x, a_, b_, c_, d_)
fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.plot(x, stds, 'o')
ax.plot(x, y_fit, '-')
plt.show()'''

plt.plot(x, means)
plt.title("Means")
plt.xlabel("Hurst")
plt.ylabel("Mean")
plt.savefig("img/means.png")
plt.clf()

plt.plot(x, medians)
plt.title("Medians")
plt.xlabel("Hurst")
plt.ylabel("Median")
plt.savefig("img/medians.png")
plt.clf()

plt.plot(x, stds)
plt.title("Standard Deviations")
plt.xlabel("Hurst")
plt.ylabel("Standard Deviation")
plt.savefig("img/deviation.png")
plt.clf()

'''means = np.array(means)
m = np.mean(means)
# print(m)
sharpe = []
for i in range(len(means)):
  print(m, means[i], stds[i], m * (means[i] - 1) / stds[i])
  sharpe.append((means[i] - 1) / stds[i])
plt.plot(x, sharpe)
plt.title("Sharpe Ratio")
plt.show()'''

# Choice between risk and reward