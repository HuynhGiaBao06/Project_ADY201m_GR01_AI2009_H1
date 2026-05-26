-- ==============================================================================
-- Tên file: feature_summary.sql
-- Mục tiêu: Tạo VIEW tổng hợp các biến đặc trưng (Feature Engineering) 
-- phục vụ mô hình dự đoán Churn.
-- ==============================================================================

CREATE VIEW vw_Feature_Summary AS
SELECT
    ID,Churn,
    -- 1. tenure_group: Phân nhóm thời gian sử dụng
    CASE 
        WHEN Tenure <= 12 THEN '0-12 months'
        WHEN Tenure > 12 AND Tenure <= 24 THEN '13-24 months'
        WHEN Tenure > 24 AND Tenure <= 36 THEN '25-36 months'
        WHEN Tenure > 36 AND Tenure <= 48 THEN '37-48 months'
        WHEN Tenure > 48 AND Tenure <= 60 THEN '49-60 months'
        WHEN Tenure > 60 AND Tenure <= 72 THEN '61-72 months'
        ELSE '72+ months'

    END AS tenure_group,


    -- 2. service_diversity: Tính tổng số dịch vụ phụ trợ đang sử dụng
    -- Do các cột này đang ở kiểu BIT (0/1), cần CAST sang INT để tính tổng

    (CAST(OnlineSecurity AS INT) + 
     CAST(OnlineBackup AS INT) + 
     CAST(DeviceProtection AS INT) + 
     CAST(TechSupport AS INT)) AS service_diversity,

     -- 3. monthly_charges_ratio: Tỷ lệ chi phí tháng so với mức trung bình
    -- Sử dụng hàm cửa sổ OVER() để tính AVG cho toàn bộ bảng mà không cần GROUP BY
    MonthlyCharges / AVG(MonthlyCharges) OVER() AS monthly_charges_ratio,

    -- 4. is_paperless_electronic: Tổ hợp hóa đơn điện tử và thanh toán tự động
    CASE 
        WHEN PaperlessBilling = 1 AND PaymentMethod LIKE '%automatic%' THEN 1 
        ELSE 0 
    END AS is_paperless_electronic

FROM Predictive_Customer_Churn_DB;
GO

