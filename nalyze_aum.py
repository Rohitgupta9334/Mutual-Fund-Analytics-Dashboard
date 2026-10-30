
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")
REPORT_DIR = Path("reports")

file = next(DATA_DIR.glob("*aum_by_fund_house.csv"))
df = pd.read_csv(file)

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["aum_crore"] = pd.to_numeric(df["aum_crore"], errors="coerce")

df = df.dropna(subset=["date", "fund_house", "aum_crore"])

# Keep the latest available record for each fund house
latest = (
    df.sort_values("date")
    .groupby("fund_house", as_index=False)
    .tail(1)
    .sort_values("aum_crore", ascending=False)
)

print("Latest AUM date:", latest["date"].max().date())
print("\nFund-house ranking by latest AUM:")
print(
    latest[["fund_house", "date", "aum_crore", "num_schemes"]]
    .to_string(index=False)
)

print("\nTotal AUM across fund houses (₹ crore):",
      round(latest["aum_crore"].sum(), 2))

REPORT_DIR.mkdir(exist_ok=True)
output = REPORT_DIR / "fund_house_latest_aum.csv"
latest.to_csv(output, index=False)

print(f"\nSaved report to {output}")
