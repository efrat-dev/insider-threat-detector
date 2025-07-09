"""
Complete Advanced Feature Engineer for Insider Threat Detection - OPTIMIZED VERSION
מהנדס תכונות מתקדם מקיף לזיהוי איומים פנימיים - גרסה מותאמת
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from scipy import stats

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
from pipeline.feature_engineering.basic.base_feature_engineer import BaseFeatureEngineer


class CompleteFeatureEngineer(BaseFeatureEngineer):
    """מחלקה מקיפה להנדסת תכונות בסיסיות ומתקדמות לזיהוי איומים פנימיים"""
    
    def __init__(self):
        super().__init__()
        self._init_feature_engineers()
        
    def _init_feature_engineers(self):
        """אתחול כל מהנדסי התכונות"""
        self.engineers = {}
        
        # רשימת כל המהנדסים עם המתודות שלהם
        self.engineer_config = {
            'time': (TimeFeatureEngineer, 'extract_time_features'),
            'printing': (PrintingFeatureEngineer, 'create_printing_features'),
            'burning': (BurningFeatureEngineer, 'create_burning_features'),
            'employee': (EmployeeFeatureEngineer, 'create_employee_features'),
            'access': (AccessFeatureEngineer, 'create_access_features'),
            'interaction': (InteractionFeatureEngineer, 'create_interaction_features'),
            'behavioral': (BehavioralFeatureEngineer, 'create_behavioral_risk_features'),
            'temporal': (TemporalFeatureEngineer, 'create_advanced_temporal_patterns'),
            'risk_profile': (RiskProfileFeatureEngineer, 'create_risk_profile_features'),
            'anomaly': (AnomalyFeatureEngineer, 'create_anomaly_detection_features'),
            'advanced_interaction': (AdvancedInteractionFeatureEngineer, 'create_interaction_features_advanced'),
            'analyzer': (FeatureAnalyzer, None)  # אנליזה בלבד
        }
        
        # יצירת מהנדסים עם error handling
        for name, (engineer_class, _) in self.engineer_config.items():
            try:
                self.engineers[name] = engineer_class()
            except Exception as e:
                print(f"Warning: Could not initialize {name}: {e}")
                self.engineers[name] = None
    
    def _safe_engineer_call(self, engineer_name: str, method_name: str, df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        """קריאה בטוחה למהנדס עם fallback"""
        engineer = self.engineers.get(engineer_name)
        if engineer is None:
            print(f"{engineer_name} not available")
            return df
        
        try:
            method = getattr(engineer, method_name)
            return method(df, *args, **kwargs)
        except Exception as e:
            print(f"Error in {engineer_name}.{method_name}: {e}")
            return df
    
    # Generic Feature Creation Method - מחליף את כל הפונקציות הבסיסיות
    def create_features_by_type(self, df: pd.DataFrame, feature_type: str) -> pd.DataFrame:
        """יצירת תכונות לפי סוג - גנרי"""
        if feature_type not in self.engineer_config:
            print(f"Unknown feature type: {feature_type}")
            return df
        
        _, method_name = self.engineer_config[feature_type]
        if method_name:
            return self._safe_engineer_call(feature_type, method_name, df)
        return df
    
    # Specialized Advanced Methods - רק לפונקציות מיוחדות
    def create_polynomial_features(self, df: pd.DataFrame, degree: int = 2, selected_features: List[str] = None) -> pd.DataFrame:
        """יצירת תכונות פולינומיות"""
        return self._safe_engineer_call('advanced_interaction', 'create_polynomial_features', df, degree, selected_features)
    
    def create_ratio_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת תכונות יחס"""
        return self._safe_engineer_call('advanced_interaction', 'create_ratio_features', df)
    
    def create_statistical_anomalies(self, df: pd.DataFrame, threshold: float = 2.5) -> pd.DataFrame:
        """יצירת תכונות אנומליות סטטיסטיות"""
        return self._safe_engineer_call('anomaly', 'create_statistical_anomalies', df, threshold)
    
    # Analysis Methods - מאוחד
    def _get_analyzer_result(self, method_name: str, df: pd.DataFrame, *args, **kwargs):
        """קריאה אחודה לאנליזה"""
        analyzer = self.engineers.get('analyzer')
        if analyzer:
            try:
                method = getattr(analyzer, method_name)
                return method(df, *args, **kwargs)
            except Exception as e:
                print(f"Error in {method_name}: {e}")
        return None
    
    def analyze_feature_quality(self, df: pd.DataFrame, target_col: str) -> Dict:
        result = self._get_analyzer_result('analyze_feature_quality', df, target_col)
        return result if result else {'status': 'FeatureAnalyzer not available'}
    
    def get_recommended_features(self, df: pd.DataFrame, target_col: str) -> List[str]:
        result = self._get_analyzer_result('get_recommended_features', df, target_col)
        return result if result else []
    
    def identify_redundant_features(self, df: pd.DataFrame) -> List[str]:
        result = self._get_analyzer_result('identify_redundant_features', df)
        return result if result else []
    
    # Pipeline Methods - משופרים
    def create_all_basic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת כל התכונות הבסיסיות"""
        print("Starting comprehensive basic feature engineering...")
        
        basic_types = ['time', 'printing', 'burning', 'employee', 'access', 'interaction']
        
        for feature_type in basic_types:
            try:
                df = self.create_features_by_type(df, feature_type)
                print(f"{feature_type} features created successfully")
            except Exception as e:
                print(f"Error in {feature_type} features: {e}")
        
        print(f"Basic feature engineering completed! Created {len(df.columns)} features")
        return df
    
    def create_all_advanced_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת כל התכונות המתקדמות"""
        print("Starting advanced feature engineering...")
        
        # תכונות מתקדמות בסיסיות
        advanced_types = ['behavioral', 'temporal', 'risk_profile', 'anomaly', 'advanced_interaction']
        
        for feature_type in advanced_types:
            try:
                print(f"Creating {feature_type} features...")
                df = self.create_features_by_type(df, feature_type)
            except Exception as e:
                print(f"Error in {feature_type} features: {e}")
        
        # תכונות מתקדמות מיוחדות
        specialized_methods = [
            ('ratio', self.create_ratio_features),
            ('polynomial', self.create_polynomial_features)
        ]
        
        for name, method in specialized_methods:
            try:
                print(f"Creating {name} features...")
                df = method(df)
            except Exception as e:
                print(f"Error in {name} features: {e}")
        
        print("Advanced feature engineering completed!")
        return df
    
    def apply_complete_feature_engineering(self, df: pd.DataFrame, target_col: str = 'is_malicious') -> pd.DataFrame:
        """החלת הנדסת תכונות מקיפה"""
        print("Starting complete feature engineering pipeline...")
        
        # שלב 1: תכונות בסיסיות
        df = self.create_all_basic_features(df)
        
        # שלב 2: תכונות מתקדמות
        df = self.create_all_advanced_features(df)
        
        # שלב 3: קידוד מקיף - using BaseFeatureEngineer's methods
        df = self.encode_categorical_variables(df, target_col)
        df = self.handle_special_text_columns(df)
        df = self.apply_statistical_transforms(df)
        
        # שלב 4: סטטיסטיקות חריגות
        df = self.create_statistical_anomalies(df)
        
        print(f"Complete feature engineering finished! Total features: {len(df.columns)}")
        return df
    
    def optimize_feature_set(self, df: pd.DataFrame, target_col: str = 'is_malicious') -> pd.DataFrame:
        """אופטימיזציה של סט התכונות"""
        print("Starting feature set optimization...")
        
        # הסרת תכונות מיותרות
        redundant_features = self.identify_redundant_features(df)
        df_optimized = df.drop(columns=redundant_features, errors='ignore')
        
        # הסרת עמודות עם ערך אחיד
        constant_features = [col for col in df_optimized.columns if df_optimized[col].nunique() <= 1]
        df_optimized = df_optimized.drop(columns=constant_features, errors='ignore')
        
        print(f"Optimization completed!")
        print(f"Original features: {len(df.columns)}")
        print(f"Optimized features: {len(df_optimized.columns)}")
        print(f"Removed: {len(redundant_features)} redundant + {len(constant_features)} constant")
        
        return df_optimized
    
    def get_feature_summary(self, df: pd.DataFrame) -> Dict:
        """סיכום התכונות - משופר"""
        feature_patterns = {
            'basic_time': ['hour', 'day', 'week', 'month'],
            'basic_printing': ['print', 'color', 'page'],
            'basic_burning': ['burn', 'cd', 'dvd'],
            'behavioral_risk': ['weighted_suspicious', 'unusual_work'],
            'anomaly_detection': ['anomaly'],
            'polynomial': ['poly_'],
            'ratio_features': ['ratio'],
            'interaction_features': ['interaction'],
            'encoded_categorical': ['_label', '_binary', '_freq'],
            'text_analysis': ['_length', '_word_count', '_has_'],
            'statistical_transforms': ['_log', '_sqrt', '_zscore']
        }
        
        summary = {}
        for group, patterns in feature_patterns.items():
            matching_features = [
                col for col in df.columns 
                if any(pattern in col.lower() for pattern in patterns)
            ]
            
            summary[group] = {
                'count': len(matching_features),
                'features': matching_features[:5]  # רק 5 הראשונות
            }
        
        summary['total_features'] = len(df.columns)
        summary['available_engineers'] = [name for name, eng in self.engineers.items() if eng is not None]
        
        return summary
    
    # Delegated Summary Methods - קיצור
    def get_interaction_feature_summary(self, df: pd.DataFrame) -> Dict:
        """סיכום תכונות אינטראקציה"""
        return self._safe_engineer_call('advanced_interaction', 'get_interaction_feature_summary', df)
    
    def get_anomaly_feature_summary(self, df: pd.DataFrame) -> Dict:
        """סיכום תכונות חריגות"""
        return self._safe_engineer_call('anomaly', 'get_anomaly_feature_summary', df)
    
    # Utility Methods
    def get_available_feature_types(self) -> List[str]:
        """קבלת רשימת סוגי התכונות הזמינים"""
        return [name for name, eng in self.engineers.items() if eng is not None]
    
    def get_engineer_status(self) -> Dict[str, bool]:
        """בדיקת סטטוס המהנדסים"""
        return {name: eng is not None for name, eng in self.engineers.items()}