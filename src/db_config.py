# File: src/db_config.py
import os
import urllib
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Bắt buộc load file .env từ thư mục gốc
load_dotenv() 

def get_sql_engine():
    # Chỉ lấy dữ liệu từ .env, xóa sạch các giá trị hardcode
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')

    # Kiểm tra an toàn: Nếu thiếu bất kỳ biến nào trong .env thì dừng chương trình và báo lỗi ngay
    if not all([server, database, username, password]):
        raise ValueError("LỖI BẢO MẬT: Thiếu thông tin Database! Hãy kiểm tra lại file .env")

    params = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )
    
    # Tạo và trả về engine
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=True)  
    return engine

if __name__ == "__main__":
    # Test thử kết nối
    engine = get_sql_engine()
    with engine.connect() as conn:
        print("✅ Kết nối Database thành công!")