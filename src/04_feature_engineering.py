import pandas as pd
import os
import numpy as np
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

    # 4. monthly_charges_ratio: Tỷ lệ chi phí tháng so với mức trung bình(Được tạo ở data processing, tránh data lackage [Đang bị lỗi kiến trúc dự án])

    # 5. is_paperless_electronic: Tổ hợp hóa đơn điện tử và thanh toán tự động
    # Ép kiểu sang int để đồng nhất cách so sánh
    is_paperless = df_features['PaperlessBilling'].astype(int) == 1
    is_auto_payment = df_features['PaymentMethod'].str.contains('automatic', case=False, na=False)
    df_features['is_paperless_electronic'] = (is_paperless & is_auto_payment).astype(int)

    return df_features

# ==========================================
# 2. XÁC ĐỊNH ĐƯỜNG DẪN TỚI FILE DATA (do data_extraction.py sinh ra)
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
# Lùi lại 1 thư mục (về thư mục gốc của project) rồi vào data/interim
data_file = os.path.join(current_dir, "..", "data", "interim", "extracted_data.csv")

# ==========================================
# 3. ĐỌC FILE LÊN VÀ KIỂM TRA
# ==========================================
if os.path.exists(data_file):
    print(f"⏳ Đang nạp dữ liệu từ: {data_file}...")
    df = pd.read_csv(data_file)
    print(f"Kích thước ban đầu (từ data_extraction.py): {df.shape}")
else:
    print(f"❌ Không tìm thấy file tại {data_file}. Chạy lại file data_extraction.py trước nhé.")
    exit()

# ==========================================
# 4. CHẠY LOGIC TẠO 3 CỘT MỚI
# ==========================================
print("\n⚙️ Đang tiến hành tạo các đặc trưng mới...")
df_engineered = feature_engineering(df)

# ==========================================
# 5. GHI ĐÈ TRỰC TIẾP LẠI VÀO DATASET ĐÓ
# ==========================================
df_engineered.to_csv(data_file, index=False)

print(f"\n✅ Đã thêm 3 cột mới và GHI ĐÈ thành công vào file cũ!")
print(f"Kích thước bộ dữ liệu hiện tại: {df_engineered.shape}")

# ==========================================
# 6. KIỂM TRA KẾT QUẢ
# ==========================================
cols_to_check = ['tenure_group', 'service_diversity' , 'is_paperless_electronic']
print("\n🔍 Xem trước các cột mới đã được gắn vào dataset:")
print(df_engineered[cols_to_check].head())