### [THÔNG TIN DỰ ÁN ĐỂ CHIA TASK VÀ VIẾT LATEX IEEE] ###

---
1. NỘI DUNG FILE REQUEST.MD (Yêu cầu dự án)
---
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


---
2. QUY TẮC LÀM VIỆC (Trello & Git)
---
Nội dung Trello Guidelines.md:
# 📋 Hướng Dẫn Quản Lý Công Việc Với Trello (Trello Guidelines)

Để đảm bảo tiến độ dự án được theo dõi sát sao, phân chia công việc minh bạch và đồng bộ với quá trình code trên GitHub, team sẽ quản lý task trên Trello theo quy trình Kanban dưới đây.

---

## 🗂 1. Cấu Trúc Các Cột (Lists Structure)

Bảng Trello của dự án được chia thành các cột theo luồng công việc từ trái sang phải. Bất kỳ task nào cũng phải đi qua luồng này:

- **[1] 💡 Backlog (Ý tưởng / Task tồn đọng):** Chứa tất cả các ý tưởng, task phát sinh hoặc yêu cầu cần làm trong tương lai nhưng chưa đưa vào kế hoạch của tuần hiện tại.
- **[2] 🎯 To Do (Cần làm tuần này):** Các task đã được chốt phải hoàn thành trong tuần hoặc giai đoạn nước rút hiện tại.
- **[3] 🏃 In Progress (Đang thực hiện):** Task đang được code hoặc xử lý. 
  > ⚠️ **Lưu ý:** Để đảm bảo chất lượng, mỗi thành viên chỉ nên có tối đa **1-2 thẻ (cards)** ở cột này cùng một thời điểm.
- **[4] 🔍 Review / PR (Chờ duyệt):** Các task đã code xong, đã tạo Pull Request (PR) trên GitHub và đang chờ thành viên khác vào kiểm tra (review).
- **[5] ✅ Done (Đã hoàn thành):** PR đã được gộp (merge) thành công vào nhánh `main` và task đã hoàn toàn kết thúc.

---

## 🏷 2. Quy Định Tạo Thẻ Công Việc (Card Rules)

Một thẻ công việc (Card) hợp lệ phải đáp ứng các tiêu chuẩn sau:

1. **Tiêu đề (Title) rõ ràng:** - Không đặt tên chung chung (VD: *Làm data*, *Vẽ chart*). 
   - Đặt tên cụ thể có tiền tố (VD: `[Clean] Xử lý missing values cột Age` hoặc `[Viz] Vẽ biểu đồ phân bố giá nhà`).
2. **Mô tả (Description):** Phải nêu rõ mục tiêu của task. Nên có một Checklist (danh sách công việc con) nếu task phức tạp.
3. **Người phụ trách (Members):** Ai đảm nhận task nào bắt buộc phải tự gắn (assign) tên tài khoản của mình vào thẻ đó.
4. **Thời hạn (Due Date):** Bắt buộc phải thiết lập deadline để cả team chủ động theo dõi tiến độ.

---

## 🎨 3. Quy Tắc Gắn Nhãn (Labels)

Sử dụng nhãn màu trên Trello để team dễ dàng phân loại và lọc công việc:

- 🔵 **Data Cleaning:** Tiền xử lý dữ liệu, ép kiểu, xử lý NaN.
- 🟢 **EDA / Model:** Phân tích, vẽ biểu đồ, tính toán thống kê.
- 🔴 **Bug:** Sửa lỗi code chạy không lên, lỗi logic hoặc lỗi conflict.
- 🟡 **Docs:** Viết báo cáo, cập nhật file `README.md`, slide thuyết trình.
- 🟣 **Review Needed:** Nhãn ưu tiên cần đồng đội vào review PR gấp.

---

## 🔄 4. Quy Trình Cập Nhật Task Hàng Ngày (Daily Workflow)

Để Trello không bị "chết", yêu cầu mọi người cập nhật trạng thái làm việc theo quy trình:

1. **Bắt đầu task:** Kéo card từ `To Do` ➡️ `In Progress`.
2. **Gắn link GitHub:** Ngay khi tạo Pull Request trên GitHub, hãy copy link PR đó dán vào phần bình luận (Comment) của thẻ Trello.
3. **Chờ Review:** Kéo card từ `In Progress` ➡️ `Review / PR`. Báo trên group chat để team vào review.
4. **Đóng task:** Chỉ kéo card sang `Done` **SAU KHI** Pull Request trên GitHub đã được Merge thành công.

Nội dung CONTRIBUTING.md (Tùy chọn):

# 📖 Hướng Dẫn Đóng Góp (Contributing Guidelines)

Chào mừng bạn đến với dự án phân tích dữ liệu (EDA)! Để đảm bảo quy trình làm việc nhóm hiệu quả và tránh xung đột code, vui lòng tuân thủ các quy tắc dưới đây.

---

## 🛠 1. Cài đặt môi trường làm việc (Getting Started)

Mỗi thành viên cần thiết lập môi trường phát triển độc lập trên máy cá nhân:

1. **Clone repository:**
    `git clone <url_của_repository>`
    `cd <tên_thư_mục_dự_án>`

2. **Tạo môi trường ảo (Virtual Environment):**
    `python -m venv venv`
    - *Windows:* `venv\Scripts\activate`
    - *macOS/Linux:* `source venv/bin/activate`

3. **Cài đặt thư viện:**
    `pip install -r requirements.txt`

---

## 🌿 2. Quy Tắc Đặt Tên Branch (Branching Strategy)

**Tuyệt đối không push code trực tiếp lên nhánh `main`.** Mọi thay đổi phải thực hiện trên nhánh riêng.

### Cú pháp:
### `<loại_branch>/<tên-nhiệm-vụ-viet-thuong-khong-dau-dat-ten-theo-tieng-anh>` 

- **`feat/`**: Tính năng mới, phân tích mới (Ví dụ: `feat/eda-salary-correlation`)
- **`fix/`**: Sửa lỗi code hoặc logic (Ví dụ: `fix/missing-value-handler`)
- **`docs/`**: Chỉnh sửa tài liệu (Ví dụ: `docs/update-readme`)
- **`refactor/`**: Tối ưu hóa code nhưng không đổi kết quả.

---

## 📊 3. Quy Tắc Với Dữ Liệu & Notebook

1. **Không commit file dữ liệu lớn:** Các file `.csv`, `.xlsx` nặng phải được liệt kê trong `.gitignore`.
2. **Quy tắc Jupyter Notebook:**
   - Trước khi commit, chọn **Kernel -> Restart & Run All** để đảm bảo code chạy không lỗi.
   - **Xóa output quá dài:** Tránh in ra hàng nghìn dòng dữ liệu làm phình to file `.ipynb`.
   - Sử dụng Markdown cells để giải thích các bước và Insight rút ra.

---

## 📝 4. Quy Tắc Viết Commit Message

Sử dụng định dạng **Conventional Commits**: `<loại>: <mô tả ngắn gọn>`

- `feat: add distribution plots for age`
- `fix: handle NaN values in price column`
- `docs: update setup instructions`

*Lưu ý: Không dùng các commit chung chung như "update", "fix", "done".*

---

## 🚀 5. Quy Trình Tạo & Gộp Pull Request (PR)

1. **Cập nhật code mới nhất:** Trước khi tạo PR, hãy merge `main` vào branch của bạn để xử lý conflict.
    `git pull origin main`

2. **Tạo PR:**
   - Điền đầy đủ thông tin theo mẫu `PULL_REQUEST_TEMPLATE.md`.
   - Gán ít nhất **1 thành viên khác** vào mục **Reviewers**.

3. **Review & Merge:**
   - Không tự ý merge PR của chính mình.
   - PR chỉ được gộp khi có ít nhất **1 lượt Approve**.
   - Sau khi merge, hãy xóa branch cá nhân trên GitHub.


---
3. THÔNG TIN ĐỘI NHÓM (Team Members & Roles)
---
Tổng số thành viên: [Điền số lượng, ví dụ: 4 người]
Phân bổ vai trò (Ghi rõ thế mạnh/công việc dự kiến của từng người nếu có):
- Thành viên 1 ([Huỳnh Gia Bảo]): [Thế mạnh/Vai trò - Team Leader,Đã từng làm qua 1 số bài liên quan tới data analysis]
- Thành viên 2 ([Nguyễn An Duy]): [Thế mạnh/Vai trò - Member, Chưa biết gì về data analytis]
- Thành viên 3 ([Nguyễn Hữu Kiệt]): [Thế mạnh/Vai trò - Member, Chưa biết gì về data analytis]


---
4. THỜI GIAN & TIẾN ĐỘ (Timeline & Status)
---
- Trạng thái hiện tại: [Mới bắt đầu]
- Ngày bắt đầu (Sprint 1): [18/5]
- Deadline tổng (Final Deadline): [14/6]

---
5. YÊU CẦU ĐẦU RA (Output Preferences)
---
- Ngôn ngữ báo cáo IEEE: [Tiếng Anh]
- Cấu trúc LaTeX mong muốn: LaTeX Springer 1 cột
- Final Report: 10–12 trang, định dạng LaTeX Springer 1 cột (template chính thức để nộp paper). 

### [HẾT] ###