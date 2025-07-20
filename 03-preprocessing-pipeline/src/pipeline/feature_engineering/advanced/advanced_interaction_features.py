"""
Advanced Interaction Feature Engineering for Insider Threat Detection
יצירת תכונות אינטראקציה מתקדמות לזיהוי איומים פנימיים
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from typing import Dict, List


class AdvancedInteractionFeatureEngineer:
    """מהנדס תכונות אינטראקציה מתקדם"""
    
    def __init__(self):
        self.interaction_features = []
    
    def create_interaction_features_advanced(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת תכונות אינטראקציה מתקדמות"""
        df = df.copy()
        
        # אינטראקציות סיכון מתקדמות
        df['risk_behavior_interaction'] = (
            df.get('combined_risk_score', 0) * 
            df.get('behavioral_risk_advanced', 0)
        )
        
        # אינטראקציה בין זמן לפעילות
        df['time_activity_risk'] = (
            df.get('weighted_suspicious_activity', 0) * 
            df.get('time_anomaly', 0)
        )
        
        # אינטראקציה בין ותק לחריגות
        df['seniority_anomaly_interaction'] = (
            df.get('employee_seniority_years', 0) * 
            df.get('is_behavioral_anomaly', 0)
        )
        
        # אינטראקציה בין גישה לפעילות דיגיטלית
        df['access_digital_risk'] = (
            df.get('access_risk_profile', 0) * 
            df.get('digital_footprint_risk', 0)
        )
        
        # אינטראקציה עם נסיעות חוץ
        df['travel_activity_risk'] = (
            df.get('foreign_activity_risk', 0) * 
            df.get('total_activity_score', 0)
        )
        
        # אינטראקציה בין סיכון אישי לפעילות
        df['personal_risk_activity'] = (
            df.get('personal_risk_flags', 0) * 
            df.get('daily_activity_intensity', 0)
        )
        
        # אינטראקציה בין סיווג לפעילות
        df['classification_activity_risk'] = (
            df.get('intelligence_risk_score', 0) * 
            df.get('classified_activity_intensity', 0)
        )
        
        # אינטראקציה בין זמן לסיכון
        df['temporal_risk_interaction'] = (
            df.get('time_consistency_score', 0) * 
            df.get('combined_risk_score', 0)
        )
        
        self.interaction_features.extend([
            'risk_behavior_interaction', 'time_activity_risk',
            'seniority_anomaly_interaction', 'access_digital_risk',
            'travel_activity_risk', 'personal_risk_activity',
            'classification_activity_risk', 'temporal_risk_interaction'
        ])
        
        return df
    
    def create_polynomial_features(self, df: pd.DataFrame, degree: int = 2, 
                                 selected_features: List[str] = None) -> pd.DataFrame:
        """יצירת תכונות פולינומיות"""
        df = df.copy()
        
        if selected_features is None:
            selected_features = [
                'combined_risk_score', 'behavioral_risk_advanced',
                'weighted_suspicious_activity', 'digital_footprint_risk',
                'access_risk_profile', 'intelligence_risk_score'
            ]
        
        # בחירת תכונות קיימות
        available_features = [col for col in selected_features if col in df.columns]
        
        if len(available_features) < 2:
            print("Not enough features for polynomial transformation")
            return df
        
        # יצירת תכונות פולינומיות
        poly = PolynomialFeatures(degree=degree, include_bias=False, 
                                interaction_only=True)
        
        try:
            poly_features = poly.fit_transform(df[available_features])
            poly_feature_names = poly.get_feature_names_out(available_features)
            
            # הוספת תכונות חדשות (רק האינטראקציות)
            for i, name in enumerate(poly_feature_names):
                if name not in available_features:  # רק תכונות חדשות
                    df[f'poly_{name}'] = poly_features[:, i]
        except Exception as e:
            print(f"Error creating polynomial features: {e}")
        
        return df
    
    def create_ratio_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת תכונות יחס"""
        df = df.copy()
        
        # יחס בין סיכון לפעילות
        df['risk_activity_ratio'] = (
            df.get('combined_risk_score', 0) / 
            np.maximum(df.get('total_activity_score', 1), 1)
        )
        
        # יחס בין חריגות לזמן
        df['anomaly_time_ratio'] = (
            df.get('anomaly_score', 0) / 
            np.maximum(df.get('work_duration_hours', 1), 1)
        )
        
        # יחס בין פעילות דיגיטלית לפעילות כללית
        df['digital_total_ratio'] = (
            df.get('digital_footprint_risk', 0) / 
            np.maximum(df.get('total_activity_score', 1), 1)
        )
        
        # יחס בין פעילות לילה לפעילות כללית
        df['night_activity_ratio'] = (
            df.get('night_shift_pattern', 0) * df.get('total_activity_score', 0) / 
            np.maximum(df.get('total_activity_score', 1), 1)
        )
        
        return df