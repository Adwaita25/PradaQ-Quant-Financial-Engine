import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import statsmodels.api as sm

class QVisuals:
    """
    Visualization Layer for Project PradaQ.
    Converts raw data into 3D Geometric Surfaces.
    """

    @staticmethod
    def plot_3D(engine, stock_a, stock_b):
        """
        Creates a 3D trajectory of the spread between two assets.
        """
        S1 = engine.data[stock_a]
        S2 = engine.data[stock_b]
        
        # Calculate Hedge Ratio (Beta)
        model = sm.OLS(S1, sm.add_constant(S2)).fit()
        beta = model.params[stock_b]
        
        # Calculate Z-Score of the Spread
        spread = S1 - (beta * S2)
        zscore = (spread - spread.mean()) / spread.std()
        
        time_index = np.arange(len(zscore))
        
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plotting the Z-score path
        ax.plot(time_index, zscore, zs=0, zdir='z', color='blue', label='Spread Path')
        
        # Threshold Planes (Industry standard +/- 2 sigma)
        ax.axhline(2, color='red', linestyle='--', alpha=0.3, label='Upper Bound')
        ax.axhline(-2, color='green', linestyle='--', alpha=0.3, label='Lower Bound')
        
        ax.set_title(f"Arbitrage Spread Geometry: {stock_a} vs {stock_b}")
        ax.set_xlabel("Days")
        ax.set_ylabel("Z-Score")
        ax.set_zlabel("Intensity")
        plt.legend()
        plt.show()