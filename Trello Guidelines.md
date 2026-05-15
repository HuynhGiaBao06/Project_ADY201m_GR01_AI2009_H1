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