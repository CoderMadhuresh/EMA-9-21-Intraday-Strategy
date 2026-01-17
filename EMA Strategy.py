import yfinance as yf
import mplfinance as mpf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)

# PARAMETERS
ticker = "RELIANCE.NS"
interval = "1h"
period = "2y"
initial_capital = 100000.0
quantity = 100

# DOWNLOAD DATA
data = yf.download(
    tickers=ticker,
    period=period,
    interval=interval,
    auto_adjust=False,
    progress=False
)

# FIX MULTIINDEX
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# TIMEZONE → IST
data.index = data.index.tz_convert("Asia/Kolkata")

# CLEAN OHLC
ohlc_cols = ["Open", "High", "Low", "Close", "Volume"]
data[ohlc_cols] = data[ohlc_cols].apply(pd.to_numeric, errors="coerce")
data.dropna(subset=ohlc_cols, inplace=True)

# EMA CALCULATION
data["EMA_9"] = data["Close"].ewm(span=9, adjust=False).mean()
data["EMA_21"] = data["Close"].ewm(span=21, adjust=False).mean()

# SIGNALS
data["Signal"] = 0
data.loc[
    (data["EMA_9"] > data["EMA_21"]) &
    (data["EMA_9"].shift(1) <= data["EMA_21"].shift(1)),
    "Signal"
] = 1
data.loc[
    (data["EMA_9"] < data["EMA_21"]) &
    (data["EMA_9"].shift(1) >= data["EMA_21"].shift(1)),
    "Signal"
] = -1
print(data)

# PRICE CHART WITH EMA & SIGNALS
buy_scatter = pd.Series(index=data.index, dtype=float)
sell_scatter = pd.Series(index=data.index, dtype=float)

buy_scatter[data["Signal"] == 1] = data["Close"]
sell_scatter[data["Signal"] == -1] = data["Close"]

price_plots = [
    mpf.make_addplot(data["EMA_9"], color="blue", width=1.2),
    mpf.make_addplot(data["EMA_21"], color="orange", width=1.2),
    mpf.make_addplot(buy_scatter, type="scatter", marker="o", color="green", markersize=80),
    mpf.make_addplot(sell_scatter, type="scatter", marker="o", color="red", markersize=80)
]

mpf.plot(
    data,
    type="candle",
    style="yahoo",
    addplot=price_plots,
    volume=True,
    title="RELIANCE.NS | 1H | EMA 9 / EMA 21 Crossover",
    ylabel="Price",
    figsize=(14, 7)
)

# TRADE SIMULATION
capital = initial_capital
position = None
entry_price = None
trade_log = []

for idx, row in data.iterrows():
    signal = row["Signal"]
    price = row["Close"]

    if signal == 1 and position is None:
        position = "LONG"
        entry_price = price
        trade_log.append({"Type": "BUY", "Entry Date": idx, "Entry Price": price})

    elif signal == -1 and position is None:
        position = "SHORT"
        entry_price = price
        trade_log.append({"Type": "SELL", "Entry Date": idx, "Entry Price": price})

    elif signal == -1 and position == "LONG":
        pnl = (price - entry_price) * quantity
        capital += pnl
        trade_log[-1].update({"Exit Date": idx, "Exit Price": price, "PnL": pnl})
        position = "SHORT"
        entry_price = price
        trade_log.append({"Type": "SELL", "Entry Date": idx, "Entry Price": price})

    elif signal == 1 and position == "SHORT":
        pnl = (entry_price - price) * quantity
        capital += pnl
        trade_log[-1].update({"Exit Date": idx, "Exit Price": price, "PnL": pnl})
        position = "LONG"
        entry_price = price
        trade_log.append({"Type": "BUY", "Entry Date": idx, "Entry Price": price})

# Close last trade
if position:
    last_price = data.iloc[-1]["Close"]
    pnl = (last_price - entry_price) * quantity if position == "LONG" else (entry_price - last_price) * quantity
    capital += pnl
    trade_log[-1].update({"Exit Date": data.index[-1], "Exit Price": last_price, "PnL": pnl})

trade_df = pd.DataFrame(trade_log)

# ADD CUMULATIVE PnL
trade_df["Cumulative_PnL"] = trade_df["PnL"].cumsum()
print(trade_df)

# SAVE TRADE LOG TO CSV
trade_df.to_csv(f"Trade Log {ticker}.csv", index=False)


# PERFORMANCE METRICS
def metrics_block(df, label):
    wins = df[df["PnL"] > 0]
    losses = df[df["PnL"] < 0]
    gp = wins["PnL"].sum()
    gl = abs(losses["PnL"].sum())

    return {
        "Category": label,
        "Net_PnL": df["PnL"].sum(),
        "Net_PnL_%": (df["PnL"].sum() / initial_capital) * 100,
        "Trades": len(df),
        "Wins": len(wins),
        "Losses": len(losses),
        "Win_Rate_%": (len(wins) / len(df)) * 100 if len(df) else 0,
        "Profit_Factor": gp / gl if gl else np.nan,
        "Max_Win": wins["PnL"].max(),
        "Max_Loss": losses["PnL"].min()
    }


overall_metrics = metrics_block(trade_df, "OVERALL")
long_metrics = metrics_block(trade_df[trade_df["Type"] == "BUY"], "LONG")
short_metrics = metrics_block(trade_df[trade_df["Type"] == "SELL"], "SHORT")

metrics_df = pd.DataFrame([overall_metrics, long_metrics, short_metrics])

# SAVE METRICS TO CSV
metrics_df.to_csv(f"Performance Metrics {ticker}.csv", index=False)

print("\n========= METRICS TABLE =========\n")
print(metrics_df)

# EQUITY CURVE
equity = initial_capital + trade_df["PnL"].cumsum()
equity.index = trade_df["Exit Date"]
plt.figure(figsize=(14, 7))
plt.plot(equity.index, equity, label="Strategy Equity", linewidth=2)
plt.title("Equity Curve")
plt.xlabel("Date")
plt.ylabel("Capital (₹)")
plt.legend()
plt.grid(True)
plt.show()
