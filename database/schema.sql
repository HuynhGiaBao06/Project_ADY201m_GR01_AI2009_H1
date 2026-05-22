-- Tạo bảng Predictive_Customer_Churn_DB trong SQL Server (T-SQL)
CREATE TABLE Predictive_Customer_Churn_DB (
    ID VARCHAR(50) PRIMARY KEY,              -- Chuỗi định danh khách hàng, Khóa chính
    Churn BIT NOT NULL,                      -- Dữ liệu 0/1 tối ưu thành kiểu BIT
    SeniorCitizen VARCHAR(50) NOT NULL,      -- Chuyển đổi thành VARCHAR(50) theo yêu cầu
    Partner BIT NOT NULL,                    -- Dữ liệu 0/1 tối ưu thành kiểu BIT
    Dependents VARCHAR(50) NOT NULL,         -- Chuyển đổi thành VARCHAR(50) theo yêu cầu
    InternetService VARCHAR(50) NOT NULL,    -- Chuyển đổi thành VARCHAR(50) theo yêu cầu
    OnlineSecurity BIT NOT NULL,             -- Dữ liệu 0/1 tối ưu thành kiểu BIT
    OnlineBackup BIT NOT NULL,               -- Dữ liệu 0/1 tối ưu thành kiểu BIT
    DeviceProtection BIT NOT NULL,           -- Dữ liệu 0/1 tối ưu thành kiểu BIT
    TechSupport BIT NOT NULL,                -- Dữ liệu 0/1 tối ưu thành kiểu BIT
    Tenure INT NOT NULL,                     -- Cột này lưu số tháng (ví dụ: từ 1 đến 72 tháng), giữ nguyên INT
    Contract INT NOT NULL,                   -- Nếu cột này lưu số năm/tháng (ví dụ: 1, 2) hoặc phân loại dạng ID số, giữ nguyên INT
    PaymentMethod VARCHAR(50) NOT NULL,      -- Chuyển đổi thành VARCHAR(50) theo yêu cầu
    PaperlessBilling BIT NOT NULL,           -- Dữ liệu 0/1 tối ưu thành kiểu BIT
    MonthlyCharges DECIMAL(10,4) NOT NULL,   -- Số thập phân cho chi phí hàng tháng
    TotalCharges DECIMAL(12,4) NOT NULL      -- Số thập phân cho tổng chi phí
);
GO