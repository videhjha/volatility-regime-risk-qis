import statsmodels.api as sm

def compute_acf(series, nlags=20):     #Computes autocorrelation values up to nlags.
    return sm.tsa.acf(series, nlags=nlags, fft=False)