from .time_features import TimeFeatureEngineer
from .printing_features import PrintingFeatureEngineer
from .burning_features import BurningFeatureEngineer
from .employee_features import EmployeeFeatureEngineer
from .access_features import AccessFeatureEngineer
from .interaction_features import InteractionFeatureEngineer

class CompleteFeatureEngineer(
    TimeFeatureEngineer,
    PrintingFeatureEngineer,
    BurningFeatureEngineer,
    EmployeeFeatureEngineer,
    AccessFeatureEngineer,
    InteractionFeatureEngineer
):
    """מחלקה מקיפה להנדסת תכונות בסיסיות לזיהוי איומים פנימיים"""
    
    def __init__(self):
        super().__init__()
    
    def create_all_basic_features(self, df):
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