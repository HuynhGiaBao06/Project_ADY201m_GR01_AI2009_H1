# ADY201m Churn Project — CodeX Refactor Work Plan & Safety Rules

## 1. Mục tiêu tài liệu

Tài liệu này dùng để giao việc cho CodeX khi refactor project ADY201m Churn từ kiến trúc script sequence sang OOP Pipeline Builder.

Mục tiêu chính:

```text
Không sửa trực tiếp project cũ ngay.
Tạo folder con mới để refactor.
Chạy được end-to-end trong folder mới.
Sau khi ổn mới xóa/migrate cấu trúc cũ.
```

---

## 2. Cấu hình CodeX bắt buộc

Khi làm việc với CodeX, dùng cấu hình an toàn sau:

```text
Mode: Ask for approval
Full access: Off
Approve for me: Off
Network: Off nếu không cần cài package hoặc tìm internet
```

Giải thích:

- `Ask for approval`: CodeX phải hỏi trước khi sửa.
- `Full access: Off`: hạn chế quyền tự thao tác rộng.
- `Approve for me: Off`: không cho CodeX tự đồng ý thay người dùng.
- `Network: Off`: tắt mạng nếu không cần cài package hoặc tra cứu.

---

## 3. Quy tắc bắt buộc khi giao việc cho CodeX

Luôn đưa các rule này vào prompt quan trọng:

```text
Bạn chỉ được phân tích trước, không sửa file nếu tôi chưa nói "OK sửa".

Nếu cần sửa, hãy liệt kê:
1. file cần sửa
2. lý do sửa
3. thay đổi dự kiến

Sau đó chờ xác nhận.

Không tự refactor ngoài phạm vi.

Không chạy:
- git add
- git commit
- git push
- git reset

Sau khi sửa, hiển thị:
1. diff
2. danh sách file đã thay đổi
3. ghi chú rủi ro nếu có
```

---

## 4. Nguyên tắc phạm vi làm việc

CodeX không được:

```text
- Sửa project cũ trực tiếp khi chưa được yêu cầu.
- Xóa file/folder cũ khi folder mới chưa chạy ổn.
- Đổi tên output tùy tiện.
- Thay đổi logic research ngoài phạm vi refactor.
- Train model trong pipeline_builder.py.
- Fit preprocessing trên validation/test.
- Dùng test set để tuning.
- Chạy git command nguy hiểm.
- Cài package nếu chưa hỏi.
- Tự bật network nếu chưa hỏi.
```

CodeX được phép:

```text
- Đọc file.
- Phân tích trách nhiệm từng file.
- Đề xuất mapping refactor.
- Tạo folder mới nếu đã được xác nhận.
- Viết code trong folder refactor mới nếu đã được xác nhận.
- Hiển thị diff sau khi sửa.
```

---

## 5. Chiến lược refactor an toàn

Ưu tiên tạo folder con mới trong project chính:

```text
churn_pipeline_v2/
```

Hoặc:

```text
refactor_oop_pipeline/
```

Nguyên tắc:

```text
Project cũ giữ nguyên.
Folder mới là nơi viết lại kiến trúc OOP.
Khi folder mới chạy được thì mới migrate/xóa folder cũ.
```

---

## 6. Kiến trúc folder mới CodeX cần tạo

```text
churn_pipeline_v2/
│   .env.example
│   .gitignore
│   README.md
│   requirements.txt
│
├── data/
│   ├── raw_data/
│   ├── checkpoint_data/
│   ├── EDA_data/
│   └── logger_data/
│
├── docs/
│   ├── database_guideline.md
│   ├── dataflow.md
│   └── pipeline.md
│
├── models/
├── notebooks/
├── reports/
│   ├── data_reports/
│   └── figures/
│
├── sql/
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

Không tạo:

```text
src/pre_processing/logistic_processor.py
src/pre_processing/tree_processor.py
```

Lý do:

- Branch được tạo trong `pipeline_builder.py`.
- Không cần thêm processor trung gian.

---

## 7. Phase 0 — Phân tích project cũ, chưa sửa gì

### Mục tiêu

CodeX đọc project hiện tại và hiểu logic cũ.

### Prompt gợi ý

```text
Read the current project structure and all files in src. Do not modify any file.

You are only allowed to analyze.

Return a responsibility map:
1. What each current src file does.
2. What input files each file reads.
3. What output files each file creates.
4. Which logic belongs to ingestion.
5. Which logic belongs to cleaning.
6. Which logic belongs to feature engineering.
7. Which logic belongs to logistic preprocessing.
8. Which logic belongs to tree preprocessing.
9. Which parts may cause data leakage.
10. Which outputs must be preserved.

Do not edit files.
Do not create files.
Do not run git commands.
```

### Expected output

```text
- Responsibility map
- Dataflow map
- Leakage risk list
- Refactor mapping proposal
```

---

## 8. Phase 1 — Tạo folder mới

### Mục tiêu

Tạo folder refactor mới nhưng chưa migrate logic.

### Prompt gợi ý

```text
Create a new folder named churn_pipeline_v2 inside the project root.

Only create the agreed folder and file skeleton.

Do not modify old project files.
Do not delete anything.
Do not implement business logic yet.
Do not run git commands.

Before editing, list the folders and files you will create and wait for my confirmation.
```

Người dùng chỉ cho phép sửa khi trả lời:

```text
OK sửa
```

---

## 9. Phase 2 — Implement `path.py`

### Mục tiêu

Chuẩn hóa đường dẫn.

### File được phép sửa

```text
churn_pipeline_v2/src/path.py
```

### Prompt gợi ý

```text
Implement churn_pipeline_v2/src/path.py.

Rules:
1. This file is the single source of truth for all paths.
2. Define paths for project root, data folders, docs, models, notebooks, reports, sql, src.
3. Do not implement preprocessing logic.
4. Do not modify other files.
5. Do not run git commands.

Before editing, show the planned changes and wait for my "OK sửa".
After editing, show diff and list changed files.
```

---

## 10. Phase 3 — Implement logger

### Mục tiêu

Tạo logger trước khi chạy pipeline.

### File được phép sửa

```text
churn_pipeline_v2/src/utils/logger.py
```

### Prompt gợi ý

```text
Implement churn_pipeline_v2/src/utils/logger.py.

Requirements:
1. Write logs to data/logger_data/logger_data.txt.
2. Support simple pipeline step logging.
3. Support logging dataset shapes.
4. Do not add preprocessing logic.
5. Do not modify other files.
6. Do not run git commands.

Before editing, list the planned changes and wait for my "OK sửa".
After editing, show diff and list changed files.
```

---

## 11. Phase 4 — Implement `data_ingestion.py`

### Mục tiêu

Load raw data và split 70/15/15 ngay từ đầu.

### File được phép sửa

```text
churn_pipeline_v2/src/data_ingestion.py
```

### Quy tắc kỹ thuật

```text
Input:
data/raw_data/data_raw.csv

Output:
data/checkpoint_data/train_df.csv
data/checkpoint_data/validation_df.csv
data/checkpoint_data/test_df.csv
```

Split:

```text
train      = 70%
validation = 15%
test       = 15%
```

### Prompt gợi ý

```text
Implement churn_pipeline_v2/src/data_ingestion.py.

Requirements:
1. Load raw churn data from data/raw_data/data_raw.csv.
2. Split into train/validation/test with ratio 70/15/15.
3. Use a fixed random_state.
4. Preserve class distribution by target if possible.
5. Save train_df.csv, validation_df.csv, and test_df.csv into data/checkpoint_data/.
6. Lock the test set conceptually after this step.
7. Do not perform feature engineering.
8. Do not perform scaling.
9. Do not perform capping.
10. Do not perform categorical encoding except target handling only if explicitly needed.
11. Log dataset shapes.
12. Do not train models.
13. Do not modify other files.
14. Do not run git commands.

Before editing, list the planned changes and wait for my "OK sửa".
After editing, show diff and list changed files.
```

---

## 12. Phase 5 — Implement preprocessing components

### Mục tiêu

Tạo các preprocessing class nhỏ, sklearn-compatible.

### Quy tắc chung

Mọi class trong `src/pre_processing/` phải:

```text
- Inherit BaseEstimator and TransformerMixin.
- Implement fit() and transform().
- fit() only learns from train.
- transform() must not learn anything.
- Do not read files.
- Do not write files.
- Do not train models.
- Do not hard-code paths.
```

### Thứ tự nên làm

```text
1. target_encoder.py
2. feature_engineer.py
3. capping_outlier.py
4. categorical_encoder.py
5. scaler.py
```

---

### 12.1 `target_encoder.py`

Prompt gợi ý:

```text
Implement churn_pipeline_v2/src/pre_processing/target_encoder.py.

Rules:
1. Class must inherit BaseEstimator and TransformerMixin.
2. It handles target Churn encoding, for example Yes/No to 1/0.
3. fit() should not learn from validation/test.
4. transform() should not recompute learned state.
5. Do not read or write files.
6. Do not train models.
7. Do not modify other files.
8. Do not run git commands.

Before editing, list planned changes and wait for my "OK sửa".
After editing, show diff and list changed files.
```

---

### 12.2 `feature_engineer.py`

Prompt gợi ý:

```text
Implement churn_pipeline_v2/src/pre_processing/feature_engineer.py.

Feature requirements:
1. tenure_group
2. service_diversity
3. monthly_charges_ratio
4. is_paperless_electronic

Rules:
1. Class must inherit BaseEstimator and TransformerMixin.
2. fit() can learn statistics only from train.
3. monthly_charges_ratio must use MonthlyCharges mean learned from train only.
4. validation/test must only transform using learned train statistics.
5. transform() must not learn new statistics.
6. Do not read or write files.
7. Do not train models.
8. Do not modify other files.
9. Do not run git commands.

Before editing, list planned changes and wait for my "OK sửa".
After editing, show diff and list changed files.
```

---

### 12.3 `capping_outlier.py`

Prompt gợi ý:

```text
Implement churn_pipeline_v2/src/pre_processing/capping_outlier.py.

Rules:
1. Class must inherit BaseEstimator and TransformerMixin.
2. Fit capping bounds on train only.
3. Transform validation/test using train-fitted bounds.
4. Do not recompute bounds in transform().
5. This component is mainly for the Logistic Regression branch.
6. Do not apply it to the tree branch in pipeline_builder.py.
7. Do not read or write files.
8. Do not train models.
9. Do not modify other files.
10. Do not run git commands.

Before editing, list planned changes and wait for my "OK sửa".
After editing, show diff and list changed files.
```

---

### 12.4 `categorical_encoder.py`

Prompt gợi ý:

```text
Implement churn_pipeline_v2/src/pre_processing/categorical_encoder.py.

Rules:
1. Class must inherit BaseEstimator and TransformerMixin.
2. Support categorical encoding needed by the pipeline branches.
3. Logistic branch may use one-hot style encoding.
4. Tree branch may use ordinal/label style encoding.
5. Encoder must fit on train only.
6. Validation/test must only transform.
7. Do not learn categories in transform().
8. Do not read or write files.
9. Do not train models.
10. Do not modify other files.
11. Do not run git commands.

Before editing, list planned changes and wait for my "OK sửa".
After editing, show diff and list changed files.
```

---

### 12.5 `scaler.py`

Prompt gợi ý:

```text
Implement churn_pipeline_v2/src/pre_processing/scaler.py.

Rules:
1. Class must inherit BaseEstimator and TransformerMixin.
2. Fit scaler on train only.
3. Transform validation/test using train-fitted scaler.
4. This component is mainly for the Logistic Regression branch.
5. Do not use it in the tree branch unless explicitly requested.
6. Do not read or write files.
7. Do not train models.
8. Do not modify other files.
9. Do not run git commands.

Before editing, list planned changes and wait for my "OK sửa".
After editing, show diff and list changed files.
```

---

## 13. Phase 6 — Implement `pipeline_builder.py`

### Mục tiêu

Tạo pipeline và chia branch.

### File được phép sửa

```text
churn_pipeline_v2/src/pipeline_builder.py
```

### Vai trò

`pipeline_builder.py` tạo:

```text
global preprocessing pipeline
logistic preprocessing branch
tree preprocessing branch
```

Không train model.

### Prompt gợi ý

```text
Implement churn_pipeline_v2/src/pipeline_builder.py.

Requirements:
1. Build preprocessing pipelines only.
2. Do not train any model.
3. Create separate branches:
   - logistic preprocessing branch
   - tree preprocessing branch
4. Logistic branch may include:
   - target encoding
   - feature engineering
   - outlier capping
   - categorical encoding
   - scaling
5. Tree branch may include:
   - target encoding
   - feature engineering
   - categorical encoding
6. Tree branch must not include:
   - outlier capping
   - scaling
7. fit() must be called only on train.
8. validation and test must only be transformed.
9. Do not create logistic_processor.py.
10. Do not create tree_processor.py.
11. Keep branch composition inside pipeline_builder.py.
12. Do not modify notebooks.
13. Do not run git commands.

Before editing, list planned changes and wait for my "OK sửa".
After editing, show diff and list changed files.
```

---

## 14. Phase 7 — Implement `main.py`

### Mục tiêu

Điều phối flow chính.

### File được phép sửa

```text
churn_pipeline_v2/src/main.py
```

### Vai trò

`main.py` gọi:

```text
data_ingestion.py
pipeline_builder.py
logger.py
```

Không chứa logic chi tiết.

### Prompt gợi ý

```text
Implement churn_pipeline_v2/src/main.py as the orchestration entry point.

Responsibilities:
1. Run data ingestion if checkpoint files do not exist or if forced.
2. Call pipeline_builder to build and apply preprocessing branches.
3. Do not perform feature engineering directly.
4. Do not perform encoding directly.
5. Do not perform capping directly.
6. Do not perform scaling directly.
7. Do not train models.
8. Log each major step.
9. Do not modify other files.
10. Do not run git commands.

Before editing, list planned changes and wait for my "OK sửa".
After editing, show diff and list changed files.
```

---

## 15. Phase 8 — Update notebooks

### Mục tiêu

Notebook dùng pipeline mới để train model.

### Quy tắc

Notebook được:

```text
- Train model.
- Evaluate model.
- Tune threshold on validation.
- Save model to models/.
- Save reports to reports/data_reports/.
- Save figures to reports/figures/.
```

Notebook không được:

```text
- Fit preprocessing lại trên validation/test.
- Fit scaler/encoder/capper riêng ngoài pipeline.
- Dùng test để chọn threshold/model.
- Ghi đè checkpoint split tùy tiện.
```

### Prompt gợi ý

```text
Update notebooks to use the new churn_pipeline_v2 pipeline outputs.

Rules:
1. Do not refit preprocessing in notebooks.
2. Logistic notebook uses logistic branch output.
3. Random Forest and XGBoost notebooks use tree branch output.
4. Use validation for model selection and threshold tuning.
5. Use test only for final evaluation.
6. Save trained models to models/.
7. Save metrics to reports/data_reports/.
8. Save figures to reports/figures/.
9. Do not modify src files in this step.
10. Do not run git commands.

Before editing, list planned notebook changes and wait for my "OK sửa".
After editing, show diff and list changed files.
```

---

## 16. Phase 9 — Validation checklist

Trước khi xóa/migrate project cũ, kiểm tra:

```text
[ ] Folder churn_pipeline_v2 tồn tại.
[ ] data_ingestion chạy được.
[ ] train/validation/test đúng tỷ lệ 70/15/15.
[ ] Class distribution được giữ nếu stratify.
[ ] test_df.csv được tạo và không bị fit.
[ ] fit chỉ xảy ra trên train.
[ ] validation chỉ transform.
[ ] test chỉ transform.
[ ] pipeline_builder chạy được.
[ ] logistic branch chạy được.
[ ] tree branch chạy được.
[ ] Không có logistic_processor.py.
[ ] Không có tree_processor.py.
[ ] Không xuất preprocessed CSV trung gian vào data/processing.
[ ] Notebooks train được Logistic Regression.
[ ] Notebooks train được Random Forest.
[ ] Notebooks train được XGBoost.
[ ] Metrics không lệch bất thường so với bản cũ.
[ ] Models được lưu vào models/.
[ ] Reports được lưu vào reports/.
[ ] Figures được lưu vào reports/figures/.
[ ] README được cập nhật.
[ ] docs/dataflow.md được cập nhật.
[ ] docs/pipeline.md được cập nhật.
```

---

## 17. Phase 10 — Migrate / replace project cũ

Chỉ thực hiện sau khi folder mới chạy ổn.

Quy trình:

```text
1. Backup project cũ.
2. So sánh output cũ và output mới.
3. Giữ lại dashboard, SQL scripts, docs, reports quan trọng.
4. Xóa script sequence cũ:
   - 01_data_ingestion.py
   - 02_data_cleaning.py
   - 03_data_extraction.py
   - 04_feature_engineering.py
   - 05_data_processing.py
   - 06_tree_data_processing.py
5. Đưa churn_pipeline_v2 thành cấu trúc chính.
6. Cập nhật README.
7. Cập nhật docs.
8. Chạy lại toàn bộ pipeline.
```

Không chạy các lệnh git sau nếu chưa được người dùng yêu cầu:

```text
git add
git commit
git push
git reset
```

---

## 18. Prompt khung cho mọi task CodeX

Dùng prompt khung này ở đầu mỗi task:

```text
You are working on the ADY201m Churn Project refactor.

Safety rules:
- Mode: Ask for approval.
- Full access: Off.
- Approve for me: Off.
- Network: Off unless package installation or internet lookup is explicitly needed.
- Analyze first.
- Do not modify files unless I say "OK sửa".
- If changes are needed, list files to modify, reasons, and expected changes.
- Wait for my confirmation before editing.
- Do not refactor outside the requested scope.
- Do not run git add, git commit, git push, or git reset.
- After editing, show diff and list changed files.

Project rules:
- Refactor inside a new folder first.
- Do not delete old project files.
- data_ingestion performs 70/15/15 split.
- Test set is locked after ingestion.
- fit() only on train.
- validation/test only transform().
- pipeline_builder creates preprocessing pipelines and branches.
- pipeline_builder does not train models.
- notebooks train models.
- preprocessing classes inherit BaseEstimator and TransformerMixin.
- Do not create logistic_processor.py or tree_processor.py.
```

---

## 19. Recommended CodeX execution order

```text
1. Analyze old project only.
2. Create churn_pipeline_v2 skeleton.
3. Implement path.py.
4. Implement logger.py.
5. Implement data_ingestion.py.
6. Implement target_encoder.py.
7. Implement feature_engineer.py.
8. Implement capping_outlier.py.
9. Implement categorical_encoder.py.
10. Implement scaler.py.
11. Implement pipeline_builder.py.
12. Implement main.py.
13. Update notebooks.
14. Validate outputs.
15. Migrate only after confirmation.
```

---

## 20. Final rule

Nếu CodeX đề xuất sửa nhiều file cùng lúc, yêu cầu tách nhỏ lại.

Ưu tiên:

```text
Một prompt = một nhóm file nhỏ.
Một thay đổi = một mục tiêu rõ ràng.
Không sửa lan rộng.
Không tự động migrate.
Không tự động xóa.
```
