import pandas as pd
import numpy as np

class DataCleaner:
    """מחלקה לניקוי נתונים"""
    
    @staticmethod
    def handle_missing_values(df):
        """טיפול בערכים חסרים"""
        df_processed = df.copy()
        
        # עמודות עם ערכים חסרים רבים (לפי הנתונים שלך)
        travel_columns = ['trip_day_number', 'country_name']
        time_columns = ['first_entry_time', 'last_exit_time']
        
        # טיפול בעמודות נסיעות
        for col in travel_columns:
            if col in df_processed.columns:
                if col == 'trip_day_number':
                    df_processed[col] = df_processed[col].fillna(0)
                elif col == 'country_name':
                    df_processed[col] = df_processed[col].fillna('No_Travel')
        
        # טיפול בעמודות זמן
        for col in time_columns:
            if col in df_processed.columns:
                df_processed[col] = df_processed[col].fillna('No_Entry_Exit')
        
        # טיפול בערכים חסרים נוספים
        numeric_columns = df_processed.select_dtypes(include=[np.number]).columns
        categorical_columns = df_processed.select_dtypes(include=['object']).columns
        
        for col in numeric_columns:
            if df_processed[col].isnull().sum() > 0:
                median_val = df_processed[col].median()
                df_processed[col] = df_processed[col].fillna(median_val)
        
        for col in categorical_columns:
            if df_processed[col].isnull().sum() > 0:
                mode_val = df_processed[col].mode()[0] if not df_processed[col].mode().empty else 'Unknown'
                df_processed[col] = df_processed[col].fillna(mode_val)
        
        print("Missing values handled successfully")
        return df_processed
    
    @staticmethod
    def handle_outliers(df, method='cap', threshold=0.05):
        """טיפול בחריגים"""
        df_processed = df.copy()
        numeric_columns = df_processed.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if col in ['employee_id', 'is_malicious', 'is_emp_malicios']:  # לא לטפל בעמודות מזהות ותווית
                continue
                
            if method == 'cap':
                Q1 = df_processed[col].quantile(0.25)
                Q3 = df_processed[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                df_processed[col] = np.where(df_processed[col] < lower_bound, lower_bound, df_processed[col])
                df_processed[col] = np.where(df_processed[col] > upper_bound, upper_bound, df_processed[col])
            
            elif method == 'remove':
                Q1 = df_processed[col].quantile(0.25)
                Q3 = df_processed[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                df_processed = df_processed[(df_processed[col] >= lower_bound) & (df_processed[col] <= upper_bound)]
        
        print(f"Outliers handled using {method} method")
        return df_processed
    
    @staticmethod
    def convert_data_types(df):
        """המרת טיפוסי נתונים"""
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
        
        print("Data types converted successfully")
        return df_processed
    