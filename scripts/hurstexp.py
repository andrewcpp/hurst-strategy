import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import math
import scipy.stats
from datetime import datetime
from mpmath import gamma
from hurst import compute_Hc, random_walk
import sklearn.linear_model as ln

yf_data = yf.download('GOOG', start='2021-01-01', end='2021-06-30')
closings = np.array(yf_data['Close'].tolist())

# Calculate mean
mean = np.average(closings)

mean_adjusted = np.array([p - mean for p in closings])

deviate = np.array([np.sum(mean_adjusted[:i+1])
                   for i in range(0, len(closings))])

def Rn(n):
    slice = deviate[:n+1]
    return np.max(slice) - np.min(slice)

def Sn(n):
    slice = deviate[:n+1]
    return np.std(slice)

rescaled = np.array([Rn(i) / Sn(i) for i in range(1, len(closings))])

rescaled_sum = np.array([np.sum(rescaled[:i+1]) for i in range(0, len(rescaled))])
rescaled_avg = np.array([rescaled_sum[i] / (i + 1) for i in range(0, len(rescaled_sum))])
x = np.array([np.log(n) for n in range(2, len(closings) + 1)])
y = np.log(rescaled_avg)

reg = scipy.stats.linregress(x, y)
print(reg.slope)

# reg = ln.LinearRegression().fit(x, y)
# print(reg.coef_)

H, c, vak = compute_Hc(closings)
print(H)