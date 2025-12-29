import numpy as np

def compute_log_returns(price_series):   # Computes log returns from a price series.
    returns = np.log(price_series / price_series.shift(1))
    return returns.dropna()