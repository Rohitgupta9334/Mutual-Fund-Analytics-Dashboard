
from pathlib import Path
import sqlite3
import pandas as pd

DATA_DIR = Path("data/processed")
DB_DIR = Path("data")
DB_PATH = DB_DIR / "mutual_funds.db"

DB_DIR.mkdir(exist_ok=True)

csv_files = list(DATA_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV files found in data/processed")

with sqlite3.connect(DB_PATH) as conn:
    for file in csv_files:
        table_name = file.stem

        # SQLite table names should be simple identifiers
        table_name = (
            table_name.lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("(", "")
            .replace(")", "")
        )

        df = pd.read_csv(file)
        df.to_sql(table_name, conn, if_exists="replace", index=False)

        print(f"Loaded {file.name} -> {table_name} ({len(df)} rows)")

    tables = pd.read_sql_query(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name",
        conn,
    )

print("\nDatabase created at:", DB_PATH)
print("\nTables created:")
print(tables.to_string(index=False))
