import backtrader as bt

returns = []

class MeanReversion(bt.Strategy):
    params = (
        ('period', 20),
        ('devfactor', 2),
        ('movav', bt.ind.MovingAverageSimple)
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.returnRates = []

        self.mid, self.upper, self.lower = bt.ind.BollingerBands(period=self.params.period, devfactor=self.params.devfactor).lines
        self.crossup = bt.ind.CrossUp(self.dataclose, self.lower)
        self.crossmid = bt.ind.CrossUp(self.dataclose, self.mid)
        self.crossdown = bt.ind.CrossDown(self.dataclose, self.upper)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BOUGHT, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('SOLD, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.returnRates.append(trade.pnlcomm / self.buyprice)
        returns.append(trade.pnlcomm / self.buyprice)
        return_rate = sum(self.returnRates) / len(self.returnRates)

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f, RETURN %.2f' %
                 (trade.pnl, trade.pnlcomm, return_rate))

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.crossup == 1.0:
                self.log('BUY, %.2f' % self.dataclose[0])
                self.order = self.buy()
        elif self.crossmid == 1.0 or self.crossdown == 1.0:
                self.log('SELL, %.2f' % self.dataclose[0])
                self.order = self.sell()