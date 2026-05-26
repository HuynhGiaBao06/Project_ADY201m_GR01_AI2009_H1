📋 PHÂN CHIA CÔNG VIỆC CHI TIẾT (TASK BREAKDOWN)

Dự án: Predictive Customer Churn in Telecommunication Services
Thời gian thực hiện: 18/05/2026 – 14/06/2026

## 👥 THÔNG TIN ĐỘI NHÓM

* **Huỳnh Gia Bảo (Team Leader)**: Chịu trách nhiệm thiết lập dự án, thiết kế schema & pipeline Microsoft SQL Server, Feature Engineering. Phụ trách mô hình cốt lõi và phức tạp nhất (XGBoost) và Review code tổng thể.
* **Nguyễn An Duy (Member)**: Tập trung vào tiền xử lý dữ liệu (Data Cleaning) bằng Python, truy vấn SQL kiểm tra dữ liệu, trực quan hóa cơ bản, phụ trách mô hình Logistic Regression (Baseline) và thiết kế Dashboard.
* **Nguyễn Hữu Kiệt (Member)**: Tập trung vào truy vấn SQL (Churn Rate, hành vi theo nhóm hợp đồng/dịch vụ), trực quan hóa nâng cao, phụ trách mô hình Random Forest và tổng hợp Insight chiến lược.

---

## 📅 LỘ TRÌNH CHI TIẾT THEO SPRINT

### Sprint 1: Khởi tạo dự án, Xử lý dữ liệu thô & Thiết lập SQL (18/05 - 24/05)

**Mục tiêu:** Cài đặt xong môi trường làm việc nhóm, đọc và làm sạch toàn bộ dữ liệu thô từ bộ Telco Customer Churn: IBM dataset, thiết lập Microsoft SQL Server phục vụ lưu trữ và truy vấn.

**1. Huỳnh Gia Bảo**
* Task 1: Thiết lập GitHub Repository (Tạo file `.gitignore`, `requirements.txt`, thư mục cấu trúc bao gồm `sql/`).
* Task 2: Viết Base Code (Jupyter Notebook) cấu hình môi trường ảo (venv) và viết tài liệu hướng dẫn cài đặt cho nhóm.
* Task 3 (SQL Server): Thiết kế schema trên Microsoft SQL Server:
  * Viết file DDL T-SQL (`sql/schema.sql`) tạo bảng thông tin khách hàng (nhân khẩu học), hợp đồng & thanh toán, và dịch vụ viễn thông.
  * Viết script import nạp CSV đã sạch vào SQL Server. Cung cấp file mẫu `sql/.env.example`.

**2. Nguyễn An Duy**
* Task 1: Thiết lập không gian quản lý dự án trên Notion và tạo kênh giao tiếp riêng trên Discord.
* Task 2 (Python - Global Pipeline): Dùng pandas làm sạch missing value (đặc biệt lưu ý cột TotalCharges trống ở khách hàng mới), mã hóa phân loại (encoding) và xử lý lỗi logic. **Tuyệt đối giữ nguyên dữ liệu ngoại lai (outliers) và không thực hiện chuẩn hóa (scaling) ở bước này**.
* Task 3 (SQL): Viết truy vấn SQL kiểm tra chất lượng dữ liệu sau khi import (`sql/data_quality_checks.sql`).

**3. Nguyễn Hữu Kiệt**
* Task 1 (Python): Sử dụng `pandas.groupby()` để khám phá nhanh hành vi tiêu dùng, số tháng gắn bó (Tenure) và cước phí.
* Task 2 (SQL): Viết truy vấn SQL tính Churn Rate (`sql/churn_rate_by_segment.sql`) theo Loại hợp đồng, Phương thức thanh toán, và các gói dịch vụ đi kèm.

---

### Sprint 2: Phân tích SQL nâng cao, Kỹ nghệ đặc trưng & Trực quan hóa (25/05 - 31/05)

**Mục tiêu:** Phác họa hành vi khách hàng viễn thông, tạo biến mới (Feature Engineering) và vẽ biểu đồ đối chiếu giữa nhóm Churn và Non-churn.

**1. Huỳnh Gia Bảo**
* Task 1 (Python): Thực hiện Kỹ nghệ đặc trưng tạo các biến mới: `tenure_group`, `service_diversity`, `monthly_charges_ratio`, và `is_paperless_electronic`.
* Task 2 (SQL Server): Tạo VIEW tổng hợp T-SQL (`sql/feature_summary.sql`) đẩy các đặc trưng mới vào CSDL để hỗ trợ quá trình query sau này.
* Task 3: Code Review và Merge các Pull Request của Sprint 1 & 2.

**2. Nguyễn An Duy**
* Task 1 (SQL): Viết truy vấn SQL so sánh mức cước phí và số tháng gắn bó giữa nhóm churn và non-churn.
* Task 2 (Python): Sử dụng seaborn/matplotlib vẽ Bar Chart và Boxplot trực quan hóa sự khác biệt về cước phí (MonthlyCharges, TotalCharges) dựa trên dữ liệu đã truy vấn.

**3. Nguyễn Hữu Kiệt**
* Task 1 (SQL): Viết truy vấn xác định các yếu tố dịch vụ có tỷ lệ rời bỏ cao bất thường (ví dụ: thiếu Tech Support).
* Task 2 (Python): Vẽ Correlation Heatmap đánh giá tương quan đa biến và biểu đồ Churn theo nhóm Tenure để tìm điểm gãy trải nghiệm.

---

### Sprint 3: Huấn luyện Mô hình & Xây dựng Dashboard (01/06 - 07/06)

**Mục tiêu:** Độc lập xây dựng 3 mô hình học máy theo đúng kiến trúc phân nhánh cục bộ, đánh giá chéo và tạo Dashboard báo cáo.

**1. Huỳnh Gia Bảo**
* Task 1 (Data Prep): Chịu trách nhiệm phân chia tập Train/Test chuẩn từ tập "Dữ liệu sạch nhưng VẪN CHỨA OUTLIER" (đầu ra của Giai đoạn 1 luồng chung) để cả nhóm sử dụng.
* Task 2 (Modeling - Local Pipeline): Triển khai, huấn luyện và tinh chỉnh siêu tham số cho mô hình XGBoost. **Nhấn mạnh: Truyền trực tiếp tập dữ liệu chứa outlier vào mô hình mà không thực hiện scaling**. Trích xuất Feature Importance chuyên sâu.
* Task 3: Điều chỉnh ngưỡng cắt (Threshold tuning) trên XGBoost để tối ưu hóa tối đa chỉ số Recall (giảm thiểu False Negative).

**2. Nguyễn An Duy**
* Task 1 (Modeling - Local Pipeline): Tự thiết kế Local Pipeline bằng Scikit-learn gồm các bước Capping/Quantile Outliers và StandardScaler trước khi fit vào mô hình Baseline Logistic Regression. Phân tích chi tiết các hệ số hồi quy (coefficients) để giải thích chiều tác động của từng biến.
* Task 2 (Dashboard): Kết nối Power BI/Tableau với SQL Server. Xây dựng Dashboard (Tổng quan Churn Rate, Top risk segments).

**3. Nguyễn Hữu Kiệt**
* Task 1 (Modeling - Local Pipeline): Triển khai và huấn luyện mô hình Random Forest. **Nhấn mạnh: Truyền trực tiếp tập dữ liệu chứa outlier vào mô hình mà không thực hiện scaling**. Thu thập Feature Importance từ cây quyết định.
* Task 2 (Evaluation & Insights): Tổng hợp Metrics (Accuracy, Precision, Recall, F1-score, ROC-AUC) của cả 3 mô hình để lập bảng so sánh. Xây dựng khung đề xuất giải pháp: kịch bản chuyển đổi hợp đồng dài hạn và hệ thống Early-warning cho cước phí.

---

### Sprint 4: Viết Báo cáo & Tổng duyệt (08/06 - 14/06)

**Mục tiêu:** Hoàn thiện báo cáo học thuật và chuẩn bị slide thuyết trình.

**1. Huỳnh Gia Bảo**
* Task 1: Viết phần Methodology và phân tích chuyên sâu hiệu suất của XGBoost. Đưa ra quyết định chọn mô hình cuối cùng.
* Task 2: Quản lý cấu trúc file LaTeX, đảm bảo format chuẩn học thuật.

**2. Nguyễn An Duy**
* Task 1: Viết phần Introduction và Business Understanding (nhấn mạnh bài toán CAC). Trình bày kết quả của Logistic Regression.
* Task 2: Trích xuất hình ảnh từ Dashboard, chèn biểu đồ và bảng kết quả SQL vào báo cáo.

**3. Nguyễn Hữu Kiệt**
* Task 1: Trình bày kết quả của Random Forest. Viết phần Conclusion và các Actionable Insights (Khuyến nghị hành động).
* Task 2: Thiết kế Slide thuyết trình tổng kết dự án để cả nhóm bảo vệ.