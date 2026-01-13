import yfinance as yf
import numpy as np
import pandas as pd
import scipy.stats as si
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

class PradaQ:
    """
    A Quant Pipeline for Multivariate Risk and Alpha Generation
    """

    def __init__(self, tickers):
        self.tickers = tickers
        self.data = None
        self.returns = None

    def ingest_and_clean(self, start, end):
        #High level firms use Adjusted close to account for Splits/Dividends
        raw = yf.download(self.tickers, start = start, end = end)['Close']
        self.data = raw.ffill().dropna()

        #Log returns are additive and standard for high level math
        self.returns = np.log(self.data / self.data.shift(1)).dropna()
        return self.returns
    
    def compute_covariance(self):
        #Interaction Layer for 3D Surfaces
        return self.returns.cov(), self.returns.corr()
