import numpy as np
import matplotlib.pyplot as plt

class SMA:
  def __init__(self, prices, dates, balance):
    # arguments initialization
    self.prices = prices
    self.dates = dates
    self.balance = balance

    # state and hyper parameters
    self.last_buy = 0
    self.holdings = False
    self.sma1_period = 10
    self.sma2_period = 20
    self.shares = 5

    self.n = len(prices)
    self.prev_sma1 = 0
    self.prev_sma2 = 0

    # return params
    self.yields = []
    self.buys = 0
    self.sells = 0

    # graphing arrays
    self.sma1_line = []
    self.sma2_line = []

    self.bought = []
    self.bought_dates = []
    self.sold = []
    self.sold_dates = []

  def run(self):
    for i in range(self.sma2_period, self.n):
      sma1 = np.average(self.prices[:i][-self.sma1_period:])
      sma2 = np.average(self.prices[:i][-self.sma2_period:])

      self.sma1_line.append(sma1)
      self.sma2_line.append(sma2)

      if (not self.holdings) and self.prev_sma1 <= self.prev_sma2 and sma1 >= sma2: # golden cross, BUY
        self.balance -= self.prices[i] * self.shares
        self.buys += self.prices[i] * self.shares
        self.last_buy = self.prices[i]
        self.holdings = True

        self.bought.append(self.prices[i])
        self.bought_dates.append(self.dates[i])

      elif self.holdings and self.prev_sma1 >= self.prev_sma2 and sma1 <= sma2: # death cross, SELL
        self.balance += self.prices[i] * self.shares
        self.sells += self.prices[i] * self.shares
        self.holdings = False

        rate = (self.prices[i] - self.last_buy) / self.last_buy * 100
        self.yields.append(rate)

        self.sold.append(self.prices[i])
        self.sold_dates.append(self.dates[i])

      self.prev_sma1 = sma1
      self.prev_sma2 = sma2

    return (self.balance, self.yields, self.buys, self.sells)

  def graph(self):
    plt.plot(self.dates, self.prices)
    plt.plot(self.dates[self.sma2_period:], self.sma1_line)
    plt.plot(self.dates[self.sma2_period:], self.sma2_line)
    plt.scatter(self.bought_dates, self.bought, marker='^', c="green")
    plt.scatter(self.sold_dates, self.sold, marker='v', c="red")
    plt.legend(['Price', 'SMA1 = 10', 'SMA2 = 20', 'Buy', 'Sell'])
    plt.title("Prices vs Date")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.xticks(ticks=np.arange(0, len(self.dates), 28), rotation=40)
    plt.show()