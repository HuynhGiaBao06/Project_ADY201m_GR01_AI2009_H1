# 🛒 Predictive Customer Churn in E-commerce Subscription Services

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Machine Learning](https://img.shields.io/badge/ML-Classification-success)
![SQL](https://img.shields.io/badge/SQL-Analysis-orange)
![PowerBI](https://img.shields.io/badge/Dashboard-PowerBI/Tableau-brightgreen)

## 📌 1. Tổng quan dự án (Project Overview)
Dự án tập trung vào việc phân tích và dự đoán hành vi rời bỏ (churn) của khách hàng trong lĩnh vực dịch vụ đăng ký thương mại điện tử. Thông qua việc sử dụng các mô hình học máy (Machine Learning), nhóm hướng tới việc xác định các yếu tố rủi ro và đề xuất các chiến lược giữ chân khách hàng (retention strategies) tối ưu về chi phí cho doanh nghiệp.

### Vấn đề kinh doanh (Business Problem)
Doanh nghiệp đang đối mặt với sự thất thoát doanh thu đáng kể do khách hàng hủy dịch vụ hoặc rời bỏ sớm. Việc xác định ai sẽ rời đi và tại sao họ rời đi là chìa khóa để tồn tại trong thị trường cạnh tranh.

---

## 🚀 Hướng dẫn "Nhập môn" cho thành viên (Onboarding Guide)

Nếu bạn là thành viên mới tham gia dự án, đừng lo lắng về số lượng file tài liệu! Hãy làm theo đúng thứ tự checklist dưới đây để bắt nhịp nhanh nhất:

- [ ] **Bước 1: Hiểu bức tranh tổng thể.** Đọc lướt qua các phần còn lại của file `README.md` (chính là file này) để nắm được bài toán kinh doanh và các thư viện chúng ta sẽ dùng.
- [ ] **Bước 2: Nắm quy trình quản lý task.** Đọc file `Trello Guidelines.md` để biết cách nhận việc, báo cáo tiến độ và kéo-thả thẻ công việc đúng cột.
- [ ] **Bước 3: Thiết lập môi trường code.** Mở file `CONTRIBUTING.md` và làm đúng theo **Mục 1 (Cài đặt môi trường)** để clone code về máy và cài thư viện từ `requirements.txt` mà không bị lỗi.
- [ ] **Bước 4: Học luật làm việc nhóm trên Git.** Đọc các phần còn lại của `CONTRIBUTING.md` để biết cách tạo nhánh (branch) mới, cách viết commit và cách tạo Pull Request (PR).
- [ ] **Bước 5: Thực chiến!** Mở Trello, nhận task đầu tiên của bạn ở cột "To Do", kéo sang cột "In Progress" và bắt đầu code thôi!

## ❓ 2. Câu hỏi nghiên cứu (Research Questions)
1. Yếu tố nào tác động mạnh mẽ nhất đến xác suất rời bỏ dịch vụ của khách hàng?
2. Giữa các thuật toán **Logistic Regression**, **Random Forest** và **XGBoost**, mô hình nào đem lại hiệu suất dự đoán chính xác nhất?
3. Doanh nghiệp nên ưu tiên phân bổ nguồn lực giữ chân nhóm khách hàng nào để tối ưu hóa chi phí và hiệu quả?

---

## 🛠 3. Công nghệ & Thư viện sử dụng (Tech Stack)
- **Ngôn ngữ:** Python, SQL.
- **Xử lý dữ liệu:** Pandas, NumPy.
- **Trực quan hóa:** Matplotlib, Seaborn, Power BI/Tableau.
- **Học máy:** Scikit-learn, XGBoost.
- **Môi trường:** Jupyter Notebook, GitHub Dev.

---

## 📊 4. Dữ liệu & Tiền xử lý (Data & Preparation)
- **Nguồn:** [Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/static/public/468/data.csv).
- **Đặc trưng chính:** Hành vi duyệt web, thời lượng phiên truy cập, số trang đã xem, phân loại khách hàng, thời điểm truy cập.
- **Kỹ nghệ đặc trưng (Feature Engineering):**
  - `session_intensity`: Cường độ tương tác trong phiên.
  - `visit_frequency`: Tần suất truy cập.
  - `weekend_behavior`: Hành vi ngày cuối tuần.
  - Các biến liên quan đến tỷ lệ chuyển đổi.

---

## 📂 5. Cấu trúc dự án (Directory Structure)
```text
├── .github/                # Cấu hình GitHub (chứa Template Pull Request)
├── data/                   # Chứa dữ liệu thô (raw) và đã xử lý (processed)
├── notebooks/              # Chứa các file Jupyter Notebook (.ipynb) phân tích EDA & Model
├── project_request/        # Tài liệu yêu cầu chi tiết của dự án (Request.md)
├── src/                    # Thư mục chứa mã nguồn Python (.py), các script xử lý sau này
├── .gitignore              # Cấu hình chặn push file data nặng và môi trường ảo
├── CONTRIBUTING.md         # Hướng dẫn cài đặt môi trường và quy tắc Git cho nhóm
├── README.md               # Tài liệu tổng quan của dự án (file bạn đang đọc)
├── requirements.txt        # Danh sách thư viện và phiên bản chuẩn cần cài đặt
└── Trello Guidelines.md    # Quy tắc quản lý tiến độ và phân chia công việc trên Trello

---

## 🧪 6. Kế hoạch phân tích & Triển khai (Analysis Plan)

### 6.1. Phân tích với SQL
- **Mô hình hóa:** Thiết lập bảng thông tin khách hàng và chi tiết phiên truy cập.
- **Truy vấn:** Tính toán Churn Rate theo thiết bị, nguồn truy cập, tháng và loại khách hàng.
- **Đối chiếu:** So sánh sự khác biệt hành vi giữa nhóm Churn và Non-churn.

### 6.2. Mô hình hóa với Python
- **Xây dựng Baseline:** Sử dụng Logistic Regression làm mô hình cơ sở.
- **Huấn luyện mô hình nâng cao:** Triển khai Random Forest và XGBoost.
- **Đánh giá:** Ưu tiên tối ưu hóa chỉ số Recall để đảm bảo phát hiện tối đa lượng khách hàng có rủi ro rời bỏ cao (giảm False Negatives).

---

## 📈 7. Trực quan hóa & Dashboard
Hệ thống Dashboard (Power BI/Tableau) cung cấp cái nhìn đa chiều:
- **Real-time Churn:** Tổng quan tỷ lệ rời bỏ theo thời gian thực.
- **Conversion Funnel:** Phân tích phễu chuyển đổi hành vi.
- **Heatmap:** Biểu diễn mối tương quan đa biến và đa cộng tuyến.
- **Cohort Chart:** Theo dõi tỷ lệ giữ chân khách hàng theo nhóm thế hệ.

---

## 💡 8. Khuyến nghị hành động (Actionable Insights)
Dựa trên kết quả mô hình, doanh nghiệp triển khai các chiến dịch:
- **Automation:** Tự động gửi Email Remarketing với thông điệp cá nhân hóa.
- **Promotion:** Cung cấp gói ưu đãi/khuyến mãi nhắm mục tiêu vào phân khúc rủi ro cao.
- **Personalization:** Cá nhân hóa hệ thống đề xuất sản phẩm dựa trên hành vi truy cập gần nhất.

---

## 👥 9. Đội ngũ thực hiện (Contributors)
- **Huỳnh Gia Bảo** - AI Student at FPT University HCMC (SE204913)
- **[Nguyễn An Duy]** - [Vai trò/MSSV]
- **[Nguyễn Hữu Kiệt]** - [Vai trò/MSSV]