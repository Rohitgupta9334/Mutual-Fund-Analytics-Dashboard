
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")
REPORT_DIR = Path("reports")

file = next(DATA_DIR.glob("*portfolio_holdings.csv"))
df = pd.read_csv(file)

df["weight_pct"] = pd.to_numeric(df["weight_pct"], errors="coerce")
df["market_value_cr"] = pd.to_numeric(
    df["market_value_cr"], errors="coerce"
)

# Total holding weight for each scheme
scheme_summary = (
    df.groupby("amfi_code")
    .agg(
        stock_count=("stock_symbol", "nunique"),
        total_weight_pct=("weight_pct", "sum"),
        total_market_value_cr=("market_value_cr", "sum"),
    )
    .reset_index()
    .round(2)
    .sort_values("total_market_value_cr", ascending=False)
)

print("Scheme-wise portfolio summary:")
print(scheme_summary.to_string(index=False))

# Sector exposure across all supplied holding records
sector_summary = (
    df.groupby("sector")
    .agg(
        holding_records=("stock_symbol", "count"),
        total_market_value_cr=("market_value_cr", "sum"),
        average_weight_pct=("weight_pct", "mean"),
    )
    .reset_index()
    .round(2)
    .sort_values("total_market_value_cr", ascending=False)
)

print("\nSector summary:")
print(sector_summary.to_string(index=False))

REPORT_DIR.mkdir(exist_ok=True)
scheme_summary.to_csv(
    REPORT_DIR / "scheme_portfolio_summary.csv", index=False
)
sector_summary.to_csv(
    REPORT_DIR / "portfolio_sector_summary.csv", index=False
)

print("\nSaved reports:")
print("reports/scheme_portfolio_summary.csv")
print("reports/portfolio_sector_summary.csv")
