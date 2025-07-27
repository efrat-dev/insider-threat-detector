from pipeline.data_cleaning import DataCleaner
from pipeline.data_transformation import DataTransformer
from .feature_engineer import FeatureEngineer
from .feature_creator import FeatureCreator
import pandas as pd

class PreprocessingPipeline:
    """Pipeline מלא לעיבוד מקדים ללא זליגת מידע"""
    
    def __init__(self):
        self.data_cleaner = DataCleaner()
        self.data_transformer = DataTransformer()
        self.feature_engineer = FeatureEngineer()
        self.feature_creator = FeatureCreator()

        self.fitted_params = {}
        self.is_fitted = False
    
    def fit(self, X_train, y_train=None):
        """אימון הפייפליין על נתוני הטריין בלבד"""
        print("Fitting preprocessing pipeline on training data...")
        
        df_train = X_train.copy()
        if y_train is not None:
            df_train['target'] = y_train
        
        df_train = self.data_cleaner.fit_handle_missing_values(df_train)
        
        df_train = self.data_cleaner.convert_data_types(df_train)

        df_train = self.feature_engineer.fit_apply_all_feature_engineering(df_train)

        df_train = self.data_cleaner.fit_handle_outliers(df_train, method='cap')
        
        df_train = self.data_transformer.fit_feature_filtering(df_train)
        
        self.data_transformer.fit_normalize_features(df_train)
        
        self.is_fitted = True
        print("Pipeline fitting completed!")
        return self
    
    def transform(self, X):
        """החלת הפייפליין על דאטה חדש (טריין או טסט)"""
        if not self.is_fitted:
            raise ValueError("Pipeline must be fitted before transform")
        
        print("Transforming data using fitted pipeline...")
        df = X.copy()
        
        df = self.data_cleaner.transform_handle_missing_values(df)
        
        df = self.data_cleaner.convert_data_types(df)
        
        df = self.feature_engineer.transform_apply_all_feature_engineering(df)

        df = self.data_cleaner.transform_handle_outliers(df)
        
        df = self.data_transformer.transform_feature_filtering(df)
        
        df = self.data_transformer.transform_normalize_features(df)
        
        print(f"Transform completed! Shape: {df.shape}")
        return df
    
    def fit_transform(self, X_train, y_train=None):
        """fit + transform במקום אחד לנתוני הטריין"""
        return self.fit(X_train, y_train).transform(X_train)