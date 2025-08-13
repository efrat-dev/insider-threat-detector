from pipeline.data_cleaning import DataCleaner
from pipeline.variance_correlation_filter import VarianceCorrelationFilter
from pipeline.feature_normalizer import FeatureNormalizer
from pipeline.feature_creator import FeatureCreator
from pipeline.categorical_encoder import CategoricalEncoder
from pipeline.statistical_transformer import StatisticalTransformer
from pipeline.data_type_converter import DataTypeConverter

import pandas as pd

class PreprocessingPipeline:
    """Complete preprocessing pipeline"""
    
    def __init__(self):
        
        # Initialize all pipeline components
        self.data_cleaner = DataCleaner()
        self.data_type_converter = DataTypeConverter()
        self.feature_creator = FeatureCreator()
        self.categorical_encoder = CategoricalEncoder()
        self.statistical_transformer = StatisticalTransformer()
        self.variance_correlation_filter = VarianceCorrelationFilter()
        self.feature_normalizer = FeatureNormalizer()

        self.is_fitted = False
        self.variance_threshold = None
        self.correlation_threshold = None
        self.selected_features = None
        self.scaler = None
    
    def fit(self, X_train, y_train=None):
        """
        Fit the pipeline on training data only.
        
        Args:
            X_train (DataFrame): Training features
            y_train (Series, optional): Training target variable
            
        Returns:
            self: Returns the fitted pipeline instance
        """
        
        df_train = X_train.copy()
        # Add target to dataframe if provided to maintain alignment during transformations
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

        return self
    
    def transform(self, X):
        """
        Apply the fitted pipeline to new data (train or test).
        
        Args:
            X (DataFrame): Data to transform
            
        Returns:
            DataFrame: Transformed data
            
        Raises:
            ValueError: If pipeline hasn't been fitted yet
        """
        if not self.is_fitted:
            raise ValueError("Pipeline must be fitted before transform")
        
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
        
        return df
    
    def fit_transform(self, X_train, y_train=None):
        """
        Fit and transform training data in one step.
        
        Args:
            X_train (DataFrame): Training features
            y_train (Series, optional): Training target variable
            
        Returns:
            DataFrame: Fitted and transformed training data
        """
        return self.fit(X_train, y_train).transform(X_train)
    
    def _remove_original_columns(self, df: pd.DataFrame, columns_to_remove=None) -> pd.DataFrame:
        """
        Remove original columns after feature creation - these columns are no longer needed 
        since desired features have already been derived from them.
        
        Args:
            df (DataFrame): Input dataframe
            columns_to_remove (list, optional): List of columns to remove
            
        Returns:
            DataFrame: Dataframe with specified columns removed
        """
        if columns_to_remove is None:
            columns_to_remove = ['employee_origin_country', 'country_name',  'modification_details', 'row_modified']
        
        df_processed = df.copy()
        # Only remove columns that actually exist to avoid KeyError
        existing_columns = [col for col in columns_to_remove if col in df_processed.columns]
        
        if existing_columns:
            df_processed = df_processed.drop(columns=existing_columns)
        
        return df_processed
    
    def _standardize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize data types across the dataframe.
        
        Args:
            df (DataFrame): Input dataframe
            
        Returns:
            DataFrame: Dataframe with standardized data types
        """
        exclude_cols = {'first_entry_time', 'last_exit_time', 'date'}

        # Automatic identification of target column
        possible_targets = ['target', 'is_malicious', 'is_emp_malicious']
        target_col = next((col for col in possible_targets if col in df.columns), None)
        
        # Convert boolean columns to numeric
        bool_cols = df.select_dtypes(include=['bool']).columns
        df[bool_cols] = df[bool_cols].astype(int)
        
        # Convert object columns that are actually numeric, excluding special columns
        for col in df.select_dtypes(include=['object']).columns:
            if col not in exclude_cols and (target_col is None or col != target_col):
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
                    pass

        return df