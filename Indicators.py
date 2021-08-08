import pandas as pd
import numpy as np
import MySQLdb as mdb
import rqdatac as rq
from rqdatac import *
from pylab import mpl,plt
import matplotlib
import abc

class IndicatorClass(object):
    def __init__(self):
        pass

    def SMA_generator(self,prices,period):

        sma = prices.rolling(period).mean()
        return sma

    def EMA_generator(self, prices):
        pass
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