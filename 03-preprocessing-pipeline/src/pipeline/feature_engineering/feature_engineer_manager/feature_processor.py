# File 3b: feature_processor.py (Data Processing and Encoding - 70 lines)
import numpy as np
import pandas as pd

class FeatureProcessor:
    """מעבד נתונים וקידוד לפיצ'רים"""
    
    def __init__(self, factory):
        self.factory = factory
        self.base_encoder = None
    
    def _initialize_encoder(self):
        """אתחול encoder בסיסי"""
        if not hasattr(self, 'base_encoder') or self.base_encoder is None:
            from pipeline.feature_engineering.basic.base_feature_engineer import BaseFeatureEngineer
            self.base_encoder = BaseFeatureEngineer()
    
    def apply_encoding_transforms(self, df: pd.DataFrame, target_col: str) -> pd.DataFrame:
        """קידוד ועיבוד מקיף"""
        print("Starting encoding and transformation phase...")
        
        # שלב 1: קידוד משתנים קטגוריים
        try:
            self._initialize_encoder()
            df = self.base_encoder.encode_categorical_variables(df, target_col)
            print("Categorical encoding completed")
        except Exception as e:
            print(f"Error in categorical encoding: {e}")
        
        # שלב 2: טיפול בעמודות טקסט מיוחדות
        try:
            df = self.base_encoder.handle_special_text_columns(df)
            print("Special text columns handled")
        except Exception as e:
            print(f"Error in text processing: {e}")
        
        # שלב 3: טרנספורמציות סטטיסטיות
        try:
            df = self.base_encoder.apply_statistical_transforms(df)
            print("Statistical transforms applied")
        except Exception as e:
            print(f"Error in statistical transforms: {e}")
        
        # שלב 4: טיפול בערכים חסרים
        try:
            df = self._handle_missing_values(df)
            print("Missing values handled")
        except Exception as e:
            print(f"Error in missing values handling: {e}")
        
        # שלב 5: וידוא טיפוסי נתונים
        try:
            df = self._standardize_data_types(df, target_col)
            print("Data types standardized")
        except Exception as e:
            print(f"Error in data type standardization: {e}")
        
        print(f"Encoding and transformation completed! Features: {len(df.columns)}")
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """טיפול בערכים חסרים"""
        # מילוי ערכים חסרים בעמודות נומריות
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)
        
        # מילוי ערכים חסרים בעמודות קטגוריות
        categorical_cols = df.select_dtypes(include=['object']).columns
        df[categorical_cols] = df[categorical_cols].fillna('unknown')
        
        return df
    
    def _standardize_data_types(self, df: pd.DataFrame, target_col: str) -> pd.DataFrame:
        """סטנדרטיזציה של טיפוסי נתונים"""
        # המרת עמודות boolean לנומריות
        bool_cols = df.select_dtypes(include=['bool']).columns
        df[bool_cols] = df[bool_cols].astype(int)
        
        # המרת עמודות object שהן למעשה נומריות
        for col in df.select_dtypes(include=['object']).columns:
            if col != target_col:
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
                    pass
        
        return df