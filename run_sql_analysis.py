
import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("data/mutual_funds.db")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

queries = {
    "sql_transaction_summary": """
        SELECT transaction_type,
               COUNT(*) AS transaction_count,
               SUM(amount_inr) AS total_amount_inr,
               ROUND(AVG(amount_inr), 2) AS average_amount_inr
        FROM investor_transactions
        GROUP BY transaction_type
        ORDER BY total_amount_inr DESC
    """,

    "sql_top_sectors": """
        SELECT sector,
               COUNT(*) AS holding_records,
               ROUND(SUM(market_value_cr), 2) AS total_market_value_cr
        FROM portfolio_holdings
        GROUP BY sector
        ORDER BY total_market_value_cr DESC
    """,

    "sql_latest_fund_house_aum": """
        SELECT fund_house, date, aum_crore, num_schemes
        FROM aum_by_fund_house
        WHERE date = (SELECT MAX(date) FROM aum_by_fund_house)
        ORDER BY aum_crore DESC
    """,

    "sql_monthly_sip_yearly": """
        SELECT strftime('%Y', month) AS year,
               COUNT(*) AS months,
               SUM(sip_inflow_crore) AS total_sip_inflow_crore,
               ROUND(AVG(sip_inflow_crore), 2) AS average_monthly_inflow_crore
        FROM monthly_sip_inflows
        GROUP BY strftime('%Y', month)
        ORDER BY year
    """
}

with sqlite3.connect(DB_PATH) as conn:
    for report_name, query in queries.items():
        result = pd.read_sql_query(query, conn)

        print(f"\n--- {report_name} ---")
        print(result.to_string(index=False))

        output = REPORT_DIR / f"{report_name}.csv"
        result.to_csv(output, index=False)
        print(f"Saved: {output}")

print("\nSQL analysis completed successfully.")
