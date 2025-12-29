import pandas as pd
import numpy as np

def assign_volatility_regimes(rv_series):
    # Assigns Low / Medium / High volatility regimes based on quantiles of realized volatility.

    q30 = rv_series.quantile(0.30)
    q70 = rv_series.quantile(0.70)

    regimes = pd.cut(
        rv_series,
        bins=[-np.inf, q30, q70, np.inf],
        labels=["Low", "Medium", "High"]
    )

    return regimes