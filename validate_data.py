
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

# Find the master and NAV files by their filenames
fund_file = next(RAW_DIR.glob("*fund_master.csv"))
nav_file = next(RAW_DIR.glob("*nav_history.csv"))

funds = pd.read_csv(fund_file)
nav = pd.read_csv(nav_file)

# Compare unique scheme codes
fund_codes = set(funds["amfi_code"].dropna())
nav_codes = set(nav["amfi_code"].dropna())

missing_in_nav = sorted(fund_codes - nav_codes)
unknown_in_master = sorted(nav_codes - fund_codes)

print("Fund master schemes:", len(fund_codes))
print("NAV history schemes:", len(nav_codes))
print("Master schemes missing from NAV:", len(missing_in_nav))
print("NAV schemes missing from master:", len(unknown_in_master))

print("\nMissing NAV codes:")
print(missing_in_nav)

print("\nNAV codes not in master:")
print(unknown_in_master)

# Save a report
pd.DataFrame({
    "amfi_code": missing_in_nav
}).to_csv(REPORT_DIR / "missing_scheme_codes.csv", index=False)

print("\nReport saved to reports/missing_scheme_codes.csv")
