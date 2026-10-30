
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

file = next(DATA_DIR.glob("*nav_history.csv"))
df = pd.read_csv(file)

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

print("Total NAV records:", len(df))
print("Invalid dates:", df["date"].isna().sum())
print("Missing or invalid NAV values:", df["nav"].isna().sum())
print("Zero or negative NAV values:", (df["nav"] <= 0).sum())

duplicates = df.duplicated(
    subset=["amfi_code", "date"], keep=False
)

print("Duplicate scheme-date records:", duplicates.sum())

print("\nDate range:")
print("Start:", df["date"].min())
print("End:", df["date"].max())

print("\nNAV summary:")
print(df["nav"].describe())

# Save rows requiring investigation
issues = df[
    df["date"].isna()
    | df["nav"].isna()
    | (df["nav"] <= 0)
    | duplicates
]

issues.to_csv(
    REPORT_DIR / "nav_validation_issues.csv",
    index=False
)

print("\nIssue report saved to reports/nav_validation_issues.csv")
