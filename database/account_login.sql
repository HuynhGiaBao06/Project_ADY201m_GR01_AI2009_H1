-- Tạo tài khoản đăng nhập
-- Đảm bảo đang thao tác trên đúng database dự án
USE Predictive_Customer_Churn_DB;
GO

-- ========================================================
-- 1. CẤU HÌNH CHO THÀNH VIÊN KIỆT (member_kietnh)
-- ========================================================
-- Tạo User trong database từ Login hệ thống
CREATE USER [member_kietnh] FOR LOGIN [member_kietnh];
GO
-- Cấp quyền CHỈ ĐỌC VÀ QUERY cho Kiệt
ALTER ROLE db_datareader ADD MEMBER [member_kietnh];
GO

-- ========================================================
-- 2. CẤU HÌNH CHO THÀNH VIÊN DUY (member_duyna)
-- ========================================================
-- Tạo User trong database từ Login hệ thống
CREATE USER [member_duyna] FOR LOGIN [member_duyna];
GO
-- Cấp quyền CHỈ ĐỌC VÀ QUERY cho Duy
ALTER ROLE db_datareader ADD MEMBER [member_duyna];
GO