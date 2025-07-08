"""
Complete Advanced Feature Engineer for Insider Threat Detection
מהנדס תכונות מתקדם מקיף לזיהוי איומים פנימיים
"""

import pandas as pd
import numpy as np
from typing import Dict, List

# ייבוא מחלקות הבסיס
from .basic.time_features import TimeFeatureEngineer
from .basic.printing_features import PrintingFeatureEngineer
from .basic.burning_features import BurningFeatureEngineer
from .basic.employee_features import EmployeeFeatureEngineer
from .basic.access_features import AccessFeatureEngineer
from .basic.interaction_features import InteractionFeatureEngineer

from .advanced.behavioral_features import BehavioralFeatureEngineer
from .advanced.temporal_features import TemporalFeatureEngineer
from .advanced.risk_profile_features import RiskProfileFeatureEngineer
from .advanced.anomaly_features import AnomalyFeatureEngineer
from .advanced.advanced_interaction_features import AdvancedInteractionFeatureEngineer

from pipeline.feature_engineering.advanced.feature_analysis import FeatureAnalyzer


class CompleteFeatureEngineer(
    # מחלקות בסיס
    TimeFeatureEngineer,
    PrintingFeatureEngineer,
    BurningFeatureEngineer,
    EmployeeFeatureEngineer,
    AccessFeatureEngineer,
    InteractionFeatureEngineer,
    
    # מחלקות מתקדמות
    BehavioralFeatureEngineer,
    TemporalFeatureEngineer,
    RiskProfileFeatureEngineer,
    AnomalyFeatureEngineer,
    AdvancedInteractionFeatureEngineer,
    FeatureAnalyzer
):
    """מחלקה מקיפה להנדסת תכונות בסיסיות ומתקדמות לזיהוי איומים פנימיים"""
    
    def __init__(self):
        super().__init__()
        self.feature_groups = {
            'basic': [],
            'behavioral': [],
            'temporal': [],
            'risk_profile': [],
            'anomaly': [],
            'interaction': [],
            'polynomial': []
        }
    
            # אתחול מפורש של כל הרשימות הנדרשות מהמחלקות השונות
        self.behavioral_features = []
        self.temporal_features = []
        self.risk_profile_features = []
        self.risk_features = []  
        self.anomaly_features = []
        self.interaction_features = []
        self.time_features = []
        self.printing_features = []
        self.burning_features = []
        self.employee_features = []
        self.access_features = []
        self.polynomial_features = []
 
    def create_all_basic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת כל התכונות הבסיסיות"""
        print("Starting comprehensive basic feature engineering...")
        
        df = self.extract_time_features(df)
        df = self.create_printing_features(df)
        df = self.create_burning_features(df)
        df = self.create_employee_features(df)
        df = self.create_access_features(df)
        df = self.create_interaction_features(df)
        df = self.apply_statistical_transforms(df)
        df = self.encode_categorical_variables(df)
        
        print(f"Basic feature engineering completed! Created {len(df.columns)} features")
        return df
    
    def create_all_advanced_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת כל התכונות המתקדמות"""
        print("Starting advanced feature engineering...")
        
        print("Creating behavioral risk features...")
        df = self.create_behavioral_risk_features(df)
        
        print("Creating advanced temporal patterns...")
        df = self.create_advanced_temporal_patterns(df)
        
        print("Creating risk profile features...")
        df = self.create_risk_profile_features(df)
        
        print("Creating anomaly detection features...")
        df = self.create_anomaly_detection_features(df)
        
        print("Creating advanced interaction features...")
        df = self.create_interaction_features_advanced(df)
        
        print("Creating ratio features...")
        df = self.create_ratio_features(df)
        
        print("Creating polynomial features...")
        df = self.create_polynomial_features(df)
        
        print("Advanced feature engineering completed!")
        return df
    
    def apply_complete_feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """החלת הנדסת תכונות מקיפה"""
        print("Starting complete feature engineering pipeline...")
        
        # שלב 1: תכונות בסיסיות
        df = self.create_all_basic_features(df)
        
        # שלב 2: תכונות מתקדמות
        df = self.create_all_advanced_features(df)
        
        # שלב 3: סטטיסטיקות חריגות
        df = self.create_statistical_anomalies(df)
        
        print(f"Complete feature engineering finished! Total features: {len(df.columns)}")
        return df
    
    def get_complete_feature_summary(self, df: pd.DataFrame) -> Dict:
        """סיכום מקיף של כל התכונות"""
        
        # קבוצות תכונות
        feature_groups = {
            'basic_time': [col for col in df.columns if any(x in col for x in ['hour', 'day', 'week', 'month'])],
            'basic_printing': [col for col in df.columns if any(x in col for x in ['print', 'color', 'page'])],
            'basic_burning': [col for col in df.columns if any(x in col for x in ['burn', 'cd', 'dvd'])],
            'basic_employee': [col for col in df.columns if any(x in col for x in ['employee', 'seniority', 'department'])],
            'basic_access': [col for col in df.columns if any(x in col for x in ['access', 'entry', 'exit'])],
            'behavioral_risk': [col for col in df.columns if any(x in col for x in ['weighted_suspicious', 'unusual_work', 'digital_footprint'])],
            'temporal_advanced': [col for col in df.columns if any(x in col for x in ['time_consistency', 'schedule_stability', 'night_shift'])],
            'risk_profile': [col for col in df.columns if any(x in col for x in ['combined_risk', 'access_risk', 'intelligence_risk'])],
            'anomaly_detection': [col for col in df.columns if 'anomaly' in col.lower()],
            'interaction_advanced': [col for col in df.columns if any(x in col for x in ['_interaction', '_risk', '_ratio'])],
            'polynomial': [col for col in df.columns if col.startswith('poly_')],
            'statistical': [col for col in df.columns if col.endswith('_z_anomaly')]
        }
        
        summary = {}
        total_features = 0
        
        for group, features in feature_groups.items():
            actual_features = [f for f in features if f in df.columns]
            summary[group] = {
                'count': len(actual_features),
                'features': actual_features[:10],  # רק 10 הראשונות לתצוגה
                'total_features': len(actual_features)
            }
            total_features += len(actual_features)
        
        summary['total_engineered_features'] = total_features
        summary['original_features'] = len(df.columns) - total_features
        
        return summary
    
    def analyze_feature_quality(self, df: pd.DataFrame, 
                              target_col: str = 'is_malicious') -> Dict:
        """ניתוח איכות התכונות"""
        print("Analyzing feature quality...")
        
        # ניתוח חשיבות תכונות
        importance_analysis = self.get_feature_importance_analysis(df, target_col)
        
        # ניתוח קורלציות
        correlation_analysis = self.analyze_feature_correlations(df)
        
        # זיהוי תכונות מיותרות
        redundant_features = self.identify_redundant_features(df)
        
        # ניתוח התפלגות
        distribution_analysis = self.get_feature_distribution_analysis(df, target_col)
        
        return {
            'importance_analysis': importance_analysis,
            'correlation_analysis': correlation_analysis,
            'redundant_features': redundant_features,
            'distribution_analysis': distribution_analysis,
            'feature_quality_score': len(importance_analysis.get('top_features_mi', [])) / max(len(df.columns), 1)
        }
    
    def get_recommended_features(self, df: pd.DataFrame, 
                               target_col: str = 'is_malicious',
                               top_k: int = 50) -> List[str]:
        """קבלת תכונות מומלצות"""
        
        # ניתוח חשיבות
        importance_analysis = self.get_feature_importance_analysis(df, target_col)
        
        if not importance_analysis:
            return []
        
        # בחירת תכונות מומלצות
        top_mi_features = importance_analysis.get('top_features_mi', [])[:top_k//2]
        top_f_features = importance_analysis.get('top_features_f', [])[:top_k//2]
        
        # איחוד והסרת כפילויות
        recommended_features = list(set(top_mi_features + top_f_features))[:top_k]
        
        return recommended_features
    
    def optimize_feature_set(self, df: pd.DataFrame, 
                           target_col: str = 'is_malicious') -> pd.DataFrame:
        """אופטימיזציה של סט התכונות"""
        print("Optimizing feature set...")
        
        # הסרת תכונות מיותרות
        redundant_features = self.identify_redundant_features(df)
        df_optimized = df.drop(columns=redundant_features, errors='ignore')
        
        # קבלת תכונות מומלצות
        recommended_features = self.get_recommended_features(df_optimized, target_col)
        
        # שמירת עמודות חשובות
        important_cols = [target_col] + [col for col in df_optimized.columns 
                                       if col in recommended_features or col == target_col]
        
        df_final = df_optimized[important_cols]
        
        print(f"Feature optimization completed! Reduced from {len(df.columns)} to {len(df_final.columns)} features")
        return df_final