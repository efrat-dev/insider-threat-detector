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
    def detect_outliers(df, columns=None):
        """זיהוי חריגים באמצעות IQR"""
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        outliers_info = {}
        
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outliers_info[col] = {
                'count': len(outliers),
                'percentage': (len(outliers) / len(df)) * 100,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
        
        return outliers_info
    
    @staticmethod
    def handle_outliers(df, method='cap', threshold=0.05):
        """טיפול בחריגים"""
        df_processed = df.copy()
        numeric_columns = df_processed.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if col in ['employee_id', 'is_malicious']:  # לא לטפל בעמודות מזהות ותווית
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
                          'has_medical_history', 'is_malicious', 'is_abroad', 'is_hostile_country_trip',
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
    
    @staticmethod
    def remove_columns(df, columns_to_remove=None):
        """הסרת עמודות מהנתונים"""
        if columns_to_remove is None:
            columns_to_remove = ['employee_origin_country', 'country_name', 'first_entry_time', 'last_exit_time']
        
        df_processed = df.copy()
        existing_columns = [col for col in columns_to_remove if col in df_processed.columns]
        
        if existing_columns:
            df_processed = df_processed.drop(columns=existing_columns)
            print(f"Removed columns: {existing_columns}")
        else:
            print("No specified columns found to remove")
        
        return df_processed

    @staticmethod
    def consistency_checks(df):
        """בדיקות עקביות"""
        issues = []
        
        # בדיקת ערכים שליליים בעמודות שאמורות להיות חיוביות
        positive_columns = ['num_print_commands', 'total_printed_pages', 'num_burn_requests', 
                          'total_burn_volume_mb', 'employee_seniority_years']
        
        for col in positive_columns:
            if col in df.columns:
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    issues.append(f"{col}: {negative_count} negative values")
        
        # בדיקת יחסים לוגיים
        if 'num_print_commands' in df.columns and 'total_printed_pages' in df.columns:
            illogical = (df['num_print_commands'] > 0) & (df['total_printed_pages'] == 0)
            if illogical.sum() > 0:
                issues.append(f"Print commands without pages: {illogical.sum()} cases")
        
        # בדיקת תאריכים
        if 'first_entry_time' in df.columns and 'last_exit_time' in df.columns:
            invalid_times = df['first_entry_time'] > df['last_exit_time']
            if invalid_times.sum() > 0:
                issues.append(f"Entry time after exit time: {invalid_times.sum()} cases")
        
        if issues:
            print("Data consistency issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("No data consistency issues found")
        
        return issues