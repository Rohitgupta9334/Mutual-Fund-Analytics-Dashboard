
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

for file in RAW_DIR.glob("*.csv"):
    df = pd.read_csv(file)

    # Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)

    # Convert common date columns to datetime
    for column in ["date", "transaction_date", "portfolio_date", "month", "launch_date"]:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    # Save cleaned file
    output_file = PROCESSED_DIR / file.name
    df.to_csv(output_file, index=False)

    print(f"\nFile: {file.name}")
    print(f"Duplicate rows removed: {removed}")
    print(f"Saved to: {output_file}")

print("\nPreprocessing completed!")
