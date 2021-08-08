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
data['position'] = np.sign(data['returns'])
data['strategy'] = data['position'].shift(1)*data['returns']
data[['returns','strategy']].dropna().cumsum().apply(np.exp).plot(figsize = (10,6))

rq.init()
stock_data = rq.get_price('300467.XSHE',start_date = '2015-12-01',end_date='2021-08-04',frequency = '1d')
data = stock_data[['close']]
data = data.rename(columns = {'close':'price'})
data['returns'] = np.log(data['price']/data['price'].shift(1))
to_plot = ['returns'] # Define a list object to select the columns to be plotted later
for n in [1,3,5,7,9,10,20,30,60]:
    data['position_%d'% n ] = np.sign(data['returns'].rolling(n).mean())
    data['strategy_%d'%n ] = (data['position_%d'%n].shift(1)*data['returns'])
    to_plot.append('strategy_%d'%n)
data[to_plot].cumsum().apply(np.exp).plot(figsize=(10,6),style=['-','--','--','--','--','--','--','--','--','--'])