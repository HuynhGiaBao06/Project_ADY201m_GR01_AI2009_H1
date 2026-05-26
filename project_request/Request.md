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

4. Thu thập, Hiểu & Chuẩn bị Dữ liệu (Data Collection, Understanding, Preparation)

* Nguồn dữ liệu (Dataset): Telco Customer Churn: IBM dataset.
* Đặc trưng dữ liệu ban đầu:
  * Thông tin khách hàng: Giới tính, đối tác (partner), người phụ thuộc (dependents).
  * Thông tin dịch vụ: Internet, Phone, Streaming, Online Security, Tech Support.
  * Thông tin tài khoản: Loại hợp đồng (Contract), Phương thức thanh toán (Payment Method), Chi phí hàng tháng (Monthly Charges), Tổng chi phí (Total Charges), Số tháng gắn bó (Tenure).
* Quy trình Tiền xử lý (Data Preparation) chia làm 2 giai đoạn:
  * Giai đoạn 1 (Global): Làm sạch cơ bản, điền missing values, mã hóa biến phân loại và tuyệt đối giữ nguyên outlier. 
  * Giai đoạn 2 (Local): Khai báo rõ việc phân nhánh tiền xử lý cục bộ bằng thư viện `sklearn.pipeline.Pipeline` cho nhánh tuyến tính (Logistic) và nhánh cây (XGBoost/RF). Nhánh Logistic sẽ xử lý outlier và chuẩn hóa biến số; nhánh XGBoost/RF sử dụng nguyên dữ liệu thô (raw data) không lọc outlier.
* Kỹ nghệ Đặc trưng (Feature Engineering): Cần tổng hợp và tạo thêm các biến mới có giá trị phân tích cao như:
  * tenure_group: Phân nhóm thời gian sử dụng (Ví dụ: 0-12 tháng, 12-24 tháng...) để tìm điểm gãy trải nghiệm.
  * service_diversity: Số lượng dịch vụ phụ trợ mà khách hàng có đăng ký (để đo độ gắn kết/trung thành).
  * monthly_charges_ratio: Tỷ lệ chi phí tháng so với mức trung bình để tìm ra khách hàng đang trả cước quá cao.
  * is_paperless_electronic: Tổ hợp phương thức nhận hóa đơn điện tử và thanh toán tự động (nhóm này thường ít churn hơn).

5. Kế hoạch Phân tích & Triển khai Kỹ thuật

5.1. Phân tích Dữ liệu với SQL & Python

* SQL: Thiết lập bảng thông tin khách hàng, tính toán Churn Rate theo Loại hợp đồng, Phương thức thanh toán, và các gói dịch vụ đi kèm. Đối chiếu sự khác biệt hành vi.
* Python: Sử dụng pandas để xử lý dữ liệu, seaborn / matplotlib để trực quan hóa (Bar chart, Boxplot, Heatmap, Churn theo nhóm Tenure).

5.2. Huấn luyện & Đánh giá Mô hình

* Baseline Model: Sử dụng Logistic Regression. Phân tích chi tiết các hệ số hồi quy (coefficients).
* Advanced Models: Triển khai Random Forest và XGBoost.
* Metrics Đánh giá: Accuracy, Precision, Recall, F1-score, ROC-AUC. Ưu tiên tối ưu hóa Recall để tránh bỏ sót khách hàng có nguy cơ rời đi.

6. Xây dựng Dashboard & Đề xuất Chiến lược

* Nền tảng: Power BI hoặc Tableau.
* Thành phần: Tổng quan Churn Rate, Top risk segments (Nhóm rủi ro cao), Feature importance, Churn by Service Type.
* Khuyến nghị Hành động (Actionable Insights):
  * Đề xuất chuyển đổi từ hợp đồng Month-to-month sang hợp đồng dài hạn (1-2 năm) bằng ưu đãi cước phí.
  * Thiết lập hệ thống cảnh báo sớm (Early-warning system) khi khách hàng có chỉ số monthly_charges_ratio tăng cao để chủ động CSKH tư vấn gói cước tối ưu hơn.