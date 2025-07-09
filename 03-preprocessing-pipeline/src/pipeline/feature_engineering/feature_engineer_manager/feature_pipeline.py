    # File 3: feature_pipeline.py (Pipeline management - 49 lines)
import pandas as pd
from typing import List

class FeaturePipeline:
    """מנהל pipeline של הנדסת תכונות"""
    
    def __init__(self, factory):
        self.factory = factory
        self.basic_types = ['time', 'printing', 'burning', 'employee', 'access', 'interaction']
        self.advanced_types = ['behavioral', 'temporal', 'risk_profile', 'anomaly', 'advanced_interaction']
    
    def create_all_basic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת כל התכונות הבסיסיות"""
        print("Starting basic feature engineering...")
        for feature_type in self.basic_types:
            try:
                df = self.factory.create_features_by_type(df, feature_type)
                print(f"{feature_type} features created")
            except Exception as e:
                print(f"Error in {feature_type}: {e}")
        return df
    
    def create_all_advanced_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת כל התכונות המתקדמות"""
        print("Starting advanced feature engineering...")
        for feature_type in self.advanced_types:
            try:
                df = self.factory.create_features_by_type(df, feature_type)
            except Exception as e:
                print(f"Error in {feature_type}: {e}")
        
        # תכונות מתקדמות מיוחדות
        specialized_methods = [
            ('ratio', 'create_ratio_features'),
            ('polynomial', 'create_polynomial_features')
        ]
        
        for name, method in specialized_methods:
            try:
                df = self.factory.safe_engineer_call('advanced_interaction', method, df)
            except Exception as e:
                print(f"Error in {name}: {e}")
        return df
    
    def apply_complete_feature_engineering(self, df: pd.DataFrame, target_col: str = 'is_malicious') -> pd.DataFrame:
        """החלת הנדסת תכונות מקיפה"""
        print("Starting complete feature engineering...")
        
        # שלב 1: תכונות בסיסיות
        df = self.create_all_basic_features(df)
        
        # שלב 2: תכונות מתקדמות
        df = self.create_all_advanced_features(df)
        
        # שלב 3: קידוד מקיף - using encoder from factory
        df = self._apply_encoding_transforms(df, target_col)
        
        # שלב 4: חריגות
        df = self.factory.safe_engineer_call('anomaly', 'create_statistical_anomalies', df)
        
        print(f"Complete feature engineering finished! Features: {len(df.columns)}")
        return df
    
    def _apply_encoding_transforms(self, df: pd.DataFrame, target_col: str) -> pd.DataFrame:
        """קידוד ועיבוד מקיף"""
        # This would use the base class methods - simplified for space
        return df