# 📋 PHÂN CHIA CÔNG VIỆC CHI TIẾT (TASK BREAKDOWN)
**Dự án:** Predictive Customer Churn in E-commerce Subscription Services
**Thời gian thực hiện:** 18/05/2026 – /06/2026

---

## 👥 THÔNG TIN ĐỘI NHÓM
*   **Huỳnh Gia Bảo (Team Leader):** Chịu trách nhiệm thiết lập dự án, xử lý logic phức tạp (Feature Engineering, Modeling) và Review code.
*   **Nguyễn An Duy (Member):** Tập trung vào tiền xử lý dữ liệu (Data Cleaning), trực quan hóa cơ bản và thiết kế Dashboard.
*   **Nguyễn Hữu Kiệt (Member):** Tập trung vào tổng hợp dữ liệu (Aggregation bằng Pandas), trực quan hóa nâng cao và tổng hợp Insight.

---

## 📅 LỘ TRÌNH CHI TIẾT THEO SPRINT

### Sprint 1: Khởi tạo dự án & Xử lý dữ liệu thô (18/05 - 25/05)
**Mục tiêu:** Cài đặt xong môi trường làm việc nhóm, đọc và làm sạch toàn bộ dữ liệu thô.

**1. Huỳnh Gia Bảo**
*   **Task 1:** Thiết lập GitHub Repository (Tạo file `.gitignore`, `requirements.txt`, thư mục cấu trúc).
*   **Task 2:** Viết Base Code (Jupyter Notebook) để đọc dữ liệu từ UCI, cấu hình môi trường ảo (`venv`) và viết tài liệu hướng dẫn nhanh cho Duy và Kiệt cài đặt.
*   *Đầu ra:* Mọi người đều clone được code về máy và chạy được file base thành công.

**2. Nguyễn An Duy**
*   **Task 1:** Thiết lập bảng Trello theo cấu trúc nhóm (Backlog, To Do, In Progress, Review, Done) và tạo các nhãn (Labels) màu sắc.
*   **Task 2:** Xử lý dữ liệu thiếu (Missing values) và dữ liệu nhiễu/ngoại lệ (Outliers) bằng thư viện `pandas` dựa trên file base của Leader.
*   *Đầu ra:* File `.csv` hoặc DataFrame đã sạch, không còn giá trị `NaN`, sẵn sàng cho bước phân tích.

**3. Nguyễn Hữu Kiệt**
*   **Task 1:** Sử dụng `pandas.groupby()` để tổng hợp dữ liệu (Data Aggregation).
*   **Task 2:** Tính toán tỷ lệ rời bỏ (Churn Rate) cơ bản phân loại theo thiết bị (Device) và nguồn truy cập (Source).
*   *Đầu ra:* Các bảng thống kê dạng số (Dataframes) thể hiện rõ nhóm nào có tỷ lệ churn cao nhất.

---

### Sprint 2: Kỹ nghệ đặc trưng (Feature Engineering) & Trực quan hóa (26/05 - 02/06)
**Mục tiêu:** Tạo thêm các biến có ý nghĩa và vẽ biểu đồ để tìm ra câu chuyện từ dữ liệu.

**1. Huỳnh Gia Bảo**
*   **Task 1:** Tạo các biến phức tạp (Feature Engineering) như mức độ tương tác phiên (`session intensity`), hành vi cuối tuần (`weekend behavior`).
*   **Task 2:** Đọc, góp ý và duyệt (Review & Merge) các Pull Request của Duy và Kiệt trên GitHub.
*   *Đầu ra:* Bộ dữ liệu hoàn chỉnh cuối cùng đã sẵn sàng để đưa vào huấn luyện mô hình.

**2. Nguyễn An Duy**
*   **Task 1:** Sử dụng thư viện `seaborn` và `matplotlib` để vẽ Bar Chart (Biểu đồ cột) so sánh tỷ lệ churn giữa các nhóm khách hàng.
*   **Task 2:** Vẽ Boxplot để xem xét sự khác biệt về thời lượng truy cập (`session duration`) giữa nhóm rời bỏ và nhóm ở lại.
*   *Đầu ra:* Các biểu đồ rõ nét, có tiêu đề và chú thích đầy đủ, được lưu trữ trong thư mục báo cáo.

**3. Nguyễn Hữu Kiệt**
*   **Task 1:** Vẽ biểu đồ nhiệt (Correlation Heatmap) để tìm ra các biến có ảnh hưởng mạnh nhất đến nhau và đến tỷ lệ Churn.
*   **Task 2:** Thực hiện phân tích Cohort (Cohort Analysis) bằng `pandas` và vẽ biểu đồ biểu diễn tỷ lệ giữ chân (Retention) theo thời gian.
*   *Đầu ra:* Biểu đồ Heatmap và Cohort rõ ràng, kèm theo 2-3 gạch đầu dòng nhận xét bên dưới mỗi biểu đồ trong Notebook.

---

### Sprint 3: Huấn luyện Mô hình & Xây dựng Dashboard (03/06 - 09/06)
**Mục tiêu:** Xây dựng mô hình máy học dự đoán và tạo giao diện theo dõi cho Business.

**1. Huỳnh Gia Bảo**
*   **Task 1:** Chia tập dữ liệu (Train/Test Split), huấn luyện 3 mô hình: Logistic Regression, Random Forest, XGBoost.
*   **Task 2:** Đánh giá mô hình dựa trên Accuracy, Precision, ROC-AUC và đặc biệt tối ưu chỉ số **Recall**. Trích xuất Feature Importance (Biến quan trọng nhất).
*   *Đầu ra:* Kết quả đánh giá so sánh (Bảng Metrics) và mô hình tốt nhất được chọn.

**2. Nguyễn An Duy**
*   **Task 1:** Xuất file dữ liệu đã làm sạch và đưa vào Power BI hoặc Tableau.
*   **Task 2:** Kéo thả và thiết kế Dashboard hiển thị: Churn Rate tổng, Phễu chuyển đổi (Conversion funnel), và bộ lọc theo loại thiết bị/tháng.
*   *Đầu ra:* Một Dashboard có thể tương tác được (file `.pbix` hoặc link Tableau Public).

**3. Nguyễn Hữu Kiệt**
*   **Task 1:** Đọc kết quả Feature Importance từ mô hình của Bảo và Dashboard của Duy.
*   **Task 2:** Viết tài liệu tổng hợp (Research Insights): Yếu tố nào làm khách hàng rời bỏ? Nhóm nào rủi ro cao nhất? Doanh nghiệp cần làm gì?
*   *Đầu ra:* Một file `.md` hoặc Word nháp chứa các gạch đầu dòng phân tích để chuẩn bị đưa vào báo cáo chính thức.

---

### Sprint 4: Viết Báo cáo chuẩn IEEE (Springer) & Tổng duyệt (10/06 - 15/06)
**Mục tiêu:** Hoàn thiện báo cáo học thuật (10-12 trang) trên Overleaf và chuẩn bị slide thuyết trình.

**1. Huỳnh Gia Bảo**
*   **Task 1:** Viết phần **Methodology** (Phương pháp thực hiện) và **Experimental Results** (Kết quả thử nghiệm mô hình) bằng tiếng Anh trên LaTeX.
*   **Task 2:** Format toàn bộ file LaTeX đảm bảo chuẩn template, không lỗi biên dịch.

**2. Nguyễn An Duy**
*   **Task 1:** Viết phần **Introduction** (Giới thiệu bài toán) và **Business Understanding** (Hiểu biết nghiệp vụ) bằng tiếng Anh trên LaTeX.
*   **Task 2:** Chèn các hình ảnh biểu đồ và Dashboard vào báo cáo LaTeX.

**3. Nguyễn Hữu Kiệt**
*   **Task 1:** Viết phần **Conclusion** (Kết luận và Đề xuất hành động) bằng tiếng Anh trên LaTeX dựa trên phần Insights đã làm ở Sprint 3.
*   **Task 2:** Thiết kế Slide PowerPoint (hoặc Canva) phục vụ cho buổi thuyết trình bảo vệ dự án.

---
## 📌 LƯU Ý QUAN TRỌNG (Dành cho Duy & Kiệt)
1. **GitHub:** Luôn tạo nhánh mới (branch) trước khi code. KHÔNG BAO GIỜ tự ý push thẳng lên nhánh `main`. Nhờ Bảo review code trước khi gộp (merge).
2. **Trello:** Bắt đầu làm task nào thì kéo thẻ (Card) đó sang cột "In Progress". Code xong tạo Pull Request thì kéo sang "Review".
3. **Môi trường ảo:** Nhớ luôn bật môi trường ảo (`venv`) trước khi mở Jupyter Notebook để tránh xung đột thư viện.