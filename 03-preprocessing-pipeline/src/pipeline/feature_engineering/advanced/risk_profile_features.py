"""
Risk Profile Feature Engineering for Insider Threat Detection
יצירת תכונות פרופיל סיכון לזיהוי איומים פנימיים
"""

import pandas as pd
import numpy as np
from typing import Dict, List


class RiskProfileFeatureEngineer:
    """מהנדס תכונות פרופיל סיכון"""
    
    def __init__(self):
        self.risk_features = []
    
    def create_risk_profile_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת תכונות פרופיל סיכון מתקדמות"""
        df = df.copy()
        
        # מדד סיכון משולב
        df['combined_risk_score'] = (
            df.get('personal_risk_flags', 0) * 2 +
            df.get('employment_risk_score', 0) * 1.5 +
            df.get('hostile_travel_risk', 0) * 4 +
            df.get('unofficial_travel_risk', 0) * 3
        )
        
        # מדד סיכון גישה
        df['access_risk_profile'] = (
            df.get('is_multi_campus_user', 0) * 2 +
            df.get('campus_mobility_score', 0) * 1.5 +
            df.get('has_travel_history', 0) * 1 +
            df.get('department_risk_level', 1) * 0.5
        )
        
        # מדד סיכון מודיעיני
        df['intelligence_risk_score'] = (
            df.get('high_classification_burn', 0) * 4 +
            df.get('classification_consistency', 0) * 2 +
            df.get('classification_variance', 0) * 1.5
        )
        
        # מדד פעילות מסווגת
        df['classified_activity_intensity'] = (
            df.get('max_request_classification', 0) * 
            df.get('burn_activity_intensity', 0)
        )
        
        # מדד סיכון מדיה
        df['media_risk_score'] = (
            df.get('color_print_preference', 0) * 2 +
            df.get('avg_burn_volume_per_request', 0) * 0.1 +
            df.get('avg_file_size_mb', 0) * 0.05
        )
        
        # מדד סיכון פעילות חוץ
        df['foreign_activity_risk'] = (
            df.get('hostile_travel_risk', 0) * 3 +
            df.get('unofficial_travel_risk', 0) * 2 +
            df.get('has_travel_history', 0) * 1
        )
        
        self.risk_features.extend([
            'combined_risk_score', 'access_risk_profile',
            'intelligence_risk_score', 'classified_activity_intensity',
            'media_risk_score', 'foreign_activity_risk'
        ])
        
        return df