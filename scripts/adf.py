from statsmodels.tsa.stattools import adfuller
import numpy as np
import yfinance as yf

from hurst import compute_Hc

yf_data = yf.download('RCI', start="2018-07-01", end="2020-02-01")
closings = np.array(yf_data['Close'].tolist())

result = adfuller(closings, autolag='AIC')
if result[0] < result[4]["5%"]:
    print ("Stationary")
else:
    print ("Non-Stationary")

H, c, vak = compute_Hc(closings)
print(H)