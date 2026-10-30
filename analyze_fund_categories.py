
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")
REPORT_DIR = Path("reports")

file = next(DATA_DIR.glob("*scheme_performance*.csv"))
df = pd.read_csv(file)

# Convert numeric columns safely
numeric_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "aum_crore",
    "expense_ratio_pct",
    "sharpe_ratio",
    "std_dev_ann_pct",
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

summary = (
    df.groupby("category", dropna=False)
    .agg(
        scheme_count=("amfi_code", "nunique"),
        average_1yr_return_pct=("return_1yr_pct", "mean"),
        average_3yr_return_pct=("return_3yr_pct", "mean"),
        average_5yr_return_pct=("return_5yr_pct", "mean"),
        total_aum_crore=("aum_crore", "sum"),
        average_expense_ratio_pct=("expense_ratio_pct", "mean"),
        average_sharpe_ratio=("sharpe_ratio", "mean"),
        average_annual_volatility_pct=("std_dev_ann_pct", "mean"),
    )
    .reset_index()
)

summary = summary.round(2)

print("Fund Category Analysis")
print(summary.to_string(index=False))

REPORT_DIR.mkdir(exist_ok=True)
output = REPORT_DIR / "fund_category_analysis.csv"
summary.to_csv(output, index=False)

print(f"\nSaved report to {output}")
