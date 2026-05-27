# Sơ đồ Khung kiến trúc Dữ liệu & Huấn luyện Mô hình (Pipeline)

```text
[ Dữ liệu thô (Raw Data) ]
                                   │
                                   ▼
=======================================================================
GIAI ĐOẠN 1: LUỒNG CHUNG (Global Pipeline - Áp dụng cho TẤT CẢ mô hình)
=======================================================================
 │
 ├──> Xóa các dòng lỗi logic nặng (VD: Tuổi = -5)
 ├──> Điền dữ liệu bị thiếu (Missing values imputation)
 ├──> Chuyển đổi kiểu dữ liệu (Date/Time, String sang Category)
 └──> Tạo đặc trưng mới (Feature Engineering)
                                   │
                                   ▼
          [ Dữ liệu sạch (Clean Data) nhưng VẪN CHỨA OUTLIER ]
                                   │
                                   ▼
=======================================================================
  GIAI ĐOẠN 2: PHÂN NHÁNH CỤC BỘ (Local Pipelines - sklearn.Pipeline)
=======================================================================
                                   │
                 ┌─────────────────┴─────────────────┐
                 ▼                                   ▼
    [Nhánh 1: Logistic Regression]     [Nhánh 2: XGBoost / Random Forest]
                 │                                   │
                 ▼                                   ▼
       Bước 1: Lọc Outlier                 Bước 1: Bỏ qua lọc Outlier
       (Bằng Custom Transformer)           (Giữ nguyên dữ liệu)
                 │                                   │
                 ▼                                   ▼
       Bước 2: Chuẩn hóa dữ liệu           Bước 2: Bỏ qua chuẩn hóa
       (StandardScaler/MinMaxScaler)
                 │                                   │
                 ▼                                   ▼
       Bước 3: Huấn luyện mô hình          Bước 3: Huấn luyện mô hình
       (Logistic Regression)               (XGBoost / Random Forest)
```