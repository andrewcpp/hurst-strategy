'''
Testing if backtrader implementation of strategies work.
'''

import backtrader as bt
import yfinance as yf

import sma_bt
import bollinger_bt

cerebro = bt.Cerebro()

# one or the other, comment
cerebro.addstrategy(sma_bt.SMACross)
# cerebro.addstrategy(bollinger_bt.MeanReversion)

yf_data = yf.download('GOOG', start='2020-01-01', end='2020-12-31')
data = bt.feeds.PandasData(dataname=yf_data)

cerebro.adddata(data)
cerebro.broker.setcash(100000)
cerebro.addsizer(bt.sizers.FixedSize, stake=5)
cerebro.broker.setcommission(commission=0.0)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()