import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import yfinance as yf

class ExecutionSimulator:
    """
    Backtests the 'LVQ' Arbitrage Strategy.
    Calculates Sharpe Ratio, Equity Curves, and Drawdowns.
    """
    @staticmethod
    def run_backtest(engine, stock_a, stock_b, entry_z=2.0, cost = 0.002):
        # 1. Basics: Calculate Spread & Z-Score
        s1, s2 = engine.data[stock_a], engine.data[stock_b]
        res = sm.OLS(s1, sm.add_constant(s2)).fit()
        beta = res.params[stock_b]
        spread = s1 - (beta * s2)
        zscore = (spread - spread.mean()) / spread.std()
        
        # 2. Strategy Logic
        signals = pd.Series(0, index=zscore.index)
        pos = 0
        for i in range(len(zscore)):
            z = zscore.iloc[i]
            if pos == 0:
                if z > entry_z: pos = -1
                elif z < -entry_z: pos = 1
            elif (pos == 1 and z >= 0) or (pos == -1 and z <= 0):
                pos = 0
            signals.iloc[i] = pos
            
        # 3. Calculate Returns & Friction
        s1_ret, s2_ret = engine.returns[stock_a], engine.returns[stock_b]
        port_ret = signals.shift(1) * (s1_ret - beta * s2_ret)
        
        # Identify when a trade happens (Signal Change)
        # Each change incurs the 'cost' penalty
        trade_count = signals.diff().abs()
        friction = trade_count * cost
        final_returns = port_ret - friction
        
        # 4. Metrics
        sharpe = (final_returns.mean() / final_returns.std()) * np.sqrt(252)
        equity_curve = (1 + final_returns.fillna(0)).cumprod()
        max_dd = ((equity_curve - equity_curve.cummax()) / equity_curve.cummax()).min()
        
        return equity_curve, sharpe, max_dd
    
    @staticmethod
    def run_adaptive_backtest(engine, stock_a, stock_b, dyn_z, dyn_beta, cost=0.002):
        """
        Atomic Adaptive Backtester: 
        Forcibly aligns all inputs to the same time-index to prevent shape mismatches.
        """
        # 1. Extract the raw returns from the engine
        s1_ret = engine.returns[stock_a]
        s2_ret = engine.returns[stock_b]

        # 2. Alignment Table: This forces dyn_z, dyn_beta, and returns into perfect sync
        # It automatically handles the 1112 vs 987 discrepancy by dropping mismatches
        alignment_df = pd.DataFrame({
            'z': dyn_z,
            'beta': pd.Series(dyn_beta, index=dyn_z.index) if not isinstance(dyn_beta, pd.Series) else dyn_beta,
            'ret_a': s1_ret,
            'ret_b': s2_ret
        }).dropna()

        # 3. Strategy Logic (Execute on the aligned index)
        signals = pd.Series(0, index=alignment_df.index)
        pos = 0
        for i in range(len(alignment_df)):
            z = alignment_df['z'].iloc[i]
            if pos == 0:
                if z > 2.0: pos = -1
                elif z < -2.0: pos = 1
            elif (pos == 1 and z >= 0) or (pos == -1 and z <= 0):
                pos = 0
            signals.iloc[i] = pos
            
        # 4. Performance Math using the aligned table
        # We shift signals by 1 to represent trading on the next day's open
        applied_signals = signals.shift(1).fillna(0)
        
        # Pure Pair Return = Return_A - (Rolling_Beta * Return_B)
        pair_return = alignment_df['ret_a'] - (alignment_df['beta'] * alignment_df['ret_b'])
        
        port_ret = applied_signals * pair_return
        friction = signals.diff().abs().fillna(0) * cost
        final_ret = port_ret - friction
        
        # 5. Metrics
        sharpe = (final_ret.mean() / final_ret.std()) * np.sqrt(252) if final_ret.std() != 0 else 0
        equity = (1 + final_ret).cumprod()
        
        return equity, sharpe, signals, pair_return, friction

    @staticmethod
    def plot_performance(equity_curve, engine_data):
        """
        Plots the Equity Curve against the Nifty 50 Benchmark.
        """
        # Fetch Nifty 50 for the same period
        start_date = equity_curve.index[0]
        end_date = equity_curve.index[-1]
        nifty = yf.download("^NSEI", start=start_date, end=end_date)['Close']
        
        # Normalize Benchmark
        nifty_bench = (nifty / nifty.iloc[0])
        
        plt.figure(figsize=(12, 6))
        plt.plot(equity_curve, label='Strategy (Market Neutral)', color='blue', linewidth=2)
        plt.plot(nifty_bench, label='Nifty 50 Benchmark', color='orange', linestyle='--', alpha=0.7)
        
        plt.title("Equity Curve vs. Nifty 50 Benchmark")
        plt.ylabel("Growth Multiplier (Starting at 1.0)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()