def feature_engineering(df):
    """
    Hàm tạo các biến đặc trưng mới phục vụ mô hình dự đoán Churn.
    Đầu vào là DataFrame đã được trích xuất từ SQL View.
    """
    # 1. Sửa lỗi tham số: Dùng đúng df truyền vào thay vì df_raw
    df_features = df.copy()
    
    # 2. tenure_group: Phân nhóm thời gian sử dụng
    bins = [0, 12, 24, 36, 48, 60, 72, np.inf]
    labels = ['0-12 months', '13-24 months', '25-36 months', '37-48 months', '49-60 months', '61-72 months', '72+ months']
    # Lưu ý: include_lowest=True giúp bao gồm cả những khách hàng mới dùng (Tenure = 0)
    df_features['tenure_group'] = pd.cut(df_features['Tenure'], bins=bins, labels=labels, right=True, include_lowest=True)

    # 3. service_diversity: Tính tổng số dịch vụ phụ trợ đang sử dụng
    services_cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport']
    # Ép kiểu astype(int) đảm bảo an toàn nếu SQL trả về True/False (kiểu BIT)
    df_features['service_diversity'] = df_features[services_cols].astype(int).sum(axis=1)

    # 4. monthly_charges_ratio: Tỷ lệ chi phí tháng so với mức trung bình
    mean_monthly_charges = df_features['MonthlyCharges'].mean()
    df_features['monthly_charges_ratio'] = df_features['MonthlyCharges'] / mean_monthly_charges

    # 5. is_paperless_electronic: Tổ hợp hóa đơn điện tử và thanh toán tự động
    # Ép kiểu sang int để đồng nhất cách so sánh
    is_paperless = df_features['PaperlessBilling'].astype(int) == 1
    is_auto_payment = df_features['PaymentMethod'].str.contains('automatic', case=False, na=False)
    df_features['is_paperless_electronic'] = (is_paperless & is_auto_payment).astype(int)

    return df_features

# ==========================================
# CÁCH TEST HÀM (Chạy trong Cell tiếp theo)
# ==========================================
# Giả sử 'df' là biến bạn đã nạp từ file CSV trung gian ở Cell 1
print("Đang tiến hành tạo các đặc trưng mới...")
df_engineered = feature_engineering(df)

# In ra 5 dòng đầu tiên để kiểm tra kết quả của 4 biến vừa tạo
cols_to_check = ['tenure_group', 'service_diversity', 'monthly_charges_ratio', 'is_paperless_electronic']
print("\n✅ Kết quả Feature Engineering:")
display(df_engineered[cols_to_check].head())