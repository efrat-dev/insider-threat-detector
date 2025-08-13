import numpy as np
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class StatisticalTransformer:
    """Special class for statistical transformations - Z-score and quartiles according to model type"""
    
    def __init__(self):
        self.scalers = {}
        self.fitted_params = {}
        self.is_fitted = False
        
    def fit(self, df):
        """
        Fit statistical transformation parameters on training data.
        
        Args:
            df (DataFrame): Training dataframe to fit parameters on
            
        Returns:
            DataFrame: Original dataframe (unchanged)
        """
        
        # Reset parameters
        self.fitted_params = {}
        self.scalers = {}
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        exclude_cols = ['is_malicious', 'is_emp_malicious', 'target', 'date', 'timestamp', 'employee_id']
        transform_columns = [col for col in numeric_columns if col not in exclude_cols]
        
        self.fitted_params['transform_columns'] = transform_columns
                
        successful_fits = 0
        
        for col in transform_columns:
            if col in df.columns:
                # Data validity check
                if df[col].isna().all():
                    print(f"Skipping column {col} - all values are NaN")
                    continue
                
                # Store parameters for each column
                col_params = {}
                
                try:
                    col_params['std'] = df[col].std()
                    col_params['has_variance'] = col_params['std'] > 0
                    col_params['unique_values'] = df[col].nunique()
                    col_params['min_val'] = df[col].min()
                    col_params['max_val'] = df[col].max()
                    
                    if col_params['has_variance']:
                        scaler = StandardScaler()
                        scaler.fit(df[col].values.reshape(-1, 1))
                        self.scalers[col] = scaler
                    
                    self.fitted_params[col] = col_params
                    successful_fits += 1
                    
                except Exception as e:
                    print(f"Error fitting parameters for column {col}: {str(e)}")
                    continue
        
        self.is_fitted = True
            
        return df  
    
    def transform(self, df):
        """
        Apply statistical transformations using fitted parameters.
        
        Args:
            df (DataFrame): Dataframe to transform
            
        Returns:
            DataFrame: Transformed dataframe with new statistical features
            
        Raises:
            ValueError: If transformer hasn't been fitted yet
        """
        if not self.is_fitted:
            raise ValueError("StatisticalTransformer must be fitted before transform")
        
        df_processed = df.copy()
        
        transform_columns = self.fitted_params.get('transform_columns', [])
        zscore_successes = 0
        
        for col in transform_columns:
            if col not in df_processed.columns or col not in self.fitted_params:
                continue
            
            col_params = self.fitted_params[col]
            
            try:
                # Apply Z-score transformation only if column has variance and scaler exists
                if col_params.get('has_variance', False) and col in self.scalers:
                    try:
                        df_processed[f'{col}_zscore'] = self.scalers[col].transform(
                            df_processed[col].values.reshape(-1, 1)
                        ).flatten()
                        zscore_successes += 1
                    except Exception as e:
                        print(f"Error applying Z-score to {col}: {str(e)}")
                        continue
                
            except Exception as e:
                print(f"Error transforming column {col}: {str(e)}")
                continue
                
        return df_processed
    
    def fit_transform(self, df):
        """
        Fit and transform in one step.
        
        Args:
            df (DataFrame): Dataframe to fit and transform
            
        Returns:
            DataFrame: Transformed dataframe
        """
        self.fit(df)
        return self.transform(df)