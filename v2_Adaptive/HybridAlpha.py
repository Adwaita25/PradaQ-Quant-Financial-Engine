import numpy as np
import pandas as pd
import statsmodels.api as sm

class HybridAlpha:
    """
    Hybrid Alpha Layer: Uses a Rolling OLS Beta to balance
    stability (Static) with adaptability (Adaptive).
    """

    @staticmethod
    def get_rolling_method(engine, stock_a, stock_b, window = 126):
        s1 = engine.data[stock_a]
        s2 = engine.data[stock_b]

        #Calculating  Rolling Beta - We use a simple loop or rolling apply for the OLS
        betas = []
        for i in range(len(s1)):
            if i < window:
                betas.append(np.nan)
                continue

            y = s1.iloc[i-window:i]
            x = sm.add_constant(s2.iloc[i-window:i])

            #Solve OLS Beta = (X'X)^-1 X'y
            model = sm.OLS(y,x).fit()
            betas.append(model.params[stock_b])
        
        rolling_beta = pd.Series(betas, index = s1.index)

        spread = s1 - (rolling_beta * s2)
        mean = spread.rolling(window = window).mean()
        std = spread.rolling(window = window).std()
        rolling_z = (spread - mean) / std

        return rolling_z.dropna(), rolling_beta.dropna()