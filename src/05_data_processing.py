import os
import pandas as pd
import numpy as np
import joblib

# BẮT BUỘC PHẢI CÓ DÒNG NÀY ĐỂ ĐỊNH NGHĨA CUSTOM CLASS:
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# ==========================================
# 0. TỰ ĐỘNG XỬ LÝ ĐƯỜNG DẪN BẰNG THƯ VIỆN 'OS'
# ==========================================
# Xác định thư mục gốc của dự án (Project Root)
current_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(current_dir)

# Nối chuỗi đường dẫn tới thư mục data và file csv (interim chứa đủ 19 cột)
DATA_PATH = os.path.join(BASE_DIR, 'data', 'interim' ,'extracted_data.csv') 

print(f"📂 Đang tìm kiếm dữ liệu tại: {DATA_PATH}")

try:
    df = pd.read_csv(DATA_PATH)
    print("✅ Đã nạp thành công dữ liệu vào DataFrame 'df'!")
except FileNotFoundError:
    # Phương án dự phòng
    fallback_path = os.path.join('data', 'cleaned_data.csv')
    try:
        df = pd.read_csv(fallback_path)
        print(f"✅ Đã tìm thấy dữ liệu tại đường dẫn tương đối '{fallback_path}'!")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"❌ Không tìm thấy file dữ liệu tại {DATA_PATH}. "
            f"Hãy đảm bảo bạn đã đặt file data sạch vào thư mục."
        )

# ==========================================
# 1. ĐỊNH NGHĨA CLASS OutlierCapperIQR
# ==========================================
class OutlierCapperIQR(BaseEstimator, TransformerMixin):
    def __init__(self, factor=1.5):
        self.factor = factor
        self.lower_bounds_ = {}
        self.upper_bounds_ = {}

    def fit(self, X, y=None):
        X_df = pd.DataFrame(X)
        # Lưu lại tên cột đầu vào theo chuẩn Sklearn
        self.feature_names_in_ = X_df.columns.values 
        
        for col in X_df.columns:
            Q1 = X_df[col].quantile(0.25)
            Q3 = X_df[col].quantile(0.75)
            IQR = Q3 - Q1
            self.lower_bounds_[col] = Q1 - self.factor * IQR
            self.upper_bounds_[col] = Q3 + self.factor * IQR
        return self

    def transform(self, X):
        X_df = pd.DataFrame(X).copy()
        for col in X_df.columns:
            # Ép giá trị ngoại lai về các ngưỡng (Capping)
            X_df[col] = np.clip(X_df[col], self.lower_bounds_[col], self.upper_bounds_[col])
        return X_df

    # 🚀 BẮT BUỘC THÊM HÀM NÀY ĐỂ TƯƠNG THÍCH VỚI set_output(transform="pandas")
    def get_feature_names_out(self, input_features=None):
        if input_features is not None:
            return input_features
        return self.feature_names_in_
# ==========================================
# 2. PHÂN TÁCH BIẾN X, Y VÀ CHIA TẬP TRAIN/TEST
# ==========================================
# Loại bỏ cột định danh 'ID' nếu có và cột mục tiêu 'Churn' để làm đặc trưng X
id_col = 'ID' if 'ID' in df.columns else ('customerID' if 'customerID' in df.columns else None)

if id_col:
    X = df.drop(columns=[id_col, 'Churn'])
else:
    X = df.drop(columns=['Churn'])

y = df['Churn']

# Thực hiện tách tập Train/Test (80/20, Stratify theo y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"📊 Kích thước tập huấn luyện (Train set): {X_train.shape}")
print(f"📊 Kích thước tập kiểm thử (Test set)   : {X_test.shape}")

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
# 3. XÂY DỰNG COLUMN TRANSFORMER (SUB-PIPELINE)
# ==========================================
iqr_cols = ['Tenure', 'MonthlyCharges']
log_cols = ['TotalCharges']

# Chọn các cột có kiểu 'object' (chữ) để One-Hot Encode (Dependents, PaymentMethod, InternetService, tenure_group)
# Các cột int64/float64 còn lại sẽ tự động đi qua luồng passthrough
cat_cols = X.select_dtypes(include=['object']).columns.tolist()

feature_transforms = ColumnTransformer(
    transformers=[
        ('iqr_capper', OutlierCapperIQR(factor=1.5), iqr_cols),
        ('log_transform', FunctionTransformer(np.log1p, validate=False), log_cols),
        ('encoder', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), cat_cols)
    ],
    remainder='passthrough'
)

# 🚀 ÉP SKLEARN TRẢ VỀ DATAFRAME ĐỂ GIỮ NGUYÊN TÊN CỘT
feature_transforms.set_output(transform="pandas")

# Pipeline tổng quát
preprocessing_pipeline = Pipeline(steps=[
    ('feature_transforms', feature_transforms),
    ('scaler', StandardScaler())
])

# 🚀 ÉP PIPELINE TRẢ VỀ DATAFRAME
preprocessing_pipeline.set_output(transform="pandas")

# FIT & TRANSFORM DỮ LIỆU LUÔN TẠI ĐÂY ĐỂ XUẤT RA CSV ĐÃ QUA XỬ LÝ
X_train_processed = preprocessing_pipeline.fit_transform(X_train)
X_test_processed = preprocessing_pipeline.transform(X_test)

# ==========================================
# 4. ĐÓNG GÓI PIPELINE VÀ DỮ LIỆU ĐỂ XUẤT FILE (BẰNG OS)
# ==========================================
artifacts_dir = os.path.join(BASE_DIR, 'artifacts')
os.makedirs(artifacts_dir, exist_ok=True)

# Xuất đối tượng Pipeline để sau này tái sử dụng
joblib.dump(preprocessing_pipeline, os.path.join(artifacts_dir, 'preprocessing_pipeline.pkl'))

# Xuất dữ liệu đã xử lý qua Pipeline ra file CSV
X_train_processed.to_csv(os.path.join(artifacts_dir, 'X_train.csv'), index=False)
X_test_processed.to_csv(os.path.join(artifacts_dir, 'X_test.csv'), index=False)
y_train.to_csv(os.path.join(artifacts_dir, 'y_train.csv'), index=False)
y_test.to_csv(os.path.join(artifacts_dir, 'y_test.csv'), index=False)

print("\n💾 ĐÃ ĐÓNG GÓI VÀ XUẤT FILE THÀNH CÔNG!")
print(f"📍 Toàn bộ tệp tin được lưu tại thư mục: {artifacts_dir}")