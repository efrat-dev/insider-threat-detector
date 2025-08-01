import pandas as pd
import numpy as np

class DataCleaner:
    """מחלקה לניקוי נתונים"""
    
    def __init__(self):
        # פרמטרים שנשמרים מהטריין
        self.fitted_params = {}
        self.is_fitted = False
    
    def fit_handle_missing_values(self, df):
        """אימון פרמטרי הטיפול בערכים חסרים על נתוני הטריין"""
        print("Fitting missing values handling parameters...")
        
        # שמירת פרמטרים לטיפול בערכים חסרים
        self.fitted_params['missing_values'] = {}
        
        # עמודות עם ערכים חסרים רבים (לפי הנתונים שלך)
        travel_columns = ['trip_day_number', 'country_name']
        time_columns = ['first_entry_time', 'last_exit_time']
        derived_time_columns = ['entry_time_numeric', 'exit_time_numeric', 
                               'entry_time_numeric_zscore', 'exit_time_numeric_zscore']
        
        # שמירת פרמטרים לעמודות נסיעות
        for col in travel_columns:
            if col in df.columns:
                if col == 'trip_day_number':
                    self.fitted_params['missing_values'][col] = {'method': 'fill_zero', 'value': 0}
                elif col == 'country_name':
                    self.fitted_params['missing_values'][col] = {'method': 'fill_constant', 'value': 'No_Travel'}
        
        # שמירת פרמטרים לעמודות זמן - מילוי עם ערכים שמתאימים לטיפוס
        for col in time_columns:
            if col in df.columns:
                # עבור datetime columns - נמלא עם תאריך default או NaT
                self.fitted_params['missing_values'][col] = {'method': 'fill_datetime', 'value': pd.NaT}
        
        # שמירת פרמטרים לעמודות זמן נגזרות (שייווצרו בהמשך)
        for col in derived_time_columns:
            # עבור עמודות נומריות שנגזרות מזמן - נמלא עם 0 או median
            self.fitted_params['missing_values'][col] = {'method': 'fill_zero', 'value': 0}
        
        # התמודדות עם total_presence_minutes
        if 'total_presence_minutes' in df.columns:
            self.fitted_params['missing_values']['total_presence_minutes'] = {'method': 'fill_zero', 'value': 0}
        
        # חישוב פרמטרים לעמודות נומריות אחרות
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if (col not in self.fitted_params['missing_values'] and 
                df[col].isnull().sum() > 0 and 
                col not in ['employee_id', 'is_malicious', 'target']):
                
                median_val = df[col].median()
                self.fitted_params['missing_values'][col] = {'method': 'fill_median', 'value': median_val}
        
        # חישוב פרמטרים לעמודות קטגוריות
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_columns:
            if (col not in self.fitted_params['missing_values'] and 
                df[col].isnull().sum() > 0):
                
                mode_val = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
                self.fitted_params['missing_values'][col] = {'method': 'fill_mode', 'value': mode_val}
        
        self.is_fitted = True
        print(f"Missing values parameters fitted for {len(self.fitted_params['missing_values'])} columns")
        
        # החזרת הדאטה לאחר הטיפול
        return self.transform_handle_missing_values(df)
    
    def transform_handle_missing_values(self, df):
        """החלת פרמטרי הטיפול בערכים חסרים על דאטה חדש"""
        if not self.is_fitted:
            raise ValueError("DataCleaner must be fitted before transform")
        
        print("Transforming missing values using fitted parameters...")
        df_processed = df.copy()
        
        # החלת הפרמטרים השמורים
        for col, params in self.fitted_params['missing_values'].items():
            if col in df_processed.columns and df_processed[col].isnull().sum() > 0:
                method = params['method']
                value = params['value']
                
                if method == 'fill_zero':
                    df_processed[col] = df_processed[col].fillna(0)
                elif method == 'fill_constant':
                    df_processed[col] = df_processed[col].fillna(value)
                elif method == 'fill_median':
                    df_processed[col] = df_processed[col].fillna(value)
                elif method == 'fill_mode':
                    df_processed[col] = df_processed[col].fillna(value)
                elif method == 'fill_datetime':
                    # עבור datetime columns - אפשר למלא עם תאריך ברירת מחדל או להשאיר NaT
                    # או להמיר לזמן "לא קיים" כמו 1900-01-01
                    default_date = pd.Timestamp('1900-01-01')  # תאריך שמייצג "לא קיים"
                    df_processed[col] = df_processed[col].fillna(default_date)
        
        print("Missing values transformed successfully")
        return df_processed
    
    def handle_missing_after_feature_engineering(self, df):
        """טיפול נוסף בערכים חסרים אחרי יצירת פיצ'רים"""
        print("Handling missing values after feature engineering...")
        df_processed = df.copy()
        
        # טיפול בעמודות שנוצרו במהלך feature engineering
        derived_numeric_cols = [col for col in df_processed.columns 
                               if any(suffix in col for suffix in ['_zscore', '_numeric', '_freq', '_binary'])]
        
        for col in derived_numeric_cols:
            if df_processed[col].isnull().sum() > 0:
                print(f"  Filling {col} with 0 (derived feature)")
                df_processed[col] = df_processed[col].fillna(0)
        
        # טיפול בעמודות זמן שנוצרו
        time_numeric_cols = [col for col in df_processed.columns 
                           if 'time_numeric' in col]
        
        for col in time_numeric_cols:
            if df_processed[col].isnull().sum() > 0:
                print(f"  Filling {col} with 0 (time feature)")
                df_processed[col] = df_processed[col].fillna(0)
        
        print("Post-feature-engineering missing values handled")
        return df_processed
    
    def fit_handle_outliers(self, df, method='cap', threshold=0.05):
        """אימון פרמטרי הטיפול בחריגים על נתוני הטריין"""
        print(f"Fitting outliers handling parameters with method: {method}...")
        
        if 'outliers' not in self.fitted_params:
            self.fitted_params['outliers'] = {}
        
        self.fitted_params['outliers']['method'] = method
        self.fitted_params['outliers']['bounds'] = {}
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if col in ['employee_id', 'is_malicious', 'is_emp_malicios', 'target']:  # לא לטפל בעמודות מזהות ותווית
                continue
            
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            self.fitted_params['outliers']['bounds'][col] = {
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
        
        print(f"Outliers parameters fitted for {len(self.fitted_params['outliers']['bounds'])} columns")
        return df  # בפיט רק שומרים פרמטרים, לא מבצעים שינויים
    
    def transform_handle_outliers(self, df):
        """החלת פרמטרי הטיפול בחריגים על דאטה חדש"""
        if not self.is_fitted or 'outliers' not in self.fitted_params:
            print("Warning: Outliers parameters not fitted, skipping outliers handling")
            return df

        print("Transforming outliers using fitted parameters...")
        df_processed = df.copy()
        method = self.fitted_params['outliers']['method']
        exclude_cols = {'first_entry_time', 'last_exit_time', 'date'}

        for col, bounds in self.fitted_params['outliers']['bounds'].items():
            if col in df_processed.columns and col not in exclude_cols:
                lower_bound = bounds['lower_bound']
                upper_bound = bounds['upper_bound']

                if method == 'cap':
                    df_processed[col] = np.where(df_processed[col] < lower_bound, lower_bound, df_processed[col])
                    df_processed[col] = np.where(df_processed[col] > upper_bound, upper_bound, df_processed[col])
                elif method == 'remove':
                    # בטרנספורם לא מוחקים שורות, רק מסמנים או מחליפים
                    df_processed[col] = np.where(
                        (df_processed[col] < lower_bound) | (df_processed[col] > upper_bound),
                        np.nan, df_processed[col]
                    )

        print(f"Outliers transformed using {method} method")
        return df_processed
    
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
        
        print("Data types converted successfully")
        return df_processed