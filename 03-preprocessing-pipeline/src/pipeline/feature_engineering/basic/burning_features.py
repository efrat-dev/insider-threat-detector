import pandas as pd
import numpy as np

class BurningFeatureEngineer():
    """מחלקה ליצירת תכונות שריפה"""
    
    def create_burning_features(self, df):
        """יצירת תכונות מקיפות לשריפה"""
        df_processed = df.copy()
        
        # יחסי שריפה בסיסיים
        df_processed['avg_burn_volume_per_request'] = df_processed['total_burn_volume_mb'] / np.maximum(df_processed['num_burn_requests'], 1)
        df_processed['avg_files_per_burn'] = df_processed['total_files_burned'] / np.maximum(df_processed['num_burn_requests'], 1)
        df_processed['avg_file_size_mb'] = df_processed['total_burn_volume_mb'] / np.maximum(df_processed['total_files_burned'], 1)
        
        # תכונות שריפה מחוץ לשעות
        df_processed['off_hours_burn_ratio'] = df_processed['num_burn_requests_off_hours'] / np.maximum(df_processed['num_burn_requests'], 1)
        df_processed['burn_intensity'] = df_processed['num_burn_requests'] / np.maximum(df_processed['total_presence_minutes'] / 60, 1)
        
        # תכונות סיווג ביטחוני
        df_processed['high_classification_burn'] = (df_processed['max_request_classification'] >= 4).astype(int)
        df_processed['classification_consistency'] = df_processed['max_request_classification'] - df_processed['avg_request_classification']
        df_processed['classification_variance'] = df_processed['max_request_classification'] / np.maximum(df_processed['avg_request_classification'], 1)
        
        # תכונות מיקום שריפה
        df_processed['burns_from_other_campus'] = (df_processed['burned_from_other'] > 0).astype(int)
        df_processed['burn_mobility_score'] = df_processed['burn_campuses'] / np.maximum(df_processed['num_unique_campus'], 1)
        
        # תכונות מתקדמות
        df_processed['is_heavy_burner'] = (df_processed['num_burn_requests'] > df_processed['num_burn_requests'].quantile(0.9)).astype(int)
        df_processed['is_high_volume_burner'] = (df_processed['total_burn_volume_mb'] > df_processed['total_burn_volume_mb'].quantile(0.9)).astype(int)
        df_processed['burn_efficiency'] = df_processed['total_burn_volume_mb'] / np.maximum(df_processed['work_duration_hours'], 1)
        
        # תכונות קטגוריות
        df_processed['burn_activity_level'] = pd.cut(
            df_processed['num_burn_requests'],
            bins=[0, 1, 5, 15, np.inf],
            labels=['none', 'low', 'medium', 'high']
        )
        
        df_processed['burn_volume_category'] = pd.cut(
            df_processed['total_burn_volume_mb'],
            bins=[0, 100, 1000, 10000, np.inf],
            labels=['small', 'medium', 'large', 'huge']
        )
        
        print("Burning features created successfully")
        return df_processed