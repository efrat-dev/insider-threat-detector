import pandas as pd
import numpy as np

class TimeFeatureEngineer():
    """מחלקה לחילוץ תכונות זמן"""
    
    def extract_time_features(self, df):
        """חילוץ תכונות זמן מקיפות"""
        df_processed = df.copy()
        
        # המרת עמודת התאריך
        df_processed['date'] = pd.to_datetime(df_processed['date'])
        
        # תכונות זמן בסיסיות
        df_processed['year'] = df_processed['date'].dt.year
        df_processed['month'] = df_processed['date'].dt.month
        df_processed['day'] = df_processed['date'].dt.day
        df_processed['weekday'] = df_processed['date'].dt.weekday
        df_processed['quarter'] = df_processed['date'].dt.quarter
        df_processed['day_of_year'] = df_processed['date'].dt.dayofyear
        df_processed['week_of_year'] = df_processed['date'].dt.isocalendar().week
        
        # תכונות זמן מתקדמות
        df_processed['is_weekend'] = df_processed['weekday'].isin([5, 6]).astype(int)
        df_processed['is_monday'] = (df_processed['weekday'] == 0).astype(int)
        df_processed['is_friday'] = (df_processed['weekday'] == 4).astype(int)
        df_processed['is_beginning_of_month'] = (df_processed['day'] <= 5).astype(int)
        df_processed['is_end_of_month'] = (df_processed['day'] >= 25).astype(int)
        df_processed['is_quarter_end'] = df_processed['month'].isin([3, 6, 9, 12]).astype(int)
        
        # תכונות עונתיות
        df_processed['season'] = df_processed['month'].map({
            12: 'winter', 1: 'winter', 2: 'winter',
            3: 'spring', 4: 'spring', 5: 'spring',
            6: 'summer', 7: 'summer', 8: 'summer',
            9: 'autumn', 10: 'autumn', 11: 'autumn'
        })
        
        # עיבוד זמני כניסה ויציאה
        df_processed = self._process_entry_exit_times(df_processed)
        
        print("Time features extracted successfully")
        return df_processed
    
    def _process_entry_exit_times(self, df):
        """עיבוד זמני כניסה ויציאה"""
        df_processed = df.copy()
        
        # עיבוד זמן כניסה
        if 'first_entry_time' in df_processed.columns:
            df_processed['first_entry_time'] = pd.to_datetime(df_processed['first_entry_time'], errors='coerce')
            df_processed['entry_hour'] = df_processed['first_entry_time'].dt.hour
            df_processed['entry_minute'] = df_processed['first_entry_time'].dt.minute
            df_processed['entry_time_numeric'] = df_processed['entry_hour'] + df_processed['entry_minute']/60
            
            # תכונות שעות כניסה
            df_processed['is_very_early_entry'] = (df_processed['entry_hour'] < 6).astype(int)
            df_processed['is_early_entry'] = (df_processed['entry_hour'] < 8).astype(int)
            df_processed['is_late_entry'] = (df_processed['entry_hour'] > 10).astype(int)
            df_processed['is_lunch_entry'] = df_processed['entry_hour'].between(12, 14).astype(int)
            df_processed['is_night_entry'] = (df_processed['entry_hour'] >= 20).astype(int)
        
        # עיבוד זמן יציאה
        if 'last_exit_time' in df_processed.columns:
            df_processed['last_exit_time'] = pd.to_datetime(df_processed['last_exit_time'], errors='coerce')
            df_processed['exit_hour'] = df_processed['last_exit_time'].dt.hour
            df_processed['exit_minute'] = df_processed['last_exit_time'].dt.minute
            df_processed['exit_time_numeric'] = df_processed['exit_hour'] + df_processed['exit_minute']/60
            
            # תכונות שעות יציאה
            df_processed['is_early_exit'] = (df_processed['exit_hour'] < 16).astype(int)
            df_processed['is_late_exit'] = (df_processed['exit_hour'] > 19).astype(int)
            df_processed['is_very_late_exit'] = (df_processed['exit_hour'] > 22).astype(int)
            df_processed['is_night_exit'] = (df_processed['exit_hour'] >= 23).astype(int)
            
            # זמן עבודה
            df_processed['work_duration_hours'] = df_processed['total_presence_minutes'] / 60
            df_processed['work_duration_category'] = pd.cut(
                df_processed['work_duration_hours'],
                bins=[0, 4, 8, 12, 24],
                labels=['short', 'normal', 'long', 'very_long']
            )
        
        return df_processed