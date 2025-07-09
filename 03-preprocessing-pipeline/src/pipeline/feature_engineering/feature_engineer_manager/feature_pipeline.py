# File 3a: feature_pipeline.py (Core Pipeline Management - 70 lines)
import numpy as np
import pandas as pd
from typing import List
from .feature_processor import FeatureProcessor

class FeaturePipeline:
    """מנהל pipeline של הנדסת תכונות"""
    
    def __init__(self, factory, complete_engineer=None):
        self.factory = factory
        self.processor = FeatureProcessor(factory)
        self.complete_engineer = complete_engineer
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
                
        print("Advanced feature engineering completed!")
        return df
    
    def apply_complete_feature_engineering(self, df: pd.DataFrame, target_col: str = 'is_malicious') -> pd.DataFrame:
        """החלת הנדסת תכונות מקיפה"""
        print("Starting complete feature engineering...")
                
        # שלב 1: תכונות בסיסיות
        df = self.create_all_basic_features(df)
        
        # שלב 2: תכונות מתקדמות
        df = self.create_all_advanced_features(df)
        
        # שלב 3: קידוד מקיף
        df = self.processor.apply_encoding_transforms(df, target_col)
        
        # שלב 4: חריגות
        df = self.factory.safe_engineer_call('anomaly', 'create_statistical_anomalies', df)
        
        # שלב 5: ניתוח ופינוי תכונות מיותרות
        print("Analyzing redundant features...")
        try:
            redundant_features = self.factory.get_analyzer_result('identify_redundant_features', df)
            if redundant_features:
                print(f"Found {len(redundant_features)} redundant features: {redundant_features}")
                df = df.drop(columns=redundant_features)
                print(f"Removed redundant features. Remaining features: {len(df.columns)}")
            else:
                print("No redundant features found")
        except Exception as e:
            print(f"Error in redundant features analysis: {e}")
        
        # שלב 6: אופטימיזציה של סט התכונות
        if self.complete_engineer:
            print("Optimizing feature set...")
            try:
                df = self.complete_engineer.optimize_feature_set(df, target_col)
                print(f"Feature optimization completed. Final features: {len(df.columns)}")
            except Exception as e:
                print(f"Error in feature optimization: {e}")
        
        # שלב 7: הכנת סיכום תכונות
        if self.complete_engineer:
            print("Generating feature summary...")
            try:
                feature_summary = self.complete_engineer.get_feature_summary(df)
                print(f"Feature summary generated with {len(feature_summary)} items")
            except Exception as e:
                print(f"Error in feature summary generation: {e}")

        print(f"Complete feature engineering finished! Final features: {len(df.columns)}")
        
        return df