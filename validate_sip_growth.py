
from pathlib import Path
import pandas as pd
import numpy as np

file = next(
    Path("data/processed").glob("*monthly_sip_inflows.csv")
)

df = pd.read_csv(file)
df["month"] = pd.to_datetime(df["month"])

# Calculate YoY growth using the same month of the previous year
df["calculated_yoy_pct"] = (
    (df["sip_inflow_crore"] - df["sip_inflow_crore"].shift(12))
    / df["sip_inflow_crore"].shift(12)
    * 100
)

# Compare calculated and provided growth values
df["difference"] = (
    df["yoy_growth_pct"] - df["calculated_yoy_pct"]
).abs()

check = df[df["yoy_growth_pct"].notna()]

print("Rows checked:", len(check))
print(
    "Average absolute difference:",
    round(check["difference"].mean(), 2),
    "percentage points"
)
print(
    "Maximum absolute difference:",
    round(check["difference"].max(), 2),
    "percentage points"
)

print("\nSample comparison:")
print(
    check[
        ["month", "yoy_growth_pct", "calculated_yoy_pct", "difference"]
    ].head(10).round(2).to_string(index=False)
)

# Save detailed comparison
check.to_csv(
    "reports/sip_growth_validation.csv",
    index=False
)

print("\nReport saved to reports/sip_growth_validation.csv")
