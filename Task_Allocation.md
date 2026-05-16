# 📋 PHÂN CHIA CÔNG VIỆC CHI TIẾT (TASK BREAKDOWN)
**Dự án:** Predictive Customer Churn in E-commerce Subscription Services
**Thời gian thực hiện:** 18/05/2026 – /06/2026

---

## 👥 THÔNG TIN ĐỘI NHÓM
*   **Huỳnh Gia Bảo (Team Leader):** Chịu trách nhiệm thiết lập dự án, thiết kế schema & pipeline **Microsoft SQL Server**, xử lý logic phức tạp (Feature Engineering, Modeling) và Review code.
*   **Nguyễn An Duy (Member):** Tập trung vào tiền xử lý dữ liệu (Data Cleaning), truy vấn SQL kiểm tra chất lượng & so sánh nhóm churn, trực quan hóa cơ bản và thiết kế Dashboard.
*   **Nguyễn Hữu Kiệt (Member):** Tập trung vào truy vấn SQL (Churn Rate, hành vi theo nhóm), tổng hợp dữ liệu (Aggregation bằng Pandas), trực quan hóa nâng cao và tổng hợp Insight.

---

## 📅 LỘ TRÌNH CHI TIẾT THEO SPRINT

### Sprint 1: Khởi tạo dự án, Xử lý dữ liệu thô & Thiết lập SQL (18/05 - 25/05)
**Mục tiêu:** Cài đặt xong môi trường làm việc nhóm, đọc và làm sạch toàn bộ dữ liệu thô, thiết lập **Microsoft SQL Server** phục vụ phân tích (theo mục 5 – `Request.md`).

**1. Huỳnh Gia Bảo**
*   **Task 1:** Thiết lập GitHub Repository (Tạo file `.gitignore`, `requirements.txt`, thư mục cấu trúc bao gồm `sql/`).
*   **Task 2:** Viết Base Code (Jupyter Notebook) để đọc dữ liệu từ UCI, cấu hình môi trường ảo (`venv`) và viết tài liệu hướng dẫn nhanh cho Duy và Kiệt cài đặt.
*   **Task 3 (SQL Server):** Thiết kế schema và tạo database trên **Microsoft SQL Server**:
    * Cài **SQL Server** (Express/Developer) + **SSMS** (SQL Server Management Studio) hoặc **Azure Data Studio** trên máy Leader; tạo database dự án (ví dụ: `ChurnEcommerce`).
    * Viết file DDL T-SQL (ví dụ: `sql/schema.sql`) tạo bảng **khách hàng** (`customers`) và bảng **phiên truy cập** (`sessions`) từ dữ liệu UCI đã làm sạch.
    * Viết script import (`sql/import_data.sql` hoặc notebook Python dùng `pyodbc` + `pandas.to_sql` / `BULK INSERT`) nạp CSV đã sạch vào SQL Server.
    * Cung cấp file mẫu `sql/.env.example` (connection string, **không** commit `.env` thật).
*   *Đầu ra:* Mọi người clone được code, chạy được file base; database SQL Server và script DDL/import sẵn sàng cho truy vấn.

**2. Nguyễn An Duy**
*   **Task 1:** Thiết lập bảng Trello theo cấu trúc nhóm (Backlog, To Do, In Progress, Review, Done) và tạo các nhãn (Labels) màu sắc.
*   **Task 2:** Xử lý dữ liệu thiếu (Missing values) và dữ liệu nhiễu/ngoại lệ (Outliers) bằng thư viện `pandas` dựa trên file base của Leader.
*   **Task 3 (SQL):** Viết truy vấn SQL kiểm tra chất lượng dữ liệu sau khi import (file `sql/data_quality_checks.sql` hoặc notebook tương đương):
    * Đếm số dòng, kiểm tra giá trị `NULL`, trùng lặp khóa phiên.
    * Xác nhận phân bố cơ bản của biến phân loại (device, traffic source, visitor type) trước khi phân tích churn.
*   *Đầu ra:* File `.csv` / DataFrame đã sạch; báo cáo ngắn (bảng kết quả SQL) xác nhận dữ liệu sẵn sàng phân tích.

**3. Nguyễn Hữu Kiệt**
*   **Task 1:** Sử dụng `pandas.groupby()` để tổng hợp dữ liệu (Data Aggregation) — khám phá nhanh, đối chiếu với kết quả SQL.
*   **Task 2 (SQL):** Viết truy vấn SQL tính **Churn Rate** theo các chiều yêu cầu trong `Request.md` (file `sql/churn_rate_by_segment.sql`):
    * Theo thiết bị (`OperatingSystems` / device).
    * Theo nguồn truy cập (`TrafficType` / source).
    * Theo tháng (`Month`) và loại khách (`VisitorType`).
    * Sắp xếp nhóm có churn rate cao nhất để phục vụ báo cáo.
*   *Đầu ra:* Các bảng kết quả SQL (export `.csv` nhỏ hoặc screenshot trong notebook) thể hiện rõ nhóm nào có tỷ lệ churn cao nhất; đối chiếu khớp với aggregation Pandas ở Task 1.

---

### Sprint 2: Phân tích SQL nâng cao, Kỹ nghệ đặc trưng & Trực quan hóa (26/05 - 02/06)
**Mục tiêu:** Hoàn thành phân tích SQL (so sánh churn/non-churn, yếu tố ảnh hưởng), tạo biến mới và vẽ biểu đồ để kể câu chuyện từ dữ liệu.

**1. Huỳnh Gia Bảo**
*   **Task 1:** Tạo các biến phức tạp (Feature Engineering) như mức độ tương tác phiên (`session intensity`), hành vi cuối tuần (`weekend behavior`); đồng bộ các biến mới vào bảng SQL nếu cần cho truy vấn tiếp theo.
*   **Task 2 (SQL Server):** Tạo **VIEW** hoặc bảng tổng hợp T-SQL (`sql/feature_summary.sql`) hỗ trợ modeling: tổng hợp metric phiên theo nhóm churn/non-churn, phục vụ đối chiếu với Feature Importance sau này.
*   **Task 3:** Đọc, góp ý và duyệt (Review & Merge) các Pull Request của Duy và Kiệt trên GitHub (bao gồm file `.sql` và notebook).
*   *Đầu ra:* Bộ dữ liệu hoàn chỉnh + bộ truy vấn/view SQL sẵn sàng cho huấn luyện mô hình và báo cáo.

**2. Nguyễn An Duy**
*   **Task 1 (SQL):** Viết truy vấn SQL **so sánh hành vi chi tiết** giữa nhóm churn và non-churn (`sql/churn_vs_nonchurn_behavior.sql`):
    * So sánh trung bình/trung vị: thời lượng phiên (`ProductRelated_Duration`, `Administrative_Duration`, …), số trang đã xem, `BounceRates`, `ExitRates`, `PageValues`.
    * Dùng `GROUP BY` churn label + `HAVING` / window function nếu cần.
*   **Task 2:** Dùng kết quả SQL ở Task 1 làm nguồn số liệu, vẽ Bar Chart (tỷ lệ churn theo nhóm) và Boxplot (`session duration` / duration tương ứng) bằng `seaborn`/`matplotlib`.
*   *Đầu ra:* File SQL + biểu đồ rõ nét, có tiêu đề và chú thích, lưu trong thư mục báo cáo/notebook.

**3. Nguyễn Hữu Kiệt**
*   **Task 1 (SQL):** Viết truy vấn SQL xác định **các yếu tố có mối liên hệ mạnh với churn** (`sql/churn_correlation_factors.sql`):
    * Ranking chênh lệch metric giữa churn vs non-churn; dùng T-SQL (`AVG`, `STDEV`, window functions như `ROW_NUMBER`, `RANK`) hoặc xuất bảng tổng hợp sang Python cho correlation nếu cần.
    * Ghi 2–3 nhận xét insight phục vụ phần giải thích nghiên cứu trong báo cáo.
*   **Task 2:** Vẽ Correlation Heatmap (Python) dựa trên bảng đã tổng hợp; thực hiện Cohort Analysis bằng `pandas` và vẽ biểu đồ Retention.
*   *Đầu ra:* Kết quả SQL + Heatmap/Cohort rõ ràng, kèm 2–3 gạch đầu dòng nhận xét mỗi phần trong Notebook.

---

### Sprint 3: Huấn luyện Mô hình & Xây dựng Dashboard (03/06 - 09/06)
**Mục tiêu:** Xây dựng mô hình máy học dự đoán và tạo giao diện theo dõi cho Business.

**1. Huỳnh Gia Bảo**
*   **Task 1:** Chia tập dữ liệu (Train/Test Split), huấn luyện 3 mô hình: Logistic Regression, Random Forest, XGBoost.
*   **Task 2:** Đánh giá mô hình dựa trên Accuracy, Precision, ROC-AUC và đặc biệt tối ưu chỉ số **Recall**. Trích xuất Feature Importance (Biến quan trọng nhất).
*   *Đầu ra:* Kết quả đánh giá so sánh (Bảng Metrics) và mô hình tốt nhất được chọn.

**2. Nguyễn An Duy**
*   **Task 1:** Kết nối Power BI trực tiếp tới **SQL Server** (Import hoặc DirectQuery) và/hoặc xuất bảng tổng hợp từ view/truy vấn SQL (churn rate theo segment).
*   **Task 2:** Kéo thả và thiết kế Dashboard hiển thị: Churn Rate tổng, Phễu chuyển đổi (Conversion funnel), và bộ lọc theo loại thiết bị/tháng (đồng bộ với các chiều đã phân tích bằng SQL).
*   *Đầu ra:* Một Dashboard có thể tương tác được (file `.pbix` hoặc link Tableau Public).

**3. Nguyễn Hữu Kiệt**
*   **Task 1:** Đọc kết quả Feature Importance từ mô hình của Bảo, Dashboard của Duy và **đối chiếu với kết quả phân tích SQL** (Sprint 1–2).
*   **Task 2:** Viết tài liệu tổng hợp (Research Insights): Yếu tố nào làm khách hàng rời bỏ? Nhóm segment SQL nào rủi ro cao nhất? Doanh nghiệp cần làm gì?
*   *Đầu ra:* File `.md` hoặc Word nháp có mục riêng **SQL Findings vs Model Findings** để chuẩn bị báo cáo chính thức.

---

### Sprint 4: Viết Báo cáo chuẩn IEEE (Springer) & Tổng duyệt (10/06 - 15/06)
**Mục tiêu:** Hoàn thiện báo cáo học thuật (10-12 trang) trên Overleaf và chuẩn bị slide thuyết trình.

**1. Huỳnh Gia Bảo**
*   **Task 1:** Viết phần **Methodology** (gồm mô tả pipeline SQL: schema, import, các nhóm truy vấn chính) và **Experimental Results** (kết quả mô hình) bằng tiếng Anh trên LaTeX.
*   **Task 2:** Format toàn bộ file LaTeX đảm bảo chuẩn template, không lỗi biên dịch.

**2. Nguyễn An Duy**
*   **Task 1:** Viết phần **Introduction** (Giới thiệu bài toán) và **Business Understanding** (Hiểu biết nghiệp vụ) bằng tiếng Anh trên LaTeX.
*   **Task 2:** Chèn biểu đồ, **bảng kết quả truy vấn SQL** (churn rate theo segment, so sánh churn vs non-churn) và Dashboard vào báo cáo LaTeX.

**3. Nguyễn Hữu Kiệt**
*   **Task 1:** Viết phần **Conclusion** (Kết luận và Đề xuất hành động) bằng tiếng Anh trên LaTeX dựa trên phần Insights đã làm ở Sprint 3.
*   **Task 2:** Thiết kế Slide PowerPoint (hoặc Canva) phục vụ cho buổi thuyết trình bảo vệ dự án.

---
## 🗄️ YÊU CẦU SQL (Đối chiếu `project_request/Request.md` – Mục 5)

| Yêu cầu trong Request | Sprint | Người phụ trách |
|------------------------|--------|-----------------|
| Tạo bảng khách hàng & phiên truy cập | Sprint 1 | Huỳnh Gia Bảo |
| Churn Rate theo device, source, tháng, loại khách | Sprint 1 | Nguyễn Hữu Kiệt |
| Kiểm tra & làm sạch dữ liệu trong DB | Sprint 1 | Nguyễn An Duy |
| So sánh hành vi churn vs non-churn | Sprint 2 | Nguyễn An Duy |
| Yếu tố tương quan / ảnh hưởng mạnh đến churn | Sprint 2 | Nguyễn Hữu Kiệt |
| View/tổng hợp phục vụ modeling | Sprint 2 | Huỳnh Gia Bảo |
| Đưa kết quả SQL vào báo cáo LaTeX | Sprint 4 | Duy (bảng/hình), Bảo (Methodology) |

### Công nghệ SQL: Microsoft SQL Server

| Thành phần | Gợi ý |
|------------|--------|
| **Database** | SQL Server Express hoặc Developer Edition (miễn phí cho học tập) |
| **Quản lý & chạy query** | SSMS hoặc Azure Data Studio |
| **Ngôn ngữ** | T-SQL (file `.sql` trong thư mục `sql/`) |
| **Python ↔ SQL Server** | `pyodbc` + ODBC Driver 17/18 for SQL Server; `pandas.read_sql` / `to_sql` |
| **Power BI** | Connector **SQL Server** (native) — phù hợp Sprint 3 |
| **Bảo mật repo** | Chỉ commit `sql/.env.example`; mật khẩu/connection string đặt trong `.env` (đã `.gitignore`) |

**Đồng bộ nhóm:** Cả 3 thành viên dùng chung tên database (`ChurnEcommerce`), cùng script `schema.sql` + `import_data.sql`. Nếu không cài SQL Server local, có thể dùng **SQL Server trên Docker** hoặc **Azure SQL Database** (1 instance dùng chung, Leader cấp connection string qua kênh riêng).

---

## 📌 LƯU Ý QUAN TRỌNG (Dành cho Duy & Kiệt)
1. **GitHub:** Luôn tạo nhánh mới (branch) trước khi code. KHÔNG BAO GIỜ tự ý push thẳng lên nhánh `main`. Nhờ Bảo review code trước khi gộp (merge).
2. **Trello:** Bắt đầu làm task nào thì kéo thẻ (Card) đó sang cột "In Progress". Code xong tạo Pull Request thì kéo sang "Review". Task SQL nên gắn nhãn **Data Cleaning** hoặc **EDA / Model** tùy giai đoạn.
3. **Môi trường ảo:** Nhớ luôn bật môi trường ảo (`venv`) trước khi mở Jupyter Notebook; cài `pyodbc` theo `requirements.txt` khi Leader cập nhật.
4. **SQL Server:** Commit file `.sql`, notebook và `.env.example`; **không** commit `.env`, backup `.bak` hay file dữ liệu nặng — chỉ giữ script tái tạo database từ CSV đã sạch.