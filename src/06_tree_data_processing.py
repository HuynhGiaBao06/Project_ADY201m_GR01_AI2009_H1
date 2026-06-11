import os
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder # Đã đổi từ OneHotEncoder sang OrdinalEncoder
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
# 2. CHIA TẬP TRAIN/TEST (CHUYỂN LÊN TRƯỚC ĐỂ TRÁNH DATA LEAKAGE)
# ==========================================
# CỰC KỲ QUAN TRỌNG: Phải chia dữ liệu thô trước khi đưa vào Pipeline
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ==========================================
# 🚀 XỬ LÝ FIX DATA LEAKAGE: TẠO CỘT MỚI TẠI ĐÂY
# ==========================================
# Copy để tránh lỗi SettingWithCopyWarning của Pandas
X_train = X_train.copy()
X_test = X_test.copy()

# Tính trung bình MonthlyCharges CHỈ TRÊN TẬP TRAIN
mean_charges_train = X_train['MonthlyCharges'].mean()

# Tạo cột tỷ lệ cho cả Train và Test bằng mean của Train
X_train['monthly_charges_ratio'] = X_train['MonthlyCharges'] / mean_charges_train
X_test['monthly_charges_ratio'] = X_test['MonthlyCharges'] / mean_charges_train

# ==========================================
# 3. XÂY DỰNG PIPELINE VÀ ENCODE DỮ LIỆU
# ==========================================
# Lấy danh sách cột object từ tập Train để đảm bảo tính nhất quán
cat_cols = X_train.select_dtypes(include=['object']).columns.tolist()

feature_transforms = ColumnTransformer(
    transformers=[
        # Sử dụng OrdinalEncoder với cấu hình handle_unknown để xử lý giá trị lạ trong tập Test
        ('encoder', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1), cat_cols)
    ],
    remainder='passthrough' # Giữ nguyên Outliers và các biến số học, không Scaling
).set_output(transform="pandas")

preprocessing_pipeline = Pipeline(steps=[
    ('feature_transforms', feature_transforms)
])

# THỰC HIỆN ENCODE (FIT TRÊN TRAIN, TRANSFORM TRÊN CẢ TRAIN VÀ TEST)
print("🔄 Đang tiến hành Ordinal Encoding (Tránh Data Leakage)...")
X_train_encoded = preprocessing_pipeline.fit_transform(X_train)
X_test_encoded = preprocessing_pipeline.transform(X_test)

# ==========================================
# 4. ĐÓNG GÓI PIPELINE VÀ DỮ LIỆU ĐÃ XỬ LÝ
# ==========================================
artifacts_dir = os.path.join(BASE_DIR, 'artifacts')
os.makedirs(artifacts_dir, exist_ok=True)

# Lưu pipeline đã fit (Lúc này Pipeline đã học được các Categories từ tập Train)
joblib.dump(preprocessing_pipeline, os.path.join(artifacts_dir, 'tree_preprocessing_pipeline.pkl'))

# Lưu tập dữ liệu đã chia (lúc này X_train_tree và X_test_tree ĐÃ LÀ SỐ HOÀN TOÀN và KHÔNG RÒ RỈ)
X_train_encoded.to_csv(os.path.join(artifacts_dir, 'X_train_tree.csv'), index=False)
X_test_encoded.to_csv(os.path.join(artifacts_dir, 'X_test_tree.csv'), index=False)
y_train.to_csv(os.path.join(artifacts_dir, 'y_train_tree.csv'), index=False)
y_test.to_csv(os.path.join(artifacts_dir, 'y_test_tree.csv'), index=False)

print("\n💾 Đã đóng gói pipeline và lưu dữ liệu Train/Test (đã encoded) thành công.")