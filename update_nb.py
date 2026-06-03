import json

file_path = r"d:\FPTU_Study\SU2026\ADY201m\Project_ADY201m_GR01_AI2009_H1\notebooks\01_EDA_and_Feature_Engineering.ipynb"

with open(file_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

old_dict = """academic_names = {
    'Contract': 'Contract Type',
    'PaymentMethod': 'Payment Method',
    'InternetService': 'Internet Service Provider'
}"""

new_dict = """custom_names = {
    # Nhóm biến sinh ra từ One-Hot Encoding
    'Dependents_Yes': 'Dependents: Yes',
    'PaymentMethod_Credit card (automatic)': 'Payment Method: Credit Card (Auto)',
    'PaymentMethod_Electronic check': 'Payment Method: Electronic Check',
    'PaymentMethod_Mailed check': 'Payment Method: Mailed Check',
    'InternetService_Fiber optic': 'Internet Service: Fiber Optic',
    'InternetService_No': 'Internet Service: None',
    'tenure_group_13-24 months': 'Tenure Group: 13-24 Months',
    'tenure_group_25-36 months': 'Tenure Group: 25-36 Months',
    'tenure_group_37-48 months': 'Tenure Group: 37-48 Months',
    'tenure_group_49-60 months': 'Tenure Group: 49-60 Months',
    'tenure_group_61-72 months': 'Tenure Group: 61-72 Months',
    
    # Nhóm biến số / Nhị phân giữ nguyên (Remainder)
    'SeniorCitizen': 'Senior Citizen Status',
    'Partner': 'Partner Status',
    'Tenure': 'Tenure (Months)',
    'Contract': 'Contract Type',
    'PaperlessBilling': 'Paperless Billing',
    'MonthlyCharges': 'Monthly Charges',
    'TotalCharges': 'Total Charges',
    'OnlineSecurity': 'Online Security Opt-in',
    'OnlineBackup': 'Online Backup Opt-in',
    'DeviceProtection': 'Device Protection Opt-in',
    'TechSupport': 'Technical Support Opt-in',
    
    # Nhóm Feature Engineering do Bảo tạo
    'service_diversity': 'Service Diversity Score',
    'monthly_charges_ratio': 'Monthly Charges Ratio',
    'is_paperless_electronic': 'Paperless & Auto-Payment Combo'
}"""

for cell in nb.get("cells", []):
    if cell.get("cell_type") == "code":
        src = "".join(cell.get("source", []))
        
        # Replace the old dict
        if "academic_names = {" in src:
            src = src.replace(old_dict, new_dict)
            
        # Replace variable usages
        src = src.replace("academic_names", "custom_names")
        
        # Replace {col} with {custom_names.get(col, col)} in f-strings
        src = src.replace("{col}", "{custom_names.get(col, col)}")
        
        # Replace plt.xlabel(col...
        src = src.replace("plt.xlabel(col", "plt.xlabel(custom_names.get(col, col)")
        
        # Convert back to list of strings
        if isinstance(cell.get("source"), list):
            cell["source"] = [line + ("\n" if not line.endswith("\n") and i < len(src.split("\n"))-1 else "") for i, line in enumerate(src.split("\n"))]
            # remove trailing empty strings if split added them incorrectly, better to use splitlines
            # Wait, splitlines(True) keeps \n
            cell["source"] = src.splitlines(True)
        else:
            cell["source"] = src

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated successfully.")
