import pandas as pd
import numpy as np
import rqdatac as rq
from rqdatac import *
import matplotlib.pyplot as plt


class IndicatorClass(object):
    def __init__(self):
        pass

    def SMA_generator(self, prices, period):
        sma = prices.rolling(period).mean()
        return sma

    def EMA_generator(self, prices,period):
        ema = list()
        for i in range(len(prices)):
            if i == 0:
                ema.append(prices.iloc[0])
            else:
                smooth_coef = 2/(period+1)
                current_ema = smooth_coef*prices.iloc[i]+(1-smooth_coef)*ema[i-1]
                ema.append(current_ema)
        ema = pd.DataFrame(index = prices.index,data = ema)
        return ema

    def RSI_generator(self, prices):
        pass

    def BOLL_generator(self, prices):
        pass

    def SAR_generator(self, prices):
        pass

    def BBI_generator(self, prices):
        pass

    def ROC_generator(self, prices):
        pass

    def MACD_generator(self, prices):
        pass

    def VOL_generator(self, prices):
        pass

    def CCI_generator(self, prices):
        pass

    def WR_generator(self, prices):
        pass

    def WVAD_generator(self, prices):
        pass

    def DMI_generator(self, prices):
        pass

    def PSY_generator(self, prices):
        pass

    def KDJ_generator(self, prices):
        pass

    def OBV_generator(self, prices):
        pass


if __name__=="__main__":
    rq.init()
    Ind = IndicatorClass()
    data = rq.get_price('300467.XSHE', '2015-05-01', '2021-08-06', frequency='1d', adjust_type="pre")
    ema = Ind.EMA_generator(data.close,20)
    ema.plot()
    plt.show()