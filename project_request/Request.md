# PROJECT REQUIREMENTS: Predictive Customer Churn in E-commerce Subscription Services

## 1. Mục tiêu Tổng quan (Project Requirements)
Phân tích các yếu tố khiến khách hàng ngừng sử dụng dịch vụ, từ đó xây dựng mô hình học máy dự đoán khả năng rời bỏ (churn) nhằm đề xuất các chiến lược giữ chân khách hàng hiệu quả.

---

## 2. Hiểu biết Kinh doanh & Hướng Tiếp cận (Business Understanding and Analytic Approach)
* **Vấn đề kinh doanh:** Doanh nghiệp thất thoát doanh thu do khách hàng hủy dịch vụ hoặc rời bỏ sớm. Chi phí tìm kiếm khách hàng mới (CAC) luôn đắt đỏ hơn chi phí chăm sóc khách hàng cũ, do đó giảm thiểu tỷ lệ "Churn" là bài toán tối ưu lợi nhuận trực tiếp nhất.
* **Mục tiêu phân tích:** Xác định chính xác nhóm khách hàng có nguy cơ churn cao và các nguyên nhân cốt lõi dẫn đến quyết định rời đi.
* **Hướng phân tích:**
  * Mô tả và phác họa hành vi khách hàng.
  * Đối chiếu, so sánh đặc điểm giữa hai nhóm: **Churn** (rời bỏ) và **Non-churn** (ở lại).
  * Xây dựng mô hình phân loại (*Classification model*) để dự đoán xác suất rời đi của từng cá nhân dựa trên dữ liệu lịch sử.
* **Định hướng báo cáo:** Tập trung làm nổi bật hiệu suất dự báo của các mô hình và phân tích sâu các yếu tố có trọng số ảnh hưởng mạnh nhất đến quyết định churn. Đưa ra các gói giải pháp (*actionable insights*) giúp doanh nghiệp can thiệp kịp thời.

---

## 3. Câu hỏi Nghiên cứu Trọng tâm (Research Questions)
1. Yếu tố nào tác động mạnh mẽ nhất đến xác suất rời bỏ dịch vụ của khách hàng? *(Phân tích Feature Importance)*
2. Giữa các thuật toán **Logistic Regression** (Baseline), **Random Forest**, và **XGBoost**, mô hình nào đem lại hiệu suất dự đoán chính xác nhất?
3. Khi áp dụng mô hình vào thực tế, doanh nghiệp nên ưu tiên phân bổ nguồn lực giữ chân nhóm khách hàng nào trước tiên để tối ưu chi phí?

---

## 4. Thu thập, Hiểu & Chuẩn bị Dữ liệu (Data Collection, Understanding, Preparation)
* **Nguồn dữ liệu (Dataset):** UCI Machine Learning Repository - *Online Shoppers Purchasing Intention*
* **Đặc trưng dữ liệu ban đầu:** Hành vi duyệt web, thời lượng phiên truy cập, số trang đã xem, phân loại khách hàng, và thời điểm truy cập.
* **Quy trình Tiền xử lý (Data Preparation):**
  * Làm sạch các giá trị bị thiếu (*missing values*) và xử lý dữ liệu ngoại lai (*outliers*).
  * Mã hóa các biến phân loại (*Categorical encoding*) và chuẩn hóa các biến số (*Feature scaling/normalization*) nếu cần thiết.
* **Kỹ nghệ Đặc trưng (Feature Engineering):** Cần tổng hợp và tạo thêm các biến mới có giá trị phân tích cao như:
  * `session_intensity`: Cường độ tương tác trong phiên
  * `visit_frequency`: Tần suất truy cập
  * `weekend_behavior`: Hành vi ngày cuối tuần
  * Các biến liên quan đến tỷ lệ chuyển đổi (*conversion-related features*).

---

## 5. Kế hoạch Phân tích & Triển khai Kỹ thuật

### 5.1. Phân tích Dữ liệu với SQL & Python
* **SQL:** Thiết lập bảng thông tin khách hàng, tính toán Churn Rate theo thiết bị, nguồn, tháng. Đối chiếu sự khác biệt hành vi.
* **Python:** Sử dụng `pandas` để xử lý dữ liệu, `seaborn` / `matplotlib` để trực quan hóa (Bar chart, Boxplot, Heatmap, Cohort chart).

### 5.2. Huấn luyện & Đánh giá Mô hình

| Giai đoạn | Chi tiết công việc |
| :--- | :--- |
| **Baseline Model** | Sử dụng Logistic Regression. Phân tích chi tiết các hệ số hồi quy (*coefficients*). |
| **Advanced Models** | Triển khai Random Forest và XGBoost. |
| **Metrics Đánh giá** | Accuracy, Precision, Recall, F1-score, ROC-AUC. **Ưu tiên tối ưu hóa Recall**. |

---

## 6. Xây dựng Dashboard & Đề xuất Chiến lược
* **Nền tảng:** Power BI hoặc Tableau.
* **Thành phần:** Tổng quan Churn Rate, Top risk segments, Feature importance, Conversion funnel.
* **Khuyến nghị Hành động:** Tự động gửi Email Remarketing, Cung cấp ưu đãi nhắm mục tiêu, Cá nhân hóa hệ thống đề xuất.