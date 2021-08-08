import abc

import numpy as np
import pandas as pd
import rqdatac as rq
from pylab import plt
from rqdatac import *

from Statistics import StatisticsClass


class VecBacktest(metaclass=abc.ABCMeta):
    def __init__(self, price_info, returns_tupe):
        """
        :type price: pd.Series
        :type returns_tupe: str
        """
        self.price_info = price_info
        self.returns_type = returns_tupe
        self._data_preprocessor()

    def _data_preprocessor(self):
        if self.returns_type == "normal":
            self.results_df = self.price_info['close'].pct_change()
        elif self.returns_type == "log":
            self.results_df = np.log(self.price_info['close'] / self.price_info['close'].shift(1))
        else:
            try:
                raise ValueError("Invalid declaration. You must claim type of returns correctly, i.e. normal or log.")
            except ValueError as error:
                print(error)
        self.results_df.dropna(inplace=True)
        self.results_df = pd.DataFrame(self.results_df)
        self.results_df.columns = ['returns']

    def strategy_return_generator(self):

        self.results_df['strategy'] = self.results_df['positions'].shift(1)*self.results_df['returns']

    def return_generator(self):
        """
        Generate stock returns and strategy returns
        :return:
        """
        self.results_df.dropna(inplace=True)
        if self.returns_type == "normal":
            self.results_df['cum_returns'] = (self.results_df['returns'] + 1).cumprod()
            self.results_df['cum_strategy'] = (self.results_df['strategy'] + 1).cumprod()
            self.total_return = np.prod(self.results_df['returns']) - 1
            self.total_strategy_return = np.prod(self.results_df['strategy']) - 1
        elif self.returns_type == "log":
            self.results_df['cum_returns']= self.results_df['returns'].cumsum().apply(np.exp)
            self.results_df['cum_strategy'] = (self.results_df['strategy'] + 1).cumprod()
            self.total_return = np.exp(self.results_df['returns'].sum()) - 1
            self.total_strategy_return = np.exp(self.results_df['strategy'].sum()) - 1
        else:
            try:
                raise ValueError("Invalid declaration. You must claim type of returns correctly, i.e. normal or log.")
            except ValueError as error:
                print(error)

    def statistics(self):
        Stat = StatisticsClass()
        metric_frame = Stat.calculate_metrics(returns=self.results_df['strategy'], benchmark_returns=self.results_df['returns'],return_type=self.returns_type)
        metric_frame['total_strategy_return'] = "%f%%" % ( self.total_strategy_return*100)
        metric_frame['total_benchmark_return'] = "%f%%" % (self.total_return *100)
        metric_frame = pd.DataFrame.from_dict(metric_frame, orient="index")
        return metric_frame

    def visualization(self):
        """
        # plt.subplot(311)
        # plt.title('Return Distribution')
        # self.results_df['returns'].hist(bins=35, figsize=(10, 6))
        # plt.subplot(312)
        # plt.title('Cumulative Return')
        # self.results_df['cum_returns'].plot(figsize=(10, 6))
        :return:
        """

        """
                Plots the cumulative performance of the trading strategy compared to the symbol.
                :return:
                """
        if self.results_df[['cum_returns', 'cum_strategy']] is None:
            print('No results to plot yet. Run a strategy.')
        else:
            title = 'PnL'
            self.results_df[['cum_returns', 'cum_strategy']].plot(title = title, legend = True,figsize=(10, 6))
            plt.show()