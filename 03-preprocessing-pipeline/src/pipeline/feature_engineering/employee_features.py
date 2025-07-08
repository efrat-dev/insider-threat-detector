import pandas as pd
import numpy as np
from .base_feature_engineer import BaseFeatureEngineer

class EmployeeFeatureEngineer(BaseFeatureEngineer):
    """מחלקה ליצירת תכונות עובד"""
    
    def create_employee_features(self, df):
        """יצירת תכונות עובד מקיפות"""
        df_processed = df.copy()
        
        # תכונות ותק
        df_processed['seniority_category'] = pd.cut(
            df_processed['employee_seniority_years'],
            bins=[0, 1, 3, 10, np.inf],
            labels=['new', 'junior', 'senior', 'veteran']
        )
        
        df_processed['is_new_employee'] = (df_processed['employee_seniority_years'] < 1).astype(int)
        df_processed['is_veteran_employee'] = (df_processed['employee_seniority_years'] > 10).astype(int)
        
        # תכונות סיכון אישיות
        df_processed['personal_risk_flags'] = (
            df_processed['has_foreign_citizenship'] +
            df_processed['has_criminal_record'] +
            df_processed['has_medical_history']
        )
        
        df_processed['employment_risk_score'] = (
            df_processed['is_contractor'] * 2 +
            df_processed['has_foreign_citizenship'] * 1.5 +
            df_processed['has_criminal_record'] * 3 +
            df_processed['risk_travel_indicator'] * 2
        )
        
        # תכונות מיקום וניידות
        df_processed['is_multi_campus_user'] = (df_processed['num_unique_campus'] > 1).astype(int)
        df_processed['campus_mobility_score'] = df_processed['num_unique_campus']
        
        # תכונות נסיעות
        df_processed['has_travel_history'] = (df_processed['is_abroad'] > 0).astype(int)
        df_processed['hostile_travel_risk'] = (df_processed['is_hostile_country_trip'] > 0).astype(int)
        df_processed['unofficial_travel_risk'] = (df_processed['is_abroad'] & ~df_processed['is_official_trip']).astype(int)
        
        # תכונות קטגוריות למחלקה ותפקיד
        department_risk_map = {
            'IT': 3, 'Security': 4, 'Finance': 3, 'HR': 2,
            'Research': 3, 'Operations': 1, 'Management': 2
        }
        df_processed['department_risk_level'] = df_processed['employee_department'].map(department_risk_map).fillna(1)
        
        print("Employee features created successfully")
        return df_processed