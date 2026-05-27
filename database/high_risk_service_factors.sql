--Viết truy vấn xác định các yếu tố dịch vụ có tỷ lệ rời bỏ cao bất thường (ví dụ: thiếu Tech Support)
-- sql/high_risk_service_factors.sql

SELECT
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport,

    COUNT(*) AS TotalCustomers,

    SUM(CAST(Churn AS INT)) AS ChurnCustomers,

    ROUND(
        100.0 * SUM(CAST(Churn AS INT)) / COUNT(*),
        2
    ) AS ChurnRatePercent

FROM dbo.Predictive_Customer_Churn_DB

GROUP BY
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport

HAVING
    ROUND(
        100.0 * SUM(CAST(Churn AS INT)) / COUNT(*),
        2
    ) > 50

ORDER BY
    ChurnRatePercent DESC,
    ChurnCustomers DESC;