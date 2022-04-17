import backtrader as bt
import yfinance as yf

import momentum
import reversion

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use('PDF')

# Get list of NASDAQ stocks with mega market cap
stocks = pd.read_csv('data/nasdaq_mega.csv')
stocks = stocks['Symbol'].to_numpy()
print(stocks)

returns_momentum = []
returns_reversion = []

# Generate returns histogram for momentum strategy
for s in stocks[10:20]:
  cerebro_momentum = bt.Cerebro()
  cerebro_reversion = bt.Cerebro()

  cerebro_momentum.addstrategy(momentum.SMACross)
  cerebro_reversion.addstrategy(reversion.MeanReversion)

  yf_data = yf.download(s, start='2019-01-01', end='2020-12-31')
  data = bt.feeds.PandasData(dataname=yf_data)

  cerebro_momentum.adddata(data)
  cerebro_momentum.broker.setcash(100000)
  cerebro_momentum.addsizer(bt.sizers.FixedSize, stake=5)
  cerebro_momentum.broker.setcommission(commission=0.0)

  cerebro_reversion.adddata(data)
  cerebro_reversion.broker.setcash(100000)
  cerebro_momentum.addsizer(bt.sizers.FixedSize, stake=5)
  cerebro_reversion.broker.setcommission(commission=0.0)

  print('Starting Portfolio Value: %.2f' % cerebro_momentum.broker.getvalue())
  cerebro_momentum.run()
  print('Final Portfolio Value: %.2f' % cerebro_momentum.broker.getvalue())

  print('Starting Portfolio Value: %.2f' % cerebro_reversion.broker.getvalue())
  cerebro_reversion.run()
  print('Final Portfolio Value: %.2f' % cerebro_reversion.broker.getvalue())

  returns_momentum.append(momentum.returns)
  returns_reversion.append(reversion.returns)

returns_momentum = np.array(returns_momentum)
returns_momentum = returns_momentum.flatten()

returns_reversion = np.array(returns_reversion)
returns_reversion = returns_reversion.flatten()

plt.hist(returns_momentum, bins=15)
plt.title("Return for Stocks on Momentum Strategy")
plt.xlabel("Rates of Return")
plt.ylabel("Frequency")
plt.show()
# plt.savefig('img/hist_momentum.pdf')

plt.clf()

plt.hist(returns_reversion, bins=15)
plt.title("Return for Stocks on Mean Reversion Strategy")
plt.xlabel("Rates of Return")
plt.ylabel("Frequency")
plt.show()
# plt.savefig('img/hist_reversion.pdf')