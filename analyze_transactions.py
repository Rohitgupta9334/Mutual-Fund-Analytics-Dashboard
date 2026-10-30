
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")
REPORT_DIR = Path("reports")

file = next(DATA_DIR.glob("*investor_transactions.csv"))
df = pd.read_csv(file)

print("Columns:", df.columns.tolist())
print("\nDataset shape:", df.shape)
print("\nFirst five rows:")
print(df.head().to_string(index=False))

print("\nData types:")
print(df.dtypes.to_string())

print("\nMissing values:")
print(df.isnull().sum().to_string())

# Identify likely transaction type and amount columns
type_col = next(
    (c for c in df.columns if "transaction_type" in c.lower()
     or "txn_type" in c.lower()),
    None
)

amount_col = next(
    (c for c in df.columns if "amount" in c.lower()),
    None
)

if type_col is None or amount_col is None:
    print("\nCould not automatically identify transaction type/amount.")
    print("Use the column names printed above to adjust the script.")
else:
    df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")

    print("\nTransaction count by type:")
    print(df[type_col].value_counts(dropna=False).to_string())

    summary = (
        df.groupby(type_col, dropna=False)
        .agg(
            transaction_count=(amount_col, "count"),
            total_amount=(amount_col, "sum"),
            average_amount=(amount_col, "mean"),
        )
        .reset_index()
        .round(2)
    )

    print("\nTransaction amount summary:")
    print(summary.to_string(index=False))

    REPORT_DIR.mkdir(exist_ok=True)
    output = REPORT_DIR / "transaction_type_analysis.csv"
    summary.to_csv(output, index=False)
    print(f"\nSaved report to {output}")

