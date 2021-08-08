import numpy as np
import pandas as pd
import scipy.stats


class StatisticsClass(object):
    def __init__(self):
        pass

    def calculate_daily_mean_std(self, returns, return_type="normal"):
        if return_type == "log":
            returns = returns.apply(np.exp) - 1
        mean = np.mean(returns)
        std = np.std(returns)
        return mean, std

    def calculate_annualized_mean_std(self, returns, return_type="normal"):
        if return_type == "log":
            returns = returns.apply(np.exp) - 1
        mean = np.mean(returns) * 252
        std = np.std(returns) * (252 ** 0.5)
        return mean, std

    def calculate_VaR(self, returns, return_type="normal"):
        if return_type == "log":
            returns = returns.apply(np.exp) - 1
        # Calculate the average and volatility
        avg = np.mean(returns)
        vol = np.std(returns)
        # Calculate the 0.99 VaR
        VaR = dict()
        VaR[r"95%_VaR"] = -(avg - 1.645 * vol)
        VaR[r"99%_VaR"] = -(avg - 2.326 * vol)
        return VaR

    def calculate_sharpe_ratio(self, returns, window_size=252, risk_free_rate=0, return_type="normal"):
        if return_type == "log":
            returns = returns.apply(np.exp) - 1
        return np.sqrt(window_size) * (np.mean(returns) - risk_free_rate) / np.std(returns)

    def calculate_alpha_beta(self, returns, benchmark_returns, risk_free_rate=0, return_type="normal"):
        if return_type == "log":
            returns = returns.apply(np.exp) - 1
        cov = np.cov(returns, benchmark_returns)[0, 1]
        var = np.var(benchmark_returns)
        beta = cov / var
        alpha =( returns - (risk_free_rate + beta * (benchmark_returns - risk_free_rate)))[-1]
        return [alpha, beta]

    def calculate_drawdown(self, returns, window_size=252, rolling_drawdown_duration=None, return_type="normal"):
        if return_type == "log":
            returns = returns.apply(np.exp) - 1
        # By using a rolling maximum
        # Calculate the drawdown by computing the falling ratio from the maximum return
        # maximum drawdown duration is the longest time from peak to peak
        returns.dropna(inplace=True)
        returns = pd.DataFrame(returns)
        returns['roll_max'] = returns['strategy'].rolling(window=window_size).max()
        returns= returns.fillna(value = returns.strategy[0])
        #returns.dropna(inplace=True)
        drawdown = 1 - returns.strategy / returns.roll_max
        if not rolling_drawdown_duration:
            maxDD = drawdown.max()
        elif rolling_drawdown_duration:
            maxDD = drawdown.rolling(window=rolling_drawdown_duration).max()
        #drawdown.dropna(inplace=True)
        temp = drawdown[drawdown == 0]
        durations = (temp.index[1:].to_pydatetime() - temp.index[:-1].to_pydatetime())
        max_duration = durations.max()
        return [maxDD, max_duration]

    def calculate_calmar_ratio(self, returns, max_drawdown, risk_free_rate=0, return_type="normal"):
        if return_type == "log":
            returns = returns.apply(np.exp) - 1

        calmar_ratio = (np.mean(returns) - risk_free_rate) / max_drawdown
        return calmar_ratio

    def calculate_corr(self, returns, benchmark_returns, return_type="normal"):
        if return_type == "log":
            returns = returns.apply(np.exp) - 1
        comb_df = pd.merge(returns.reset_index(), benchmark_returns.reset_index(), how="inner",
                           on="date").dropna().set_index(
            "date")
        coef, p = scipy.stats.pearsonr(comb_df.iloc[:, 0], comb_df.iloc[:, 1])
        return [coef, p]

    def calculate_metrics(self, returns,benchmark_returns=None, return_type="normal"):

        metrics = {}

        # returns
        metrics['daily_return'] = "%f%%" % (self.calculate_daily_mean_std(returns=returns, return_type=return_type)[0]*100)  # Calculate average daily
        # return
        metrics['annual_return'] = "%f%%" % (self.calculate_annualized_mean_std(returns=returns, return_type=return_type)[0]*100) 

        # Volatility
        metrics['daily_volatility'] = self.calculate_daily_mean_std(returns, return_type)[1]
        metrics['annualized_volatility'] = self.calculate_annualized_mean_std(returns, return_type)[1]


        # Drawdown
        maxDD = self.calculate_drawdown(returns = returns, return_type=return_type)[0]
        metrics['max_drawdown'] = "%f%%" % (100 * maxDD)  # Calculate maximum drawdown
        # Risk and variance
        metrics[r"95%_VaR"] = self.calculate_VaR(returns, return_type)[r"95%_VaR"]
        metrics[r"99%_VaR"] = self.calculate_VaR(returns, return_type)[r"99%_VaR"]
        metrics['sharpe_ratio'] = self.calculate_sharpe_ratio(returns=returns,
                                                              return_type=return_type)  # Calculate Sharpe ratio
        metrics['calmar_ratio'] = self.calculate_calmar_ratio(returns=returns,
                                                              return_type=return_type,max_drawdown=maxDD)  # Calculate Sharpe ratio
        # Risk and variance with respect to benchmark
        if benchmark_returns is not None:
            # returns
            metrics['benchmark_daily_return'] = "%f%%" % (
                        self.calculate_daily_mean_std(returns=benchmark_returns, return_type=return_type)[
                            0] * 100)  # Calculate average daily
            # return
            metrics['benchmark_annual_return'] = "%f%%" % (
                    self.calculate_annualized_mean_std(returns=benchmark_returns, return_type=return_type)[0] * 100)

            # Volatility
            metrics['benchmark_daily_volatility'] = self.calculate_daily_mean_std(benchmark_returns, return_type)[1]
            metrics['benchmark_annualized_volatility'] = \
            self.calculate_annualized_mean_std(benchmark_returns, return_type)[1]


            alpha_beta_list = self.calculate_alpha_beta(returns=returns,return_type=return_type,benchmark_returns=benchmark_returns)
            metrics['alpha'] = alpha_beta_list[0]
            metrics['beta'] = alpha_beta_list[1]
            corr_p_list = self.calculate_corr(returns=returns, return_type=return_type,benchmark_returns=benchmark_returns)
            metrics['correlation_coefficient'] = corr_p_list[0]
            metrics['p'] = corr_p_list[1]
        # Summary
        # metrics_df = pd.DataFrame.from_dict(metrics, orient="index")
        return metrics
