from pipeline.data_cleaning import DataCleaner
from pipeline.variance_correlation_filter import VarianceCorrelationFilter
from pipeline.feature_normalizer import FeatureNormalizer
from pipeline.feature_creator import FeatureCreator
from pipeline.categorical_encoder import CategoricalEncoder
from pipeline.statistical_transformer import StatisticalTransformer
from pipeline.data_type_converter import DataTypeConverter

import pandas as pd

class PreprocessingPipeline:
    """Pipeline מלא לעיבוד מקדים ללא זליגת מידע"""
    
    def __init__(self, model_type='isolation-forest'):
        self.model_type = model_type
        
        # Initialize all pipeline components
        self.data_cleaner = DataCleaner()
        self.data_type_converter = DataTypeConverter()
        self.feature_creator = FeatureCreator()
        self.categorical_encoder = CategoricalEncoder()
        self.statistical_transformer = StatisticalTransformer(model_type=model_type)
        self.variance_correlation_filter = VarianceCorrelationFilter()
        self.feature_normalizer = FeatureNormalizer()

        self.is_fitted = False
        self.variance_threshold = None
        self.correlation_threshold = None
        self.selected_features = None
        self.scaler = None
    
    def fit(self, X_train, y_train=None):
        """אימון הפייפליין על נתוני הטריין בלבד"""
        print(f"Fitting preprocessing pipeline on training data for {self.model_type} model...")
        
        df_train = X_train.copy()
        if y_train is not None:
            df_train['target'] = y_train
        
        df_train = self.data_cleaner.fit_handle_missing_values(df_train)
        
        df_train = self.data_type_converter.convert_data_types(df_train)

        df_train = self.feature_creator.create_all_features(df_train)

        df_train = self._remove_original_columns(df_train)

        df_train = self._standardize_data_types(df_train)

        df_train = self.categorical_encoder.fit_encode(df_train)

        df_train = self.statistical_transformer.fit_transform(df_train)

        df_train = self.data_cleaner.fit_handle_outliers(df_train, method='cap')
        
        df_train = self.variance_correlation_filter.fit_variance_filtering(df_train)
        
        df_train = self.variance_correlation_filter.fit_correlation_filtering(df_train)

        self.feature_normalizer.fit_normalize_features(df_train)
        
        self.is_fitted = True
        print("Pipeline fitting completed!")
        return self
    
    def transform(self, X):
        """החלת הפייפליין על דאטה חדש (טריין או טסט)"""
        if not self.is_fitted:
            raise ValueError("Pipeline must be fitted before transform")
        
        print(f"Transforming data using fitted pipeline for {self.model_type} model...")
        df = X.copy()
        
        df = self.data_cleaner.transform_handle_missing_values(df)
        
        df = self.data_type_converter.convert_data_types(df)
        
        df = self.feature_creator.create_all_features(df)

        df = self._remove_original_columns(df)

        df = self._standardize_data_types(df)

        df = self.categorical_encoder.transform_encode(df)

        df = self.statistical_transformer.transform(df)

        df = self.data_cleaner.transform_handle_outliers(df)
        
        df = self.variance_correlation_filter.transform_variance_filtering(df)
        
        df = self.variance_correlation_filter.transform_correlation_filtering(df)

        df = self.feature_normalizer.transform_normalize_features(df)
        
        print(f"Transform completed! Shape: {df.shape}")
        return df
    
    def fit_transform(self, X_train, y_train=None):
        """fit + transform במקום אחד לנתוני הטריין"""
        return self.fit(X_train, y_train).transform(X_train)
    
    def _remove_original_columns(self, df: pd.DataFrame, columns_to_remove=None) -> pd.DataFrame:
        """הסרת עמודות מקוריות לפני הקידוד"""
        if columns_to_remove is None:
            columns_to_remove = ['employee_origin_country', 'country_name',  'modification_details', 'row_modified']
        
        df_processed = df.copy()
        existing_columns = [col for col in columns_to_remove if col in df_processed.columns]
        
        if existing_columns:
            df_processed = df_processed.drop(columns=existing_columns)
            print(f"Removed original columns before encoding: {existing_columns}")
        else:
            print("No original columns found to remove")
        
        return df_processed
    
    def _standardize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """סטנדרטיזציה של טיפוסי נתונים"""
        exclude_cols = {'first_entry_time', 'last_exit_time', 'date'}

        # זיהוי אוטומטי של עמודת המטרה
        possible_targets = ['target', 'is_malicious', 'is_emp_malicious']
        target_col = next((col for col in possible_targets if col in df.columns), None)
        
        # המרת עמודות boolean לנומריות
        bool_cols = df.select_dtypes(include=['bool']).columns
        df[bool_cols] = df[bool_cols].astype(int)
        
        # המרת עמודות object שהן למעשה נומריות, מלבד עמודות מוחרגות
        for col in df.select_dtypes(include=['object']).columns:
            if col not in exclude_cols and (target_col is None or col != target_col):
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
                    pass

        return df