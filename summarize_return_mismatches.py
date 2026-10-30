
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")
REPORT_DIR = Path("reports")

nav_file = next(DATA_DIR.glob("*nav_history.csv"))
performance_file = next(DATA_DIR.glob("*scheme_performance*.csv"))

nav = pd.read_csv(nav_file)
performance = pd.read_csv(performance_file)

nav["date"] = pd.to_datetime(nav["date"])
nav["nav"] = pd.to_numeric(nav["nav"])

nav = nav.sort_values(["amfi_code", "date"])
latest_date = nav["date"].max()

results = []

for code, group in nav.groupby("amfi_code"):
    group = group.sort_values("date")
    latest = group.iloc[-1]

    row = performance[performance["amfi_code"] == code]
    if row.empty:
        continue

    result = {
        "amfi_code": code,
        "scheme_name": row.iloc[0]["scheme_name"],
        "latest_nav_date": latest["date"],
    }

    for years in [1, 3]:
        target = latest_date - pd.DateOffset(years=years)
        starting_rows = group[group["date"] <= target]

        if starting_rows.empty:
            result[f"calculated_{years}yr_pct"] = None
            result[f"reported_{years}yr_pct"] = row.iloc[0][f"return_{years}yr_pct"]
            result[f"difference_{years}yr_pct_points"] = None
            continue

        start = starting_rows.iloc[-1]
        actual_years = (latest["date"] - start["date"]).days / 365.25

        calculated = (
            (latest["nav"] / start["nav"]) ** (1 / actual_years) - 1
        ) * 100

        reported = row.iloc[0][f"return_{years}yr_pct"]

        result[f"calculated_{years}yr_pct"] = round(calculated, 2)
        result[f"reported_{years}yr_pct"] = reported
        result[f"difference_{years}yr_pct_points"] = round(
            calculated - reported, 2
        )

    results.append(result)

comparison = pd.DataFrame(results)

for years in [1, 3]:
    col = f"difference_{years}yr_pct_points"
    valid = comparison[col].dropna()

    print(f"\n{years}-year return mismatch summary")
    print("Schemes compared:", len(valid))
    if not valid.empty:
        print("Mean absolute difference:", round(valid.abs().mean(), 2), "percentage points")
        print("Maximum absolute difference:", round(valid.abs().max(), 2), "percentage points")
        print("Within 2 percentage points:", int((valid.abs() <= 2).sum()))

REPORT_DIR.mkdir(exist_ok=True)
output = REPORT_DIR / "return_mismatch_summary.csv"
comparison.to_csv(output, index=False)

print(f"\nSaved report to {output}")
