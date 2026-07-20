"""Data upload utilities for the churn pipeline."""
import pandas as pd

from .utils.logger import get_pipeline_logger
from .db_config import NeonDBManager
from .path import DATA_RAW_FILE, check_and_create_directories

class DataUploader:
    """
    Class chuyên trách việc đọc dữ liệu thô từ thư mục 'data/' cục bộ
    và đẩy lên hệ quản trị cơ sở dữ liệu Neon PostgreSQL.
    """

    def __init__(self):
        self.db = NeonDBManager()
        self.log = get_pipeline_logger(self.__class__.__name__)
        self.log.debug("Created class NeonDBManager")
        
    # Đã bỏ tham số filename vì chúng ta dùng trực tiếp DATA_RAW_FILE
    def upload_raw_data(self, table_name: str, if_exists: str = "append"):
        """
        Đọc file CSV/Excel và ghi lên bảng SQL.
        
        Args:
            table_name (str): Tên bảng sẽ được tạo hoặc ghi đè trên PostgreSQL.
            if_exists (str): 'append' (thêm dòng), 'fail' (dừng nếu bảng tồn tại),
                hoặc 'replace' (ghi đè bảng cũ; chỉ dùng khi cố ý rebuild schema).
        """
        
        # Trỏ chính xác đến file dữ liệu nhờ biến DATA_RAW_FILE từ path.py
        file_path = DATA_RAW_FILE

        if not file_path.exists():
            # Sử dụng ERROR vì file không tồn tại làm gián đoạn toàn bộ quá trình
            self.log.error(f"Data file not found at path: {file_path}")
            self.log.info("Hint: Please verify if the file has been copied to the 'data/' directory.")
            return False
        
        self.log.info(f"Reading data file from: {file_path}...")

        try:
            # Hỗ trợ đọc cả định dạng CSV và Excel
            if file_path.suffix == ".csv":
                df = pd.read_csv(file_path)

            elif file_path.suffix in ['.xls', '.xlsx']:
                df = pd.read_excel(file_path) 

            else:
                self.log.error("Unsupported file format. Please use .csv or .xlsx only.")
                return False
            
            self.log.info(f"Successfully loaded {len(df)} rows of data into Pandas DataFrame.")

        except Exception as e:
            # exc_info=True giúp log lưu lại toàn bộ traceback của lỗi, cực kỳ hữu ích khi debug
            self.log.error(f"File reading failed. Local memory load error. Details: {e}", exc_info=True)
            return False
        
        # Đẩy dữ liệu lên cơ sở dữ liệu
        self.log.info(f"Starting to push data to DB table '{table_name}'...")
        if if_exists == "replace":
            self.log.warning(
                "if_exists='replace' will drop and recreate the target table from the CSV shape."
            )

        success = self.db.push_data(df=df, table_name=table_name, if_exists=if_exists)

        if success:
            self.log.info(f"SUCCESS: Data successfully uploaded to DB. Target table: '{table_name}'.")
        else:
            self.log.error("FAILED: Could not push data to DB. Please review the logs above for details.")

        return success
    
# === Cách sử dụng (Thực thi độc lập) ===
if __name__ == "__main__":
    uploader = DataUploader()
    
    TARGET_TABLE = "db_predictive_churn"
    
    uploader.upload_raw_data(
        table_name=TARGET_TABLE,
        if_exists="append" 
    )
