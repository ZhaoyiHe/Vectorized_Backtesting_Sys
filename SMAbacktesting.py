import numpy as np
import rqdatac as rq
from scipy.optimize import brute

from Indicators import IndicatorClass
from VectorizedBacktesting import VecBacktest


class SMABacktest(VecBacktest):

    def set_parameters(self, SMA_short, SMA_long):
        IndicatorCalculator = IndicatorClass()
        if SMA_short is not None:
            self.SMA_short = SMA_short
            self.results_df['SMA_%d' % SMA_short] = IndicatorCalculator.SMA_generator(prices=self.price_info['close'],
                                                                                      period=SMA_short)
            # self.results_df['SMA_%d'%SMA_short] = self.results_df['returns'].rolling(SMA_short).mean()

        if SMA_long is not None:
            self.SMA_long = SMA_long
            self.results_df['SMA_%d' % SMA_long] = IndicatorCalculator.SMA_generator(prices=self.price_info['close'],
                                                                                     period=SMA_long)
            # self.results_df['SMA_%d' % SMA_long] = self.results_df['returns'].rolling(SMA_long).mean()

    def strategy_generator(self):
        self.results_df['positions'] = np.where(
            self.results_df['SMA_%d' % self.SMA_short] > self.results_df['SMA_%d' % self.SMA_long], 1, -1)
        self.results_df['positions'] = self.results_df['positions'].ffill().fillna(0)
    def run_strategy(self, SMA_short, SMA_long):

        self.set_parameters(SMA_short=SMA_short, SMA_long=SMA_long)
        self.strategy_generator()
        self.strategy_return_generator()
        self.return_generator()

    def update_and_run(self, SMA):
        """Update SMA parameters and returns negative absolute performance.
        (for minimization algorithm).

        :parameters
        ===========
        SMA: tuple
            SMA parameter tuple
        """

        self.run_strategy(int(SMA[0]), int(SMA[1]))
        return -self.total_strategy_return  ######

    def optimize_parameters(self, SMA_short_range, SMA_long_range):
        """
        Finds global maximum given the SMA parameter ranges.

        :param SMA_short:
        :param SMA_long:
        tuples of the from (start, end ,step size)
        :return:
        """
        opt = brute(self.update_and_run, (SMA_short_range, SMA_long_range), finish=None)
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


    smabacktest = SMABacktest(price_info=stock_data, returns_tupe="log")
    # smabacktest.output_results()
    best_params = smabacktest.optimize_parameters((5, 20, 5), (10, 120, 10))[0]
    smabacktest.run_strategy(SMA_short=int(best_params[0]), SMA_long=int(best_params[1]))
    smabacktest.output_results()
