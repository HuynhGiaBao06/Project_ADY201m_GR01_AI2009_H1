-- 1. KIỂM TRA TÍNH DUY NHẤT VÀ KHÓA CHÍNH (PRIMARY KEY CHECK)
-- Kiểm tra xem ID có bị trùng lặp hoặc bị NULL hay không.
SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT ID) AS unique_ids,
    COUNT(*) - COUNT(ID) AS null_ids
FROM dbo.Predictive_Customer_Churn_DB;


-- 2. KIỂM TRA DỮ LIỆU KHUYẾT THIẾU (NULL VALUE CHECK)
-- Đếm số lượng dòng bị trống (NULL) ở các cột quan trọng phục vụ phân tích.
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
-- Số tháng sử dụng (Tenure) = 0 thì TotalCharges phải bằng 0 (hoặc NULL tùy cách hệ thống ghi nhận).
-- Nếu Tenure > 0, TotalCharges không thể bằng 0 hoặc nhỏ hơn MonthlyCharges một cách phi lý.
SELECT 
    ID, 
    Tenure, 
    MonthlyCharges, 
    TotalCharges,
    CASE 
        WHEN Tenure = 0 AND TotalCharges > 0 THEN 'Tenure is 0 but TotalCharges > 0'
        WHEN Tenure > 0 AND TotalCharges = 0 THEN 'Customer has tenure but TotalCharges is 0'
        WHEN TotalCharges < 0 OR MonthlyCharges < 0 THEN 'Negative charges detected'
        ELSE 'Inconsistent logic'
    END AS logic_error_type    
FROM dbo.Predictive_Customer_Churn_DB
WHERE (Tenure = 0 AND TotalCharges > 0)
   OR (Tenure > 0 AND TotalCharges = 0)
   OR TotalCharges < 0 
   OR MonthlyCharges < 0;


-- 4. PHÂN TÍCH GIÁ TRỊ MIỀN DỮ LIỆU PHÂN LOẠI (CATEGORICAL DOMAIN CHECK)
-- Đảm bảo các cột định tính không chứa các ký tự lạ hoặc sai chính tả.
-- Kiểm tra cột Churn (Biến mục tiêu)
SELECT Churn, COUNT(*) AS quantity 
FROM dbo.Predictive_Customer_Churn_DB 
GROUP BY Churn;

-- Kiểm tra cột SeniorCitizen (Thường là số 0/1 hoặc Yes/No)
SELECT SeniorCitizen, COUNT(*) AS quantity 
FROM dbo.Predictive_Customer_Churn_DB 
GROUP BY SeniorCitizen;

-- Kiểm tra các loại hình dịch vụ đi kèm xem có giá trị lạ không
SELECT
    InternetService,
    OnlineSecurity,
    TechSupport,
    Contract,
    PaymentMethod
FROM dbo.Predictive_Customer_Churn_DB
AS sample_categories
GROUP BY
    InternetService,
    OnlineSecurity,
    TechSupport,
    Contract,
    PaymentMethod;
 
-- 5. KIỂM TRA GIÁ TRỊ NGOẠI LAI / BẤT THƯỜNG Ở CÁC CỘT SỐ (NUMERICAL OUTLIERS)
-- Xem giá trị tối thiểu, tối đa để phát hiện các con số "bất bình thường" (ví dụ: số tháng âm, hoặc cước phí quá cao).
SELECT 
    MIN(Tenure) AS min_tenure,
    MAX(Tenure) AS max_tenure,
    AVG(Tenure) AS avg_tenure,
    MIN(MonthlyCharges) AS min_monthly,
    MAX(MonthlyCharges) AS max_monthly,
    AVG(MonthlyCharges) AS avg_monthly,
    MIN(TotalCharges) AS min_total,
    MAX(TotalCharges) AS max_total
FROM dbo.Predictive_Customer_Churn_DB;