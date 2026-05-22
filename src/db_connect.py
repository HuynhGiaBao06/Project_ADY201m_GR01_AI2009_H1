import pandas as pd
from sqlalchemy import create_engine
import urllib
import os

# 1. Tự động lấy đường dẫn tuyệt đối
# Lấy thư mục chứa file db_connect.py (tức là thư mục 'src')
current_dir = os.path.dirname(os.path.abspath(__file__))

# Đi lùi lên 1 cấp (về thư mục Project) rồi vào data -> processing -> file csv
output_path = os.path.join(current_dir, "..", "data", "processing", "data_processing.csv")

# Để chắc chắn, in ra đường dẫn xem đã đúng chưa:
print(f"Đường dẫn file CSV: {os.path.abspath(output_path)}")

# 2. Đọc dữ liệu từ file CSV
print("Đang đọc dữ liệu từ CSV...")
df = pd.read_csv(output_path)

# 3. Thông tin cấu hình kết nối SQL Server
server = 'fptu-project-db.database.windows.net'       # Ví dụ: 'localhost' hoặc '192.168.1.10'
database = 'Predictive_Customer_Churn_DB'           # Tên cơ sở dữ liệu của bạn
username = 'admin_baohg'                     # Tài khoản SQL
password = 'Huynhgiabao123@'               # Mật khẩu SQL
table_name = 'Predictive_Customer_Churn_DB'       # Tên bảng bạn đã tạo schema

# 4. Tạo Connection String
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password}"
)

# Thêm fast_executemany=True để tăng tốc độ insert dữ liệu (rất hữu ích với file CSV lớn)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=True)

# 5. Đẩy dữ liệu vào T-SQL
print(f"Đang đẩy dữ liệu vào bảng '{table_name}'...")
try:
    # index=False: Bỏ qua cột index mặc định của pandas
    # if_exists='append': Thêm dữ liệu vào bảng đã có sẵn schema
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    print("✅ Đẩy dữ liệu vào SQL Server thành công!")
except Exception as e:
    print(f"❌ Có lỗi xảy ra: {e}")

# Đọc lại dữ liệu từ SQL lên pandas
df_sql = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)

print(f"Số dòng trong CSV: {len(df)}")
print(f"Số dòng trong SQL: {len(df_sql)}")

if len(df) == len(df_sql):
    print("✅ Khớp số lượng dòng!")
else:
    print("❌ Lệch số lượng dòng, hãy kiểm tra lại!")