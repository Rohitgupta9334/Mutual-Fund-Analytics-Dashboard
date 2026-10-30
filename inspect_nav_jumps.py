
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")

file = next(DATA_DIR.glob("*nav_history.csv"))
df = pd.read_csv(file)

df["date"] = pd.to_datetime(df["date"])
df["nav"] = pd.to_numeric(df["nav"])

df = df.sort_values(["amfi_code", "date"])

# Calculate daily percentage change within each scheme
df["daily_change_pct"] = (
    df.groupby("amfi_code")["nav"].pct_change() * 100
)

# Flag unusually large daily movements for inspection
jumps = df[df["daily_change_pct"].abs() > 10].copy()

print("Total NAV records:", len(df))
print("Daily changes exceeding +/-10%:", len(jumps))

print("\nLargest daily NAV movements:")
print(
    jumps[
        ["amfi_code", "date", "nav", "daily_change_pct"]
    ]
    .assign(
        absolute_change=lambda x: x["daily_change_pct"].abs()
    )
    .sort_values("absolute_change", ascending=False)
    .drop(columns="absolute_change")
    .head(30)
    .round(2)
    .to_string(index=False)
)

output = Path("reports/nav_jumps_to_review.csv")
output.parent.mkdir(exist_ok=True)
jumps.to_csv(output, index=False)

print(f"\nSaved to {output}")
