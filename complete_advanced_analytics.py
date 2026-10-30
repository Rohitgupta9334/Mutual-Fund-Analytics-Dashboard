from pathlib import Path
import json
import pandas as pd
import numpy as np

root = Path.cwd()
data = root / "data" / "processed"
reports = root / "reports"
reports.mkdir(exist_ok=True)

def read(pattern):
    files = list(data.glob(pattern))
    if not files:
        raise FileNotFoundError(pattern)
    return pd.read_csv(files[0])

transactions = read("*investor_transactions*.csv")
nav = read("*nav_history*.csv")
funds = read("*fund_master*.csv")
metrics = pd.read_csv(reports / "fund_performance_metrics.csv")

# 1. Historical 95% VaR
nav["date"] = pd.to_datetime(nav["date"])
nav = nav.sort_values(["amfi_code", "date"])
nav["daily_return"] = nav.groupby("amfi_code")["nav"].pct_change()

var = (
    nav.groupby("amfi_code")["daily_return"]
    .quantile(0.05)
    .mul(-100)
    .reset_index(name="historical_var_95_daily_pct")
)
var = var.merge(funds[["amfi_code", "scheme_name", "category"]],
                on="amfi_code", how="left")
var.to_csv(reports / "advanced_var_analysis.csv", index=False)

# 2. Investor cohort analysis
transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"]
)
transactions["transaction_month"] = (
    transactions["transaction_date"].dt.to_period("M")
)
first_month = transactions.groupby("investor_id")[
    "transaction_month"
].min().rename("cohort_month")

transactions = transactions.join(first_month, on="investor_id")
transactions["cohort_age_month"] = (
    transactions["transaction_month"].astype("int64")
    - transactions["cohort_month"].astype("int64")
)

cohort = transactions.groupby(
    ["cohort_month", "cohort_age_month"]
).agg(
    active_investors=("investor_id", "nunique"),
    transaction_count=("investor_id", "size"),
    total_amount_inr=("amount_inr", "sum")
).reset_index()

cohort_sizes = (
    transactions.groupby("cohort_month")["investor_id"]
    .nunique().rename("cohort_size")
)
cohort = cohort.join(cohort_sizes, on="cohort_month")
cohort["retention_pct"] = (
    cohort["active_investors"] / cohort["cohort_size"] * 100
)
cohort["cohort_month"] = cohort["cohort_month"].astype(str)
cohort.to_csv(reports / "investor_cohort_analysis.csv", index=False)

# 3. Basic risk-profile-based fund recommendation
recommend = funds.merge(
    metrics[["amfi_code", "annualized_return_pct", "sharpe_ratio"]],
    on="amfi_code", how="left"
)
recommend["expense_score"] = (
    1 - recommend["expense_ratio_pct"].rank(pct=True)
)
recommend["sharpe_score"] = recommend["sharpe_ratio"].rank(pct=True)
recommend["return_score"] = recommend["annualized_return_pct"].rank(pct=True)

recommend["recommendation_score"] = (
    0.50 * recommend["sharpe_score"]
    + 0.30 * recommend["return_score"]
    + 0.20 * recommend["expense_score"]
)

recommend["investor_risk_profile"] = recommend["risk_category"].map({
    "Low": "Conservative",
    "Moderate": "Conservative",
    "Moderately High": "Moderate",
    "High": "Aggressive",
    "Very High": "Aggressive"
}).fillna("Unclassified")

recommend = recommend.sort_values(
    ["investor_risk_profile", "recommendation_score"],
    ascending=[True, False]
)
recommend.to_csv(reports / "fund_recommendations.csv", index=False)

# Add analysis documentation and executable code to the existing notebook
notebook_path = root / "05_advanced_analytics.ipynb"
if notebook_path.exists():
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
else:
    notebook = {
        "cells": [], "metadata": {},
        "nbformat": 4, "nbformat_minor": 5
    }

markdown = """## Advanced Analytics

### 1. Historical Value at Risk (VaR)
The 95% historical daily VaR estimates the loss threshold from the
5th percentile of observed daily NAV returns.

### 2. Investor Cohort Analysis
Investors are grouped by their first transaction month. Monthly active
investors and retention are calculated for each cohort.

### 3. Fund Recommendation Logic
Funds are ranked using Sharpe ratio, annualized return and expense ratio.
Risk categories are grouped into Conservative, Moderate and Aggressive.
This is an illustrative dataset-based ranking, not financial advice.

Generated CSV outputs are saved in the reports folder.
"""

cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": markdown.splitlines(keepends=True)
}
if not any(
    c["cell_type"] == "markdown"
    and "Advanced Analytics" in "".join(c.get("source", []))
    for c in notebook["cells"]
):
    notebook["cells"].append(cell)

code = """from pathlib import Path
import pandas as pd
import numpy as np

reports = Path("../reports") if Path.cwd().name == "notebooks" else Path("reports")
data = Path("../data/processed") if Path.cwd().name == "notebooks" else Path("data/processed")

print("VaR:", pd.read_csv(reports / "advanced_var_analysis.csv").shape)
print("Cohorts:", pd.read_csv(reports / "investor_cohort_analysis.csv").shape)
print("Recommendations:", pd.read_csv(reports / "fund_recommendations.csv").shape)
"""

notebook["cells"].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": code.splitlines(keepends=True)
})

notebook_path.write_text(
    json.dumps(notebook, indent=2), encoding="utf-8"
)

print("\\nSUCCESS - Advanced analytics generated:")
for name in [
    "advanced_var_analysis.csv",
    "investor_cohort_analysis.csv",
    "fund_recommendations.csv"
]:
    p = reports / name
    print(name, "-", p.stat().st_size, "bytes")

print("\\nNotebook updated:", notebook_path.name)
print("VaR schemes:", len(var))
print("Investor cohorts:", cohort["cohort_month"].nunique())
print("Fund recommendations:", len(recommend))
