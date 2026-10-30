from pathlib import Path
import pandas as pd
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "reports"
OUTPUT = ROOT / "Mutual_Fund_Analytics_Final_Report.pdf"

doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4,
    rightMargin=0.65 * inch, leftMargin=0.65 * inch,
    topMargin=0.7 * inch, bottomMargin=0.65 * inch
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Title"],
    fontSize=25, leading=32, alignment=TA_CENTER,
    textColor=colors.HexColor("#163A5F"), spaceAfter=18
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading1"],
    fontSize=16, leading=20, textColor=colors.HexColor("#163A5F"),
    spaceBefore=12, spaceAfter=8
))
styles.add(ParagraphStyle(
    name="SubSection", parent=styles["Heading2"],
    fontSize=11, leading=14, textColor=colors.HexColor("#276678"),
    spaceBefore=8, spaceAfter=5
))
styles.add(ParagraphStyle(
    name="BodyCustom", parent=styles["BodyText"],
    fontSize=9, leading=13, spaceAfter=7
))
styles.add(ParagraphStyle(
    name="SmallCustom", parent=styles["BodyText"],
    fontSize=7, leading=9, spaceAfter=2
))

story = []

def para(text, style="BodyCustom"):
    story.append(Paragraph(str(text), styles[style]))

def heading(text):
    para(text, "Section")

def bullet(text):
    para("&#8226; " + text)

def load_report(filename):
    path = REPORTS / filename
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception:
        return None

def fmt(value):
    if pd.isna(value):
        return "-"
    if isinstance(value, float):
        return f"{value:,.2f}"
    return str(value)

def add_table(df, max_rows=10, max_cols=6):
    if df is None or df.empty:
        para("No corresponding output file was available for this table.")
        return
    data = [list(map(str, df.columns[:max_cols]))]
    for _, row in df.iloc[:max_rows, :max_cols].iterrows():
        data.append([fmt(x) for x in row.tolist()])
    widths = [doc.width / len(data[0])] * len(data[0])
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#163A5F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("LEADING", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CCD5DF")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F1F5F9")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(table)
    story.append(Spacer(1, 9))

def footer(canvas, document):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(0.65 * inch, 0.35 * inch,
                      "Mutual Fund Analytics Platform | Rohit Kumar")
    canvas.drawRightString(A4[0] - 0.65 * inch, 0.35 * inch,
                           f"Page {document.page}")
    canvas.restoreState()

# Cover page
story.append(Spacer(1, 1.35 * inch))
para("MUTUAL FUND ANALYTICS<br/>PLATFORM", "CoverTitle")
para("Data Analysis, Performance Metrics, Investor Transactions and SIP Trends",
     "BodyCustom")
story.append(Spacer(1, 0.35 * inch))
para("<b>Final Project Report</b>", "Heading2")
story.append(Spacer(1, 0.15 * inch))
para("Prepared by: Rohit Kumar")
para("Department: Computer Science and Engineering")
para("Technologies: Python, Pandas, SQLite, SQL, Streamlit")
para(f"Report date: {date.today().strftime('%d %B %Y')}")
story.append(Spacer(1, 1.2 * inch))
para("This report documents the analysis workflow, outputs and limitations of the mutual fund analytics project.",
     "BodyCustom")
story.append(PageBreak())

heading("1. Executive Summary")
para(
    "The Mutual Fund Analytics Platform is a data analytics project designed to "
    "explore mutual fund performance, historical Net Asset Value (NAV), Systematic "
    "Investment Plan (SIP) inflows, fund-house assets under management (AUM), "
    "investor transactions and portfolio holdings. Python is used for data "
    "processing and analysis, SQLite and SQL for structured queries, and Streamlit "
    "for an interactive dashboard."
)
para(
    "The project includes data ingestion, validation, preprocessing, exploratory "
    "data analysis, performance metrics, advanced analytics and exportable CSV "
    "reports. Results are based on the supplied datasets and should not be "
    "interpreted as live market information or personalized investment advice."
)

heading("2. Project Objectives")
for item in [
    "Inspect and validate the supplied mutual fund datasets.",
    "Analyze historical NAV and calculate NAV-based returns.",
    "Summarize SIP inflows across months and years.",
    "Compare fund-house AUM and reported scheme performance.",
    "Examine investor transactions, KYC status and transaction patterns.",
    "Summarize portfolio holdings and sector exposure.",
    "Store data in SQLite and perform SQL-based analysis.",
    "Present selected findings through a Streamlit dashboard."
]:
    bullet(item)

heading("3. Dataset Overview")
dataset_rows = [
    ["Dataset", "Records / coverage", "Purpose"],
    ["Fund master", "40 schemes", "Scheme and fund metadata"],
    ["NAV history", "46,000 records", "Historical NAV analysis"],
    ["Investor transactions", "32,778 records", "Transaction and investor patterns"],
    ["Portfolio holdings", "322 records", "Holdings and sector exposure"],
    ["Monthly SIP inflows", "48 months", "SIP trends, 2022–2025"],
    ["Scheme performance", "40 schemes", "Reported returns and risk fields"],
    ["Benchmark indices", "Supplied index records", "Benchmark comparison where available"],
]
table = Table(dataset_rows, colWidths=[1.45*inch, 1.3*inch, 3.6*inch], repeatRows=1)
table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#163A5F")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 8),
    ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#CCD5DF")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F1F5F9")]),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
    ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(table)
story.append(Spacer(1, 8))
para(
    "The project uses raw and processed CSV files. Processed files are used by "
    "analysis scripts and notebooks, while the SQLite database supports structured "
    "queries. Record counts describe the supplied project data, not necessarily "
    "the entire Indian mutual fund market."
)

heading("4. Methodology")
for title, detail in [
    ("Data ingestion", "Load CSV datasets and inspect columns, record counts and data types."),
    ("Data validation", "Check missing values, duplicates, date fields, NAV records and selected SIP growth values."),
    ("Preprocessing", "Convert dates and prepare data for consistent grouping and calculations."),
    ("Exploratory analysis", "Summarize categories, investor transactions, SIP trends, AUM and holdings."),
    ("Performance analytics", "Calculate selected annualized returns, volatility, Sharpe ratio, beta and historical Value at Risk where data permits."),
    ("SQL analysis", "Load datasets into SQLite and query AUM, SIP inflows, transactions, sector exposure and scheme performance."),
    ("Dashboard", "Use Streamlit to present selected analytics interactively.")
]:
    story.append(KeepTogether([
        Paragraph(f"<b>{title}</b>", styles["SubSection"]),
        Paragraph(detail, styles["BodyCustom"])
    ]))

heading("5. Exploratory Data Analysis")
para("The analysis examined fund categories, risk classifications, monthly SIP inflows, transaction types, fund-house AUM, NAV trends and portfolio sector exposure.")
bullet("Fund master contains 40 schemes: 34 categorized as Equity and 6 as Debt in the supplied category field.")
bullet("Reported risk categories include Moderate (16 schemes), High (8), Very High (6), Low (6) and Moderately High (4).")
bullet("Investor transaction records include SIP (19,716), Lumpsum (8,095) and Redemption (4,967).")
bullet("KYC status is recorded as Verified for 30,146 transaction records and Pending for 2,632.")
bullet("Average expense ratio in the supplied data is approximately 1.337% for Equity and 0.668% for Debt.")
para(
    "These figures summarize the supplied dataset. Category labels and totals depend "
    "on the source files and should be checked before making external market claims."
)

heading("6. SIP Inflow Analysis")
sip = load_report("advanced_yearly_sip_growth.csv")
if sip is None:
    sip = load_report("sql_monthly_sip_yearly.csv")
add_table(sip, max_rows=10)
para(
    "Yearly SIP inflows increased across the supplied 2022–2025 period. Based on "
    "the recorded annual totals, year-over-year growth was approximately 23.64% "
    "in 2023, 46.01% in 2024 and 24.45% in 2025. These are dataset-level values "
    "and should not be assumed to be independently verified industry statistics."
)
para("The yearly aggregation is useful for identifying changes in recorded inflow levels, while monthly analysis helps reveal seasonality and short-term movement.")

heading("7. Investor Transaction Analysis")
transactions = load_report("investor_transaction_analysis.csv")
add_table(transactions, max_rows=10)
para(
    "SIP transactions account for the highest number of records. Lumpsum transactions "
    "have a substantially higher average transaction amount than SIP transactions, "
    "while redemption records represent withdrawals. Transaction counts and amounts "
    "describe the dataset and do not establish the behavior of all mutual fund investors."
)

heading("8. Fund Performance and Risk Analysis")
performance = load_report("fund_performance_metrics.csv")
if performance is None:
    performance = load_report("risk_return_analysis.csv")
add_table(performance, max_rows=12)
para(
    "Performance analysis includes available reported returns and risk measures. "
    "Risk-return comparisons can help organize schemes for further review, but "
    "historical returns and risk statistics do not predict future performance."
)
para(
    "A significant limitation was identified: NAV-derived returns and supplied "
    "scheme-performance returns differ for some schemes. Benchmark correlations "
    "were also implausibly close to zero for certain index-fund comparisons. "
    "These inconsistencies indicate that the relevant source data, dates, benchmark "
    "mapping and calculation assumptions require further verification. Performance "
    "metrics should therefore be treated as exploratory rather than fully validated."
)

heading("9. Fund-House AUM Analysis")
aum = load_report("sql_latest_fund_house_aum.csv")
if aum is None:
    aum = load_report("fund_house_latest_aum.csv")
add_table(aum, max_rows=12)
para(
    "The SQL workflow aggregates AUM for the latest available reporting date and "
    "ranks fund houses by the resulting total. The output depends on the dates and "
    "units supplied in the source dataset."
)

heading("10. Portfolio Holdings and Sector Exposure")
holdings = load_report("portfolio_sector_summary.csv")
if holdings is None:
    holdings = load_report("portfolio_holdings_analysis.csv")
add_table(holdings, max_rows=12)
para(
    "Portfolio analysis summarizes holding records by stock and sector. Summing "
    "market values across multiple schemes can count the same underlying stock "
    "more than once. The resulting totals represent aggregated scheme-level exposure "
    "and should not be described as unique market-wide ownership."
)

heading("11. SQL and Database Implementation")
para(
    "A SQLite database stores the main datasets in tables for fund metadata, NAV "
    "history, AUM, SIP inflows, category inflows, folio counts, scheme performance, "
    "investor transactions, portfolio holdings and benchmark indices."
)
para("The SQL analysis includes:")
for item in [
    "Latest AUM by fund house.",
    "Year-wise SIP inflows.",
    "Transaction counts and amounts by transaction type.",
    "Top schemes by supplied one-year return.",
    "Portfolio market value by sector.",
    "Investor KYC status counts.",
    "Average reported returns by category.",
    "Monthly SIP inflows and reported growth."
]:
    bullet(item)

heading("12. Interactive Dashboard")
para(
    "The Streamlit application is located at dashboard/app.py. It provides a local "
    "interface for viewing selected mutual fund analytics. Run it from the project "
    "root using: python -m streamlit run dashboard/app.py. The terminal displays "
    "the local address to open in a browser."
)

heading("13. Data Quality, Assumptions and Limitations")
for item in [
    "The supplied datasets may not represent live or independently verified market data.",
    "NAV-based and supplied scheme-performance returns show discrepancies for some schemes.",
    "Some benchmark comparisons are unreliable because benchmark coverage or mapping may be incomplete.",
    "Five-year NAV returns are unavailable where the historical coverage is shorter than five years.",
    "2022 SIP year-over-year growth cannot be calculated without prior-year data.",
    "Portfolio sector totals may include repeated exposure to the same underlying stock.",
    "Risk measures depend on available history, data alignment and calculation assumptions.",
    "The platform is an analytical project and does not provide personalized investment advice."
]:
    bullet(item)

heading("14. Future Enhancements")
for item in [
    "Investigate NAV and reported-return discrepancies and validate benchmark mappings.",
    "Add automated tests for data types, duplicates, missing values and date coverage.",
    "Improve dashboard filters and scheme-level comparisons.",
    "Add documented benchmark alignment and risk-free-rate assumptions.",
    "Automate data refresh and report generation.",
    "Deploy the dashboard and document the deployment environment."
]:
    bullet(item)

heading("15. Conclusion")
para(
    "The project brings together data ingestion, cleaning, exploratory analysis, "
    "performance calculations, SQL reporting and an interactive dashboard in one "
    "Python-based workflow. It demonstrates how structured financial datasets can "
    "be explored to understand SIP trends, investor transaction patterns, AUM and "
    "portfolio exposure. The most important next step for analytical reliability is "
    "to investigate the identified NAV, reported-return and benchmark inconsistencies."
)

heading("Appendix: Reproducibility")
para("From the project root, activate the virtual environment and install dependencies from requirements.txt if available. The principal commands are:")
for cmd in [
    "python data_ingestion.py",
    "python validate_data.py",
    "python preprocess_data.py",
    "python load_sql_database.py",
    "python setup_sql_views.py",
    "python run_sql_analysis.py",
    "python -m streamlit run dashboard/app.py"
]:
    para(f"<font name='Courier'>{cmd}</font>", "SmallCustom")
para(
    "Run scripts in the appropriate order and check their expected inputs before "
    "executing them. This report reflects the analysis outputs available at the time "
    "of generation."
)

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"PDF report created: {OUTPUT}")
