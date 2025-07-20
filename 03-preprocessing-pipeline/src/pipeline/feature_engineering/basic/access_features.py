import pandas as pd
import numpy as np

class AccessFeatureEngineer():
    """מחלקה ליצירת תכונות גישה ונוכחות"""
    
    def create_access_features(self, df):
        """יצירת תכונות גישה ונוכחות"""
        df_processed = df.copy()
        
        # תכונות כניסות ויציאות
        df_processed['entry_exit_balance'] = df_processed['num_entries'] - df_processed['num_exits']
        df_processed['avg_presence_per_entry'] = df_processed['total_presence_minutes'] / np.maximum(df_processed['num_entries'], 1)
        df_processed['access_frequency'] = df_processed['num_entries'] + df_processed['num_exits']
        
        # תכונות זמן נוכחות
        df_processed['presence_intensity'] = df_processed['total_presence_minutes'] / (24 * 60)  # יחס מהיום
        df_processed['is_long_presence'] = (df_processed['total_presence_minutes'] > 12 * 60).astype(int)
        df_processed['is_short_presence'] = (df_processed['total_presence_minutes'] < 4 * 60).astype(int)
        
        # תכונות גישה חשודה
        df_processed['suspicious_access_score'] = (
            df_processed['entered_during_night_hours'] * 2 +
            df_processed['early_entry_flag'] * 1 +
            df_processed['late_exit_flag'] * 1 +
            df_processed['entry_during_weekend'] * 2
        )
        
        df_processed['has_suspicious_access'] = (df_processed['suspicious_access_score'] > 0).astype(int)
        
        # תכונות קטגוריות
        df_processed['access_pattern'] = pd.cut(
            df_processed['num_entries'],
            bins=[0, 1, 3, 10, np.inf],
            labels=['rare', 'occasional', 'regular', 'frequent']
        )
        
        print("Access features created successfully")
        return df_processed