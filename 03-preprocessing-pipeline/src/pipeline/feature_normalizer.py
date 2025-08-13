import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

class FeatureNormalizer:
    """Class for feature normalization"""
    
    def __init__(self):
        self.scaler = None        
        self.fitted_params = {}
        self.scalers = {}
        
    
    def fit_normalize_features(self, df, method='standard'):
        """
        Fit normalization parameters on training data.
        
        Args:
            df (DataFrame): Training dataframe to fit normalization on
            method (str): Normalization method ('standard', 'minmax', or 'robust')
            
        Returns:
            DataFrame: Original dataframe (unchanged during fit)
        """
        
        self.fitted_params['normalization'] = {
            'method': method
        }
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        exclude_cols = ['employee_id', 'is_malicious', 'is_emp_malicious_binary', 'target', 'date', 'first_entry_time', 'last_exit_time']
        numeric_columns = [col for col in numeric_columns if col not in exclude_cols]
        
        # Store list of columns for normalization
        self.fitted_params['normalization']['columns_to_normalize'] = numeric_columns
        
        if len(numeric_columns) == 0:
            print("No numeric columns found for normalization")
            return df
        
        # Fit the appropriate scaler
        if method == 'standard':
            scaler = StandardScaler()
            scaler.fit(df[numeric_columns])
            self.scalers['standard'] = scaler
        
        elif method == 'minmax':
            scaler = MinMaxScaler()
            scaler.fit(df[numeric_columns])
            self.scalers['minmax'] = scaler
        
        elif method == 'robust':
            scaler = RobustScaler()
            scaler.fit(df[numeric_columns])
            self.scalers['robust'] = scaler
        
        return df  # Don't modify data during fit
    
    def transform_normalize_features(self, df):
        """
        Apply normalization using fitted parameters.
        
        Args:
            df (DataFrame): Dataframe to normalize
            
        Returns:
            DataFrame: Normalized dataframe
            
        Raises:
            ValueError: If normalization hasn't been fitted yet or scaler not found
        """
        if not self.fitted_params.get('normalization'):
            raise ValueError("Normalization must be fitted before transform")
                
        df_processed = df.copy()
        method = self.fitted_params['normalization']['method']
        columns_to_normalize = self.fitted_params['normalization']['columns_to_normalize']
        
        # Columns that exist in the new data
        available_columns = [col for col in columns_to_normalize if col in df_processed.columns]
        
        if len(available_columns) == 0:
            return df_processed
        
        # Check for missing columns (potential data drift)
        if len(available_columns) != len(columns_to_normalize):
            missing_cols = set(columns_to_normalize) - set(available_columns)
            print(f"Warning: {len(missing_cols)} normalization columns missing in transform data")
        
        # Apply the appropriate scaler
        scaler = self.scalers.get(method)
        if scaler is None:
            raise ValueError(f"Scaler for method '{method}' not found")
        
        try:
            df_processed[available_columns] = scaler.transform(df_processed[available_columns])
        except Exception as e:
            print(f"Error in normalization: {str(e)}")
            
        return df_processed