from pykalman import KalmanFilter
import numpy as np
import pandas as pd

class AdaptiveAlpha:
    """
    V2: Adaptive Intelligence Layer.
    Uses Kalman Filters to track Dynamic Hedge Ratios.
    """

    @staticmethod
    def get_dynamic_spread(engine, stock_a, stock_b):
        #Prepare data
        obs_mat = pd.DataFrame(engine.data[stock_b])
        obs_mat['intercept'] = 1.0

        #Initialize kalman Filter
        #We are tracking 2 states: Slope(Beta) and Intercept
        kf = KalmanFilter(
            n_dim_obs = 1,
            n_dim_state = 2,
            initial_state_mean = np.zeros(2),
            initial_state_covariance = np.ones((2,2)),
            transition_matrices = np.eye(2),
            observation_matrices = obs_mat.values[:, np.newaxis, :],
            observation_covariance = 1.0,
            transition_covariance = np.eye(2) * 1e-4 #How fast Beta changes
        )

        #Filter data to find state means(Dynamic Beta)
        state_means, _ = kf.filter(engine.data[stock_a].values)

        #state_means[:, 0] is our Dynamic Beta
        #state_means[:, 1] is our Dynamic Intercept
        dynamic_beta = state_means[:, 0]
        dynamic_intercept = state_means[:, 1]

        spread = engine.data[stock_a] - (dynamic_beta * engine.data[stock_b] + dynamic_intercept)

        #Use a rolling Z-Score (Basics: Dont look at 5-year spread)
        window = 30 #looking at last 30 days spread
        mean = spread.rolling(window = window).mean()
        std = spread.rolling(window = window).std()
        dynamic_z = (spread - mean) / std

        return dynamic_z, dynamic_beta
    
    # Add this to your AdaptiveAlpha class
    @staticmethod
    def get_velocity(spread, window=5):
        # If velocity is positive, spread is growing. 
        # If negative, it's shrinking back to mean.
        return spread.diff(window)