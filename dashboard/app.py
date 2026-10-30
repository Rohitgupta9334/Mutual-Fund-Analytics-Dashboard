
from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_DIR / "data" / "mutual_funds.db"

st.set_page_config(
    page_title="Mutual Funds Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Mutual Funds Analytics Dashboard")
st.caption("Explore SIP trends, investor transactions, fund-house AUM and portfolio sectors.")

if not DB_PATH.exists():
    st.error(f"Database not found: {DB_PATH}")
    st.stop()


@st.cache_data
def load_query(query):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)


try:
    sip = load_query("""
        SELECT month, sip_inflow_crore
        FROM monthly_sip_inflows
        ORDER BY month
    """)

    transactions = load_query("""
        SELECT transaction_type,
               COUNT(*) AS transaction_count,
               SUM(amount_inr) AS total_amount_inr
        FROM investor_transactions
        GROUP BY transaction_type
        ORDER BY total_amount_inr DESC
    """)

    aum = load_query("""
        SELECT fund_house, aum_crore, date
        FROM aum_by_fund_house
        WHERE date = (SELECT MAX(date) FROM aum_by_fund_house)
        ORDER BY aum_crore DESC
    """)

    sectors = load_query("""
        SELECT sector,
               SUM(market_value_cr) AS market_value_cr
        FROM portfolio_holdings
        GROUP BY sector
        ORDER BY market_value_cr DESC
    """)

except Exception as error:
    st.error(f"Unable to load dashboard data: {error}")
    st.stop()


# Key metrics
total_transactions = int(transactions["transaction_count"].sum())
total_sip = float(sip["sip_inflow_crore"].sum())
latest_aum = float(aum["aum_crore"].sum())

col1, col2, col3 = st.columns(3)

col1.metric("Investor Transactions", f"{total_transactions:,}")
col2.metric("SIP Inflow (₹ crore)", f"{total_sip:,.0f}")
col3.metric("Latest Fund-house AUM (₹ crore)", f"{latest_aum:,.0f}")

st.divider()

# SIP trend
st.subheader("1. Monthly SIP Inflow Trend")
sip["month"] = pd.to_datetime(sip["month"], errors="coerce")
sip = sip.dropna(subset=["month"]).set_index("month")
st.line_chart(sip["sip_inflow_crore"])

# Transaction analysis
left, right = st.columns(2)

with left:
    st.subheader("2. Transactions by Type")
    st.bar_chart(
        transactions.set_index("transaction_type")["transaction_count"]
    )

with right:
    st.subheader("3. Latest AUM by Fund House")
    st.bar_chart(aum.set_index("fund_house")["aum_crore"])

# Sector analysis
st.subheader("4. Portfolio Sector Exposure")
st.bar_chart(sectors.set_index("sector")["market_value_cr"])

# Data tables
with st.expander("View transaction summary"):
    st.dataframe(transactions, use_container_width=True)

with st.expander("View fund-house AUM details"):
    st.dataframe(aum, use_container_width=True)

with st.expander("View sector details"):
    st.dataframe(sectors, use_container_width=True)

st.caption(
    "Data source: project CSV datasets. "
    "Figures reflect the supplied dataset and may not represent live market data."
)
