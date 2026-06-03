# YÊU CẦU DỰ ÁN (PROJECT REQUIREMENTS)

**Dự án:** Predictive Customer Churn in E-commerce Subscription Services (Dự đoán khách hàng rời bỏ trong dịch vụ đăng ký thương mại điện tử)

---

## 1. Mục tiêu Tổng quan
Phân tích các yếu tố khiến khách hàng ngừng sử dụng dịch vụ, từ đó xây dựng mô hình học máy dự đoán khả năng rời bỏ (churn) nhằm đề xuất các chiến lược giữ chân khách hàng hiệu quả.

---

## 2. Hiểu biết Kinh doanh & Hướng Tiếp cận (Business Understanding and Analytic Approach)
* **Vấn đề kinh doanh:** Doanh nghiệp thất thoát doanh thu do khách hàng hủy dịch vụ hoặc rời bỏ sớm. Chi phí tìm kiếm khách hàng mới (CAC) luôn đắt đỏ hơn chi phí chăm sóc khách hàng cũ, do đó giảm thiểu tỷ lệ "Churn" là bài toán tối ưu lợi nhuận trực tiếp nhất.
* **Mục tiêu phân tích:** Xác định chính xác nhóm khách hàng có nguy cơ churn cao và các nguyên nhân cốt lõi dẫn đến quyết định rời đi.
* **Hướng phân tích:**
    * Mô tả và phác họa hành vi khách hàng.
    * Đối chiếu, so sánh đặc điểm giữa hai nhóm: Churn (rời bỏ) và Non-churn (ở lại).
    * Xây dựng mô hình phân loại (Classification model) để dự đoán xác suất rời đi của từng cá nhân dựa trên dữ liệu lịch sử.
* **Định hướng báo cáo:** Tập trung làm nổi bật hiệu suất dự báo của các mô hình và phân tích sâu các yếu tố có trọng số ảnh hưởng mạnh nhất đến quyết định churn. Đưa ra các gói giải pháp (*actionable insights*) giúp doanh nghiệp can thiệp kịp thời.

---

## 3. Câu hỏi Nghiên cứu Trọng tâm (Research Questions)
1. Yếu tố nào tác động mạnh mẽ nhất đến xác suất rời bỏ dịch vụ của khách hàng? (Phân tích *Feature Importance*)
2. Giữa các thuật toán Logistic Regression (Baseline), Random Forest, và XGBoost, mô hình nào đem lại hiệu suất dự đoán chính xác nhất?
3. Khi áp dụng mô hình vào thực tế, doanh nghiệp nên ưu tiên phân bổ nguồn lực giữ chân nhóm khách hàng nào trước tiên để tối ưu chi phí?

---

## 4. Thu thập, Hiểu & Chuẩn bị Dữ liệu (Data Collection & Preparation)
* **Nguồn dữ liệu (Dataset):** Telco Customer Churn: IBM dataset.
* **Đặc trưng dữ liệu ban đầu:** Dữ liệu được phân loại và xử lý theo các nhóm biến sau:
    * **Nhóm biến Category:** Bao gồm trạng thái người phụ thuộc (*Dependents*), phương thức thanh toán (*Payment Method*), loại hình dịch vụ Internet (*Internet Service*) và các nhóm thời gian gắn bó (*Tenure Group*).
    * **Nhóm biến Số & Nhị phân (Remainder):** Các thông tin cơ bản gồm tình trạng *Senior Citizen*, *Partner*, *Tenure*, *Contract Type*, *Paperless Billing*, *Monthly Charges*, *Total Charges* và các tùy chọn bổ trợ (*Online Security*, *Online Backup*, *Device Protection*, *Tech Support*).
    * **Nhóm biến Kỹ nghệ Đặc trưng (Feature Engineering):** Các chỉ số phái sinh bao gồm *Service Diversity Score*, *Monthly Charges Ratio* và *Paperless & Auto-Payment Combo*.
* **Quy trình Tiền xử lý (Data Preparation):**
    * Làm sạch các giá trị bị thiếu (*missing values*) và xử lý dữ liệu ngoại lai (*outliers*).
    * Mã hóa các biến phân loại (*Categorical encoding*) và chuẩn hóa các biến số (*Feature scaling*) nếu cần thiết.
* **Kỹ nghệ Đặc trưng (Feature Engineering):** Cần tổng hợp và tạo thêm các biến mới có giá trị phân tích cao như:
    * `tenure_group`: Phân nhóm thời gian sử dụng (Ví dụ: 0-12 tháng, 12-24 tháng...)
    * `service_diversity`: Số lượng dịch vụ phụ trợ mà khách hàng có đăng ký (để đo độ trung thành).
    * `monthly_charges_ratio`: Tỷ lệ chi phí tháng so với mức trung bình để tìm ra khách hàng đang trả quá cao.
    * `is_paperless_electronic`: Tổ hợp phương thức nhận hóa đơn điện tử và thanh toán tự động.

---

## 5. Kế hoạch Phân tích & Đánh giá Mô hình
* **Xử lý và Trực quan hóa (Python/SQL):** Sử dụng `pandas` để tổng hợp dữ liệu (Churn Rate theo thiết bị, nguồn); dùng `seaborn`/`matplotlib` để vẽ Bar chart, Boxplot, Heatmap và Cohort chart.
* **Tiến trình Huấn luyện Mô hình:**
    * **Baseline Model:** Sử dụng Logistic Regression. Phân tích chi tiết các hệ số hồi quy (*coefficients*).
    * **Advanced Models:** Triển khai Random Forest và XGBoost.
* **Metrics Đánh giá:** Accuracy, Precision, Recall, F1-score, ROC-AUC.
    > **Lưu ý nghiệp vụ:** Ưu tiên tối ưu hóa **Recall** để phát hiện tối đa lượng khách hàng sắp rời đi.

---

## 6. Dashboard & Đề xuất Chiến lược
* **Nền tảng:** Power BI hoặc Tableau.
* **Thành phần hiển thị:** Tổng quan Churn Rate, Top risk segments, Feature importance, Conversion funnel.
* **Khuyến nghị Hành động (Actionable Insights):** Tự động thiết lập quy trình gửi Email Remarketing, cung cấp ưu đãi nhắm mục tiêu, và cá nhân hóa hệ thống đề xuất sản phẩm dựa trên hành vi truy cập gần nhất.