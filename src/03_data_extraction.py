# File: src/data_extraction.py
import pandas as pd
import os
from db_config import get_sql_engine

# 1. Gọi engine và nạp dữ liệu
engine = get_sql_engine()
view_name = 'vw_Cleaned_Customer_Data'

print(f"Đang trích xuất dữ liệu từ view {view_name}...")
df_clean = pd.read_sql(f"SELECT * FROM {view_name}", con=engine)

# ---- PHẦN MỚI THÊM VÀO: KIỂM TRA VÀ CHUYỂN ĐỔI KIỂU BIT -> INT ----
print("\n🔍 [Kiểm tra] Kiểu dữ liệu gốc của một số cột BIT khi vừa kéo về:")
# Lấy danh sách các cột BIT dựa trên Schema DB của nhóm
bit_columns = ['Churn', 'Partner', 'OnlineSecurity', 'OnlineBackup', 
               'DeviceProtection', 'TechSupport', 'PaperlessBilling', 'SeniorCitizen']

# In ra thử vài dòng để xem dạng True/False hay 1/0
print(df_clean[bit_columns].head(3)) 

print("\n⚙️ Đang ép kiểu (Casting) các cột BIT sang dạng Integer (1/0)...")
# Ép kiểu an toàn
for col in bit_columns:
    if col in df_clean.columns:
        # Chuyển True/False thành 1/0
        df_clean[col] = df_clean[col].astype(int)

print("✅ Đã ép kiểu thành công! Xem thử kết quả:")
print(df_clean[bit_columns].head(3))
# ------------------------------------------------------------------

# 2. Tự động tìm đường dẫn để lưu vào thư mục data/interim
current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(current_dir, "..", "data", "interim")

# Tạo thư mục nếu chưa có
os.makedirs(output_dir, exist_ok=True) 

# 3. Lưu file
output_file = os.path.join(output_dir, "extracted_data.csv")
df_clean.to_csv(output_file, index=False)

print(f"\n✅ Đã kéo, xử lý kiểu dữ liệu và lưu thành công tại: {output_file}")
print(f"Kích thước bộ dữ liệu: {df_clean.shape}")