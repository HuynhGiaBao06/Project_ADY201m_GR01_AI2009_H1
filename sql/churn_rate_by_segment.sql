-- sql/churn_rate_by_segment.sql

SELECT 
    Contract,
    PaymentMethod,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport,
    
    -- Tổng số khách hàng trong phân khúc này
    COUNT(ID) AS Total_Customers,
    
    -- Tổng số khách hàng đã rời bỏ (Ép kiểu BIT sang INT để tính tổng)
    SUM(CAST(Churn AS INT)) AS Churned_Customers,
    
    -- Tính Tỷ lệ rời bỏ (%) và làm tròn 2 chữ số thập phân
    ROUND(AVG(CAST(Churn AS FLOAT)) * 100, 2) AS Churn_Rate_Percentage

FROM dbo.Predictive_Customer_Churn_DB

GROUP BY 
    Contract,
    PaymentMethod,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport

-- Sắp xếp giảm dần theo Tỷ lệ rời bỏ để tìm ra nhóm rủi ro cao nhất
-- Lọc thêm ưu tiên các nhóm có số lượng khách hàng lớn để đảm bảo insight có ý nghĩa
ORDER BY 
    Churn_Rate_Percentage DESC, 
    Total_Customers DESC;
