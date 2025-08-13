import pandas as pd

class DataTypeConverter:
    """מחלקה להמרת טיפוסי נתונים"""
    
    @staticmethod
    def convert_data_types(df):
        """המרת טיפוסי נתונים - פונקציה סטטית שלא צריכה fit"""
        df_processed = df.copy()
        
        # המרת עמודות תאריך
        date_columns = ['date', 'first_entry_time', 'last_exit_time']
        for col in date_columns:
            if col in df_processed.columns:
                try:
                    df_processed[col] = pd.to_datetime(df_processed[col], errors='coerce')
                except:
                    print(f"Could not convert {col} to datetime")
        
        # המרת עמודות בוליאניות
        boolean_columns = ['is_contractor', 'has_foreign_citizenship', 'has_criminal_record', 
                          'has_medical_history', 'is_malicious', 'is_emp_malicios', 'is_abroad', 'is_hostile_country_trip',
                          'is_official_trip', 'entered_during_night_hours', 'early_entry_flag',
                          'late_exit_flag', 'entry_during_weekend']
        
        for col in boolean_columns:
            if col in df_processed.columns:
                df_processed[col] = df_processed[col].astype(bool)
        
        # המרת עמודות קטגוריות
        categorical_columns = ['employee_department', 'employee_campus', 'employee_position', 
                             'employee_classification', 'employee_origin_country', 'country_name']
        
        for col in categorical_columns:
            if col in df_processed.columns:
                df_processed[col] = df_processed[col].astype('category')
        
        return df_processed