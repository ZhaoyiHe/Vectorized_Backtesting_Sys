import numpy as np
import rqdatac as rq
from scipy.optimize import brute

from Indicators import IndicatorClass
from VectorizedBacktesting import VecBacktest


class MRBacktest(VecBacktest):

    def set_parameters(self, SMA, threshold):
        IndicatorCalculator = IndicatorClass()
        if SMA is not None:
            self.SMA = SMA
            self.results_df['SMA_%d' % SMA] = IndicatorCalculator.SMA_generator(prices=self.price_info['close'],
                                                                                      period=SMA)
            # self.results_df['SMA_%d'%SMA_short] = self.results_df['returns'].rolling(SMA_short).mean()

        if threshold is not None:
            self.threshold = threshold

            # self.results_df['SMA_%d' % SMA_long] = self.results_df['returns'].rolling(SMA_long).mean()

    def strategy_generator(self):
        self.results_df['distance'] = self.price_info['close']-self.results_df['SMA_%d' % self.SMA]
        self.results_df.dropna(inplace=True)
        self.results_df['positions'] = np.where(self.results_df['distance'] > self.threshold, -1, np.nan)
        self.results_df['positions'] = np.where(self.results_df['distance'] < -self.threshold, 1, self.results_df['positions'])
        self.results_df['positions'] = np.where(self.results_df['distance'].shift(1) * self.results_df['distance'] <0, 0, self.results_df['positions'])

        self.results_df['positions'] = self.results_df['positions'].ffill().fillna(0)



    def run_strategy(self, SMA, threshold):

        self.set_parameters(SMA=SMA, threshold=threshold)
        self.strategy_generator()
        self.strategy_return_generator()
        self.return_generator()

    def update_and_run(self, SMA_threshold_tuple):

        self.run_strategy(int( SMA_threshold_tuple[0]), SMA_threshold_tuple[1])
        return -self.total_strategy_return  ######

    def optimize_parameters(self, SMA_range, threshold_range):
        """
        Finds global maximum given the SMA parameter ranges.

        tuples of the from (start, end ,step size)
        :return:
        """
        opt = brute(self.update_and_run, (SMA_range, threshold_range), finish=None)
        print(opt)
        return opt, -self.update_and_run(opt)

    def output_results(self):
        print(self.statistics())
        self.visualization()


if __name__ == "__main__":
    rq.init()
    stock_data = rq.get_price('300467.XSHE', start_date='2015-12-01', end_date='2021-08-06', frequency='1d',
                              adjust_type="post")

    # data = stock_data.rename(columns={'close': 'price'})

    mrbacktest = MRBacktest(price_info=stock_data, returns_tupe="log")
    # smabacktest.output_results()
    best_params = mrbacktest.optimize_parameters((10,80, 5), (2, 10, 0.5))[0]
    mrbacktest.run_strategy(SMA=int(best_params[0]), threshold=best_params[1])
    mrbacktest.output_results()

