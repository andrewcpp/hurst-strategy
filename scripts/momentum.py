from __future__ import (absolute_import, division, print_function, unicode_literals)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import backtrader as bt
from datetime import datetime

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import os.path
import sys

import backtrader as bt

return_rate = 0

# Create a Stratey
class SMACross(bt.Strategy):
    params = (
        ('sma1period', 5),
        ('sma2period', 10)
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

        self.sma1 = bt.ind.SMA(period=self.params.sma1period)
        self.sma2 = bt.ind.SMA(period=self.params.sma2period)
        self.crossover = bt.ind.CrossOver(self.sma1, self.sma2)

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
        global return_rate
        return_rate = sum(self.returnRates) / len(self.returnRates)

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f, RETURN %.2f' %
                 (trade.pnl, trade.pnlcomm, return_rate))

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.crossover == 1.0:
                self.log('BUY, %.2f' % self.dataclose[0])
                self.order = self.buy()
        elif self.crossover == -1.0:
                self.log('SELL, %.2f' % self.dataclose[0])
                self.order = self.sell()

