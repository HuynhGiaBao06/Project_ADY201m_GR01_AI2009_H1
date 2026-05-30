import os
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

# ==========================================
# 0. TỰ ĐỘNG XỬ LÝ ĐƯỜNG DẪN BẰNG THƯ VIỆN 'OS'
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(current_dir)
DATA_PATH = os.path.join(BASE_DIR, 'data', 'interim' ,'extracted_data.csv') 

print(f"📂 Đang tìm kiếm dữ liệu tại: {DATA_PATH}")

try:
    df = pd.read_csv(DATA_PATH)
    print("✅ Đã nạp thành công dữ liệu vào DataFrame 'df'!")
except FileNotFoundError:
    fallback_path = os.path.join('data', 'cleaned_data.csv')
    try:
        df = pd.read_csv(fallback_path)
        print(f"✅ Đã tìm thấy dữ liệu tại '{fallback_path}'!")
    except FileNotFoundError:
        raise FileNotFoundError("❌ Không tìm thấy file dữ liệu. Hãy kiểm tra lại.")

# ==========================================
# 1. TÁCH BIẾN ĐỘC LẬP (X) VÀ MỤC TIÊU (y)
# ==========================================
id_col = 'ID' if 'ID' in df.columns else ('customerID' if 'customerID' in df.columns else None)
X = df.drop(columns=[id_col, 'Churn']) if id_col else df.drop(columns=['Churn'])
y = df['Churn']

# ==========================================
# 2. XÂY DỰNG PIPELINE VÀ ENCODE TOÀN BỘ DỮ LIỆU TRƯỚC
# ==========================================
cat_cols = X.select_dtypes(include=['object']).columns.tolist()

feature_transforms = ColumnTransformer(
    transformers=[
        ('encoder', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), cat_cols)
    ],
    remainder='passthrough'
).set_output(transform="pandas")

preprocessing_pipeline = Pipeline(steps=[
    ('feature_transforms', feature_transforms)
])

# THỰC HIỆN ENCODE TRÊN TOÀN BỘ TẬP X
print("🔄 Đang tiến hành One-Hot Encoding trên toàn bộ dữ liệu...")
X_encoded = preprocessing_pipeline.fit_transform(X)

# ==========================================
# 3. CHIA TẬP TRAIN/TEST (TỪ DỮ LIỆU ĐÃ ENCODE)
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42, stratify=y
)

# ==========================================
# 4. ĐÓNG GÓI PIPELINE VÀ DỮ LIỆU ĐÃ XỬ LÝ
# ==========================================
artifacts_dir = os.path.join(BASE_DIR, 'artifacts')
os.makedirs(artifacts_dir, exist_ok=True)

# Lưu pipeline đã fit
joblib.dump(preprocessing_pipeline, os.path.join(artifacts_dir, 'tree_preprocessing_pipeline.pkl'))

# Lưu tập dữ liệu đã chia (lúc này X_train và X_test ĐÃ LÀ SỐ HOÀN TOÀN)
X_train.to_csv(os.path.join(artifacts_dir, 'X_train.csv'), index=False)
X_test.to_csv(os.path.join(artifacts_dir, 'X_test.csv'), index=False)
y_train.to_csv(os.path.join(artifacts_dir, 'y_train.csv'), index=False)
y_test.to_csv(os.path.join(artifacts_dir, 'y_test.csv'), index=False)

print("\n💾 Đã đóng gói pipeline và lưu dữ liệu Train/Test (đã encoded) thành công.")