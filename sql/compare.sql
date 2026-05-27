WITH CleanedData AS (
    -- Bước 1: Chuẩn hóa dữ liệu, ép kiểu TotalCharges về dạng số đề phòng khoảng trắng
    SELECT 
        ID,
        Churn,
        Tenure,
        MonthlyCharges,
        CASE 
            WHEN TotalCharges = ' ' OR TotalCharges IS NULL THEN 0 
            ELSE CAST(TotalCharges AS DECIMAL(10,2)) 
        END AS TotalCharges
    FROM dbo.Predictive_Customer_Churn_DB
),

SummaryStats AS (
    -- Bước 2: Thống kê tổng quan (AVG, MIN, MAX) theo từng nhóm Churn
    SELECT 
        Churn,
        COUNT(*) AS TotalCustomers,
        -- Số tháng gắn bó (Tenure)
        ROUND(AVG(Tenure), 2) AS AvgTenure,
        MIN(Tenure) AS MinTenure,
        MAX(Tenure) AS MaxTenure,
        -- Cước phí hàng tháng (Monthly Charges)
        ROUND(AVG(MonthlyCharges), 2) AS AvgMonthlyCharges,
        MIN(MonthlyCharges) AS MinMonthlyCharges,
        MAX(MonthlyCharges) AS MaxMonthlyCharges,
        -- Tổng cước phí (Total Charges)
        ROUND(AVG(TotalCharges), 2) AS AvgTotalCharges
    FROM CleanedData
    GROUP BY Churn
),

MedianStats AS (
    -- Bước 3: Tính toán giá trị Trung vị (Median) bằng Window Function PERCENTILE_CONT
    -- Cách này hoạt động chuẩn xác trên SQL Server, PostgreSQL và Oracle
    SELECT DISTINCT
        Churn,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY Tenure) OVER (PARTITION BY Churn) AS MedianTenure,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY MonthlyCharges) OVER (PARTITION BY Churn) AS MedianMonthlyCharges
    FROM CleanedData
)

-- Bước 4: Kết hợp tất cả các chỉ số lại thành một bảng kết quả cuối cùng
SELECT 
    s.Churn,
    s.TotalCustomers,
    
    -- Nhóm chỉ số về Số tháng gắn bó (Tenure)
    s.AvgTenure,
    m.MedianTenure,
    s.MinTenure,
    s.MaxTenure,
    
    -- Nhóm chỉ số về Cước phí hàng tháng (Monthly Charges)
    s.AvgMonthlyCharges,
    m.MedianMonthlyCharges,
    s.MinMonthlyCharges,
    s.MaxMonthlyCharges,
    
    -- Nhóm chỉ số về Tổng cước phí đã thu (Total Charges)
    s.AvgTotalCharges
FROM SummaryStats s
JOIN MedianStats m ON s.Churn = m.Churn;