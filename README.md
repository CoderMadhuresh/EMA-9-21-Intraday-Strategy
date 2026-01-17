# EMA 9/21 Crossover Intraday Trading Strategy

## Overview
This project implements a **fully automated backtesting framework** for an **EMA 9/21 crossover trading strategy** using **Hourly (1H) data** for **NSE-listed stocks**.  
The strategy is demonstrated on **RELIANCE** Equity  using **two year of historical data**.

The script:
- Downloads historical data using **Yahoo Finance**
- Generates **buy/sell signals** based on EMA crossovers
- Executes **long and short trades**
- Tracks **PnL, equity curve, and performance metrics**
- Produces **candlestick charts with EMA overlays**
- Saves **trade logs and metrics to CSV**

## Strategy Logic

### Buy Signal (Long Entry)
- **EMA 9 crosses above EMA 21**
- Indicates short-term bullish momentum

### Sell Signal (Short Entry)
- **EMA 9 crosses below EMA 21**
- Indicates short-term bearish momentum

### Position Rules
- Only **one open position at a time**
- On opposite signal:
  - Existing position is **closed**
  - New position is **opened immediately**

## Configuration Parameters

| Parameter | Value |
|---------|-------|
| Ticker | `RELIANCE.NS` |
| Interval | `1h` |
| Period | `1y` |
| Initial Capital | ₹100,000 |
| Quantity per Trade | 100 shares |
| Timezone | Asia/Kolkata (IST) |

## Libraries Used

- `yfinance` – Market data
- `pandas`, `numpy` – Data processing
- `mplfinance` – Candlestick charting
- `matplotlib` – Equity curve visualization

Install dependencies:
```bash
pip install yfinance pandas numpy matplotlib mplfinance
```

## Performance Metrics

This section analyzes the **EMA 9/21 crossover strategy** over a **2-year backtest period**, capturing multiple market regimes including trends, consolidations, and drawdowns.

## Metrics Summary

| Category | Net PnL (₹) | Net PnL % | Trades | Wins | Losses | Win Rate % | Profit Factor | Max Win (₹) | Max Loss (₹) |
|--------|------------|-----------|--------|------|--------|------------|---------------|-------------|--------------|
| OVERALL | 40,434.95 | 40.43% | 142 | 48 | 94 | 33.80% | 1.29 | 19,289.99 | -11,467.49 |
| LONG | 24,722.47 | 24.72% | 71 | 26 | 45 | 36.62% | 1.36 | 19,289.99 | -11,467.49 |
| SHORT | 15,712.48 | 15.71% | 71 | 22 | 49 | 30.99% | 1.22 | 12,375.00 | -6,500.00 |

## Net PnL & Return Analysis

- **Initial Capital:** ₹100,000  
- **Final Capital:** ₹140,434.95  
- **Absolute Return:** **+40.43% over 2 years**
- Performance remains **positive across both long and short trades**
- Long trades contribute ~61% of total profits

Compared to the 1-year test, returns are lower on an annualized basis, indicating **market regime sensitivity** and the impact of **sideways phases**.


## Win Rate vs Profit Factor

- **Win Rate:** ~34% (low by design)
- **Profit Factor:** **1.29 (acceptable but modest)**

This confirms:
- Strategy still follows a **trend-following payoff structure**
- Increased trade frequency introduces **whipsaws**
- Profitability is maintained, but edge is thinner

The strategy survives noise but benefits from **filters or stops**.


##  Risk Characteristics

### Maximum Trades
- **Max Winning Trade:** ₹19,289
- **Max Losing Trade:** ₹11,467
- **Reward-to-Risk (Max):** ~1.68 : 1

This highlights:
- Larger adverse moves during extended consolidations
- EMA exits alone are insufficient risk control in range-bound markets

## Long vs Short Performance

### Long Trades
- Higher profit factor (1.36)
- Better win rate (36.6%)
- Benefit from long-term equity bullish bias

### Short Trades
- Lower profitability and hit rate
- Still net positive across 2 years
- More sensitive to false breakdowns

 Strategy remains **bi-directional but long-biased**.

## CAGR (Compounded Annual Growth Rate)

CAGR is calculated using:

```text
CAGR = (Final Capital / Initial Capital)^(1 / Years) - 1
CAGR ≈ 18.6% per annum
```
## Output Graphs

### RELIANCE.NS (1H) – EMA 9 / 21 Crossover Strategy with Trade Signals
![](https://github.com/CoderMadhuresh/EMA-9-21-Intraday-Strategy/blob/main/Assets/Figure%201.png)
![](https://github.com/CoderMadhuresh/EMA-9-21-Intraday-Strategy/blob/main/Assets/Figure%202.png)

### Straegy Equity Curve
![](https://github.com/CoderMadhuresh/EMA-9-21-Intraday-Strategy/blob/main/Assets/Figure%203.png)

