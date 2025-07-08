"""
Advanced Feature Engineering for Insider Threat Dataset
יצירת תכונות מתקדמות לזיהוי איומים פנימיים - ללא כפילויות
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from scipy import stats
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class AdvancedFeatureEngineer:
    """מהנדס תכונות מתקדם עבור נתוני איומים פנימיים"""
    
    def __init__(self):
        self.behavioral_features = []
        self.risk_features = []
        self.temporal_features = []
        self.anomaly_features = []
        
    def create_behavioral_risk_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת תכונות סיכון התנהגותי מתקדמות"""
        df = df.copy()
        
        # מדד פעילות חשודה משוקלל
        df['weighted_suspicious_activity'] = (
            df['entered_during_night_hours'] * 3 +
            df['early_entry_flag'] * 1.5 +
            df['late_exit_flag'] * 1.5 +
            df['entry_during_weekend'] * 2.5 +
            df.get('off_hours_print_ratio', 0) * 2 +
            df.get('off_hours_burn_ratio', 0) * 3
        )
        
        # דפוס עבודה חריג
        df['unusual_work_pattern'] = (
            (df['is_weekend'] & (df['total_presence_minutes'] > 240)) |  # עבודה ארוכה בסוף השבוע
            (df.get('work_duration_hours', 0) > 14) |  # עבודה מעל 14 שעות
            (df.get('work_duration_hours', 0) < 2)     # עבודה מתחת לשעתיים
        ).astype(int)
        
        # מדד פעילות דיגיטלית חשודה
        df['digital_footprint_risk'] = (
            df.get('is_heavy_printer', 0) * 2 +
            df.get('is_high_volume_printer', 0) * 2 +
            df.get('is_heavy_burner', 0) * 3 +
            df.get('is_high_volume_burner', 0) * 3 +
            df.get('prints_from_other_campus', 0) * 2 +
            df.get('burns_from_other_campus', 0) * 3
        )
        
        # מדד יעילות חשודה (פעילות גבוהה בזמן קצר)
        df['efficiency_anomaly'] = (
            df.get('print_efficiency', 0) * df.get('burn_efficiency', 0)
        ) / np.maximum(df.get('work_duration_hours', 1), 1)
        
        return df
    
    def create_advanced_temporal_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת דפוסי זמן מתקדמים שלא נוצרו כבר"""
        df = df.copy()
        
        # דפוסי זמן מתקדמים
        df['time_consistency_score'] = np.abs(
            df.get('entry_hour', 9) - df.get('entry_hour', 9).mean()
        ) + np.abs(
            df.get('exit_hour', 17) - df.get('exit_hour', 17).mean()
        )
        
        # מדד יציבות זמנים
        df['schedule_stability'] = (
            (df.get('entry_hour', 9).between(7, 10)) &
            (df.get('exit_hour', 17).between(16, 19))
        ).astype(int)
        
        # פעילות בחגים/תקופות מיוחדות
        df['holiday_activity'] = (
            df.get('is_quarter_end', 0) * df.get('suspicious_access_score', 0)
        )
        
        # דפוס עבודה לילי
        df['night_shift_pattern'] = (
            (df.get('entry_hour', 9) >= 22) | (df.get('entry_hour', 9) <= 5)
        ).astype(int)
        
        return df
    
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
        
        # מדד סיכון התנהגותי מתקדם
        df['behavioral_risk_advanced'] = (
            df.get('has_suspicious_access', 0) * 3 +
            df.get('unusual_work_pattern', 0) * 2 +
            df.get('digital_footprint_risk', 0) * 0.5 +
            df.get('night_shift_pattern', 0) * 2
        )
        
        return df
    
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
        
        return df
    
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
        
        return df
    
    def create_polynomial_features(self, df: pd.DataFrame, degree: int = 2, 
                                 selected_features: List[str] = None) -> pd.DataFrame:
        """יצירת תכונות פולינומיות"""
        df = df.copy()
        
        if selected_features is None:
            selected_features = [
                'combined_risk_score', 'behavioral_risk_advanced',
                'weighted_suspicious_activity', 'digital_footprint_risk',
                'access_risk_profile'
            ]
        
        # בחירת תכונות קיימות
        available_features = [col for col in selected_features if col in df.columns]
        
        if len(available_features) < 2:
            print("Not enough features for polynomial transformation")
            return df
        
        # יצירת תכונות פולינומיות
        poly = PolynomialFeatures(degree=degree, include_bias=False, 
                                interaction_only=True)
        
        poly_features = poly.fit_transform(df[available_features])
        poly_feature_names = poly.get_feature_names_out(available_features)
        
        # הוספת תכונות חדשות (רק האינטראקציות, לא הרבועים)
        for i, name in enumerate(poly_feature_names):
            if name not in available_features:  # רק תכונות חדשות
                df[f'poly_{name}'] = poly_features[:, i]
        
        return df
    
    def create_domain_specific_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת תכונות ספציפיות לתחום"""
        df = df.copy()
        
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
        
        return df
    
    def apply_all_advanced_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """החלת כל התכונות המתקדמות"""
        print("Creating advanced behavioral risk features...")
        df = self.create_behavioral_risk_features(df)
        
        print("Creating advanced temporal patterns...")
        df = self.create_advanced_temporal_patterns(df)
        
        print("Creating risk profile features...")
        df = self.create_risk_profile_features(df)
        
        print("Creating anomaly detection features...")
        df = self.create_anomaly_detection_features(df)
        
        print("Creating advanced interaction features...")
        df = self.create_interaction_features_advanced(df)
        
        print("Creating polynomial features...")
        df = self.create_polynomial_features(df)
        
        print("Creating domain-specific features...")
        df = self.create_domain_specific_features(df)
        
        print("Advanced feature engineering completed!")
        return df
    
    def get_feature_importance_analysis(self, df: pd.DataFrame, 
                                      target_col: str = 'is_malicious') -> Dict:
        """ניתוח חשיבות תכונות"""
        if target_col not in df.columns:
            print(f"Target column '{target_col}' not found")
            return {}
        
        # בחירת תכונות מספריות
        numerical_features = df.select_dtypes(include=[np.number]).columns
        numerical_features = [col for col in numerical_features if col != target_col]
        
        if len(numerical_features) == 0:
            print("No numerical features found for importance analysis")
            return {}
        
        X = df[numerical_features].fillna(0)
        y = df[target_col]
        
        # חישוב חשיבות עם mutual information
        mi_scores = mutual_info_classif(X, y)
        
        # חישוב חשיבות עם F-test
        f_scores, _ = f_classif(X, y)
        
        # יצירת DataFrame עם הציונים
        importance_df = pd.DataFrame({
            'feature': numerical_features,
            'mutual_info_score': mi_scores,
            'f_score': f_scores
        }).sort_values('mutual_info_score', ascending=False)
        
        return {
            'importance_analysis': importance_df,
            'top_features_mi': importance_df.head(20)['feature'].tolist(),
            'top_features_f': importance_df.nlargest(20, 'f_score')['feature'].tolist()
        }
    
    def get_advanced_feature_summary(self, df: pd.DataFrame) -> Dict:
        """סיכום התכונות המתקדמות שנוצרו"""
        feature_groups = {
            'behavioral_risk': [col for col in df.columns if any(x in col for x in ['weighted_suspicious', 'unusual_work', 'digital_footprint', 'efficiency_anomaly'])],
            'temporal_advanced': [col for col in df.columns if any(x in col for x in ['time_consistency', 'schedule_stability', 'holiday_activity', 'night_shift'])],
            'risk_profile': [col for col in df.columns if any(x in col for x in ['combined_risk', 'access_risk', 'behavioral_risk_advanced'])],
            'anomaly_detection': [col for col in df.columns if any(x in col for x in ['_anomaly', 'anomaly_score', 'is_behavioral_anomaly'])],
            'interaction_advanced': [col for col in df.columns if any(x in col for x in ['risk_behavior_interaction', 'time_activity_risk', 'travel_activity_risk'])],
            'polynomial': [col for col in df.columns if col.startswith('poly_')],
            'domain_specific': [col for col in df.columns if any(x in col for x in ['intelligence_risk', 'classified_activity', 'media_risk'])]
        }
        
        summary = {}
        for group, features in feature_groups.items():
            summary[group] = {
                'count': len(features),
                'features': features
            }
        
        return summary