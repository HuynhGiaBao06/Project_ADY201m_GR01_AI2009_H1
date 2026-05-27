-- Xóa quyền và User ở database dự án trước
DROP USER IF EXISTS [member_duyna];
DROP USER IF EXISTS [member_kietnh];
GO

-- Chắc chắn đang chọn database: master
DROP LOGIN [member_duyna];
DROP LOGIN [member_kietnh];
GO

-- Chắc chắn đang chọn database: master
CREATE LOGIN [member_duyna] WITH PASSWORD = 'NguyeAnDuy123@';
CREATE LOGIN [member_kietnh] WITH PASSWORD = 'NguyenHuuKiet123@';
GO

--======================Setup login====================================================
-- Chắc chắn đang chọn database dự án của bạn

-- 1. Kết nối User trong DB với Login ngoài Server
CREATE USER [member_duyna] FOR LOGIN [member_duyna];
CREATE USER [member_kietnh] FOR LOGIN [member_kietnh];
GO

-- 2. Cấp quyền đọc dữ liệu (SELECT)
ALTER ROLE db_datareader ADD MEMBER [member_duyna];
ALTER ROLE db_datareader ADD MEMBER [member_kietnh];
GO

-- 3. Cấp thêm quyền ghi dữ liệu (INSERT, UPDATE, DELETE) nếu cần
ALTER ROLE db_datawriter ADD MEMBER [member_duyna];
ALTER ROLE db_datawriter ADD MEMBER [member_kietnh];
GO