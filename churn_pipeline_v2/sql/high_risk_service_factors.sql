-- PostgreSQL / Neon high-risk service factor analysis.

SELECT
    "InternetService",
    CASE WHEN "OnlineSecurity" = 1 THEN 'Yes' ELSE 'No' END AS "OnlineSecurity",
    CASE WHEN "OnlineBackup" = 1 THEN 'Yes' ELSE 'No' END AS "OnlineBackup",
    CASE WHEN "DeviceProtection" = 1 THEN 'Yes' ELSE 'No' END AS "DeviceProtection",
    CASE WHEN "TechSupport" = 1 THEN 'Yes' ELSE 'No' END AS "TechSupport",
    COUNT("ID") AS total_customers,
    SUM("Churn") AS churned_customers,
    ROUND((SUM("Churn")::numeric / NULLIF(COUNT("ID"), 0)) * 100, 2) AS churn_rate_percentage
FROM vw_cleaning_data
WHERE "InternetService" <> 'No'
GROUP BY
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport"
HAVING
    ROUND((SUM("Churn")::numeric / NULLIF(COUNT("ID"), 0)) * 100, 2) > 40
    AND COUNT("ID") > 50
ORDER BY
    churn_rate_percentage DESC;
