📞 Predictive Customer Churn in Telecommunication Services

📌 1. Tổng quan dự án (Project Overview)

Dự án tập trung vào việc phân tích và dự đoán hành vi rời bỏ (churn) của khách hàng trong lĩnh vực dịch vụ Viễn thông, sử dụng tập dữ liệu IBM Telco Customer Churn. Thông qua việc sử dụng các mô hình học máy (Machine Learning), nhóm hướng tới việc xác định các yếu tố rủi ro và đề xuất các chiến lược giữ chân khách hàng (retention strategies).

Vấn đề kinh doanh (Business Problem)

Doanh nghiệp đang đối mặt với sự thất thoát doanh thu đáng kể do khách hàng hủy dịch vụ hoặc rời bỏ sớm. Bài toán kinh doanh cốt lõi ở đây là giảm thiểu chi phí tìm kiếm khách hàng mới (CAC) thông qua việc dự báo chính xác và giữ chân khách hàng cũ.

🚀 2. Hướng dẫn "Nhập môn" cho thành viên (Onboarding Guide)

Nếu bạn là thành viên mới tham gia dự án, hãy làm theo đúng thứ tự checklist dưới đây để bắt nhịp nhanh nhất:

* [ ] Bước 1: Hiểu bức tranh tổng thể. Đọc lướt qua các phần còn lại của file README.md để nắm được bài toán kinh doanh.
* [ ] Bước 2: Nắm quy trình quản lý task. Truy cập không gian làm việc chính thức trên Notion và tham gia kênh thảo luận trên Discord để xem tiến độ công việc. Tuyệt đối tuân thủ phân công theo lộ trình Sprint rõ ràng, không tự do kéo thả task.
* [ ] Bước 3: Thiết lập môi trường code. Mở file CONTRIBUTING.md và làm đúng theo Mục 1 để clone code về máy và cài thư viện từ requirements.txt.
* [ ] Bước 4: Học luật làm việc nhóm trên Git. Đọc các phần còn lại của CONTRIBUTING.md để biết cách tạo nhánh (branch), viết commit và tạo Pull Request (PR).

🏗️ 3. Kiến trúc Dữ liệu & Pipeline (Single Source of Truth)

Đây là quy định kỹ thuật cao nhất của dự án. Mọi xử lý dữ liệu phải tuân thủ nghiêm ngặt mô hình phân nhánh sau (Tham khảo sơ đồ chi tiết tại `Pipeline.md`):

* Luồng Global (Giai đoạn 1): Tiến hành làm sạch cơ bản, xử lý missing value, mã hóa phân loại (encoding) và xử lý lỗi logic. Đặc biệt lưu ý: Không đụng chạm hay xóa bỏ Outlier.
* Luồng Local (Giai đoạn 2): Độc lập sử dụng `sklearn.pipeline.Pipeline` theo từng nhánh mô hình.
  * Nhánh 1 (Logistic Regression): Thiết kế Local Pipeline gồm các bước Capping/Quantile Outliers và StandardScaler trước khi đưa vào mô hình.
  * Nhánh 2 (Random Forest / XGBoost): Truyền trực tiếp tập dữ liệu chứa outlier vào mô hình mà không thực hiện scaling hay lọc ngoại lệ.

❓ 4. Câu hỏi nghiên cứu (Research Questions)

1. Yếu tố nào tác động mạnh mẽ nhất đến xác suất rời bỏ dịch vụ của khách hàng?.
2. Giữa các thuật toán Logistic Regression, Random Forest và XGBoost, mô hình nào đem lại hiệu suất dự đoán chính xác nhất?.
3. Doanh nghiệp nên ưu tiên phân bổ nguồn lực giữ chân nhóm khách hàng nào để tối ưu hóa chi phí và hiệu quả?.

🛠 5. Công nghệ & Thư viện sử dụng (Tech Stack)

* Ngôn ngữ: Python, T-SQL.
* Quản lý Cơ sở dữ liệu: Microsoft SQL Server.
* Xử lý dữ liệu: Pandas, NumPy.
* Trực quan hóa: Matplotlib, Seaborn, Power BI/Tableau.
* Học máy: Scikit-learn, XGBoost.
* Quản lý dự án & Môi trường: Jupyter Notebook, GitHub, Notion, Discord.

📊 6. Dữ liệu & Tiền xử lý (Data & Preparation)

* Nguồn: Telco Customer Churn: IBM dataset.
* Đặc trưng chính: Thông tin nhân khẩu học, hợp đồng & thanh toán, và danh sách dịch vụ viễn thông.
* Kỹ nghệ đặc trưng (Feature Engineering):
  * tenure_group: Phân nhóm thời gian sử dụng dịch vụ.
  * service_diversity: Đo lường mức độ đa dạng dịch vụ phụ trợ.
  * monthly_charges_ratio: Tỷ lệ chi phí hàng tháng.
  * is_paperless_electronic: Hành vi thanh toán điện tử.