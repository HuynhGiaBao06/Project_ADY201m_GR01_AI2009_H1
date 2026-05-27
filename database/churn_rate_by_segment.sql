--Viết truy vấn SQL tính Churn Rate (`sql/churn_rate_by_segment.sql`) theo Loại hợp đồng, Phương thức thanh toán, và các gói dịch vụ đi kèm.-- sql/churn_rate_by_segment.sql
SELECT
    Contract,
    PaymentMethod,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport