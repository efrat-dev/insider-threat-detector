import numpy as np
from sklearn.feature_selection import VarianceThreshold


class VarianceCorrelationFilter:
    """Class for filtering features based on variance and correlation"""
    
    def __init__(self):
        self.variance_threshold = None
        self.correlation_threshold = 0.95
        self.variance_filtered_features_ = []
        self.correlation_filtered_features_ = []
        
    def _is_protected_column(self, col_name):
        """
        Check if column is protected (contains zscore).
        
        Args:
            col_name (str): Column name to check
            
        Returns:
            bool: True if column is protected from filtering
        """
        return 'zscore' in col_name.lower() 
        
    def fit_variance_filtering(self, df, threshold=0.01):
        """
        Filter features with low variance.
        
        Args:
            df (DataFrame): Input dataframe
            threshold (float): Variance threshold for filtering
            
        Returns:
            DataFrame: Dataframe with low variance features removed
        """
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'target' in numeric_cols:
            numeric_cols.remove('target')
        
        if len(numeric_cols) == 0:
            self.variance_filtered_features_ = df.columns.tolist()
            return df
        
        protected_cols = [col for col in numeric_cols if self._is_protected_column(col)]
        regular_cols = [col for col in numeric_cols if not self._is_protected_column(col)]
        
        if len(regular_cols) == 0:
            self.variance_filtered_features_ = df.columns.tolist()
            return df
        
        # Create VarianceThreshold only for regular columns
        self.variance_threshold = VarianceThreshold(threshold=threshold)
        
        self.variance_threshold.fit(df[regular_cols])
        
        # Get names of regular features that remain after filtering
        selected_regular = [col for col, selected in 
                           zip(regular_cols, self.variance_threshold.get_support()) 
                           if selected]
        
        # Store list of remaining features (regular + protected + non-numeric)
        non_numeric_cols = [col for col in df.columns if col not in numeric_cols]
        self.variance_filtered_features_ = selected_regular + protected_cols + non_numeric_cols
                
        return df[self.variance_filtered_features_]
    
    def transform_variance_filtering(self, df):
        """
        Apply variance filtering to new data.
        
        Args:
            df (DataFrame): Input dataframe to transform
            
        Returns:
            DataFrame: Filtered dataframe
            
        Raises:
            ValueError: If variance filtering hasn't been fitted yet
        """
        if self.variance_threshold is None:
            raise ValueError("Variance filtering not fitted yet")
        
        available_features = [col for col in self.variance_filtered_features_ if col in df.columns]
                
        return df[available_features]
    
    def fit_correlation_filtering(self, df, threshold=0.95):
        """
        Filter features with high correlation.
        
        Args:
            df (DataFrame): Input dataframe
            threshold (float): Correlation threshold for filtering
            
        Returns:
            DataFrame: Dataframe with highly correlated features removed
        """
        
        self.correlation_threshold = threshold
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'target' in numeric_cols:
            numeric_cols.remove('target')
        
        if len(numeric_cols) <= 1:
            self.correlation_filtered_features_ = df.columns.tolist()
            return df
        
        protected_cols = [col for col in numeric_cols if self._is_protected_column(col)]
        regular_cols = [col for col in numeric_cols if not self._is_protected_column(col)]
        
        if len(regular_cols) <= 1:
            self.correlation_filtered_features_ = df.columns.tolist()
            return df
        
        # Calculate correlation matrix only for regular columns
        corr_matrix = df[regular_cols].corr().abs()
        
        # Find pairs of features with high correlation using upper triangle
        upper_tri = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        
        to_drop = [column for column in upper_tri.columns 
                  if any(upper_tri[column] > threshold)]
        
        remaining_regular = [col for col in regular_cols if col not in to_drop]
        non_numeric_cols = [col for col in df.columns if col not in numeric_cols]
        self.correlation_filtered_features_ = remaining_regular + protected_cols + non_numeric_cols
                
        return df[self.correlation_filtered_features_]
    
    def transform_correlation_filtering(self, df):
        """
        Apply correlation filtering to new data.
        
        Args:
            df (DataFrame): Input dataframe to transform
            
        Returns:
            DataFrame: Filtered dataframe
            
        Raises:
            ValueError: If correlation filtering hasn't been fitted yet
        """
        if not hasattr(self, 'correlation_filtered_features_'):
            raise ValueError("Correlation filtering not fitted yet")
        
        # Filter features to only include those that exist in the current dataframe
        available_features = [col for col in self.correlation_filtered_features_ if col in df.columns]
                
        return df[available_features]