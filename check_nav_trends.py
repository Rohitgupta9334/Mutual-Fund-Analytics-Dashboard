
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")
nav_file = next(DATA_DIR.glob("*nav_history.csv"))

df = pd.read_csv(nav_file)
df["date"] = pd.to_datetime(df["date"])
df["nav"] = pd.to_numeric(df["nav"])

df = df.sort_values(["amfi_code", "date"])

summary = (
    df.groupby("amfi_code")
    .agg(
        first_date=("date", "min"),
        last_date=("date", "max"),
        first_nav=("nav", "first"),
        last_nav=("nav", "last"),
        records=("nav", "count"),
        minimum_nav=("nav", "min"),
        maximum_nav=("nav", "max"),
    )
    .reset_index()
)

summary["total_change_pct"] = (
    (summary["last_nav"] / summary["first_nav"]) - 1
) * 100

print("Scheme-wise NAV summary:")
print(
    summary.sort_values("total_change_pct")
    .round(2)
    .to_string(index=False)
)

output = Path("reports/nav_trend_summary.csv")
output.parent.mkdir(exist_ok=True)
summary.to_csv(output, index=False)

print(f"\nSaved report to {output}")
