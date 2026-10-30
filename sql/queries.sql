-- 1. Latest AUM by fund house
SELECT fund_house, MAX(date) AS latest_date,
       SUM(aum_crore) AS total_aum_crore
FROM aum_by_fund_house
WHERE date = (SELECT MAX(date) FROM aum_by_fund_house)
GROUP BY fund_house
ORDER BY total_aum_crore DESC;

-- 2. Year-wise SIP inflow
SELECT SUBSTR(month, 1, 4) AS year,
       SUM(sip_inflow_crore) AS total_sip_inflow_crore
FROM monthly_sip_inflows
GROUP BY SUBSTR(month, 1, 4)
ORDER BY year;

-- 3. Transaction summary by type
SELECT transaction_type,
       COUNT(*) AS transaction_count,
       SUM(amount_inr) AS total_amount_inr,
       ROUND(AVG(amount_inr), 2) AS average_amount_inr
FROM investor_transactions
GROUP BY transaction_type
ORDER BY transaction_count DESC;

-- 4. Top 10 schemes by reported 1-year return
SELECT scheme_name, category, return_1yr_pct,
       return_3yr_pct, risk_grade
FROM scheme_performance
WHERE return_1yr_pct IS NOT NULL
ORDER BY return_1yr_pct DESC
LIMIT 10;

-- 5. Portfolio exposure by sector
SELECT sector,
       ROUND(SUM(market_value_cr), 2) AS market_value_crore,
       COUNT(*) AS holding_records
FROM portfolio_holdings
GROUP BY sector
ORDER BY market_value_crore DESC;

-- 6. Investor KYC status
SELECT kyc_status, COUNT(*) AS transaction_records
FROM investor_transactions
GROUP BY kyc_status
ORDER BY transaction_records DESC;

-- 7. Average reported return by category
SELECT category,
       COUNT(*) AS fund_count,
       ROUND(AVG(return_1yr_pct), 2) AS avg_1yr_return_pct,
       ROUND(AVG(return_3yr_pct), 2) AS avg_3yr_return_pct
FROM scheme_performance
GROUP BY category
ORDER BY avg_1yr_return_pct DESC;

-- 8. Monthly SIP inflow and reported growth
SELECT month, sip_inflow_crore, yoy_growth_pct
FROM monthly_sip_inflows
ORDER BY month;
