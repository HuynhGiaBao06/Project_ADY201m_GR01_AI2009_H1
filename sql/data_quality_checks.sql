-- 1. KIỂM TRA TÍNH DUY NHẤT VÀ KHÓA CHÍNH (PRIMARY KEY CHECK)
SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT ID) AS unique_ids,
    COUNT(*) - COUNT(ID) AS null_ids
FROM dbo.Predictive_Customer_Churn_DB;


-- 2. KIỂM TRA DỮ LIỆU KHUYẾT THIẾU (NULL VALUE CHECK)
-- Vì các cột trong schema của bạn đều có thuộc tính 'NOT NULL', 
-- câu lệnh này giúp kiểm tra xem có dòng nào bị gán giá trị mặc định là 0 hoặc trống hay không.
SELECT 
    SUM(CASE WHEN Churn IS NULL THEN 1 ELSE 0 END) AS null_churn,
    SUM(CASE WHEN Tenure IS NULL THEN 1 ELSE 0 END) AS null_tenure,
    SUM(CASE WHEN MonthlyCharges IS NULL THEN 1 ELSE 0 END) AS null_monthly_charges,
    SUM(CASE WHEN TotalCharges IS NULL THEN 1 ELSE 0 END) AS null_total_charges,
    SUM(CASE WHEN InternetService IS NULL THEN 1 ELSE 0 END) AS null_internet_service
FROM dbo.Predictive_Customer_Churn_DB;


-- 3. KIỂM TRA TÍNH NHẤT QUÁN LOGIC (LOGICAL CONSISTENCY)
-- Dựa trên schema chuẩn số, ta dùng so sánh toán học trực tiếp một cách an toàn
SELECT 
    ID, 
    Tenure, 
    MonthlyCharges, 
    TotalCharges
FROM dbo.Predictive_Customer_Churn_DB
WHERE 
    -- Trường hợp 1: Số tháng sử dụng bằng 0 nhưng tổng tiền lại lớn hơn 0
    (Tenure = 0 AND TotalCharges > 0)
    
    -- Trường hợp 2: Đã sử dụng (Tenure > 0) nhưng tổng tiền lại bằng 0
    OR (Tenure > 0 AND TotalCharges = 0)
    
    -- Trường hợp 3: Chi phí bị âm (bất thường dữ liệu số)
    OR TotalCharges < 0 
    OR MonthlyCharges < 0;


-- 4. KIỂM TRA MIỀN DỮ LIỆU PHÂN LOẠI (CATEGORICAL DOMAIN CHECK)
-- Xem các giá trị thực tế của biến phân loại dạng VARCHAR và kiểm tra các biến BIT (0/1)
SELECT DISTINCT Churn FROM dbo.Predictive_Customer_Churn_DB;
SELECT DISTINCT SeniorCitizen FROM dbo.Predictive_Customer_Churn_DB;
SELECT DISTINCT InternetService, PaymentMethod FROM dbo.Predictive_Customer_Churn_DB;


-- 5. TRÍCH XUẤT GIÁ TRỊ SỐ ĐỂ KIỂM TRA NGOẠI LAI (NUMERICAL OUTLIERS)
-- Vì TotalCharges hiện tại đã là DECIMAL, ta có thể dùng hàm MIN/MAX an toàn trên SQL
SELECT 
    MIN(Tenure) AS min_tenure,
    MAX(Tenure) AS max_tenure,
    MIN(MonthlyCharges) AS min_monthly,
    MAX(MonthlyCharges) AS max_monthly,
    MIN(TotalCharges) AS min_total,
    MAX(TotalCharges) AS max_total
FROM dbo.Predictive_Customer_Churn_DB;