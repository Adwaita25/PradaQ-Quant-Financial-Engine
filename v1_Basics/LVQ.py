import statsmodels.api as sm
from statsmodels.tsa.stattools import coint as sm_coint 
import numpy as np
from v1_Basics.PradaQ import PradaQ 

class LVQ(PradaQ):
    """
    LVQ (Linear Vector Quantization) Extension:
    Focuses on Relative Value Arbitrage and Cointegration.
    """
    def find_cointegrated_pairs(self):
        # Use self.returns from the base PradaQ engine
        n = self.returns.shape[1]
        keys = self.returns.columns
        pairs = []

        for i in range(n):
            for j in range(i + 1, n):
                S1 = self.data[keys[i]]
                S2 = self.data[keys[j]]
                
                # Calling the renamed function 'sm_coint' 
                # returns: (t-statistic, p-value, critical_values)
                result = sm_coint(S1, S2)
                pvalue = result[1] 

                if pvalue < 0.05:
                    pairs.append({
                        'pair': (keys[i], keys[j]),
                        'p_value': pvalue,
                        'confidence': "95%"
                    })
        return pairs