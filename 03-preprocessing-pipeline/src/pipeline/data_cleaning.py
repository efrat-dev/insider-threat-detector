import pandas as pd
import numpy as np

class DataCleaner:
    """Class for data cleaning"""
    
    def __init__(self):
        self.fitted_params = {}
        self.is_fitted = False
    
    def fit_handle_missing_values(self, df):
        """
        Fit missing value handling parameters on training data.
        
        Args:
            df (DataFrame): Training dataframe to fit parameters on
            
        Returns:
            DataFrame: Cleaned dataframe with missing values handled
        """
        
        self.fitted_params['missing_values'] = {}
        
        # Columns with many missing values (based on data)
        travel_columns = ['trip_day_number', 'country_name']
        time_columns = ['first_entry_time', 'last_exit_time']
        derived_time_columns = ['entry_time_numeric', 'exit_time_numeric', 
                               'entry_time_numeric_zscore', 'exit_time_numeric_zscore']
        
        for col in travel_columns:
            if col in df.columns:
                if col == 'trip_day_number':
                    self.fitted_params['missing_values'][col] = {'method': 'fill_zero', 'value': 0}
                elif col == 'country_name':
                    self.fitted_params['missing_values'][col] = {'method': 'fill_constant', 'value': 'No_Travel'}
        
        for col in time_columns:
            if col in df.columns:
                self.fitted_params['missing_values'][col] = {'method': 'fill_datetime', 'value': pd.NaT}
        
        for col in derived_time_columns:
            self.fitted_params['missing_values'][col] = {'method': 'fill_zero', 'value': 0}
        
        if 'total_presence_minutes' in df.columns:
            self.fitted_params['missing_values']['total_presence_minutes'] = {'method': 'fill_zero', 'value': 0}
        
        # Calculate parameters for other numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if (col not in self.fitted_params['missing_values'] and 
                df[col].isnull().sum() > 0 and 
                col not in ['employee_id', 'is_malicious', 'target']):
                
                median_val = df[col].median()
                self.fitted_params['missing_values'][col] = {'method': 'fill_median', 'value': median_val}
        
        # Calculate parameters for categorical columns
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_columns:
            if (col not in self.fitted_params['missing_values'] and 
                df[col].isnull().sum() > 0):
                
                mode_val = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
                self.fitted_params['missing_values'][col] = {'method': 'fill_mode', 'value': mode_val}
        
        self.is_fitted = True
        
        return self.transform_handle_missing_values(df)
    
    def transform_handle_missing_values(self, df):
        """
        Apply missing value handling parameters to new data.
        
        Args:
            df (DataFrame): Dataframe to clean
            
        Returns:
            DataFrame: Cleaned dataframe
            
        Raises:
            ValueError: If DataCleaner hasn't been fitted yet
        """
        if not self.is_fitted:
            raise ValueError("DataCleaner must be fitted before transform")
        
        df_processed = df.copy()
        
        # Apply stored parameters
        for col, params in self.fitted_params['missing_values'].items():
            if col in df_processed.columns and df_processed[col].isnull().sum() > 0:
                method = params['method']
                value = params['value']
                
                if method == 'fill_zero':
                    df_processed[col] = df_processed[col].fillna(0)
                elif method == 'fill_constant':
                    df_processed[col] = df_processed[col].fillna(value)
                elif method == 'fill_median':
                    df_processed[col] = df_processed[col].fillna(value)
                elif method == 'fill_mode':
                    df_processed[col] = df_processed[col].fillna(value)
                elif method == 'fill_datetime':
                    # For datetime columns - use default date representing "non-existent"
                    default_date = pd.Timestamp('1900-01-01')  # Date representing "non-existent"
                    df_processed[col] = df_processed[col].fillna(default_date)
        
        return df_processed
    
    def fit_handle_outliers(self, df, method='cap', threshold=0.05):
        """
        Fit outlier handling parameters on training data.
        
        Args:
            df (DataFrame): Training dataframe to fit parameters on
            method (str): Method for handling outliers ('cap' or 'remove')
            threshold (float): Threshold parameter (not used in current implementation)
            
        Returns:
            DataFrame: Original dataframe (parameters only stored during fit)
        """
        
        if 'outliers' not in self.fitted_params:
            self.fitted_params['outliers'] = {}
        
        self.fitted_params['outliers']['method'] = method
        self.fitted_params['outliers']['bounds'] = {}
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if col in ['employee_id', 'is_malicious', 'is_emp_malicios', 'target']:  # Skip ID and label columns
                continue
            
            # Calculate IQR bounds for outlier detection
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            self.fitted_params['outliers']['bounds'][col] = {
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
        
        return df  # Only store parameters during fit, don't make changes
    
    def transform_handle_outliers(self, df):
        """
        Apply outlier handling parameters to new data.
        
        Args:
            df (DataFrame): Dataframe to process
            
        Returns:
            DataFrame: Dataframe with outliers handled
        """
        if not self.is_fitted or 'outliers' not in self.fitted_params:
            return df

        df_processed = df.copy()
        method = self.fitted_params['outliers']['method']
        exclude_cols = {'first_entry_time', 'last_exit_time', 'date'}

        for col, bounds in self.fitted_params['outliers']['bounds'].items():
            if col in df_processed.columns and col not in exclude_cols:
                lower_bound = bounds['lower_bound']
                upper_bound = bounds['upper_bound']

                if method == 'cap':
                    # Cap values to bounds
                    df_processed[col] = np.where(df_processed[col] < lower_bound, lower_bound, df_processed[col])
                    df_processed[col] = np.where(df_processed[col] > upper_bound, upper_bound, df_processed[col])
                elif method == 'remove':
                    # In transform, don't delete rows, just mark outliers as NaN
                    df_processed[col] = np.where(
                        (df_processed[col] < lower_bound) | (df_processed[col] > upper_bound),
                        np.nan, df_processed[col]
                    )

        return df_processed