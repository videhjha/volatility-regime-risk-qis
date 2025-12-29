import numpy as np

def volatility_targeted_returns(returns, realized_vol, target_vol=0.15, trading_days=252):
    # Applies a volatility targeting overlay to returns.

    # Convert target vol to daily
    target_daily_vol = target_vol / np.sqrt(trading_days)

    # Compute scaling factor
    scaling_factor = target_daily_vol / realized_vol

    # Cap leverage for realism
    scaling_factor = scaling_factor.clip(upper=2.0)

    # Apply scaling
    scaled_returns = scaling_factor * returns

    return scaled_returns