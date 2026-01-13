# v3_Production/PradaQ_Live.py
from v1_Basics.LVQ import LVQ # Assuming your class name is LVQ
import statsmodels.api as sm

class PradaQ_Live(LVQ):
    """
    Production-grade engine for Project Nexus.
    Adds stateful anchoring for Live Paper Trading.
    """
    def __init__(self, tickers):
        super().__init__(tickers)
        self.anchor_beta = None
        self.historical_mean = None
        self.historical_std = None

    def anchor_pair_statistics(self, stock_a, stock_b):
        """
        Freezes the historical Mean and STD.
        Run this ONCE before starting a live session.
        """
        s1 = self.data[stock_a]
        s2 = self.data[stock_b]
        
        # Calculate Static Beta (V1 Logic)
        res = sm.OLS(s1, sm.add_constant(s2)).fit()
        self.anchor_beta = res.params[stock_b]
        
        # Calculate Spread and Volatility Anchor
        spread = s1 - (self.anchor_beta * s2)
        self.historical_mean = spread.mean()
        self.historical_std = spread.std()
        
        print(f"--- PRODUCTION ANCHOR ESTABLISHED ---")
        print(f"Pair: {stock_a}/{stock_b}")
        print(f"Beta: {self.anchor_beta:.4f} | Std: {self.historical_std:.4f}")