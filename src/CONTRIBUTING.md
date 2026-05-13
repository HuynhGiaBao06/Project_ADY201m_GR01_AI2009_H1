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