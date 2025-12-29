import numpy as np

def compute_var_es(returns, alpha=0.05):
    # Computes VaR and Expected Shortfall at given alpha level.

    var = np.quantile(returns, alpha)
    es = returns[returns <= var].mean()
    return var, es