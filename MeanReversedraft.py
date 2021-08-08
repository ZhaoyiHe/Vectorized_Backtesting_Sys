import rqdatac as rq
import pandas as pd
import numpy as np
import MySQLdb as mdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import abc

rq.init()
stock_data = rq.get_price('300467.XSHE',start_date = '2015-12-01',end_date='2021-08-04',frequency = '1d')
data = stock_data[['close']]
data = data.rename(columns = {'close':'price'})
data['returns'] = np.log(data['price']/data['price'].shift(1))
SMA = 25
data['SMA'] = data['price'].rolling(SMA).mean()
threshold = 3.5
data['distance'] = data['price']-data['SMA']
data['distance'].dropna().plot(figsize=(10,6),legend =True)
plt.axhline(threshold,color = 'r')
plt.axhline(-threshold,color = 'r')
plt.axhline(0,color='r')

data['position'] = np.where(data['distance']>threshold,-1,np.nan)
data['position'] = np.where(data['distance']<-threshold,1,data['position'])
data['position'] = np.where(data['distance']*data['distance'].shift(1) <- 0 ,0,data['position']) # If there is a change in the sign of the distance value, go market neutra (set 0), otherwise keeo the column position unchanged
data['position'] = data['position'].ffill().fillna(0) # Forward fill all NaN positions with the previous values; replace all remainning NaN values by 0.

data['strategy'] = data['position'].shift(1)*data['returns']
data[['returns','strategy']].dropna().cumsum().apply(np.exp).plot(figsize = (10,6))
