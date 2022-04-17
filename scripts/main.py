import backtrader as bt
import yfinance as yf

import momentum
import reversion

import matplotlib.pyplot as plt

cerebro = bt.Cerebro()
# cerebro.addstrategy(momentum.SMACross)
cerebro.addstrategy(reversion.MeanReversion)

yf_data = yf.download('GOOG', start='2019-01-01', end='2020-12-31')
data = bt.feeds.PandasData(dataname=yf_data)

cerebro.adddata(data)
cerebro.broker.setcash(100000)
cerebro.addsizer(bt.sizers.FixedSize, stake=1)
cerebro.broker.setcommission(commission=0.0)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()