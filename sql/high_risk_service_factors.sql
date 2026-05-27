--Viết truy vấn xác định các yếu tố dịch vụ có tỷ lệ rời bỏ cao bất thường (ví dụ: thiếu Tech Support)
-- sql/high_risk_service_factors.sql
SELECT
    ID,
    Churn,
    Tenure,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport
FROM dbo.Predictive_Customer_Churn_DB
WHERE Churn = 1 
  AND (TechSupport = 0 OR OnlineSecurity = 0 OR OnlineBackup = 0)