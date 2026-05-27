-- Trích xuất dữ liệu cước phí và thời gian gắn bó cho nhóm RỜI BỎ (Churn = 1)
SELECT 
    ID, 
    Churn, 
    Tenure, 
    MonthlyCharges, 
    TotalCharges 
FROM dbo.Predictive_Customer_Churn_DB 
WHERE Churn = 1;

-- Trích xuất dữ liệu cước phí và thời gian gắn bó cho nhóm Ở LẠI (Churn = 0)
SELECT 
    ID, 
    Churn, 
    Tenure, 
    MonthlyCharges, 
    TotalCharges 
FROM dbo.Predictive_Customer_Churn_DB 
WHERE Churn = 0;