
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/processed")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

reports = []

for file in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(file)

    missing_count = df.isnull().sum().sum()
    missing_columns = df.columns[df.isnull().any()].tolist()

    reports.append({
        "file_name": file.name,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": missing_count,
        "columns_with_missing_values": ", ".join(missing_columns) or "None"
    })

    print(f"\nFile: {file.name}")
    print(f"Rows: {len(df)}")
    print(f"Missing values: {missing_count}")
    print(f"Columns with missing values: {missing_columns or 'None'}")

report_df = pd.DataFrame(reports)
report_df.to_csv(REPORT_DIR / "data_quality_report.csv", index=False)

print("\nData quality report saved to reports/data_quality_report.csv")
