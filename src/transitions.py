import pandas as pd

def compute_transition_matrix(regime_series):
    # Computes regime transition probability matrix

    transitions = pd.crosstab(
        regime_series.shift(1),
        regime_series,
        normalize="index"
    )
    return transitions