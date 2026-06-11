-- sql/high_risk_service_factors.sql

SELECT 
    InternetService,
    -- Biến đổi giá trị BIT 0/1 thành nhãn dễ đọc cho báo cáo
    CASE WHEN OnlineSecurity = 1 THEN 'Yes' ELSE 'No' END AS OnlineSecurity,
    CASE WHEN OnlineBackup = 1 THEN 'Yes' ELSE 'No' END AS OnlineBackup,
    CASE WHEN DeviceProtection = 1 THEN 'Yes' ELSE 'No' END AS DeviceProtection,
    CASE WHEN TechSupport = 1 THEN 'Yes' ELSE 'No' END AS TechSupport,
    
    -- Tính toán quy mô tập khách hàng của từng nhóm
    COUNT(ID) AS Total_Customers,
    
    -- Đếm số lượng khách hàng thực sự rời đi trong nhóm đó
    SUM(CAST(Churn AS INT)) AS Churned_Customers,
    
    -- Tính toán tỷ lệ rời bỏ (Churn Rate)
    ROUND(AVG(CAST(Churn AS FLOAT)) * 100, 2) AS Churn_Rate_Percentage

FROM dbo.Predictive_Customer_Churn_DB

-- Lọc bỏ những người không dùng Internet (vì họ mặc định không có các dịch vụ trên)
WHERE InternetService != 'No'

GROUP BY 
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport

-- "Lưới lọc" rủi ro cao bất thường: 
-- Chỉ lấy những nhóm có Tỷ lệ rời bỏ > 40% VÀ quy mô nhóm > 50 người (tránh nhiễu thống kê)
HAVING 
    ROUND(AVG(CAST(Churn AS FLOAT)) * 100, 2) > 40
    AND COUNT(ID) > 50

-- Đẩy những nhóm rủi ro cao nhất lên đầu bảng
ORDER BY 
    Churn_Rate_Percentage DESC;