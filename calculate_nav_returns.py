

from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

file = next(DATA_DIR.glob("*nav_history.csv"))
df = pd.read_csv(file)

df["date"] = pd.to_datetime(df["date"], errors="raise")
df["nav"] = pd.to_numeric(df["nav"], errors="raise")

df = df.sort_values(["amfi_code", "date"])

# Use the latest available NAV for each scheme
latest = df.groupby("amfi_code").tail(1).copy()
latest = latest.rename(
    columns={"date": "latest_date", "nav": "latest_nav"}
)

results = []

for code, group in df.groupby("amfi_code"):
    group = group.sort_values("date")
    latest_row = group.iloc[-1]

    record = {
        "amfi_code": code,
        "latest_date": latest_row["date"],
        "latest_nav": latest_row["nav"],
    }

    for years in [1, 3, 5]:
        target_date = latest_row["date"] - pd.DateOffset(years=years)

        # Find the closest available NAV on or before target date
        eligible = group[group["date"] <= target_date]

        if eligible.empty:
            record[f"return_{years}yr_pct"] = None
            continue

        base_row = eligible.iloc[-1]
        base_nav = base_row["nav"]

        if base_nav <= 0:
            record[f"return_{years}yr_pct"] = None
        else:
            record[f"return_{years}yr_pct"] = (
                (latest_row["nav"] / base_nav) ** (1 / years) - 1
            ) * 100

    results.append(record)

returns = pd.DataFrame(results)

output = REPORT_DIR / "nav_based_annualized_returns.csv"
returns.to_csv(output, index=False)

print("Schemes analyzed:", len(returns))
print("Latest NAV date:", returns["latest_date"].max())
print("\nAvailable return values:")
print(
    returns[
        ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct"]
    ].notna().sum()
)

print("\nSample results:")
print(returns.head(10).round(2).to_string(index=False))

print(f"\nReport saved to {output}")
