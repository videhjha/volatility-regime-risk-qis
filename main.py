import pandas as pd
from src.data_loader import load_prices
from src.returns import compute_log_returns
from src.realized_vol import realized_volatility
from src.regimes import assign_volatility_regimes
from src.transitions import compute_transition_matrix
from src.risk_metrics import compute_var_es
from src.vol_targeting import volatility_targeted_returns

print("Script started")

# Asset universe
assets = {
    "Infosys": "data/raw/infosys.csv",
    "Reliance": "data/raw/reliance.csv",
    "HDFC_Bank": "data/raw/hdfc.csv",
    "NIFTY_50": "data/raw/nifty50.csv",
}

results = {}

summary_rows = []
drawdown_rows = []

for asset, path in assets.items():
    print(f"\nProcessing {asset}...")

    # Load data
    df = load_prices(path)

    # Compute returns
    returns = compute_log_returns(df["close"])

    # Compute realized volatility
    rv_21 = realized_volatility(returns, window=21)
    rv_21_clean = rv_21.dropna()

    # Assign regimes
    regimes = assign_volatility_regimes(rv_21_clean)

    # ✅ CREATE result FIRST
    result = df.loc[regimes.index].copy()
    result["returns"] = returns.loc[regimes.index]
    result["rv_21"] = rv_21_clean
    result["regime"] = regimes

    # ✅ THEN apply volatility targeting
    vt_returns = volatility_targeted_returns(
        result["returns"],
        result["rv_21"],
        target_vol=0.15
    )
    result["vt_returns"] = vt_returns

    results[asset] = result

    # Sanity check
    print(result["regime"].value_counts())

    # Transition matrix
    transition_matrix = compute_transition_matrix(result["regime"])
    print("\nTransition matrix:")
    print(transition_matrix)

    # Regime-conditional risk
    print("\nRegime-conditional risk (95% VaR & ES):")

    for regime in ["Low", "Medium", "High"]:
        regime_returns = result[result["regime"] == regime]["returns"]
        var, es = compute_var_es(regime_returns, alpha=0.05)

        print(f"{regime}: VaR = {var:.4f}, ES = {es:.4f}")

        summary_rows.append({
            "Asset": asset,
            "Regime": regime,
            "VaR_95": var,
            "ES_95": es
        })

    # ===== Drawdown comparison =====

    # Cumulative returns
    cum_raw = (1 + result["returns"]).cumprod()
    cum_vt = (1 + result["vt_returns"]).cumprod()

    # Max drawdown
    dd_raw = (cum_raw / cum_raw.cummax() - 1).min()
    dd_vt = (cum_vt / cum_vt.cummax() - 1).min()

    print("\nDrawdown comparison:")
    print(f"Raw max drawdown: {dd_raw:.2%}")
    print(f"Vol-targeted max drawdown: {dd_vt:.2%}")

    drawdown_rows.append({
    "Asset": asset,
    "Raw_Max_Drawdown": dd_raw,
    "Vol_Targeted_Max_Drawdown": dd_vt,
    "Drawdown_Reduction": 1 - (dd_vt / dd_raw)
    })

summary_table = pd.DataFrame(summary_rows)

summary_table = summary_table.drop_duplicates(
    subset=["Asset", "Regime"]
).reset_index(drop=True)

print("\n================ SUMMARY TABLE ================\n")
print(summary_table)

# ================= DRAW DOWN SUMMARY TABLE =================

drawdown_table = pd.DataFrame(drawdown_rows)

formatted_dd = drawdown_table.copy()
for col in ["Raw_Max_Drawdown", "Vol_Targeted_Max_Drawdown", "Drawdown_Reduction"]:
    formatted_dd[col] = formatted_dd[col].apply(lambda x: f"{x:.2%}")

print("\n================ DRAWDOWN SUMMARY TABLE ================\n")
print(formatted_dd)