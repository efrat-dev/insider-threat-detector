# feature_creator.py - Feature Creation Module
import pandas as pd
import numpy as np


class FeatureCreator:
    """מחלקה ליצירת תכונות חדשות מהנתונים הקיימים"""
    
    def __init__(self):
        pass
    
    def create_burning_features(self, df):
        """יצירת תכונות מקיפות לשריפה"""
        df_processed = df.copy()
        
        # יחסי שריפה בסיסיים
        # df_processed['avg_burn_volume_per_request'] = df_processed['total_burn_volume_mb'] / np.maximum(df_processed['num_burn_requests'], 1)
        # df_processed['avg_files_per_burn'] = df_processed['total_files_burned'] / np.maximum(df_processed['num_burn_requests'], 1)
        # df_processed['avg_file_size_mb'] = df_processed['total_burn_volume_mb'] / np.maximum(df_processed['total_files_burned'], 1)
        
        # # תכונות שריפה מחוץ לשעות
        # df_processed['off_hours_burn_ratio'] = df_processed['num_burn_requests_off_hours'] / np.maximum(df_processed['num_burn_requests'], 1)
        # df_processed['burn_intensity'] = df_processed['num_burn_requests'] / np.maximum(df_processed['total_presence_minutes'] / 60, 1)
        
        # # תכונות סיווג ביטחוני
        # df_processed['high_classification_burn'] = (df_processed['max_request_classification'] >= 4).astype(int)
        # df_processed['classification_consistency'] = df_processed['max_request_classification'] - df_processed['avg_request_classification']
        # df_processed['classification_variance'] = df_processed['max_request_classification'] / np.maximum(df_processed['avg_request_classification'], 1)
        
        # # תכונות מיקום שריפה
        # df_processed['burns_from_other_campus'] = (df_processed['burned_from_other'] > 0).astype(int)
        # df_processed['burn_mobility_score'] = df_processed['burn_campuses'] / np.maximum(df_processed['num_unique_campus'], 1)
        
        # # תכונות מתקדמות
        # df_processed['is_heavy_burner'] = (df_processed['num_burn_requests'] > df_processed['num_burn_requests'].quantile(0.9)).astype(int)
        # df_processed['is_high_volume_burner'] = (df_processed['total_burn_volume_mb'] > df_processed['total_burn_volume_mb'].quantile(0.9)).astype(int)
        # df_processed['burn_efficiency'] = df_processed['total_burn_volume_mb'] / np.maximum(df_processed['work_duration_hours'], 1)
        
        # # תכונות קטגוריות
        # df_processed['burn_activity_level'] = pd.cut(
        #     df_processed['num_burn_requests'],
        #     bins=[0, 1, 5, 15, np.inf],
        #     labels=['none', 'low', 'medium', 'high']
        # )
        
        # df_processed['burn_volume_category'] = pd.cut(
        #     df_processed['total_burn_volume_mb'],
        #     bins=[0, 100, 1000, 10000, np.inf],
        #     labels=['small', 'medium', 'large', 'huge']
        # )
        df_processed['training'] = 5
        
        print("Burning features created successfully")
        return df_processed
    
    # def create_temporal_features(self, df):
    #     """יצירת תכונות זמן ונוכחות"""
    #     df_processed = df.copy()
        
    #     # תכונות זמן עבודה
    #     if 'work_duration_hours' in df_processed.columns and 'total_presence_minutes' in df_processed.columns:
    #         df_processed['work_intensity'] = df_processed['total_presence_minutes'] / np.maximum(df_processed['work_duration_hours'] * 60, 1)
    #         df_processed['is_long_worker'] = (df_processed['work_duration_hours'] > df_processed['work_duration_hours'].quantile(0.8)).astype(int)
    #         df_processed['presence_efficiency'] = df_processed['total_presence_minutes'] / np.maximum(df_processed['work_duration_hours'] * 60, 1)
        
    #     # תכונות פעילות לפי זמן
    #     if 'num_entries' in df_processed.columns:
    #         df_processed['avg_session_duration'] = df_processed['total_presence_minutes'] / np.maximum(df_processed['num_entries'], 1)
    #         df_processed['entry_frequency'] = df_processed['num_entries'] / np.maximum(df_processed['work_duration_hours'], 1)
        
    #     print("Temporal features created successfully")
    #     return df_processed
    
    # def create_behavioral_features(self, df):
    #     """יצירת תכונות התנהגותיות"""
    #     df_processed = df.copy()
        
    #     # תכונות מיקום והתנהגות
    #     if 'num_unique_campus' in df_processed.columns:
    #         df_processed['is_multi_campus_user'] = (df_processed['num_unique_campus'] > 1).astype(int)
    #         df_processed['campus_diversity'] = df_processed['num_unique_campus'] / np.maximum(df_processed['num_entries'], 1)
        
    #     # תכונות פעילות כללית
    #     if 'total_presence_minutes' in df_processed.columns and 'num_entries' in df_processed.columns:
    #         df_processed['activity_consistency'] = df_processed['total_presence_minutes'] / np.maximum(df_processed['num_entries'] * df_processed['work_duration_hours'], 1)
    #         df_processed['is_frequent_user'] = (df_processed['num_entries'] > df_processed['num_entries'].quantile(0.75)).astype(int)
        
    #     print("Behavioral features created successfully")
    #     return df_processed
    
    # def create_security_features(self, df):
    #     """יצירת תכונות ביטחוניות"""
    #     df_processed = df.copy()
        
    #     # תכונות ביטחון מתקדמות
    #     if 'max_request_classification' in df_processed.columns:
    #         df_processed['security_risk_score'] = (
    #             df_processed['max_request_classification'] * 0.4 +
    #             df_processed.get('num_burn_requests', 0) * 0.3 +
    #             df_processed.get('total_burn_volume_mb', 0) / 1000 * 0.3
    #         )
            
    #         df_processed['is_high_security_risk'] = (
    #             df_processed['security_risk_score'] > df_processed['security_risk_score'].quantile(0.9)
    #         ).astype(int)
        
    #     # תכונות חשד כללי
    #     suspicious_indicators = []
    #     if 'off_hours_burn_ratio' in df_processed.columns:
    #         suspicious_indicators.append(df_processed['off_hours_burn_ratio'] > 0.5)
    #     if 'burns_from_other_campus' in df_processed.columns:
    #         suspicious_indicators.append(df_processed['burns_from_other_campus'] == 1)
    #     if 'is_heavy_burner' in df_processed.columns:
    #         suspicious_indicators.append(df_processed['is_heavy_burner'] == 1)
        
    #     if suspicious_indicators:
    #         df_processed['suspicious_behavior_count'] = sum(suspicious_indicators)
    #         df_processed['is_suspicious'] = (df_processed['suspicious_behavior_count'] >= 2).astype(int)
        
    #     print("Security features created successfully")
    #     return df_processed
    
    # def create_statistical_features(self, df):
    #     """יצירת תכונות סטטיסטיות מתקדמות"""
    #     df_processed = df.copy()
        
    #     # תכונות התפלגות
    #     numeric_cols = df_processed.select_dtypes(include=[np.number]).columns
        
    #     for col in numeric_cols:
    #         if col not in ['target', 'is_malicious', 'is_emp_malicious'] and df_processed[col].std() > 0:
    #             # נורמליזציה
    #             df_processed[f'{col}_normalized'] = (df_processed[col] - df_processed[col].mean()) / df_processed[col].std()
                
    #             # בינינג לקטגוריות
    #             df_processed[f'{col}_quartile'] = pd.qcut(df_processed[col], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'], duplicates='drop')
                
    #             # זיהוי חריגים
    #             Q1 = df_processed[col].quantile(0.25)
    #             Q3 = df_processed[col].quantile(0.75)
    #             IQR = Q3 - Q1
    #             df_processed[f'{col}_is_outlier'] = (
    #                 (df_processed[col] < (Q1 - 1.5 * IQR)) | 
    #                 (df_processed[col] > (Q3 + 1.5 * IQR))
    #             ).astype(int)
        
    #     print("Statistical features created successfully")
    #     return df_processed
    
    # def create_interaction_features(self, df):
    #     """יצירת תכונות אינטראקציה בין משתנים"""
    #     df_processed = df.copy()
        
    #     # אינטראקציות ספציפיות חשובות
    #     if 'num_burn_requests' in df_processed.columns and 'total_presence_minutes' in df_processed.columns:
    #         df_processed['burn_per_presence_interaction'] = df_processed['num_burn_requests'] * df_processed['total_presence_minutes'] / 1000
        
    #     if 'max_request_classification' in df_processed.columns and 'total_burn_volume_mb' in df_processed.columns:
    #         df_processed['classification_volume_interaction'] = df_processed['max_request_classification'] * df_processed['total_burn_volume_mb'] / 1000
        
    #     if 'num_unique_campus' in df_processed.columns and 'num_entries' in df_processed.columns:
    #         df_processed['campus_entries_interaction'] = df_processed['num_unique_campus'] * df_processed['num_entries']
        
    #     print("Interaction features created successfully")
    #     return df_processed
    
    def create_all_features(self, df):
        """יצירת כל התכונות החדשות"""
        print("Starting comprehensive feature creation...")
        
        df_processed = df.copy()
        df_processed = self.create_burning_features(df_processed)
        # df_processed = self.create_temporal_features(df_processed)
        # df_processed = self.create_behavioral_features(df_processed)
        # df_processed = self.create_security_features(df_processed)
        # df_processed = self.create_statistical_features(df_processed)
        # df_processed = self.create_interaction_features(df_processed)
        
        print(f"All features created successfully. New shape: {df_processed.shape}")
        return df_processed