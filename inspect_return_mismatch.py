
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")
nav_file = next(DATA_DIR.glob("*nav_history.csv"))

nav = pd.read_csv(nav_file)
nav["date"] = pd.to_datetime(nav["date"])
nav["nav"] = pd.to_numeric(nav["nav"])

# Investigate Axis Small Cap
code = 119095

df = nav[nav["amfi_code"] == code].copy()
df = df.sort_values("date")

df["daily_change_pct"] = df["nav"].pct_change() * 100

print("Scheme code:", code)
print("Total records:", len(df))

print("\nNAV observations around May 2025:")
print(
    df[
        (df["date"] >= "2025-04-01")
        & (df["date"] <= "2025-06-30")
    ][["date", "nav", "daily_change_pct"]]
    .to_string(index=False)
)

print("\nNAV observations around May 2026:")
print(
    df[
        (df["date"] >= "2026-04-01")
        & (df["date"] <= "2026-05-29")
    ][["date", "nav", "daily_change_pct"]]
    .to_string(index=False)
)

print("\nLargest daily percentage changes:")
print(
    df.assign(
        absolute_change=df["daily_change_pct"].abs()
    )
    .sort_values("absolute_change", ascending=False)
    [["date", "nav", "daily_change_pct"]]
    .head(10)
    .round(4)
    .to_string(index=False)
)
