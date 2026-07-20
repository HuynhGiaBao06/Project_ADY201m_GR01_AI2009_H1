-- PostgreSQL / Neon churn vs non-churn customer comparison.

SELECT
    CASE
        WHEN "Churn" = 1 THEN 'Churn'
        ELSE 'Non-churn'
    END AS customer_status,
    COUNT("ID") AS total_customers,
    ROUND(AVG("Tenure"::numeric), 2) AS avg_tenure_months,
    ROUND(AVG("MonthlyCharges"), 2) AS avg_monthly_charges,
    ROUND(AVG("TotalCharges"), 2) AS avg_total_charges
FROM vw_cleaning_data
GROUP BY
    "Churn";
