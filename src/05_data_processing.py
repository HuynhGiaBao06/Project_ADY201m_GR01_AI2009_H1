# File: src/03_data_processing.py
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# =====================================================================
# 1. CUSTOM CLASS XỬ LÝ OUTLIER BẰNG PHƯƠNG PHÁP IQR CAPPING
# =====================================================================
class OutlierCapper(BaseEstimator, TransformerMixin):
    """
    Class tự chế tuân thủ chuẩn Scikit-Learn.
    Tìm biên dưới và biên trên bằng IQR, sau đó ép (cap) các giá trị vượt biên,
    giúp giữ nguyên số dòng dữ liệu mà không làm lệch mô hình tuyến tính.
    """
    def __init__(self, variables=None):
        self.variables = variables
        self.lower_bounds_ = {}
        self.upper_bounds_ = {}

    def fit(self, X, y=None):
        # Tính toán Q1, Q3 và IQR cho từng cột số học trong tập Train
        for var in self.variables:
            Q1 = X[var].quantile(0.25)
            Q3 = X[var].quantile(0.75)
            IQR = Q3 - Q1
            self.lower_bounds_[var] = Q1 - 1.5 * IQR
            self.upper_bounds_[var] = Q3 + 1.5 * IQR
        return self

    def transform(self, X):
        # Tiến hành ép giá trị ngoại lai về biên (Capping)
        X_capped = X.copy()
        for var in self.variables:
            X_capped[var] = np.where(X_capped[var] > self.upper_bounds_[var], self.upper_bounds_[var],
                             np.where(X_capped[var] < self.lower_bounds_[var], self.lower_bounds_[var], X_capped[var]))
        return X_capped

# =====================================================================
# 2. HÀM DỰNG BỘ TIỀN XỬ LÝ (PREPROCESSOR BUNDLE)
# =====================================================================
def get_logistic_preprocessor(num_cols, cat_cols):
    """
    Hàm đóng gói các bước tiền xử lý riêng cho mô hình Logistic Regression.
    Bao gồm: Capping Outlier -> Scaling cho biến số -> OneHot Encoding cho biến chữ.
    """
    # Pipeline riêng cho cột số (Xử lý Outlier trước rồi mới Scale)
    num_transformer = Pipeline(steps=[
        ('capper', OutlierCapper(variables=num_cols)),
        ('scaler', StandardScaler())
    ])
    
    # Pipeline riêng cho cột chữ (Mã hóa One-Hot)
    cat_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))
    ])
    
    # Gộp 2 luồng lại bằng ColumnTransformer
    preprocessor = ColumnTransformer(transformers=[
        ('num', num_transformer, num_cols),
        ('cat', cat_transformer, cat_cols)
    ], remainder='passthrough') # các biến đã xử lý ở Bước 5 (0/1) thì giữ nguyên
    
    return preprocessor