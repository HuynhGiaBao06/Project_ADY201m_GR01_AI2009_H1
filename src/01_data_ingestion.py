# File: src/data_ingestion.py
import pandas as pd
import os
from db_config import get_sql_engine # IMPORT TỪ FILE CẤU HÌNH

# 1. Tự động lấy đường dẫn tuyệt đối
current_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(current_dir, "..", "data", "processing", "data_processing.csv")

# 2. Đọc dữ liệu từ file CSV
print(f"Đang đọc dữ liệu từ CSV: {os.path.abspath(output_path)}")
df = pd.read_csv(output_path)

# 3. Lấy engine từ file config
engine = get_sql_engine()
table_name = 'Predictive_Customer_Churn_DB'

# 4. Đẩy dữ liệu vào T-SQL
print(f"Đang đẩy dữ liệu vào bảng '{table_name}'...")
try:
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    print("✅ Đẩy dữ liệu vào SQL Server thành công!")
except Exception as e:
    print(f"❌ Có lỗi xảy ra: {e}")

# 5. Kiểm tra chéo (Data Validation)
df_sql = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)
print(f"Số dòng trong CSV: {len(df)} | Số dòng trong SQL: {len(df_sql)}")

if len(df) == len(df_sql):
    print("✅ Khớp số lượng dòng!")
else:
    print("❌ Lệch số lượng dòng, hãy kiểm tra lại!")