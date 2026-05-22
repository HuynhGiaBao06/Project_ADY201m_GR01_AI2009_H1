# 📋 PHÂN CHIA CÔNG VIỆC CHI TIẾT (TASK BREAKDOWN)
<<<<<<< HEAD
**Dự án:** Predictive Customer Churn in Telecommunication Services
=======
**Dự án:** Predictive Customer Churn in E-commerce Subscription Services
>>>>>>> feat01-docs-project-document
**Thời gian thực hiện:** 18/05/2026 – 14/06/2026

---

## 👥 THÔNG TIN ĐỘI NHÓM
*   **Huỳnh Gia Bảo (Team Leader):** Chịu trách nhiệm thiết lập dự án, thiết kế schema & pipeline **Microsoft SQL Server**, xử lý logic phức tạp (Feature Engineering, Modeling) và Review code.
*   **Nguyễn An Duy (Member):** Tập trung vào tiền xử lý dữ liệu (Data Cleaning), truy vấn SQL kiểm tra chất lượng & so sánh nhóm churn, trực quan hóa cơ bản và thiết kế Dashboard.
<<<<<<< HEAD
*   **Nguyễn Hữu Kiệt (Member):** Tập trung vào truy vấn SQL (Churn Rate, hành vi theo nhóm hợp đồng/dịch vụ), tổng hợp dữ liệu (Aggregation bằng Pandas), trực quan hóa nâng cao và tổng hợp Insight.
=======
*   **Nguyễn Hữu Kiệt (Member):** Tập trung vào truy vấn SQL (Churn Rate, hành vi theo nhóm), tổng hợp dữ liệu (Aggregation bằng Pandas), trực quan hóa nâng cao và tổng hợp Insight.
>>>>>>> feat01-docs-project-document

---

## 📅 LỘ TRÌNH CHI TIẾT THEO SPRINT

### Sprint 1: Khởi tạo dự án, Xử lý dữ liệu thô & Thiết lập SQL (18/05 - 24/05)
<<<<<<< HEAD
**Mục tiêu:** Cài đặt xong môi trường làm việc nhóm, đọc và làm sạch toàn bộ dữ liệu thô từ bộ *Telco Customer Churn: IBM dataset*, thiết lập **Microsoft SQL Server** phục vụ phân tích.

**1. Huỳnh Gia Bảo**
*   **Task 1:** Thiết lập GitHub Repository (Tạo file `.gitignore`, `requirements.txt`, thư mục cấu trúc bao gồm `sql/`).
*   **Task 2:** Viết Base Code (Jupyter Notebook) để đọc dữ liệu Telco từ IBM, cấu hình môi trường ảo (`venv`) và viết tài liệu hướng dẫn nhanh cho Duy và Kiệt cài đặt.
*   **Task 3 (SQL Server):** Thiết kế schema và tạo database trên **Microsoft SQL Server**:
    * Cài đặt và sử dụng **Azure Data Studio** / **SSMS**; tạo database dự án.
    * Viết file DDL T-SQL (`sql/schema.sql`) tạo bảng thông tin **khách hàng** (nhân khẩu học), **hợp đồng & thanh toán**, và **dịch vụ viễn thông**.
=======
**Mục tiêu:** Cài đặt xong môi trường làm việc nhóm, đọc và làm sạch toàn bộ dữ liệu thô từ bộ *Online Shoppers Purchasing Intention*, thiết lập **Microsoft SQL Server** phục vụ phân tích.

**1. Huỳnh Gia Bảo**
*   **Task 1:** Thiết lập GitHub Repository (Tạo file `.gitignore`, `requirements.txt`, thư mục cấu trúc bao gồm `sql/`).
*   **Task 2:** Viết Base Code (Jupyter Notebook) để đọc dữ liệu từ UCI, cấu hình môi trường ảo (`venv`) và viết tài liệu hướng dẫn nhanh cho Duy và Kiệt cài đặt.
*   **Task 3 (SQL Server):** Thiết kế schema và tạo database trên **Microsoft SQL Server**:
    * Cài đặt và sử dụng **Azure Data Studio** / **SSMS**; tạo database dự án.
    * Viết file DDL T-SQL (`sql/schema.sql`) tạo bảng **khách hàng** và bảng **phiên truy cập** từ dữ liệu UCI.
>>>>>>> feat01-docs-project-document
    * Viết script import nạp CSV đã sạch vào SQL Server. Cung cấp file mẫu `sql/.env.example`.
*   *Đầu ra:* Mọi người clone được code, chạy được file base; database SQL Server và script DDL/import sẵn sàng.

**2. Nguyễn An Duy**
*   **Task 1:** Thiết lập không gian quản lý dự án trên **Notion** (Backlog, To Do, In Progress, Review, Done) và tạo kênh giao tiếp riêng cho nhóm trên **Discord** để đồng bộ tiến độ.
<<<<<<< HEAD
*   **Task 2:** Xử lý dữ liệu thiếu (Missing values) và ngoại lệ (đặc biệt lưu ý cột `TotalCharges` có thể trống ở khách hàng mới) bằng `pandas`. Mã hóa các biến phân loại (Yes/No, Contract, Payment Method) và chuẩn hóa biến số.
=======
*   **Task 2:** Xử lý dữ liệu thiếu (Missing values) và dữ liệu nhiễu/ngoại lệ (Outliers) bằng thư viện `pandas`, mã hóa biến phân loại và chuẩn hóa các biến số theo yêu cầu.
>>>>>>> feat01-docs-project-document
*   **Task 3 (SQL):** Viết truy vấn SQL kiểm tra chất lượng dữ liệu sau khi import (`sql/data_quality_checks.sql`).
*   *Đầu ra:* DataFrame đã làm sạch và chuẩn hóa; báo cáo ngắn xác nhận dữ liệu SQL sẵn sàng.

**3. Nguyễn Hữu Kiệt**
<<<<<<< HEAD
*   **Task 1:** Sử dụng `pandas.groupby()` để tổng hợp dữ liệu — khám phá nhanh hành vi tiêu dùng, số tháng gắn bó (`Tenure`) và cước phí.
*   **Task 2 (SQL):** Viết truy vấn SQL tính **Churn Rate** theo các chiều yêu cầu (`sql/churn_rate_by_segment.sql`):
    * Theo Loại hợp đồng (Contract).
    * Theo Phương thức thanh toán (Payment Method).
    * Theo các gói dịch vụ đi kèm (Internet, Tech Support, Security...).
=======
*   **Task 1:** Sử dụng `pandas.groupby()` để tổng hợp dữ liệu — khám phá nhanh hành vi duyệt web, thời lượng phiên.
*   **Task 2 (SQL):** Viết truy vấn SQL tính **Churn Rate** theo các chiều yêu cầu (`sql/churn_rate_by_segment.sql`):
    * Theo thiết bị truy cập.
    * Theo nguồn truy cập.
    * Theo tháng và phân loại khách hàng.
>>>>>>> feat01-docs-project-document
*   *Đầu ra:* Các bảng kết quả SQL thể hiện rõ nhóm có tỷ lệ rời bỏ cao nhất.

---

### Sprint 2: Phân tích SQL nâng cao, Kỹ nghệ đặc trưng & Trực quan hóa (25/05 - 31/05)
<<<<<<< HEAD
**Mục tiêu:** Phác họa hành vi khách hàng viễn thông, tạo biến mới và vẽ biểu đồ đối chiếu giữa nhóm Churn và Non-churn.

**1. Huỳnh Gia Bảo**
*   **Task 1:** Thực hiện Kỹ nghệ đặc trưng (Feature Engineering) tạo các biến phân tích chuyên sâu bằng Python: `tenure_group` (phân nhóm thời gian sử dụng), `service_diversity` (số lượng dịch vụ phụ trợ), `monthly_charges_ratio`, và `is_paperless_electronic`.
=======
**Mục tiêu:** Phác họa hành vi khách hàng, tạo biến mới và vẽ biểu đồ đối chiếu giữa nhóm Churn và Non-churn.

**1. Huỳnh Gia Bảo**
*   **Task 1:** Thực hiện Kỹ nghệ đặc trưng (Feature Engineering) tạo các biến phân tích chuyên sâu bằng Python: `session_intensity`, `visit_frequency`, `weekend_behavior`, và các biến liên quan đến tỷ lệ chuyển đổi.
>>>>>>> feat01-docs-project-document
*   **Task 2 (SQL Server):** Tạo **VIEW** hoặc bảng tổng hợp T-SQL (`sql/feature_summary.sql`) đồng bộ các đặc trưng mới để hỗ trợ modeling.
*   **Task 3:** Đọc, góp ý và duyệt (Review & Merge) các Pull Request của Duy và Kiệt.
*   *Đầu ra:* Bộ dữ liệu chuẩn bị sẵn sàng cho thuật toán phân loại.

**2. Nguyễn An Duy**
<<<<<<< HEAD
*   **Task 1 (SQL):** Viết truy vấn SQL **so sánh hành vi chi tiết** giữa nhóm churn và non-churn (mức cước phí, số tháng gắn bó...).
*   **Task 2:** Sử dụng `seaborn` / `matplotlib` vẽ **Bar Chart** và **Boxplot** để trực quan hóa sự khác biệt về cước phí hàng tháng (`MonthlyCharges`) và tổng cước (`TotalCharges`) dựa trên kết quả SQL.
*   *Đầu ra:* File SQL + biểu đồ trực quan có độ tương phản rõ rệt giữa hai nhóm.

**3. Nguyễn Hữu Kiệt**
*   **Task 1 (SQL):** Viết truy vấn SQL xác định các yếu tố dịch vụ có chênh lệch lớn nhất giữa khách ở lại và khách rời đi (ví dụ: thiếu Tech Support hay Online Security).
*   **Task 2:** Vẽ **Correlation Heatmap** đánh giá tương quan đa biến và vẽ biểu đồ **Churn theo nhóm Tenure** để tìm điểm gãy trải nghiệm.
*   *Đầu ra:* Kết quả SQL + Heatmap/Biểu đồ Tenure chỉ ra các biến có ảnh hưởng tiềm năng nhất.
=======
*   **Task 1 (SQL):** Viết truy vấn SQL **so sánh hành vi chi tiết** giữa nhóm churn và non-churn (số trang xem, thời lượng...).
*   **Task 2:** Sử dụng `seaborn` / `matplotlib` vẽ **Bar Chart** và **Boxplot** để trực quan hóa sự khác biệt hành vi dựa trên kết quả SQL.
*   *Đầu ra:* File SQL + biểu đồ trực quan có độ tương phản rõ rệt giữa hai nhóm.

**3. Nguyễn Hữu Kiệt**
*   **Task 1 (SQL):** Viết truy vấn SQL xác định các yếu tố có chênh lệch lớn nhất giữa khách ở lại và khách rời đi.
*   **Task 2:** Vẽ **Correlation Heatmap** đánh giá tương quan đa biến và vẽ **Cohort Chart** theo dõi tỷ lệ giữ chân khách hàng qua các tháng.
*   *Đầu ra:* Kết quả SQL + Heatmap/Cohort chỉ ra các biến có ảnh hưởng tiềm năng nhất.
>>>>>>> feat01-docs-project-document

---

### Sprint 3: Huấn luyện Mô hình & Xây dựng Dashboard (01/06 - 07/06)
<<<<<<< HEAD
**Mục tiêu:** Xây dựng mô hình phân loại dự đoán tỷ lệ rời bỏ mạng viễn thông và tạo Dashboard báo cáo chiến lược.
=======
**Mục tiêu:** Xây dựng mô hình phân loại dự đoán tỷ lệ rời bỏ và tạo Dashboard báo cáo chiến lược.
>>>>>>> feat01-docs-project-document

**1. Huỳnh Gia Bảo**
*   **Task 1:** Chia tập dữ liệu, triển khai và huấn luyện mô hình Baseline (**Logistic Regression**) với phần phân tích chi tiết các hệ số hồi quy.
*   **Task 2:** Triển khai các mô hình nâng cao (**Random Forest**, **XGBoost**). Trích xuất danh sách *Feature Importance*.
<<<<<<< HEAD
*   **Task 3:** Đánh giá hiệu suất tổng thể bằng Accuracy, Precision, Recall, F1-score, ROC-AUC. Tập trung điều chỉnh ngưỡng để **tối ưu hóa chỉ số Recall** (tránh bỏ sót khách hàng có nguy cơ rời đi).
=======
*   **Task 3:** Đánh giá hiệu suất tổng thể bằng Accuracy, Precision, Recall, F1-score, ROC-AUC. Tập trung điều chỉnh ngưỡng để **tối ưu hóa chỉ số Recall**.
>>>>>>> feat01-docs-project-document
*   *Đầu ra:* Lựa chọn được mô hình tốt nhất với các chỉ số đánh giá hoàn thiện.

**2. Nguyễn An Duy**
*   **Task 1:** Kết nối **Power BI** hoặc **Tableau** trực tiếp tới SQL Server.
<<<<<<< HEAD
*   **Task 2:** Xây dựng Dashboard bao gồm: Tổng quan Churn Rate, Top risk segments (Nhóm rủi ro cao), Feature importance, và Churn by Service Type.
*   *Đầu ra:* Dashboard tương tác phục vụ góc nhìn Business cho doanh nghiệp viễn thông.

**3. Nguyễn Hữu Kiệt**
*   **Task 1:** Tổng hợp kết quả từ *Feature Importance* (Mô hình) và Dashboard để trả lời các câu hỏi nghiên cứu trọng tâm.
*   **Task 2:** Xây dựng khung đề xuất giải pháp (Actionable insights): Đề xuất kịch bản chuyển đổi hợp đồng Month-to-month sang hợp đồng dài hạn (1-2 năm) và thiết lập hệ thống cảnh báo sớm (Early-warning system) khi `monthly_charges_ratio` tăng cao.
=======
*   **Task 2:** Xây dựng Dashboard bao gồm: Tổng quan Churn Rate, Top risk segments, Phễu chuyển đổi (Conversion funnel), và Feature importance.
*   *Đầu ra:* Dashboard tương tác phục vụ góc nhìn Business.

**3. Nguyễn Hữu Kiệt**
*   **Task 1:** Tổng hợp kết quả từ *Feature Importance* (Mô hình) và Dashboard để trả lời các câu hỏi nghiên cứu trọng tâm.
*   **Task 2:** Xây dựng khung đề xuất giải pháp (Actionable insights) nhằm giảm CAC và giữ chân khách hàng, cụ thể: Tự động gửi Email Remarketing, Cung cấp ưu đãi nhắm mục tiêu, Cá nhân hóa hệ thống đề xuất.
>>>>>>> feat01-docs-project-document
*   *Đầu ra:* Bản phác thảo Insights chiến lược sẵn sàng cho báo cáo học thuật.

---

### Sprint 4: Viết Báo cáo & Tổng duyệt (08/06 - 14/06)
**Mục tiêu:** Hoàn thiện báo cáo học thuật và chuẩn bị trình bày.

**1. Huỳnh Gia Bảo**
*   **Task 1:** Viết phần **Methodology** và **Experimental Results** (So sánh Logistic Regression, Random Forest, XGBoost).
*   **Task 2:** Quản lý cấu trúc file LaTeX, đảm bảo format chuẩn IEEE/Springer.

**2. Nguyễn An Duy**
<<<<<<< HEAD
*   **Task 1:** Viết phần **Introduction** và **Business Understanding** (nhấn mạnh bài toán CAC trong ngành Viễn thông).
*   **Task 2:** Trích xuất hình ảnh từ Dashboard, chèn biểu đồ và các bảng kết quả SQL vào báo cáo.

**3. Nguyễn Hữu Kiệt**
*   **Task 1:** Viết phần **Conclusion** và các **Đề xuất chiến lược** (Khuyến nghị hành động dựa trên insights dịch vụ và cước phí).
=======
*   **Task 1:** Viết phần **Introduction** và **Business Understanding**.
*   **Task 2:** Trích xuất hình ảnh từ Dashboard, chèn biểu đồ và các bảng kết quả SQL vào báo cáo.

**3. Nguyễn Hữu Kiệt**
*   **Task 1:** Viết phần **Conclusion** và các **Đề xuất chiến lược** (Khuyến nghị hành động).
>>>>>>> feat01-docs-project-document
*   **Task 2:** Thiết kế Slide thuyết trình tổng kết dự án.