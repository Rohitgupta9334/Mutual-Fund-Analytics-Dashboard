from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

ROOT = Path.cwd()
DATA = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

def load(pattern):
    files = list(DATA.glob(pattern))
    if not files:
        raise FileNotFoundError(f"Missing file: {pattern}")
    return pd.read_csv(files[0])

nav = load("*nav_history*.csv")
bench = load("*benchmark_indices*.csv")
funds = load("*fund_master*.csv")
returns3 = pd.read_csv(REPORTS / "nav_based_annualized_returns.csv")

nav["date"] = pd.to_datetime(nav["date"])
bench["date"] = pd.to_datetime(bench["date"])
nav = nav.sort_values(["amfi_code", "date"])
bench = bench.sort_values(["index_name", "date"])

nav["daily_return"] = nav.groupby("amfi_code")["nav"].pct_change()
bench["daily_return"] = bench.groupby("index_name")["close_value"].pct_change()

# Alpha and Beta against NIFTY 100 for every fund
nifty = bench[bench["index_name"] == "NIFTY100"][["date", "daily_return"]]
alpha_rows = []

for code, group in nav.groupby("amfi_code"):
    paired = group[["date", "daily_return"]].merge(
        nifty, on="date", suffixes=("_fund", "_market")
    ).dropna()

    if len(paired) < 30:
        continue

    result = linregress(
        paired["daily_return_market"],
        paired["daily_return_fund"]
    )

    alpha_rows.append({
        "amfi_code": code,
        "observations": len(paired),
        "alpha_annualized_pct": result.intercept * 252 * 100,
        "beta": result.slope,
        "correlation": result.rvalue
    })

alpha = pd.DataFrame(alpha_rows)
alpha = alpha.merge(
    funds[["amfi_code", "scheme_name", "benchmark"]],
    on="amfi_code", how="left"
)
alpha.to_csv(REPORTS / "alpha_beta.csv", index=False)

# Calculate Sharpe and maximum drawdown from NAV
risk_rows = []

for code, group in nav.groupby("amfi_code"):
    group = group.dropna(subset=["daily_return"]).copy()
    if group.empty:
        continue

    daily = group["daily_return"]
    risk_free_daily = (1 + 0.065) ** (1 / 252) - 1
    volatility = daily.std()

    sharpe = (
        ((daily.mean() - risk_free_daily) / volatility) * np.sqrt(252)
        if volatility and not np.isnan(volatility) else np.nan
    )

    running_max = group["nav"].cummax()
    drawdown = group["nav"] / running_max - 1

    risk_rows.append({
        "amfi_code": code,
        "sharpe_ratio": sharpe,
        "max_drawdown_pct": drawdown.min() * 100
    })

risk = pd.DataFrame(risk_rows)

# Build scorecard
score = returns3[["amfi_code", "return_3yr_pct"]].merge(
    funds[["amfi_code", "scheme_name", "category", "expense_ratio_pct"]],
    on="amfi_code", how="left"
).merge(alpha[["amfi_code", "alpha_annualized_pct", "beta"]],
        on="amfi_code", how="left").merge(
    risk, on="amfi_code", how="left"
)

# Percentile ranks: higher is better, except expense and drawdown
score["return_rank"] = score["return_3yr_pct"].rank(pct=True) * 100
score["sharpe_rank"] = score["sharpe_ratio"].rank(pct=True) * 100
score["alpha_rank"] = score["alpha_annualized_pct"].rank(pct=True) * 100
score["expense_rank"] = (
    score["expense_ratio_pct"].rank(ascending=False, pct=True) * 100
)
score["drawdown_rank"] = (
    score["max_drawdown_pct"].rank(pct=True) * 100
)

score["score"] = (
    0.30 * score["return_rank"]
    + 0.25 * score["sharpe_rank"]
    + 0.20 * score["alpha_rank"]
    + 0.15 * score["expense_rank"]
    + 0.10 * score["drawdown_rank"]
)

score = score.sort_values("score", ascending=False)
score.to_csv(REPORTS / "fund_scorecard.csv", index=False)

# Three-year comparison chart: top five funds vs NIFTY 50 and NIFTY 100
top5 = score.dropna(subset=["score"]).head(5)["amfi_code"].tolist()
latest_date = nav["date"].max()
start_date = latest_date - pd.DateOffset(years=3)

plt.figure(figsize=(13, 7))

for code in top5:
    g = nav[
        (nav["amfi_code"] == code)
        & (nav["date"] >= start_date)
    ].sort_values("date")

    if len(g) > 1:
        indexed = g["nav"] / g["nav"].iloc[0] * 100
        name = score.loc[score["amfi_code"] == code, "scheme_name"].iloc[0]
        plt.plot(g["date"], indexed, label=name[:35])

for index_name in ["NIFTY50", "NIFTY100"]:
    g = bench[
        (bench["index_name"] == index_name)
        & (bench["date"] >= start_date)
    ].sort_values("date")

    if len(g) > 1:
        indexed = g["close_value"] / g["close_value"].iloc[0] * 100
        plt.plot(g["date"], indexed, linestyle="--", label=index_name)

plt.title("Top 5 Mutual Funds vs NIFTY 50 and NIFTY 100 (3 Years)")
plt.xlabel("Date")
plt.ylabel("Growth of 100 (rebased)")
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(REPORTS / "benchmark_comparison.png", dpi=200)
plt.close()

print("\nSUCCESS - Generated files:")
for name in ["fund_scorecard.csv", "alpha_beta.csv", "benchmark_comparison.png"]:
    path = REPORTS / name
    print(name, "-", path.stat().st_size, "bytes")

print("\nFunds in scorecard:", len(score))
print("Funds with Alpha/Beta:", len(alpha))
