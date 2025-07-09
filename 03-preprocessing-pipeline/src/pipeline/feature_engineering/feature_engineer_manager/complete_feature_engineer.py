    # File 1: complete_feature_engineer.py (Main class - 38 lines)
from typing import Dict, List
import pandas as pd
from .engineer_factory import EngineerFactory
from .feature_pipeline import FeaturePipeline
from .feature_optimizer import FeatureOptimizer
from .feature_summary import FeatureSummary
from pipeline.feature_engineering.basic.base_feature_engineer import BaseFeatureEngineer

class CompleteFeatureEngineer(BaseFeatureEngineer):
    """מחלקה מקיפה להנדסת תכונות בסיסיות ומתקדמות לזיהוי איומים פנימיים"""
    
    def __init__(self):
        super().__init__()
        self.factory = EngineerFactory()
        self.pipeline = FeaturePipeline(self.factory)
        self.optimizer = FeatureOptimizer(self.factory)
        self.summary = FeatureSummary(self.factory)
        
    def create_features_by_type(self, df: pd.DataFrame, feature_type: str) -> pd.DataFrame:
        return self.factory.create_features_by_type(df, feature_type)
    
    def create_polynomial_features(self, df: pd.DataFrame, degree: int = 2, selected_features: List[str] = None) -> pd.DataFrame:
        return self.factory.safe_engineer_call('advanced_interaction', 'create_polynomial_features', df, degree, selected_features)
    
    def create_ratio_features(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.factory.safe_engineer_call('advanced_interaction', 'create_ratio_features', df)
    
    def create_statistical_anomalies(self, df: pd.DataFrame, threshold: float = 2.5) -> pd.DataFrame:
        return self.factory.safe_engineer_call('anomaly', 'create_statistical_anomalies', df, threshold)
    
    def analyze_feature_quality(self, df: pd.DataFrame, target_col: str) -> Dict:
        return self.factory.get_analyzer_result('analyze_feature_quality', df, target_col)
    
    def get_recommended_features(self, df: pd.DataFrame, target_col: str) -> List[str]:
        return self.factory.get_analyzer_result('get_recommended_features', df, target_col)
    
    def identify_redundant_features(self, df: pd.DataFrame) -> List[str]:
        return self.factory.get_analyzer_result('identify_redundant_features', df)
    
    def apply_complete_feature_engineering(self, df: pd.DataFrame, target_col: str = 'is_malicious') -> pd.DataFrame:
        return self.pipeline.apply_complete_feature_engineering(df, target_col)
    
    def optimize_feature_set(self, df: pd.DataFrame, target_col: str = 'is_malicious') -> pd.DataFrame:
        return self.optimizer.optimize_feature_set(df, target_col)
    
    def get_feature_summary(self, df: pd.DataFrame) -> Dict:
        return self.summary.get_feature_summary(df)