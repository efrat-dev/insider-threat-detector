    # File 5: feature_summary.py (Summary and reporting - 80 lines)
import pandas as pd
from typing import Dict, List

class FeatureSummary:
    """סיכום ודיווח תכונות"""
    
    def __init__(self, factory):
        self.factory = factory
        self.feature_patterns = {
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
    
    def get_feature_summary(self, df: pd.DataFrame) -> Dict:
        """סיכום מקיף של התכונות"""
        summary = {}
        
        for group, patterns in self.feature_patterns.items():
            matching_features = [
                col for col in df.columns 
                if any(pattern in col.lower() for pattern in patterns)
            ]
            
            summary[group] = {
                'count': len(matching_features),
                'features': matching_features[:5] if matching_features else []
            }
        
        summary['total_features'] = len(df.columns)
        summary['available_engineers'] = self.get_available_engineers()
        return summary
    
    def get_available_engineers(self) -> List[str]:
        """רשימת מהנדסים זמינים"""
        return [name for name, eng in self.factory.engineers.items() if eng is not None]
    
    def get_feature_types_summary(self, df: pd.DataFrame) -> Dict:
        """סיכום סוגי תכונות"""
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        boolean_cols = df.select_dtypes(include=['bool']).columns.tolist()
        
        return {
            'numeric': {'count': len(numeric_cols), 'sample': numeric_cols[:5]},
            'categorical': {'count': len(categorical_cols), 'sample': categorical_cols[:5]},
            'boolean': {'count': len(boolean_cols), 'sample': boolean_cols[:5]},
            'total': len(df.columns)
        }
    
    def get_missing_values_summary(self, df: pd.DataFrame) -> Dict:
        """סיכום ערכים חסרים"""
        missing_counts = df.isnull().sum()
        missing_features = missing_counts[missing_counts > 0].sort_values(ascending=False)
        
        return {
            'total_missing_features': len(missing_features),
            'worst_features': missing_features.head(5).to_dict(),
            'missing_percentage': (missing_features / len(df) * 100).head(5).to_dict()
        }
    
    def get_interaction_feature_summary(self, df: pd.DataFrame) -> Dict:
        """סיכום תכונות אינטראקציה"""
        return self.factory.safe_engineer_call('advanced_interaction', 'get_interaction_feature_summary', df)
    
    def get_anomaly_feature_summary(self, df: pd.DataFrame) -> Dict:
        """סיכום תכונות חריגות"""
        return self.factory.safe_engineer_call('anomaly', 'get_anomaly_feature_summary', df)
    
    def get_comprehensive_report(self, df: pd.DataFrame) -> Dict:
        """דוח מקיף על המערכת"""
        return {
            'feature_summary': self.get_feature_summary(df),
            'feature_types': self.get_feature_types_summary(df),
            'missing_values': self.get_missing_values_summary(df),
            'available_engineers': self.get_available_engineers(),
            'total_features': len(df.columns),
            'total_rows': len(df)
        }