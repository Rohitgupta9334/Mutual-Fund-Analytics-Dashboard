
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

nav_file = REPORT_DIR / "nav_based_annualized_returns.csv"
performance_file = next(
    DATA_DIR.glob("*scheme_performance*.csv")
)

nav_returns = pd.read_csv(nav_file)
performance = pd.read_csv(performance_file)

reported_columns = [
    "amfi_code",
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
]

reported = performance[reported_columns].copy()

comparison = nav_returns.merge(
    reported,
    on="amfi_code",
    how="left",
    suffixes=("_calculated", "_reported"),
    indicator=True
)

print("Total NAV schemes:", len(nav_returns))
print(
    "Matched performance schemes:",
    (comparison["_merge"] == "both").sum()
)
print(
    "Unmatched schemes:",
    (comparison["_merge"] != "both").sum()
)

for period in ["1yr", "3yr", "5yr"]:
    calculated = f"return_{period}_pct_calculated"
    reported_col = f"return_{period}_pct_reported"
    difference_col = f"{period}_difference"

    comparison[difference_col] = (
        comparison[calculated] - comparison[reported_col]
    ).abs()

    valid = comparison[difference_col].dropna()

    print(f"\n{period} comparisons:")
    print("Comparable values:", len(valid))

    if len(valid) > 0:
        print(
            "Mean absolute difference:",
            round(valid.mean(), 2),
            "percentage points"
        )
        print(
            "Maximum absolute difference:",
            round(valid.max(), 2),
            "percentage points"
        )
    else:
        print("No comparable values available.")

output = REPORT_DIR / "fund_returns_comparison.csv"

print("\nLargest 1-year differences:")

print(
    comparison[
        [
            "amfi_code",
            "return_1yr_pct_calculated",
            "return_1yr_pct_reported",
            "1yr_difference",
            "return_3yr_pct_calculated",
            "return_3yr_pct_reported",
            "3yr_difference",
        ]
    ]
    .sort_values("1yr_difference", ascending=False)
    .head(10)
    .round(2)
    .to_string(index=False)
)

comparison.to_csv(output, index=False)

print(f"\nReport saved to {output}")

