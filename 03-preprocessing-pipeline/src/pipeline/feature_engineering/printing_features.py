import pandas as pd
import numpy as np
from .base_feature_engineer import BaseFeatureEngineer

class PrintingFeatureEngineer(BaseFeatureEngineer):
    """מחלקה ליצירת תכונות הדפסה"""
    
    def create_printing_features(self, df):
        """יצירת תכונות מקיפות להדפסה"""
        df_processed = df.copy()
        
        # יחסי הדפסה בסיסיים
        df_processed['avg_pages_per_print'] = df_processed['total_printed_pages'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['print_intensity'] = df_processed['num_print_commands'] / np.maximum(df_processed['total_presence_minutes'] / 60, 1)
        
        # תכונות הדפסה צבעונית
        df_processed['color_print_preference'] = df_processed['num_color_prints'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['bw_print_preference'] = df_processed['num_bw_prints'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['color_vs_bw_ratio'] = df_processed['num_color_prints'] / np.maximum(df_processed['num_bw_prints'], 1)
        
        # תכונות הדפסה מחוץ לשעות
        df_processed['off_hours_print_ratio'] = df_processed['num_print_commands_off_hours'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['off_hours_pages_ratio'] = df_processed['num_printed_pages_off_hours'] / np.maximum(df_processed['total_printed_pages'], 1)
        df_processed['off_hours_avg_pages'] = df_processed['num_printed_pages_off_hours'] / np.maximum(df_processed['num_print_commands_off_hours'], 1)
        
        # תכונות הדפסה מקמפוסים אחרים
        df_processed['prints_from_other_campus'] = (df_processed['printed_from_other'] > 0).astype(int)
        df_processed['print_mobility_score'] = df_processed['print_campuses'] / np.maximum(df_processed['num_unique_campus'], 1)
        
        # תכונות מתקדמות
        df_processed['is_heavy_printer'] = (df_processed['num_print_commands'] > df_processed['num_print_commands'].quantile(0.9)).astype(int)
        df_processed['is_high_volume_printer'] = (df_processed['total_printed_pages'] > df_processed['total_printed_pages'].quantile(0.9)).astype(int)
        df_processed['print_efficiency'] = df_processed['total_printed_pages'] / np.maximum(df_processed['work_duration_hours'], 1)
        
        # תכונות קטגוריות
        df_processed['print_activity_level'] = pd.cut(
            df_processed['num_print_commands'],
            bins=[0, 5, 20, 50, np.inf],
            labels=['low', 'medium', 'high', 'very_high']
        )
        
        print("Printing features created successfully")
        return df_processed