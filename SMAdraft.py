import rqdatac as rq
import pandas as pd
import numpy as np
import MySQLdb as mdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import abc
rq.init()
stock_data = rq.get_price('300467.XSHE',start_date = '2015-12-01',end_date='2021-07-27',frequency = '1d')
stock_data['SMA1'] = stock_data.close.rolling(42).mean()
stock_data['SMA2'] = stock_data.close.rolling(252).mean()
data = stock_data[['close','SMA1','SMA2']]
data = data.rename(columns = {'close':'price'})
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'
data.plot(title = 'XYKJ | 42 &252 days SMAs',figsize = (10,6))
data['position'] = np.where(data['SMA1']> data['SMA2'],1,-1)
data.dropna(inplace=True)
data['position'].plot(ylim= [-1.1,1.1],title = 'Market Positioning',figsize = (10,6))
data['returns'] = np.log(data['price']/data['price'].shift(1))
data['returns'].hist(bins=35,figsize=(10,6))
data['strategy'] = data['returns'] * data['position'].shift(1)
data[['returns','strategy']].sum()
data[['returns','strategy']].sum().apply(np.exp)

data[['returns','strategy']].cumsum().apply(np.exp).plot(figsize = (10,6))
# annualized risk-return statistics
data[['returns','strategy']].mean() * 252
np.exp(data[['returns','strategy']].mean()*252)-1
data[['returns','strategy']].std()*252**0.5
(data[['returns','strategy']].apply(np.exp)-1).std()*252**0.5
data['cumret'] = data['strategy'].cumsum().apply(np.exp)
data['cummax'] = data['cumret'].cummax()
drawdown = data['cummax'] - data['cumret']
drawdown.max()

temp  = drawdown[drawdown == 0]
periods = (temp.index[1:].to_pydatetime()-temp.index[:-1].to_pydatetime()) # Calculate the timedelta values between all index values
periods[12:15]
periods.max() # picks out the maximum timedelta
