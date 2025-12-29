import numpy as np

def realized_volatility(returns, window):    
    # Computes realized volatility as sqrt of rolling sum of squared returns.
    return np.sqrt((returns ** 2).rolling(window).sum())