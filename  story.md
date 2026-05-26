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

5.1. Lưu trữ & Truy xuất Dữ liệu với SQL (Data Storage & Querying)

* Vai trò của SQL: Đóng vai trò là cơ sở dữ liệu (Database) dùng để lưu trữ và quản lý tập dữ liệu IBM Telco.
* Thực thi:
  * Thiết lập cấu trúc bảng (CREATE TABLE) cho thông tin khách hàng và dịch vụ.
  * Chỉ sử dụng SQL để viết các câu lệnh truy vấn (SELECT, JOIN, WHERE) nhằm trích xuất tập dữ liệu theo nhóm và đẩy vào môi trường Python. Không thực hiện xử lý logic hay tính toán phức tạp trên SQL.

5.2. Tiền xử lý, Trực quan hóa & Phân tích bằng Python (Data Processing & Visualization)

Toàn bộ logic làm sạch dữ liệu, EDA và trực quan hóa đều được thực hiện trên Python theo kiến trúc 2 giai đoạn.

* Tiền xử lý - Giai đoạn 1 (Global): Dùng pandas để làm sạch cơ bản, điền các giá trị bị thiếu (missing values), mã hóa các biến phân loại (Categorical encoding) và thực hiện Feature Engineering. Tuyệt đối giữ nguyên dữ liệu ngoại lai (outliers) ở bước này.
* Tiền xử lý - Giai đoạn 2 (Local): Sử dụng `sklearn.pipeline.Pipeline` để phân nhánh độc lập. Nhánh mô hình tuyến tính sẽ có bước xử lý outlier và chuẩn hóa (scaling), trong khi nhánh mô hình cây (Tree-based) sẽ nhận trực tiếp dữ liệu thô chứa outlier.
* Trực quan hóa: Sử dụng seaborn và matplotlib để vẽ Bar Chart, Boxplot và Heatmap nhằm phân tích cước phí và tương quan đặc trưng.

5.3. Huấn luyện & Đánh giá Mô hình (Modeling)

* Baseline Model: Sử dụng Logistic Regression. Phân tích chi tiết các hệ số hồi quy (coefficients) để hiểu chiều tác động của các biến.
* Advanced Models: Triển khai Random Forest và XGBoost để tối ưu hóa độ chính xác.
* Metrics Đánh giá: Accuracy, Precision, Recall, F1-score, ROC-AUC. Ưu tiên tối ưu hóa Recall để tránh bỏ sót khách hàng có nguy cơ rời đi.

6. Xây dựng Dashboard & Đề xuất Chiến lược

* Nền tảng: Power BI hoặc Tableau.
* Thành phần: Tổng quan Churn Rate, Top risk segments (Nhóm rủi ro cao), Feature importance, Churn by Service Type.
* Khuyến nghị Hành động (Actionable Insights):
  * Đề xuất chuyển đổi từ hợp đồng Month-to-month sang hợp đồng dài hạn (1-2 năm) bằng ưu đãi cước phí.
  * Thiết lập hệ thống cảnh báo sớm (Early-warning system) khi khách hàng có chỉ số monthly_charges_ratio tăng cao để chủ động CSKH tư vấn gói cước tối ưu hơn.