-- sql/compare.sql

SELECT 
    -- Chỉnh sửa giá trị in ra sang tiếng Anh
    CASE 
        WHEN Churn = 1 THEN 'Churn'
        ELSE 'Non-churn' 
    END AS Customer_Status,
    
    -- Đếm tổng số lượng khách hàng của mỗi nhóm
    COUNT(ID) AS Total_Customers,
    
    -- Tính trung bình thời gian gắn bó (Ép kiểu FLOAT để không bị làm tròn số nguyên)
    ROUND(AVG(CAST(Tenure AS FLOAT)), 2) AS Avg_Tenure_Months,
    
    -- Tính trung bình cước phí hàng tháng
    ROUND(AVG(MonthlyCharges), 2) AS Avg_Monthly_Charges,
    
    -- Tính trung bình tổng cước phí
    ROUND(AVG(TotalCharges), 2) AS Avg_Total_Charges

FROM dbo.Predictive_Customer_Churn_DB

GROUP BY 
    Churn;
    