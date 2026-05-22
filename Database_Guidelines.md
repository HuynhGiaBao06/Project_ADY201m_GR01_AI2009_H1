# Hướng dẫn Kết nối Database Azure SQL và Sử dụng T-SQL trên VS Code

Chào mừng các bạn thành viên nhóm **PROJECT_ADY201M_GR01_AI** đến với dự án dự đoán rời bỏ của khách hàng (**Predictive Customer Churn**). 

Tài liệu này hướng dẫn chi tiết từng bước giúp các bạn thiết lập môi trường trên máy cá nhân, cài đặt công cụ và thực thi các câu lệnh T-SQL trực tiếp trên **Visual Studio Code (VS Code)**.

---

## GIAI ĐOẠN 1: CHUẨN BỊ MẠNG (ĐÃ ĐƯỢC CẤU HÌNH SẴN)

Đối với dự án này, hệ thống tường lửa (Firewall) của Database đã được Leader cấu hình mở rộng. 

Các bạn **không cần** phải cung cấp địa chỉ IP cá nhân. Dù bạn làm việc ở nhà, trên trường hay ở quán cafe, chỉ cần máy tính có kết nối Internet ổn định là có thể tiến hành đăng nhập trực tiếp ở các bước tiếp theo mà không lo bị lỗi *Cannot connect to server*.

---

## GIAI ĐOẠN 2: CÀI ĐẶT EXTENSION TRÊN VS CODE

Bạn không cần cài đặt các phần mềm quản trị nặng nề như SQL Server Management Studio (SSMS). Hãy tận dụng ngay VS Code bằng các bước sau:

1. Mở **VS Code** trên máy tính của bạn.
2. Click vào biểu tượng **Extensions** ở thanh menu bên trái (hoặc nhấn tổ hợp phím `Ctrl + Shift + X` trên Windows / `Cmd + Shift + X` trên Mac).
3. Tại thanh tìm kiếm, nhập từ khóa: **`SQL Server (mssql)`**.
4. Chọn đúng extension do chính **Microsoft** phát hành và nhấn **Install**.
5. Chờ hệ thống cài đặt xong. Bạn sẽ thấy một biểu tượng **hình trụ Database (SQL Server)** xuất hiện ở thanh công cụ bên trái.

---

## GIAI ĐOẠN 3: CẤU HÌNH KẾT NỐI (LOGIN DATABASE)

Hãy tiến hành kết nối Database theo một trong hai cách sau:

### Cách 1: Cấu hình thủ công qua giao diện UI (Thông thường)
1. Bấm vào biểu tượng **SQL Server** ở thanh công cụ bên trái.
2. Tại mục **CONNECTIONS**, bấm vào dấu cộng (**Add Connection** `+`).
3. Một thanh nhập liệu sẽ xuất hiện ở phía trên cùng của VS Code, hãy nhập lần lượt thông tin như sau:
   - **Server name:** `fptu-project-db.database.windows.net`
   - **Database name:** `Predictive_Customer_Churn_DB`
   - **Authentication Type:** Chọn `SQL Login`
   - **User name:** *Nhập tài khoản Leader cấp riêng cho bạn* (Ví dụ: `member_kietnh` hoặc `member_duyna`)
   - **Password:** *Nhập mật khẩu tương ứng được cấp*
   - **Save Password:** Chọn `Yes` (Để không phải nhập lại ở lần sau)
   - **Profile Name:** Nhập tên gợi nhớ (Ví dụ: `FPTU_Azure_DB`)
4. Nhấn **Enter** và đợi hệ thống kết nối.

### Cách 2: Kết nối bằng Connection String (Khuyên dùng nếu gặp lỗi giao diện)
Nếu giao diện UI của extension trên VS Code bị lỗi xung đột cấu hình (`configSource`), hãy chọn tính năng **Load from Connection String** khi nhấn Add Connection và dán chuỗi dưới đây vào (nhớ thay đổi Username và Password của bạn):

```text
Server=tcp:fptu-project-db.database.windows.net,1433;Initial Catalog=Predictive_Customer_Churn_DB;Persist Security Info=False;User ID=TAI_KHOAN_CUA_BAN;Password=MAT_KHAU_CUA_BAN;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;
```
Nhấn **Enter** để hoàn tất kết nối.

---

## GIAI ĐOẠN 4: VIẾT VÀ THỰC THI T-SQL TRÊN VS CODE

1. Tạo một file mới trong dự án và lưu lại với phần mở rộng là **`.sql`** (Ví dụ: `query_data.sql`). VS Code sẽ tự động chuyển đổi chế độ cú pháp sang T-SQL.
2. Nhìn xuống **góc dưới cùng bên phải** của thanh trạng thái VS Code, đảm bảo trạng thái hiển thị đã kết nối với Profile `FPTU_Azure_DB` và database hiện tại là `Predictive_Customer_Churn_DB`. Nếu đang hiển thị `Disconnected`, hãy click vào để chọn lại Profile kết nối.
3. Viết thử một câu lệnh truy vấn mẫu:
   ```sql
   -- Kiểm tra danh sách các bảng hiện có trong Database dự án
   SELECT table_name 
   FROM information_schema.tables 
   WHERE table_type = 'BASE TABLE';
   ```
4. **Cách chạy code:** Bôi đen toàn bộ câu lệnh (hoặc đoạn lệnh cần chạy) và nhấn tổ hợp phím:
   - **Windows:** `Ctrl + Shift + E`
   - **Mac:** `Cmd + Shift + E`
5. Một cửa sổ panel bên phải sẽ mở ra hiển thị kết quả truy vấn (Results) dạng bảng cực kỳ trực quan kèm theo thời gian thực thi.

---

## 📌 QUY ĐỊNH VỀ QUYỀN HẠN TRÊN DATABASE THÀNH VIÊN

Tài khoản của các bạn thành viên nhóm (`member_*`) được phân quyền ở mức **`db_datareader` (Chỉ đọc)**. 
- **Quyền hạn được phép:** Thực thi toàn bộ lệnh `SELECT`, viết các câu lệnh Query phức tạp, kết hợp bảng (JOIN), lọc dữ liệu phục vụ quá trình phân tích (Exploratory Data Analysis - EDA) và trích xuất đặc trưng làm sạch dữ liệu (Feature Engineering) cho mô hình AI.
- **Hành vi bị chặn:** Bạn không thể thực hiện các lệnh làm thay đổi cấu trúc Database (`CREATE`, `ALTER`, `DROP`) hoặc chỉnh sửa/xóa dữ liệu gốc (`INSERT`, `UPDATE`, `DELETE`) trên các bảng chính. Quy định này nhằm đảm bảo tính toàn vẹn dữ liệu cho toàn bộ dự án của nhóm.