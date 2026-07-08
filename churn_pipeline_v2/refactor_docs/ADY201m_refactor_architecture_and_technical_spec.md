# ADY201m Churn Project — Refactor Architecture & Technical Specification

## 1. Mục tiêu refactor

Dự án hiện tại đang đi theo kiểu `script sequence` trong `src/`:

```text
01_data_ingestion.py
02_data_cleaning.py
03_data_extraction.py
04_feature_engineering.py
05_data_processing.py
06_tree_data_processing.py
```

Mục tiêu refactor là chuyển sang kiến trúc:

```text
OOP Pipeline Builder + sklearn-compatible preprocessing components
```

Trong đó:

- `main.py` là entry point điều phối.
- `pipeline_builder.py` tạo pipeline và chia pipeline branch.
- `src/pre_processing/` chứa các preprocessing class nhỏ, có `fit()` / `transform()`.
- Model training thuộc quyền của `notebooks/`.
- Không train model trong `src/`.
- Không xuất preprocessed CSV trung gian vào `data/processing/`.
- Test set bị khóa ngay từ đầu sau `data_ingestion`.

---

## 2. Kiến trúc thư mục sau refactor

```text
PROJECT ROOT
│
│   .env
│   .env.example
│   .gitignore
│   CONTRIBUTING.md
│   LICENSE
│   README.md
│   requirements.txt
│
├── data/
│   ├── raw_data/
│   │   └── data_raw.csv
│   │
│   ├── checkpoint_data/
│   │   ├── train_df.csv
│   │   ├── validation_df.csv
│   │   └── test_df.csv
│   │
│   ├── EDA_data/
│   │   └── EDA_data.csv
│   │
│   └── logger_data/
│       └── logger_data.txt
│
├── docs/
│   ├── database_guideline.md
│   ├── dataflow.md
│   └── pipeline.md
│
├── models/
│
├── notebooks/
│   ├── 01_EDA_and_Feature_Engineering.ipynb
│   ├── 02_Logistic_Regression.ipynb
│   ├── 03_tree_models_train.ipynb
│   ├── 04_xgboost_models_train.ipynb
│   └── 05_Model_Visualization.ipynb
│
├── reports/
│   ├── data_reports/
│   └── figures/
│
├── sql/
│   ├── schema.sql
│   ├── data_quality_checks.sql
│   ├── churn_rate_by_segment.sql
│   ├── compare.sql
│   ├── feature_summary.sql
│   └── high_risk_service_factors.sql
│
└── src/
    ├── data_ingestion.py
    ├── data_upload.py
    ├── db_config.py
    ├── main.py
    ├── path.py
    ├── pipeline_builder.py
    ├── __init__.py
    │
    ├── pre_processing/
    │   ├── feature_engineer.py
    │   ├── categorical_encoder.py
    │   ├── capping_outlier.py
    │   ├── scaler.py
    │   ├── target_encoder.py
    │   └── __init__.py
    │
    ├── src_guideline/
    │   ├── config_guideline.md
    │   └── path_guideline.md
    │
    └── utils/
        ├── logger.py
        └── __init__.py
```

---

## 3. Vai trò các folder

### 3.1 `data/`

Chứa dữ liệu theo tầng.

Quy tắc:

- Không lưu preprocessed CSV trung gian.
- Không dùng `data/processing/` nữa nếu pipeline đã xử lý trong memory.
- Chỉ lưu raw data, checkpoint split, EDA data và log.

```text
data/
├── raw_data/
├── checkpoint_data/
├── EDA_data/
└── logger_data/
```

### 3.2 `data/raw_data/`

Vai trò:

- Chứa dữ liệu gốc.
- Không chỉnh sửa trực tiếp.
- File chính: `data_raw.csv`.

### 3.3 `data/checkpoint_data/`

Vai trò:

- Chứa dữ liệu sau khi split 70/15/15.
- Được tạo bởi `src/data_ingestion.py`.

Các file chính:

```text
train_df.csv
validation_df.csv
test_df.csv
```

Quy tắc:

- `train_df.csv`: được dùng để `fit()`.
- `validation_df.csv`: chỉ được `transform()`.
- `test_df.csv`: bị khóa từ đầu, chỉ dùng cho final evaluation.

### 3.4 `data/EDA_data/`

Vai trò:

- Chứa dữ liệu phục vụ EDA nếu cần.
- Không được dùng để học preprocessing nếu vi phạm train/validation/test rule.

### 3.5 `data/logger_data/`

Vai trò:

- Chứa log quá trình chạy pipeline.
- File chính: `logger_data.txt`.

### 3.6 `docs/`

Vai trò:

- Chứa tài liệu kỹ thuật của project.

File chính:

```text
database_guideline.md
dataflow.md
pipeline.md
```

### 3.7 `models/`

Vai trò:

- Chứa model đã train.
- Model được tạo từ `notebooks/`, không phải từ `src/`.

Ví dụ:

```text
logistic_model.pkl
random_forest_model.pkl
xgboost_model.pkl
```

### 3.8 `notebooks/`

Vai trò:

- Train model.
- Evaluate model.
- Tuning threshold.
- Visualization.
- Feature importance.
- Logistic coefficients.
- Export reports/models.

Quy tắc:

- Notebook được train model.
- Notebook không tự fit lại preprocessing sai quy tắc.
- Notebook dùng pipeline output từ `pipeline_builder.py`.
- Validation dùng cho model selection / threshold tuning.
- Test chỉ dùng cho final evaluation.

### 3.9 `reports/`

Vai trò:

- Chứa kết quả phục vụ report học thuật và dashboard.

```text
reports/
├── data_reports/
└── figures/
```

### 3.10 `sql/`

Vai trò:

- Chứa SQL scripts.
- Phục vụ schema, data quality check, churn analysis, dashboard và business insights.

---

## 4. Vai trò các file trong `src/`

### 4.1 `src/data_ingestion.py`

Vai trò:

- Load raw data.
- Split dữ liệu ngay từ đầu theo tỷ lệ 70/15/15.
- Save checkpoint split vào `data/checkpoint_data/`.
- Khóa test set ngay sau split.

Input:

```text
data/raw_data/data_raw.csv
```

Output:

```text
data/checkpoint_data/train_df.csv
data/checkpoint_data/validation_df.csv
data/checkpoint_data/test_df.csv
```

Quy tắc:

- Không feature engineering.
- Không encoding.
- Không scaling.
- Không capping.
- Không train model.
- Có thể kiểm tra input cơ bản.
- Có thể stratify theo target `Churn` nếu phù hợp.

---

### 4.2 `src/data_upload.py`

Vai trò:

- Upload hoặc đồng bộ dữ liệu với SQL Server nếu cần.
- Hỗ trợ SQL/dashboard.
- Không chứa logic preprocessing/modeling.

---

### 4.3 `src/db_config.py`

Vai trò:

- Quản lý cấu hình kết nối database.
- Đọc `.env` nếu cần.
- Không xử lý dữ liệu.
- Không train model.

---

### 4.4 `src/path.py`

Vai trò:

- Single source of truth cho toàn bộ đường dẫn project.
- Mọi file khác lấy path từ đây.
- Không hard-code path rải rác trong các module.

Các nhóm path cần quản lý:

```text
PROJECT_ROOT
DATA_DIR
RAW_DATA_DIR
CHECKPOINT_DATA_DIR
EDA_DATA_DIR
LOGGER_DATA_DIR
DOCS_DIR
MODELS_DIR
NOTEBOOKS_DIR
REPORTS_DIR
DATA_REPORTS_DIR
FIGURES_DIR
SQL_DIR
SRC_DIR
```

---

### 4.5 `src/main.py`

Vai trò:

- Entry point chính.
- Điều phối flow tổng thể.
- Gọi `data_ingestion.py`.
- Gọi `pipeline_builder.py`.
- Gọi logger.

Không được chứa:

- Feature engineering logic.
- Encoding logic.
- Capping logic.
- Scaling logic.
- Model training logic.

Luồng chuẩn:

```text
main.py
  ↓
data_ingestion.py
  ↓
pipeline_builder.py
  ↓
notebooks/
```

---

### 4.6 `src/pipeline_builder.py`

Vai trò:

- Tạo pipeline.
- Chia pipeline branch.
- Quản lý `fit()` / `transform()`.
- Fit pipeline chỉ trên train.
- Transform validation/test.
- Không train model.

Pipeline branch cần tạo:

```text
global preprocessing pipeline
logistic preprocessing branch
tree preprocessing branch
```

Không cần tạo:

```text
logistic_processor.py
tree_processor.py
```

Vì branch được compose trực tiếp trong `pipeline_builder.py`.

---

## 5. Vai trò các file trong `src/pre_processing/`

### 5.1 `feature_engineer.py`

Vai trò:

- Tạo feature mới cho churn.

Feature chính:

```text
tenure_group
service_diversity
monthly_charges_ratio
is_paperless_electronic
```

Quy tắc:

- Nếu cần học thống kê, chỉ học trong `fit()` trên train.
- Ví dụ: `monthly_charges_ratio` dùng mean của `MonthlyCharges` học từ train.
- Validation/test chỉ dùng `transform()` với tham số đã học.

---

### 5.2 `categorical_encoder.py`

Vai trò:

- Mã hóa biến phân loại.

Có thể phục vụ nhiều branch:

```text
Logistic branch → one-hot style
Tree branch     → ordinal/label style
```

Quy tắc:

- Fit encoder chỉ trên train.
- Validation/test chỉ transform.
- Branch nào dùng encoding nào do `pipeline_builder.py` quyết định.

---

### 5.3 `capping_outlier.py`

Vai trò:

- Xử lý outlier bằng capping.

Quy tắc:

- Fit ngưỡng capping chỉ trên train.
- Validation/test chỉ transform.
- Chủ yếu dùng cho Logistic branch.
- Không áp dụng cho tree branch nếu giữ định hướng Random Forest/XGBoost preserve outliers.

---

### 5.4 `scaler.py`

Vai trò:

- Scale numerical features.

Quy tắc:

- Fit scaler chỉ trên train.
- Validation/test chỉ transform.
- Chủ yếu dùng cho Logistic branch.
- Không dùng cho Random Forest/XGBoost nếu không cần.

---

### 5.5 `target_encoder.py`

Vai trò:

- Xử lý target `Churn`.
- Ví dụ: `Yes/No` → `1/0`.
- Giữ target logic tập trung một chỗ.

---

## 6. Quy tắc OOP cho preprocessing

Tất cả preprocessing class trong `src/pre_processing/` phải tuân thủ:

```text
BaseEstimator + TransformerMixin
```

Quy tắc kỹ thuật:

1. Mỗi preprocessing class kế thừa `BaseEstimator` và `TransformerMixin`.
2. Mỗi class có `fit()` và `transform()`.
3. `fit_transform()` được kế thừa từ `TransformerMixin`.
4. `fit()` chỉ được học từ train.
5. Validation và test chỉ được `transform()`.
6. `transform()` không được học lại bất kỳ thống kê nào.
7. Mọi tham số học được phải lưu trong object.
8. Không đọc file trong preprocessing class.
9. Không ghi file trong preprocessing class.
10. Không train model trong preprocessing class.
11. Không hard-code path trong preprocessing class.
12. Không làm branch orchestration trong preprocessing class.
13. Không để logic model training trong `pipeline_builder.py`.

Ví dụ các trạng thái được học trong `fit()`:

```text
monthly_charges_mean_
capping_bounds_
encoder_categories_
scaler_mean_
scaler_std_
feature_names_
```

---

## 7. Quy tắc train / validation / test

### 7.1 Split rule

Split được thực hiện ngay trong `data_ingestion.py`.

```text
Train      = 70%
Validation = 15%
Test       = 15%
```

### 7.2 Lock test rule

Sau khi `data_ingestion.py` chạy xong:

```text
test_df.csv bị khóa
```

Test set:

- Không dùng để fit preprocessing.
- Không dùng để chọn feature.
- Không dùng để chọn model.
- Không dùng để chỉnh threshold.
- Chỉ dùng cho final evaluation.

### 7.3 Fit/Transform rule

| Dataset | Được fit? | Được transform? | Vai trò |
|---|---:|---:|---|
| Train | Có | Có | học preprocessing + train model |
| Validation | Không | Có | tuning/model selection |
| Test | Không | Có | final evaluation |

---

## 8. Luồng pipeline chuẩn

```text
Raw Data
  ↓
data_ingestion.py
  ↓
Split 70 / 15 / 15
  ↓
Lock Test Set
  ↓
checkpoint_data/
  ├── train_df.csv
  ├── validation_df.csv
  └── test_df.csv
  ↓
main.py
  ↓
pipeline_builder.py
  ├── build global pipeline
  ├── build logistic branch
  └── build tree branch
  ↓
notebooks/
  ├── train Logistic Regression
  ├── train Random Forest
  ├── train XGBoost
  └── evaluate / visualize
  ↓
models/
reports/
figures/
```

---

## 9. Branch design

### 9.1 Global pipeline

Vai trò:

- Chứa các bước dùng chung nếu cần.
- Không được làm mất thông tin cần cho các branch.
- Không capping outlier nếu tree branch cần preserve outliers.

### 9.2 Logistic branch

Có thể gồm:

```text
target encoding
feature engineering
outlier capping
categorical encoding
scaling
```

Dùng cho:

```text
Logistic Regression notebook
```

### 9.3 Tree branch

Có thể gồm:

```text
target encoding
feature engineering
categorical encoding
```

Không gồm:

```text
outlier capping
scaling
```

Dùng cho:

```text
Random Forest notebook
XGBoost notebook
```

---

## 10. Những file không cần trong kiến trúc mới

Không cần:

```text
src/pre_processing/logistic_processor.py
src/pre_processing/tree_processor.py
```

Lý do:

- Branch composition nằm trong `pipeline_builder.py`.
- Preprocessing modules chỉ nên là component nhỏ.
- Không tạo thêm file processor trung gian nếu không cần.

---

## 11. Nguyên tắc notebook sau refactor

Notebook được quyền:

- Train model.
- Tune model.
- Evaluate model.
- Save model.
- Save metrics.
- Save figures.
- Save feature importance.
- Save coefficients.

Notebook không được:

- Fit lại scaler/encoder/capper trên validation/test.
- Tự tạo preprocessing pipeline khác làm lệch `src`.
- Dùng test set để chọn model hoặc threshold.
- Ghi đè checkpoint split nếu không có lý do.

---

## 12. Nguyên tắc migration

Refactor nên làm trong folder con mới trước.

Ví dụ:

```text
churn_pipeline_v2/
```

Sau khi chạy ổn:

1. So sánh output với project cũ.
2. Đảm bảo pipeline mới chạy được.
3. Đảm bảo notebooks train được model.
4. Đảm bảo metrics không lệch bất thường.
5. Backup project cũ.
6. Migrate cấu trúc mới thành chính.
7. Xóa script sequence cũ.
8. Cập nhật README/docs.
