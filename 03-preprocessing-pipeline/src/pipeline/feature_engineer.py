# feature_pipeline.py - Unified Feature Pipeline Module
import pandas as pd
from .categorical_encoder import CategoricalEncoder
from .statistical_transformer import StatisticalTransformer
from .feature_creator import FeatureCreator

class FeatureEngineer:
    """מנהל pipeline של הנדסת תכונות - כולל גם עיבוד וקידוד נתונים"""
    
    def __init__(self):
        self.categorical_encoder = CategoricalEncoder()
        self.statistical_transformer = StatisticalTransformer()
        self.feature_creator = FeatureCreator()

    
    def remove_original_columns(self, df: pd.DataFrame, columns_to_remove=None) -> pd.DataFrame:
        """הסרת עמודות מקוריות לפני הקידוד"""
        if columns_to_remove is None:
            columns_to_remove = ['employee_origin_country', 'country_name', 'first_entry_time', 'last_exit_time', 'date', 'modification_details', 'row_modified']
        
        df_processed = df.copy()
        existing_columns = [col for col in columns_to_remove if col in df_processed.columns]
        
        if existing_columns:
            df_processed = df_processed.drop(columns=existing_columns)
            print(f"Removed original columns before encoding: {existing_columns}")
        else:
            print("No original columns found to remove")
        
        return df_processed
    
    def standardize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """סטנדרטיזציה של טיפוסי נתונים"""
        # זיהוי אוטומטי של עמודת המטרה
        possible_targets = ['target', 'is_malicious', 'is_emp_malicious']
        target_col = next((col for col in possible_targets if col in df.columns), None)
        
        # המרת עמודות boolean לנומריות
        bool_cols = df.select_dtypes(include=['bool']).columns
        df[bool_cols] = df[bool_cols].astype(int)
        
        # המרת עמודות object שהן למעשה נומריות
        for col in df.select_dtypes(include=['object']).columns:
            if target_col is None or col != target_col:
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
                    pass
        
        return df
    
    def fit_apply_all_feature_engineering(self, df):
            """הפעלת כל שלבי הנדסת התכונות + fit על encoding וטרנספורמציות"""
            print("Starting comprehensive feature engineering with fitting...")
            
            # שלב 1: יצירת תכונות בסיסית
            df_processed = self.feature_creator.create_all_features(df)
            df_processed = self.remove_original_columns(df_processed)
            df_processed = self.standardize_data_types(df_processed)
            
            # שלב 2: fit + encoding קטגוריאלי
            print("Fitting and applying categorical encoding...")
            df_processed = self.categorical_encoder.fit_encode(df_processed)
            
            # שלב 3: fit + טרנספורמציות סטטיסטיות
            print("Fitting and applying statistical transformations...")
            df_processed = self.statistical_transformer.fit_transform(df_processed)
            
            self.is_fitted = True
            print(f"Feature engineering with fitting completed. Final shape: {df_processed.shape}")
            return df_processed
        
    def transform_apply_all_feature_engineering(self, df):
            """הפעלת כל שלבי הנדסת התכונות + transform על encoding וטרנספורמציות"""
            if not self.is_fitted:
                raise ValueError("FeatureEngineer must be fitted before transform")
            
            print("Starting comprehensive feature engineering with transform...")
            
            # שלב 1: יצירת תכונות בסיסית
            df_processed = self.feature_creator.create_all_features(df)
            df_processed = self.remove_original_columns(df_processed)
            df_processed = self.standardize_data_types(df_processed)
            
            # שלב 2: transform encoding קטגוריאלי
            print("Applying categorical encoding transform...")
            df_processed = self.categorical_encoder.transform_encode(df_processed)
            
            # שלב 3: transform טרנספורמציות סטטיסטיות
            print("Applying statistical transformations transform...")
            df_processed = self.statistical_transformer.transform(df_processed)
            
            print(f"Feature engineering transform completed. Final shape: {df_processed.shape}")
            return df_processed