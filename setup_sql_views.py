
import sqlite3
from pathlib import Path

DB_PATH = Path("data/mutual_funds.db")

# Map short names to the existing database tables
views = {
    "investor_transactions":
        "1788499980509_304c1255_08_investor_transactions",
    "portfolio_holdings":
        "1788499982117_e3d6ab98_09_portfolio_holdings",
    "benchmark_indices":
        "1788499982615_f9647ab2_10_benchmark_indices",
    "fund_master":
        "1788499983024_b042c300_01_fund_master",
    "nav_history":
        "1788499983331_4389156d_02_nav_history",
    "aum_by_fund_house":
        "1788499984134_b0cbf625_03_aum_by_fund_house",
    "monthly_sip_inflows":
        "1788499984405_d702a6c6_04_monthly_sip_inflows",
    "category_inflows":
        "1788499984721_4b860901_05_category_inflows",
    "industry_folio_count":
        "1788499985036_da4a0c4a_06_industry_folio_count",
    "scheme_performance":
        "1788499985420_bb134abf_07_scheme_performance_1",
}

with sqlite3.connect(DB_PATH) as conn:
    for view_name, table_name in views.items():
        conn.execute(
            f'CREATE VIEW IF NOT EXISTS "{view_name}" '
            f'AS SELECT * FROM "{table_name}"'
        )
        print(f"Created view: {view_name}")

print("\nAll SQL views are ready.")
