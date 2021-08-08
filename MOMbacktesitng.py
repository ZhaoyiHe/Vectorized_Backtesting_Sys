import numpy as np
import rqdatac as rq
from scipy.optimize import fminbound

from Indicators import IndicatorClass
from VectorizedBacktesting import VecBacktest


class MOMBacktest(VecBacktest):

    def set_parameters(self, momentum):
        if momentum is not None:
            self.momentum = momentum

    def strategy_generator(self):
        self.results_df['positions'] = np.sign(self.results_df['returns'].rolling(self.momentum).mean())

        self.results_df['positions'] = self.results_df['positions'].ffill().fillna(0)
    def run_strategy(self, momentum):

        self.set_parameters(momentum=int(momentum))
        self.strategy_generator()
        self.strategy_return_generator()
        self.return_generator()

    def update_and_run(self, momentum):
        """Update SMA parameters and returns negative absolute performance.
        (for minimization algorithm).
        """

        self.run_strategy(int(momentum))
        return -self.total_strategy_return  ######

    def optimize_parameters(self, momentum_lb, momentum_ub):
        """
        Finds global maximum given the SMA parameter ranges.

        :return:
        """
        opt = fminbound(self.update_and_run,  momentum_lb,momentum_ub)
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

    mombacktest = MOMBacktest(price_info=stock_data, returns_tupe="log")
    # smabacktest.output_results()
    best_params = mombacktest.optimize_parameters(1,20)[0]
    mombacktest.run_strategy(best_params)
    mombacktest.output_results()
