-- PostgreSQL / Neon churn rate by customer/service segment.

SELECT
    "Contract",
    "PaymentMethod",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    COUNT("ID") AS total_customers,
    SUM("Churn") AS churned_customers,
    ROUND((SUM("Churn")::numeric / NULLIF(COUNT("ID"), 0)) * 100, 2) AS churn_rate_percentage
FROM vw_cleaning_data
GROUP BY
    "Contract",
    "PaymentMethod",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport"
ORDER BY
    churn_rate_percentage DESC,
    total_customers DESC;
