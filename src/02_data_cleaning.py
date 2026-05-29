import pandas as pd
import numpy as np
import os

class ChurnDataPipeline:
    """
    Pipeline xử lý dữ liệu chuẩn hóa cho bài toán dự đoán Churn.
    """
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None

    def load_data(self):
        """Bước 0: Tải và kiểm tra dữ liệu gốc"""
        if os.path.exists(self.input_path):
            print(f"[THÀNH CÔNG] Đã tìm thấy file dữ liệu tại: {self.input_path}")
            self.df = pd.read_csv(self.input_path)
            print(f"Kích thước dữ liệu gốc: {self.df.shape[0]} dòng, {self.df.shape[1]} cột.\n")
        else:
            print(f"[LỖI!] Không tìm thấy file dữ liệu tại đường dẫn: '{self.input_path}'")
            print("Vui lòng kiểm tra lại xem file đã được đặt đúng thư mục chưa.")
            raise FileNotFoundError("Data file not found.")

    def filter_and_rename_columns(self):
        """Bước 1 & 2: Lọc dữ liệu cần thiết và chuẩn hóa tên cột"""
        columns_to_keep = [
            'CustomerID', 'Churn Label', 'Senior Citizen', 'Partner', 'Dependents', 
            'Internet Service', 'Online Security', 'Online Backup', 'Device Protection', 
            'Tech Support', 'Tenure Months', 'Contract', 'Payment Method', 
            'Paperless Billing', 'Monthly Charges', 'Total Charges'
        ]
        
        # Chỉ giữ các cột cần thiết
        self.df = self.df[columns_to_keep].copy()

        # Đổi tên cột
        rename_mapping = {
            'CustomerID': 'ID',
            'Churn Label': 'Churn',
            'Tenure Months': 'Tenure',
            'Senior Citizen': 'SeniorCitizen',
            'Internet Service': 'InternetService',
            'Online Security': 'OnlineSecurity',
            'Online Backup': 'OnlineBackup',
            'Device Protection': 'DeviceProtection',
            'Tech Support': 'TechSupport',
            'Payment Method': 'PaymentMethod',
            'Monthly Charges': 'MonthlyCharges',
            'Total Charges': 'TotalCharges',
            'Paperless Billing': 'PaperlessBilling'
        }
        self.df.rename(columns=rename_mapping, inplace=True)
        print(f"[HOÀN TẤT] Lọc và chuẩn hóa tên cột. Kích thước: {self.df.shape}")

    def clean_garbage_values(self):
        """Bước 3: Xử lý ký tự lạ thành NaN"""
        # Thay thế khoảng trắng bằng NaN
        self.df = self.df.replace(r'^\s*$', np.nan, regex=True)
        # Thay thế các chuỗi vô nghĩa bằng NaN
        list_garbage = ['?', '-', 'N/A', 'NA', 'null', 'None']
        self.df = self.df.replace(list_garbage, np.nan)
        print("[HOÀN TẤT] Làm sạch ký tự rác.")

    def encode_categorical_features(self):
        """Bước 4: Mã hóa các biến phân loại và nhị phân"""
        # Xử lý biến boolean
        binary_cols = [
            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
            'TechSupport', 'PaperlessBilling', 'Partner', 'SeniorCitizen'
        ]
        binary_mapping = {'yes': 1, 'no': 0, 'no internet service': 0}
        
        for col in binary_cols:
            if self.df[col].dtype == 'object':
                self.df[col] = self.df[col].str.strip().str.lower().map(binary_mapping).fillna(self.df[col])

        # Xử lý Contract
        contract_mapping = {'month-to-month': 1, 'one year': 12, 'two year': 24}
        if self.df['Contract'].dtype == 'object':
            self.df['Contract'] = self.df['Contract'].str.strip().str.lower().map(contract_mapping)

        # Xử lý Churn
        churn_mapping = {'yes': 1, 'no': 0}
        if self.df['Churn'].dtype == 'object':
            self.df['Churn'] = self.df['Churn'].str.strip().str.lower().map(churn_mapping)
            
        print("[HOÀN TẤT] Mã hóa các biến hạng mục.")

    def format_and_impute_missing(self):
        """Bước 5: Xử lý kiểu dữ liệu và điền khuyết thiếu"""
        # Chuyển TotalCharges sang float
        self.df['TotalCharges'] = pd.to_numeric(self.df['TotalCharges'], errors='coerce')
        
        # Báo cáo missing values (Tùy chọn hiển thị)
        # print("Số lượng NaN trước khi xử lý:\n", self.df.isnull().sum()[self.df.isnull().sum() > 0])

        # Xử lý: Khách hàng mới (Tenure = 0) chưa phát sinh cước nên TotalCharges bị NaN
        self.df['TotalCharges'] = self.df['TotalCharges'].fillna(0)
        print("[HOÀN TẤT] Xử lý dữ liệu khuyết thiếu và chuyển đổi kiểu dữ liệu.")

    def save_data(self):
        """Bước 6: Lưu file kết quả"""
        # Đảm bảo thư mục đích tồn tại
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        
        self.df.to_csv(self.output_path, index=False, encoding='utf-8-sig')
        print(f"[THÀNH CÔNG] Đã lưu dữ liệu xử lý vào: {self.output_path}")

    def run(self):
        """Hàm Pipeline chính (Orchestrator) tự động chạy toàn bộ quy trình"""
        print("="*50)
        print("🚀 BẮT ĐẦU CHẠY PIPELINE XỬ LÝ DỮ LIỆU")
        print("="*50)
        
        self.load_data()
        self.filter_and_rename_columns()
        self.clean_garbage_values()
        self.encode_categorical_features()
        self.format_and_impute_missing()
        self.save_data()
        
        print("="*50)
        print("✨ PIPELINE HOÀN TẤT!")
        print("="*50)

# ==============================================================================
# KHỞI CHẠY PIPELINE
# ==============================================================================
if __name__ == "__main__":
    # 1. Lấy vị trí của thư mục chứa file code hiện tại (thư mục 'src')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Lùi ra 1 thư mục cha (về thư mục Project)
    project_dir = os.path.dirname(current_dir)
    
    # 3. Nối đường dẫn an toàn bằng os.path.join
    INPUT_FILE = os.path.join(project_dir, "data", "raw", "data_raw.csv")
    OUTPUT_FILE = os.path.join(project_dir, "data", "processing", "data_processing.csv")
    
    # Khởi chạy
    pipeline = ChurnDataPipeline(input_path=INPUT_FILE, output_path=OUTPUT_FILE)
    pipeline.run()