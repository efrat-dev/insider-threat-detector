    # File 2: engineer_factory.py (Factory for engineers - 53 lines)
from typing import Dict, List, Any
import pandas as pd
from ..basic.time_features import TimeFeatureEngineer
from ..basic.printing_features import PrintingFeatureEngineer
from ..basic.burning_features import BurningFeatureEngineer
from ..basic.employee_features import EmployeeFeatureEngineer
from ..basic.access_features import AccessFeatureEngineer
from ..basic.interaction_features import InteractionFeatureEngineer
from ..advanced.behavioral_features import BehavioralFeatureEngineer
from ..advanced.temporal_features import TemporalFeatureEngineer
from ..advanced.risk_profile_features import RiskProfileFeatureEngineer
from ..advanced.anomaly_features import AnomalyFeatureEngineer
from ..advanced.advanced_interaction_features import AdvancedInteractionFeatureEngineer
from ..advanced.feature_analysis import FeatureAnalyzer

class EngineerFactory:
    """מפעל ליצירת ולניהול מהנדסי תכונות"""
    
    def __init__(self):
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
            'analyzer': (FeatureAnalyzer, None)
        }
        self.engineers = {}
        self._init_engineers()
    
    def _init_engineers(self):
        """אתחול כל מהנדסי התכונות"""
        for name, (engineer_class, _) in self.engineer_config.items():
            try:
                self.engineers[name] = engineer_class()
            except Exception as e:
                print(f"Warning: Could not initialize {name}: {e}")
                self.engineers[name] = None
    
    def safe_engineer_call(self, engineer_name: str, method_name: str, df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
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
    
    def create_features_by_type(self, df: pd.DataFrame, feature_type: str) -> pd.DataFrame:
        """יצירת תכונות לפי סוג"""
        if feature_type not in self.engineer_config:
            print(f"Unknown feature type: {feature_type}")
            return df
        _, method_name = self.engineer_config[feature_type]
        if method_name:
            return self.safe_engineer_call(feature_type, method_name, df)
        return df
    
    def get_analyzer_result(self, method_name: str, df: pd.DataFrame, *args, **kwargs):
        """קריאה אחודה לאנליזה"""
        analyzer = self.engineers.get('analyzer')
        if analyzer:
            try:
                method = getattr(analyzer, method_name)
                return method(df, *args, **kwargs)
            except Exception as e:
                print(f"Error in {method_name}: {e}")
        return None    
