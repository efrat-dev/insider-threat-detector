import pandas as pd
import numpy as np

class FeatureCreator:
    """מחלקה ליצירת תכונות חדשות מהנתונים הקיימים"""
    
    def __init__(self):
        pass
    
    def create_media_features(self, df):
        """יצירת תכונות שריפה חיוניות בלבד"""
        df_processed = df.copy()
        
        df_processed['avg_burn_volume_per_request'] = df_processed['total_burn_volume_mb'] / np.maximum(df_processed['num_burn_requests'], 1)
        df_processed['burn_intensity'] = df_processed['num_burn_requests'] / np.maximum(df_processed['total_presence_minutes'] / 60, 1)
        
        df_processed['high_classification_burn'] = (df_processed['max_request_classification'] >= 4).astype(int)
        df_processed['classification_variance'] = df_processed['max_request_classification'] / np.maximum(df_processed['avg_request_classification'], 1)
        
        df_processed['off_hours_burn_ratio'] = df_processed['num_burn_requests_off_hours'] / np.maximum(df_processed['num_burn_requests'], 1)
        
        df_processed['is_heavy_burner'] = (df_processed['num_burn_requests'] > df_processed['num_burn_requests'].quantile(0.8)).astype(int)
        
        df_processed['avg_pages_per_print'] = df_processed['total_printed_pages'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['print_intensity'] = df_processed['num_print_commands'] / np.maximum(df_processed['total_presence_minutes'] / 60, 1)
        
        df_processed['off_hours_ratio'] = df_processed['num_print_commands_off_hours'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['is_heavy_printer'] = (df_processed['num_print_commands'] > df_processed['num_print_commands'].quantile(0.8)).astype(int)

        print("Essential burning features created successfully")
        return df_processed
        
    def create_temporal_features(self, df):
        """יצירת תכונות זמן ונוכחות"""

        df_processed = df.copy()
        
        df_processed['date'] = pd.to_datetime(df_processed['date'], errors='coerce')
        df_processed['weekday'] = df_processed['date'].dt.weekday
        df_processed['month'] = df_processed['date'].dt.month
        df_processed['quarter'] = df_processed['date'].dt.quarter

        df_processed['is_end_of_month'] = (df_processed['date'].dt.day >= 25).astype(int)
        df_processed['is_quarter_end'] = df_processed['month'].isin([3, 6, 9, 12]).astype(int)

        df_processed['season'] = df_processed['month'].map({
            12: 'winter', 1: 'winter', 2: 'winter',
            3: 'spring', 4: 'spring', 5: 'spring',
            6: 'summer', 7: 'summer', 8: 'summer',
            9: 'autumn', 10: 'autumn', 11: 'autumn'
        })
        df_processed['first_entry_time'] = pd.to_datetime(df_processed.get('first_entry_time'), errors='coerce')
        df_processed['entry_hour'] = df_processed['first_entry_time'].dt.hour
        df_processed['entry_minute'] = df_processed['first_entry_time'].dt.minute
        df_processed['entry_time_numeric'] = df_processed['entry_hour'] + df_processed['entry_minute'] / 60

        df_processed['last_exit_time'] = pd.to_datetime(df_processed.get('last_exit_time'), errors='coerce')
        df_processed['exit_hour'] = df_processed['last_exit_time'].dt.hour
        df_processed['exit_minute'] = df_processed['last_exit_time'].dt.minute
        df_processed['exit_time_numeric'] = df_processed['exit_hour'] + df_processed['exit_minute'] / 60

        drop_cols = ['entry_hour', 'entry_minute', 'exit_hour', 'exit_minute']

        df_processed = df_processed.drop(columns=[col for col in drop_cols if col in df_processed.columns])

        return df_processed
    
    def create_employee_features(self, df):
        """יצירת תכונות עובד חיוניות בלבד"""
        df_processed = df.copy()
        
        country_name_str = df_processed['country_name'].astype(str) if 'country_name' in df_processed.columns else None
        employee_origin_str = df_processed['employee_origin_country'].astype(str) if 'employee_origin_country' in df_processed.columns else None
        
        # בדיקה אם העובד עובד במדינת המוצא שלו
        if country_name_str is not None and employee_origin_str is not None:
            df_processed['is_employee_in_origin_country'] = (
                country_name_str == employee_origin_str
            ).astype(int)

        df_processed['is_new_employee'] = (df_processed['employee_seniority_years'] < 1).astype(int)
        df_processed['is_veteran_employee'] = (df_processed['employee_seniority_years'] > 10).astype(int)
        
        return df_processed
        
    def create_all_features(self, df):
        """יצירת כל התכונות החדשות"""
        print("Starting comprehensive feature creation...")
        
        df_processed = df.copy()
        df_processed = self.create_temporal_features(df_processed)
        df_processed = self.create_media_features(df_processed)
        df_processed = self.create_employee_features(df_processed)

        return df_processed