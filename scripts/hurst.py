import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import backtrader as bt
import math
import scipy.stats
from datetime import datetime

yf_data = yf.download('MANU', start='2020-01-01', end='2020-12-31')
closings = yf_data['Close'].tolist()
closings = closings[0:365]

# Calculate mean
mean = sum(closings) / len(closings)
print("mean: " + str(mean))

# Calculate standard deviation
def map_variance(x):
  return math.pow(x - mean, 2)

variance = sum(map(map_variance, closings)) / len(closings)
stdev = math.sqrt(variance)
print("standard deviation: " + str(stdev) + "\n")

# Calculate mean adjusted series
mean_adjusted_series = []
for x in closings:
  mean_adjusted_series.append(x - mean)
print("mean adjusted series: " + str(mean_adjusted_series) + "\n")

# Calculate cumulative deviate series
cumulative_deviate_series = []
for i in range(1, len(mean_adjusted_series) + 1):
  cumulative_deviate_series.append(sum(mean_adjusted_series[0:i]))
print("cumulative deviate series: " + str(cumulative_deviate_series) + "\n")

# Calculate range series
range_series = []
for i in range(1, len(closings) + 1):
  range_series.append(max(closings[:i]) - min(closings[:i]))
print("range series: " + str(range_series) + "\n")

# Calculate standard deviation series
stdev_series = []
for i in range(1, len(closings) + 1):
  stdev_series.append(sum(map(map_variance, closings[:i])) / i)
print("standard deviation series: " + str(stdev_series) + "\n")

# Calculate rescaled range series
rescaled_range_series = []
for i in range(len(closings)):
  rescaled_range_series.append(range_series[i] / stdev_series[i])
print("rescaled range series: " + str(rescaled_range_series) + "\n")

log_y = map(math.log, rescaled_range_series[1:])
log_y = list(log_y)

log_x = map(math.log, [x for x in range(2, len(closings) + 1)])
log_x = list(log_x)

result = scipy.stats.linregress(log_x, log_y)
print("slope: " + str(result.slope))