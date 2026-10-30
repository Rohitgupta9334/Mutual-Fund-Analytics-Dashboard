
from pathlib import Path
import pandas as pd

file = next(
    Path("data/processed").glob("*monthly_sip_inflows.csv")
)

df = pd.read_csv(file)

# Display rows where YoY growth is missing
missing = df[df["yoy_growth_pct"].isna()]

print("Total missing YoY growth values:", len(missing))
print("\nRows with missing values:")
print(missing.to_string(index=False))

print("\nAll SIP data (month and YoY growth):")
print(
    df[["month", "yoy_growth_pct"]]
    .sort_values("month")
    .to_string(index=False)
)
