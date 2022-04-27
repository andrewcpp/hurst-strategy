import numpy as np
import matplotlib.pyplot as plt

class Bollinger:
  def __init__(self, prices, dates, balance):
    # argument init
    self.prices = prices
    self.dates = dates
    self.balance = balance

    self.last_buy = 0
    self.holdings = False

    self.n = len(prices)
    self.period = 20
    self.std = 2
    self.shares = 5

    self.last_bottom = 0
    self.last_sma = 0
    self.last_top = 0

    # returns params
    self.yields = []
    self.buys = 0
    self.sells = 0

    # bands
    self.bought = []
    self.bought_dates = []
    self.sold = []
    self.sold_dates = []

    self.upper = []
    self.mid = []
    self.lower = []
  
  def run(self):
    for i in range(self.period, self.n):
      sma = np.average(self.prices[:i][-self.period:self.n])
      top = sma + 2 * np.std(self.prices[:i][-self.period:self.n])
      bottom = sma - 2 * np.std(self.prices[:i][-self.period:self.n])

      self.upper.append(top)
      self.mid.append(sma)
      self.lower.append(bottom)

      if (not self.holdings) \
        and self.prices[i-1] <= self.last_bottom \
          and self.prices[i] >= bottom:

        self.balance -= self.prices[i] * self.shares
        self.buys += self.prices[i] * self.shares
        self.last_buy = self.prices[i]
        self.holdings = True

        self.bought_dates.append(self.dates[i])
        self.bought.append(self.prices[i])

      elif self.holdings \
        and ((self.prices[i-1] >= self.last_top and self.prices[i] <= top) \
          or (self.prices[i-1] >= self.last_sma and self.prices[i] <= sma)):

        self.balance += self.prices[i] * self.shares
        self.sells += self.prices[i] * self.shares
        self.holdings = False
        rate = (self.prices[i] - self.last_buy) / self.last_buy * 100
        self.yields.append(rate)

        self.sold_dates.append(self.dates[i])
        self.sold.append(self.prices[i])
      
      self.last_top = top
      self.last_sma = sma
      self.last_bottom = bottom
    
    return (self.balance, self.yields, self.buys, self.sells)

  def graph(self):
    plt.plot(self.dates, self.prices)
    plt.plot(self.dates[self.period:], self.upper)
    plt.plot(self.dates[self.period:], self.mid)
    plt.plot(self.dates[self.period:], self.lower)
    plt.scatter(self.bought_dates, self.bought, marker='^', c="green")
    plt.scatter(self.sold_dates, self.sold, marker='v', c="red")
    plt.legend(['Price', '2SD Above', 'SMA', '2SD Below', 'Buy', 'Sell'])
    plt.title("Prices vs Date")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.xticks(ticks=np.arange(0, len(self.dates), 28), rotation=40)
    plt.show()