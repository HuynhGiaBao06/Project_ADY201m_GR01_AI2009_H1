PROJECT REQUIREMENTS: Predictive Customer Churn in Telecommunication Services

1. Mục tiêu Tổng quan (Project Requirements)

Phân tích các yếu tố khiến khách hàng ngừng sử dụng dịch vụ viễn thông, từ đó xây dựng mô hình học máy dự đoán khả năng rời bỏ (churn) nhằm đề xuất các chiến lược giữ chân khách hàng hiệu quả.

2. Hiểu biết Kinh doanh & Hướng Tiếp cận (Business Understanding and Analytic Approach)

* Vấn đề kinh doanh: Doanh nghiệp thất thoát doanh thu do khách hàng hủy hợp đồng hoặc rời bỏ dịch vụ sớm. Chi phí tìm kiếm khách hàng mới (CAC) luôn đắt đỏ hơn chi phí chăm sóc khách hàng cũ, do đó giảm thiểu tỷ lệ "Churn" là bài toán tối ưu lợi nhuận trực tiếp nhất trong ngành Viễn thông.
* Mục tiêu phân tích: Xác định chính xác nhóm khách hàng có nguy cơ churn cao và các nguyên nhân cốt lõi dẫn đến quyết định rời đi.
* Hướng phân tích:
  * Mô tả và phác họa hành vi, đặc điểm tiêu dùng của khách hàng.
  * Đối chiếu, so sánh đặc điểm giữa hai nhóm: Churn (rời bỏ) và Non-churn (ở lại).
  * Xây dựng mô hình phân loại (Classification model) để dự đoán xác suất rời đi của từng cá nhân dựa trên dữ liệu lịch sử hợp đồng và cước phí.
* Định hướng báo cáo: Tập trung làm nổi bật hiệu suất dự báo của các mô hình và phân tích sâu các yếu tố có trọng số ảnh hưởng mạnh nhất đến quyết định churn. Đưa ra các gói giải pháp (actionable insights) giúp doanh nghiệp can thiệp kịp thời.

3. Câu hỏi Nghiên cứu Trọng tâm (Research Questions)

1. Yếu tố nào tác động mạnh mẽ nhất đến xác suất rời bỏ dịch vụ của khách hàng viễn thông? (Phân tích Feature Importance).
2. Giữa các thuật toán Logistic Regression (Baseline), Random Forest, và XGBoost, mô hình nào đem lại hiệu suất dự đoán chính xác nhất?.
3. Khi áp dụng mô hình vào thực tế, doanh nghiệp nên ưu tiên phân bổ nguồn lực giữ chân nhóm khách hàng nào trước tiên để tối ưu chi phí?.

4. Hiểu & Chuẩn bị Dữ liệu (Data Understanding & Preparation)

* Nguồn dữ liệu (Dataset): Telco Customer Churn: IBM dataset. (Dữ liệu tĩnh đã có sẵn, không cần tiến hành thu thập thêm).
* Đặc trưng dữ liệu ban đầu:
  * Thông tin khách hàng: Giới tính, đối tác (partner), người phụ thuộc (dependents).
  * Thông tin dịch vụ: Internet, Phone, Streaming, Online Security, Tech Support.
  * Thông tin tài khoản: Loại hợp đồng (Contract), Phương thức thanh toán (Payment Method), Chi phí hàng tháng (Monthly Charges), Tổng chi phí (Total Charges), Số tháng gắn bó (Tenure).
* Kỹ nghệ Đặc trưng (Feature Engineering): Tổng hợp và tạo thêm các biến mới có giá trị phân tích cao:
  * tenure_group: Phân nhóm thời gian sử dụng (Ví dụ: 0-12 tháng, 12-24 tháng...) để tìm điểm gãy trải nghiệm.
  * service_diversity: Số lượng dịch vụ phụ trợ mà khách hàng có đăng ký (để đo độ gắn kết/trung thành).
  * monthly_charges_ratio: Tỷ lệ chi phí tháng so với mức trung bình để tìm ra khách hàng đang trả cước quá cao.
  * is_paperless_electronic: Tổ hợp phương thức nhận hóa đơn điện tử và thanh toán tự động (nhóm này thường ít churn hơn).

5. Kế hoạch Phân tích & Triển khai Kỹ thuật

5.1. Kiến trúc Luồng dữ liệu (Data Pipeline) & SQL

Data Cleaning & Ingestion (Python -> SQL): Dữ liệu thô (Raw Data) được xử lý làm sạch cơ bản trên Python (xử lý missing/null/sai format). Sau đó, tập dữ liệu sạch này được đẩy (ingest) lên cơ sở dữ liệu Azure SQL.

Data Storage & Views (SQL): Thiết lập cấu trúc bảng (CREATE TABLE) lưu trữ dữ liệu. Chỉ sử dụng SQL để tạo các VIEW (SELECT các cột cần thiết) và thực thi các câu lệnh truy vấn phục vụ phân tích EDA. Không thực hiện xử lý logic, tính toán phức tạp hay tạo biến mới (Feature Engineering) bằng T-SQL để đảm bảo luồng Pipeline chuẩn.

5.2. Tiền xử lý, Kỹ nghệ Đặc trưng & Trực quan hóa bằng Python
Toàn bộ quy trình chuẩn bị dữ liệu cho mô hình được thực hiện qua kiến trúc nối tiếp sau khi trích xuất (Extract) dữ liệu từ SQL View về Pandas DataFrame:

Tiền xử lý - Giai đoạn 1 (Feature Engineering): Triển khai hàm feature_engineering(df) trên Python để sinh ra các biến mới (như tenure_group, service_diversity...) từ tập dữ liệu kéo về từ SQL. Tuyệt đối giữ nguyên dữ liệu ngoại lai (outliers) ở bước này.

Tiền xử lý - Giai đoạn 2 (Sklearn Pipelines): Đưa toàn bộ Data (cột gốc + cột mới) vào ColumnTransformer. Chia làm 2 nhánh huấn luyện song song:

Nhánh Baseline (Logistic Regression): Bắt buộc có custom class xử lý ngoại lai (Capping) và chuẩn hóa (Scaling).

Nhánh Tree-based (Random Forest, XGBoost): Nhận trực tiếp dữ liệu thô (passthrough), không can thiệp outlier hay scaling.

Trực quan hóa (EDA): Sử dụng seaborn và matplotlib kết hợp với dữ liệu truy vấn từ SQL để vẽ Bar Chart, Boxplot, Heatmap nhằm phân tích hành vi rời bỏ.