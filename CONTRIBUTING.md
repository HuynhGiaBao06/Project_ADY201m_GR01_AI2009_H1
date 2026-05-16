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

### Cú pháp (bắt buộc, thống nhất cả nhóm):

```text
feat<number>-<ten-task-cua-ban>
```

| Thành phần | Quy tắc | Ví dụ |
|------------|---------|--------|
| `feat` | Tiền tố cố định, viết thường | `feat` |
| `<number>` | Số thứ tự task **2 chữ số** (`01`–`99`), thống nhất trên Trello trước khi tạo nhánh | `01`, `12` |
| `<ten-task-cua-ban>` | Tiếng Anh, **không dấu**, chữ thường, từ nối bằng `-` | `sql-churn-rate-by-segment` |

**Ví dụ nhánh hợp lệ:**
- `feat01-setup-sql-server-schema`
- `feat02-handle-missing-values`
- `feat03-sql-churn-rate-by-segment`
- `feat04-update-contributing`

**Không dùng:** `feat/...`, `fix/...`, `main`, tên chung chung (`feat01-update`, `feat02-fix`).

**Phân số task:** Ghi số trên thẻ Trello (mô tả hoặc tiêu đề, ví dụ `[feat03] SQL churn rate`). Mỗi task mới = một số mới; **không tái sử dụng** số đã merge xong.

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

## 🚀 5. Hướng Dẫn Lệnh Git Chi Tiết (Pull Request lên GitHub)

Phần này dành cho thành viên mới. Mở terminal tại thư mục dự án (PowerShell hoặc Git Bash trên Windows).

> **Ghi nhớ:** `origin` = repository trên GitHub. `main` = nhánh chính của team (không code trực tiếp trên nhánh này).

---

### 5.1. Kiểm tra trạng thái — `git status`

Dùng **trước và sau** mỗi lần `add` / `commit` / `pull` / `push`.

```bash
git status
```

| Thông báo | Ý nghĩa |
|-----------|---------|
| `On branch main` | Bạn đang ở nhánh `main` — nên chuyển sang nhánh feature trước khi sửa code. |
| `On branch feat01-...` | Đang ở nhánh làm việc của bạn — đúng quy trình. |
| `Changes not staged` | File đã sửa nhưng chưa `git add`. |
| `Changes to be committed` | Đã `git add`, sẵn sàng `git commit`. |
| `nothing to commit, working tree clean` | Không còn thay đổi chưa lưu — có thể `push` hoặc đổi nhánh. |
| `Your branch is ahead of 'origin/...'` | Có commit local chưa đẩy lên GitHub — cần `git push`. |
| `Your branch is behind 'origin/main'` | GitHub có code mới hơn — cần `git pull origin main`. |

---

### 5.2. Lấy code mới nhất từ GitHub — `git pull origin main`

**Khi nào dùng:** Buổi sáng trước khi làm việc; trước khi tạo nhánh mới; trước khi mở Pull Request.

**Bước 1 — Về nhánh `main` và cập nhật:**

```bash
git checkout main
git pull origin main
```

**Bước 2 — Đưa `main` mới vào nhánh feature (nếu đang làm dở trên nhánh riêng):**

```bash
git checkout feat01-ten-task-cua-ban
git pull origin main
```

Nếu Git báo **conflict**, mở file bị conflict, sửa phần đánh dấu `<<<<<<<` / `=======` / `>>>>>>>`, rồi:

```bash
git add .
git commit -m "fix: resolve merge conflict with main"
```

---

### 5.3. Tạo nhánh mới — `git checkout -b`

Luôn tạo nhánh **sau khi** `git pull origin main` trên `main`.

```bash
git checkout main
git pull origin main
git checkout -b feat01-ten-task-cua-ban
```

Ví dụ đúng quy tắc đặt tên (mục 2):

```bash
git checkout -b feat01-setup-sql-server-schema
git checkout -b feat02-handle-missing-values
git checkout -b feat03-sql-churn-rate-by-segment
git checkout -b feat04-update-contributing
```

Kiểm tra đang ở nhánh nào:

```bash
git branch
```

Dấu `*` là nhánh hiện tại.

---

### 5.4. Lưu thay đổi — `git add` và `git commit`

Sau khi sửa code / notebook / file `.sql`:

```bash
git status
git add ten-file.py
git add sql/churn_rate_by_segment.sql
```

Hoặc thêm tất cả file đã sửa (cẩn thận, không add file nhạy cảm như `.env`):

```bash
git add .
git status
git commit -m "feat: add SQL churn rate by device and month"
```

Quy tắc message: xem **Mục 4** (Conventional Commits).

---

### 5.5. Đẩy code lên GitHub — `git push origin`

**Lần đầu** đẩy nhánh mới (GitHub chưa có nhánh này):

```bash
git push -u origin feat01-ten-task-cua-ban
```

**Các lần sau** trên cùng nhánh:

```bash
git push origin feat01-ten-task-cua-ban
```

Hoặc ngắn gọn (nếu đã dùng `-u` lần đầu):

```bash
git push
```

Terminal sẽ in link tạo Pull Request — copy mở trên trình duyệt hoặc vào GitHub → tab **Pull requests** → **New pull request**.

---

### 5.6. Quy trình đầy đủ (tóm tắt một task)

```text
1. git checkout main
2. git pull origin main
3. git checkout -b feat01-ten-task
4. (code, test notebook...)
5. git status
6. git add .
7. git commit -m "feat: mo ta ngan gon"
8. git push -u origin feat01-ten-task
9. Trên GitHub: New Pull Request → base: main ← compare: feat01-ten-task
10. Điền template PR, gán Reviewer, chờ Approve
```

---

## 🔀 6. Quy Trình Pull Request Trên GitHub

### 6.1. Tạo Pull Request (PR)

1. Vào repository trên GitHub → **Pull requests** → **New pull request**.
2. **base:** `main` ← **compare:** nhánh của bạn (ví dụ `feat03-sql-churn-rate-by-segment`).
3. Điền mô tả theo mẫu `.github/PULL_REQUEST_TEMPLATE.md`.
4. Gán ít nhất **1 Reviewer** (thường là Team Leader).
5. Bấm **Create pull request**.

### 6.2. Sau khi được review (yêu cầu sửa thêm)

```bash
git checkout feat03-ten-task-cua-ban
# sửa code theo góp ý
git add .
git commit -m "fix: address review comments on churn query"
git push origin feat03-ten-task-cua-ban
```

PR trên GitHub tự cập nhật — **không** cần tạo PR mới.

### 6.3. Trước khi merge — đồng bộ `main` lần cuối

```bash
git checkout feat03-ten-task-cua-ban
git pull origin main
# xử lý conflict nếu có
git push origin feat03-ten-task-cua-ban
```

### 6.4. Sau khi PR được merge

```bash
git checkout main
git pull origin main
git branch -d feat03-ten-task-cua-ban
```

Trên GitHub: xóa nhánh remote (nút **Delete branch** sau khi merge).

### 6.5. Quy tắc bắt buộc

- **Không** push trực tiếp lên `main`.
- **Không** tự merge PR của chính mình.
- PR chỉ merge khi có **≥ 1 Approve**.
- Luôn `git pull origin main` trước khi bắt đầu task mới hoặc trước khi nhờ review.

---

## ❓ 7. Một Số Lỗi Thường Gặp

| Lỗi | Cách xử lý |
|-----|------------|
| `failed to push` / `rejected` | Ai đó đã push lên nhánh đó — chạy `git pull origin main` (hoặc `git pull --rebase origin main`) rồi `git push` lại. |
| Commit nhầm nhánh | `git checkout dung-nhanh` → `git cherry-pick <mã-commit>` hoặc copy file và commit lại. Nhờ Leader nếu chưa quen. |
| Quên `git add` | `git status` sẽ không liệt kê file trong "to be committed" — chạy lại `git add`. |
| Đang ở `main` mà đã sửa file | `git stash` → `git checkout -b feat01-ten-task` → `git stash pop` → `add` + `commit`. |