"""
Anomaly Detection Feature Engineering for Insider Threat Detection
יצירת תכונות לזיהוי חריגות לזיהוי איומים פנימיים
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List


class AnomalyFeatureEngineer:
    """מהנדס תכונות לזיהוי חריגות"""
    
    def __init__(self):
        self.anomaly_features = []
    
    def create_anomaly_detection_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת תכונות לזיהוי חריגות מתקדמות"""
        df = df.copy()
        
        # חריגות בפעילות יומית
        daily_metrics = [
            'total_activity_score', 'daily_activity_intensity',
            'print_intensity', 'burn_intensity'
        ]
        
        outlier_scores = []
        for col in daily_metrics:
            if col in df.columns:
                z_score = np.abs(stats.zscore(df[col]))
                df[f'{col}_anomaly'] = (z_score > 2.5).astype(int)
                outlier_scores.append(f'{col}_anomaly')
        
        # מדד חריגות כללי
        if outlier_scores:
            df['anomaly_score'] = df[outlier_scores].sum(axis=1)
            df['is_behavioral_anomaly'] = (df['anomaly_score'] >= 2).astype(int)
        
        # חריגות בדפוסי זמן
        if 'time_consistency_score' in df.columns:
            df['time_anomaly'] = (
                df['time_consistency_score'] > df['time_consistency_score'].quantile(0.9)
            ).astype(int)
        
        # חריגות בפעילות הדפסה
        if 'print_intensity' in df.columns:
            df['print_anomaly'] = (
                df['print_intensity'] > df['print_intensity'].quantile(0.95)
            ).astype(int)
        
        # חריגות בפעילות צריבה
        if 'burn_intensity' in df.columns:
            df['burn_anomaly'] = (
                df['burn_intensity'] > df['burn_intensity'].quantile(0.95)
            ).astype(int)
        
        # חריגות בפעילות גישה
        if 'access_pattern_score' in df.columns:
            df['access_anomaly'] = (
                df['access_pattern_score'] > df['access_pattern_score'].quantile(0.9)
            ).astype(int)
        
        # מדד חריגות משולב
        anomaly_cols = [col for col in df.columns if col.endswith('_anomaly')]
        if anomaly_cols:
            df['combined_anomaly_score'] = df[anomaly_cols].sum(axis=1)
            df['is_high_risk_anomaly'] = (df['combined_anomaly_score'] >= 3).astype(int)
        
        self.anomaly_features.extend([
            'anomaly_score', 'is_behavioral_anomaly', 'time_anomaly',
            'print_anomaly', 'burn_anomaly', 'access_anomaly',
            'combined_anomaly_score', 'is_high_risk_anomaly'
        ])
        
        return df
    
    def create_statistical_anomalies(self, df: pd.DataFrame, 
                                   threshold: float = 2.5) -> pd.DataFrame:
        """יצירת חריגות סטטיסטיות"""
        df = df.copy()
        
        # תכונות מספריות לבדיקת חריגות
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if col not in ['is_malicious', 'employee_id']:  # דילוג על עמודות לא רלוונטיות
                z_scores = np.abs(stats.zscore(df[col]))
                df[f'{col}_z_anomaly'] = (z_scores > threshold).astype(int)
        
        return df
    
    def get_anomaly_feature_summary(self, df: pd.DataFrame) -> Dict:
        """סיכום תכונות חריגות"""
        anomaly_cols = [col for col in df.columns if 'anomaly' in col.lower()]
        
        summary = {}
        for col in anomaly_cols:
            if col in df.columns:
                summary[col] = {
                    'count': df[col].sum(),
                    'percentage': df[col].mean() * 100,
                    'correlation_with_malicious': df[col].corr(df.get('is_malicious', pd.Series([0]*len(df))))
                }
        
        return summary