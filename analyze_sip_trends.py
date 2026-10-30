
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")
REPORT_DIR = Path("reports")

file = next(DATA_DIR.glob("*monthly_sip_inflows.csv"))
df = pd.read_csv(file)

print("Columns:", df.columns.tolist())

# Detect the date and inflow columns
date_col = next(
    (c for c in df.columns if "date" in c.lower() or "month" in c.lower()),
    None
)
inflow_col = next(
    (c for c in df.columns if "inflow" in c.lower()),
    None
)

if date_col is None or inflow_col is None:
    raise ValueError("Date/month or inflow column not found. Check the column names above.")

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df[inflow_col] = pd.to_numeric(df[inflow_col], errors="coerce")

df = df.dropna(subset=[date_col, inflow_col]).sort_values(date_col)
df["year"] = df[date_col].dt.year

print("\nRecords analyzed:", len(df))
print("Total SIP inflow:", round(df[inflow_col].sum(), 2))

highest = df.loc[df[inflow_col].idxmax()]
lowest = df.loc[df[inflow_col].idxmin()]

print("\nHighest inflow:")
print(highest[[date_col, inflow_col]].to_string())

print("\nLowest inflow:")
print(lowest[[date_col, inflow_col]].to_string())

yearly = (
    df.groupby("year")
    .agg(
        months=(inflow_col, "count"),
        total_inflow=(inflow_col, "sum"),
        average_monthly_inflow=(inflow_col, "mean"),
    )
    .reset_index()
    .round(2)
)

print("\nYear-wise SIP inflow summary:")
print(yearly.to_string(index=False))

REPORT_DIR.mkdir(exist_ok=True)
output = REPORT_DIR / "sip_trend_analysis.csv"
yearly.to_csv(output, index=False)

print(f"\nSaved report to {output}")
