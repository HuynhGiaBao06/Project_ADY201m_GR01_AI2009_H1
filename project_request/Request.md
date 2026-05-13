# YÊU CẦU DỰ ÁN (PROJECT REQUIREMENTS)

## Project 1: Predictive Customer Churn in E-commerce Subscription Services
*(Dự đoán khách hàng rời bỏ trong dịch vụ đăng ký thương mại điện tử)*

---

### 1. Mục tiêu (Objectives)
Phân tích các yếu tố khiến khách hàng ngừng sử dụng dịch vụ, sau đó xây dựng mô hình dự đoán churn để đề xuất chiến lược giữ chân khách hàng hiệu quả.

### 2. Hiểu biết Kinh doanh & Hướng tiếp cận (Business Understanding and Analytic Approach)
* **Vấn đề kinh doanh:** Doanh nghiệp mất doanh thu vì khách hàng rời bỏ sớm.
* **Mục tiêu phân tích:** Xác định nhóm khách hàng có nguy cơ churn cao và lý do chính dẫn đến churn.
* **Hướng phân tích:** Mô tả hành vi khách hàng, so sánh nhóm churn và không churn, sau đó xây dựng mô hình phân loại (classification).
* **Kết quả kỳ vọng:** Tập trung vào hiệu quả dự báo và các yếu tố ảnh hưởng mạnh nhất đến churn để trình bày trong bài báo nghiên cứu.

### 3. Câu hỏi Nghiên cứu (Research Questions - RBL)
1. Yếu tố nào ảnh hưởng mạnh nhất đến xác suất khách hàng churn?
2. Mô hình nào dự đoán churn tốt nhất giữa **Logistic Regression**, **Random Forest** và **XGBoost**?
3. Nếu áp dụng mô hình dự đoán churn, doanh nghiệp có thể ưu tiên giữ chân nhóm nào trước để tối ưu hóa nguồn lực?

### 4. Thu thập, Hiểu & Chuẩn bị Dữ liệu (Data Collection, Understanding, Preparation)
* **Dataset:** [UCI Machine Learning Repository - Online Shoppers Purchasing Intention](https://archive.ics.uci.edu/static/public/468/data.csv)
* **Đặc trưng:** Hành vi duyệt web, thời lượng phiên, số trang đã xem, loại khách, thời điểm truy cập.
* **Tiền xử lý:**
    * Làm sạch dữ liệu thiếu, kiểm tra nhiễu (outlier).
    * Mã hóa biến phân loại và chuẩn hóa biến số.
* **Kỹ nghệ đặc trưng (Feature Engineering):** Tạo thêm các biến như: `session intensity`, `visit frequency`, `weekend behavior`, `conversion-related features`.

### 5. Phân tích Dữ liệu với SQL
* **Cấu trúc:** Tạo bảng khách hàng và bảng phiên truy cập.
* **Truy vấn:**
    * Tính toán **Churn Rate** theo thiết bị (device), nguồn (source), tháng, hoặc loại khách.
    * So sánh hành vi chi tiết giữa nhóm churn và không churn.
    * Truy vấn các yếu tố có tương quan cao nhất với churn để phục vụ phần giải thích nghiên cứu.

### 6. Phân tích Dữ liệu với Python
* **Thư viện:** Dùng `pandas` để làm sạch/tạo biến; `seaborn`/`matplotlib` để kiểm tra phân phối và tương quan.
* **Huấn luyện:** Chia tập Train-Test, huấn luyện các mô hình: Logistic Regression, Random Forest, XGBoost.
* **Đánh giá:** Sử dụng các chỉ số Accuracy, Precision, Recall, F1-score, ROC-AUC.
* **Ưu tiên:** Tập trung vào chỉ số **Recall** để tránh bỏ sót khách hàng có nguy cơ rời bỏ.

### 7. Trực quan hóa Dữ liệu (Data Visualization)
* **Bar Chart:** So sánh churn rate theo các nhóm khách hàng.
* **Boxplot:** Xem xét sự khác biệt về `session duration` giữa nhóm churn và non-churn.
* **Heatmap:** Kiểm tra mối liên hệ và độ tương quan giữa các biến.
* **Cohort Chart:** Minh họa hành vi khách hàng và tỷ lệ giữ chân theo thời gian.

### 8. Phân tích Hồi quy (Regression Analysis)
* **Mô hình nền tảng:** Sử dụng **Logistic Regression** (vì biến đích churn là nhị phân).
* **Diễn giải:** Giải thích các hệ số (coefficients) để làm rõ yếu tố nào làm tăng/giảm xác suất churn.
* **So sánh:** Đối chiếu với các mô hình mạnh hơn (Random Forest, XGBoost) để chứng minh giá trị cải thiện độ chính xác.
* **Trình bày:** Làm rõ Baseline model, mô hình nâng cao và bảng so sánh các Metrics.

### 9. Phân tích với Công cụ & Dashboard (Data Analysis with Tool)
* **Triển khai:** Xây dựng Dashboard trên **Power BI** hoặc **Tableau**.
* **Nội dung:** Hiển thị Churn rate, top risk segments, feature importance, conversion funnel.
* **Tính năng:** Bộ lọc theo thời gian, nguồn truy cập, loại thiết bị để hỗ trợ ra quyết định nhanh.
* **Kết luận & Hành động:** Đề xuất các giải pháp thực tiễn như chương trình ưu đãi, Email Remarketing và cá nhân hóa trải nghiệm người dùng.