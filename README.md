# Volatility Regime Detection and Risk Analysis

This project implements a multi-asset volatility regime framework inspired by Quantitative Investment Strategies (QIS) and volatility-control index design.

## Methodology
- Daily log returns computed from NSE equity prices
- 21-day realised volatility estimation
- Quantile-based volatility regime classification (Low / Medium / High)
- Regime persistence analysis via transition matrices
- Regime-conditional Value-at-Risk (VaR) and Expected Shortfall (ES)
- Volatility-targeted overlay targeting 15% annualised volatility

## Assets Analysed
- Infosys
- Reliance
- HDFC Bank
- NIFTY 50

## Key Results
- Volatility regimes exhibit strong persistence (≈90–95%)
- Tail risk increases sharply in high-volatility regimes
- Volatility targeting reduces maximum drawdowns by ~86–90% across assets
  (e.g., Infosys −40.6% → −5.2%)

## Usage
```bash
python main.py
