--Viết truy vấn SQL tính Churn Rate (`sql/churn_rate_by_segment.sql`) theo Loại hợp đồng, Phương thức thanh toán, và các gói dịch vụ đi kèm.-- sql/churn_rate_by_segment.sql

SELECT
    Contract,
    PaymentMethod,
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
    Contract,
    PaymentMethod,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport

ORDER BY
    ChurnRatePercent DESC;