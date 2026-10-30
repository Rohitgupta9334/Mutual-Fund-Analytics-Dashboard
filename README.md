# Mutual Funds Analytics Dashboard

A data analytics project that explores mutual fund performance, investor transactions, SIP inflows, fund-house assets under management (AUM), and portfolio sector exposure using Python, SQL, and Streamlit.

## Project Overview

This project analyzes mutual fund datasets to identify trends, summarize investor transactions, compare fund-house AUM, and understand portfolio holdings. It includes data validation, preprocessing, SQL analysis, and an interactive dashboard.

## Features

- **Data Ingestion:** Load and inspect multiple CSV datasets.
- **Data Cleaning:** Handle date conversions, duplicates, and data quality checks.
- **NAV Analysis:** Calculate annualized returns using historical NAV data.
- **SIP Analysis:** Analyze monthly and yearly SIP inflow trends.
- **Fund-house Analysis:** Rank fund houses by their latest available AUM.
- **Transaction Analysis:** Compare SIP, lumpsum, and redemption transactions.
- **Portfolio Analysis:** Summarize scheme-wise holdings and sector exposure.
- **SQL Analytics:** Store datasets in SQLite and run analytical queries.
- **Interactive Dashboard:** Visualize key metrics and trends using Streamlit.

## Technologies Used

- Python
- Pandas
- SQLite
- SQL
- Streamlit
- Data Visualization

## Project Structure

```text
mutual-funds-analysis/
├── data/
│   ├── raw/
│   ├── processed/
│   └── mutual_funds.db
├── dashboard/
│   └── app.py
├── reports/
├── notebooks/
├── sql/
├── data_ingestion.py
├── validate_data.py
├── preprocess_data.py
├── check_data_quality.py
├── validate_sip_growth.py
├── validate_nav_data.py
├── calculate_nav_returns.py
├── analyze_sip_trends.py
├── analyze_aum.py
├── analyze_transactions.py
├── analyze_holdings.py
├── load_sql_database.py
├── setup_sql_views.py
├── run_sql_analysis.py
└── README.md
```

*Note: The structure above shows the main project files. Other analysis scripts and generated reports may also be present.*

## How to Run the Project

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd mutual-funds-analysis
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install pandas streamlit
```

### 4. Prepare the database

Ensure the processed CSV files are available in `data/processed/`, then run:

```bash
python load_sql_database.py
python setup_sql_views.py
python run_sql_analysis.py
```

### 5. Launch the dashboard

```bash
python -m streamlit run dashboard/app.py
```

Open the local URL shown in the terminal.

## Key Analysis Results

- Analyzed 46,000 historical NAV records across 40 schemes.
- Analyzed 32,778 investor transaction records.
- Examined 48 months of SIP inflow data from 2022 to 2025.
- Compared the latest available AUM for 10 fund houses.
- Analyzed 322 portfolio holding records.
- Generated CSV reports for data quality, returns, transactions, SIP trends, fund-house AUM, and sector exposure.

## Data Quality and Limitations

- The datasets supplied with this project may not represent live market data.
- NAV-based annualized returns showed substantial differences from the supplied scheme-performance returns. These differences require further investigation before the reported returns can be treated as verified.
- Five-year NAV returns were unavailable because the historical data covered less than five years as of the latest NAV date.
- Missing SIP year-over-year growth values for 2022 were retained because prior-year data was unavailable.
- Portfolio sector totals combine holdings across schemes and may include repeated exposure to the same stock.

## Future Improvements

- Add more interactive dashboard filters.
- Include benchmark comparisons and risk metrics.
- Investigate discrepancies between NAV-based and reported returns.
- Add automated data refresh and testing.
- Deploy the dashboard online.

## Author

Rohit Kumar

Computer Science and Engineering Student
