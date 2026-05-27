-- 1. Kiểm tra các dòng có ID bị trùng lặp (nếu có)
SELECT ID, COUNT(*) AS SoLanTrung
FROM dbo.Predictive_Customer_Churn_DB
GROUP BY ID
HAVING COUNT(*) > 1 OR ID IS NULL;

-- 2. Liệt kê các dòng khuyết thiếu dữ liệu ở các cột quan trọng
SELECT ID, Churn, Tenure, MonthlyCharges, TotalCharges, InternetService
FROM dbo.Predictive_Customer_Churn_DB
WHERE Churn IS NULL 
   OR Tenure IS NULL 
   OR MonthlyCharges IS NULL 
   OR TotalCharges IS NULL 
   OR TotalCharges = ' ' 
   OR InternetService IS NULL;

-- 3. Liệt kê các dòng bất hợp lý về mặt logic thời gian và chi phí
SELECT ID, Tenure, MonthlyCharges, TotalCharges
FROM dbo.Predictive_Customer_Churn_DB
WHERE (Tenure = 0 AND TotalCharges <> '0' AND TotalCharges IS NOT NULL AND TotalCharges <> ' ')
   OR (Tenure > 0 AND (TotalCharges = '0' OR TotalCharges = ' '));