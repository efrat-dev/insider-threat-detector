import pandas as pd
import numpy as np
from .base_feature_engineer import BaseFeatureEngineer

class InteractionFeatureEngineer(BaseFeatureEngineer):
    """מחלקה ליצירת תכונות אינטראקציה מתקדמות"""
    
    def create_interaction_features(self, df):
        """יצירת תכונות אינטראקציה מתקדמות"""
        df_processed = df.copy()
        
        # יחסים בין פעילויות
        df_processed['print_to_burn_ratio'] = df_processed['num_print_commands'] / np.maximum(df_processed['num_burn_requests'], 1)
        df_processed['burn_to_print_ratio'] = df_processed['num_burn_requests'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['total_activity_score'] = df_processed['num_print_commands'] + df_processed['num_burn_requests']
        
        # אינטראקציות עם ותק
        df_processed['prints_per_seniority'] = df_processed['num_print_commands'] / np.maximum(df_processed['employee_seniority_years'], 1)
        df_processed['burns_per_seniority'] = df_processed['num_burn_requests'] / np.maximum(df_processed['employee_seniority_years'], 1)
        df_processed['activity_per_seniority'] = df_processed['total_activity_score'] / np.maximum(df_processed['employee_seniority_years'], 1)
        
        # אינטראקציות עם זמן נוכחות
        df_processed['prints_per_hour'] = df_processed['num_print_commands'] / np.maximum(df_processed['work_duration_hours'], 1)
        df_processed['burns_per_hour'] = df_processed['num_burn_requests'] / np.maximum(df_processed['work_duration_hours'], 1)
        df_processed['pages_per_hour'] = df_processed['total_printed_pages'] / np.maximum(df_processed['work_duration_hours'], 1)
        
        # אינטראקציות עם סיכון
        df_processed['risk_activity_interaction'] = df_processed['employment_risk_score'] * df_processed['total_activity_score']
        df_processed['risk_off_hours_interaction'] = df_processed['employment_risk_score'] * df_processed['off_hours_print_ratio']
        
        # אינטראקציות חשודות
        df_processed['suspicious_print_activity'] = (
            df_processed['off_hours_print_ratio'] * df_processed['color_print_preference'] * 
            df_processed['prints_from_other_campus']
        )
        
        df_processed['suspicious_burn_activity'] = (
            df_processed['off_hours_burn_ratio'] * df_processed['high_classification_burn'] * 
            df_processed['burns_from_other_campus']
        )
        
        print("Interaction features created successfully")
        return df_processed