
from pathlib import Path
import pandas as pd

# Folder containing the original CSV files
RAW_DIR = Path("data/raw")

csv_files = sorted(RAW_DIR.glob("*.csv"))

print(f"Total CSV files found: {len(csv_files)}")

for file in csv_files:
    print("\n" + "=" * 60)
    print(f"File: {file.name}")

    try:
        df = pd.read_csv(file)

        print("Shape (rows, columns):", df.shape)
        print("\nColumn names:")
        print(df.columns.tolist())

        print("\nData types:")
        print(df.dtypes)

        print("\nFirst 5 rows:")
        print(df.head())

        print("\nMissing values:")
        print(df.isnull().sum())

        print("\nDuplicate rows:", df.duplicated().sum())

    except Exception as e:
        print(f"Error reading {file.name}: {e}")
