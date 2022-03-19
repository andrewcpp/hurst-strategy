import backtrader as bt

cerebro = bt.Cerebro()
cerebro.addstrategy(SMACross)

yf_data = yf.download('GOOG', start='2020-01-01', end='2020-12-31')
data = bt.feeds.PandasData(dataname=yf_data)

cerebro.adddata(data)
cerebro.broker.setcash(100000)
cerebro.addsizer(bt.sizers.FixedSize, stake=1)
cerebro.broker.setcommission(commission=0.002)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

print(return_rate)