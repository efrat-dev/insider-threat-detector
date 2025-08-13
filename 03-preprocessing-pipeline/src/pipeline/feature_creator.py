import pandas as pd
import numpy as np

class FeatureCreator:
    """Class for creating new features from existing data"""
    
    def __init__(self):
        pass
    
    def create_media_features(self, df):
        """
        Create essential media/burning features.
        
        Args:
            df (DataFrame): Input dataframe
            
        Returns:
            DataFrame: Dataframe with new media-related features
        """
        df_processed = df.copy()
        
        # Use np.maximum to prevent division by zero
        df_processed['avg_burn_volume_per_request'] = df_processed['total_burn_volume_mb'] / np.maximum(df_processed['num_burn_requests'], 1)
        df_processed['burn_intensity'] = df_processed['num_burn_requests'] / np.maximum(df_processed['total_presence_minutes'] / 60, 1)
        
        df_processed['high_classification_burn'] = (df_processed['max_request_classification'] >= 4).astype(int)
        df_processed['classification_variance'] = df_processed['max_request_classification'] / np.maximum(df_processed['avg_request_classification'], 1)
        
        df_processed['off_hours_burn_ratio'] = df_processed['num_burn_requests_off_hours'] / np.maximum(df_processed['num_burn_requests'], 1)
        
        df_processed['is_heavy_burner'] = (df_processed['num_burn_requests'] > df_processed['num_burn_requests'].quantile(0.8)).astype(int)
        
        df_processed['avg_pages_per_print'] = df_processed['total_printed_pages'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['print_intensity'] = df_processed['num_print_commands'] / np.maximum(df_processed['total_presence_minutes'] / 60, 1)
        
        df_processed['off_hours_ratio'] = df_processed['num_print_commands_off_hours'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['is_heavy_printer'] = (df_processed['num_print_commands'] > df_processed['num_print_commands'].quantile(0.8)).astype(int)

        return df_processed
        
    def create_temporal_features(self, df):
        """
        Create time and presence-related features.
        
        Args:
            df (DataFrame): Input dataframe
            
        Returns:
            DataFrame: Dataframe with new temporal features
        """

        df_processed = df.copy()
        
        df_processed['date'] = pd.to_datetime(df_processed['date'], errors='coerce')
        df_processed['weekday'] = df_processed['date'].dt.weekday
        df_processed['month'] = df_processed['date'].dt.month

        df_processed['is_end_of_month'] = (df_processed['date'].dt.day >= 25).astype(int)
        df_processed['is_quarter_end'] = df_processed['month'].isin([3, 6, 9, 12]).astype(int)

        df_processed['first_entry_time'] = pd.to_datetime(df_processed.get('first_entry_time'), errors='coerce')
        df_processed['entry_hour'] = df_processed['first_entry_time'].dt.hour
        df_processed['entry_minute'] = df_processed['first_entry_time'].dt.minute
        df_processed['entry_time_numeric'] = df_processed['entry_hour'] + df_processed['entry_minute'] / 60

        df_processed['last_exit_time'] = pd.to_datetime(df_processed.get('last_exit_time'), errors='coerce')
        df_processed['exit_hour'] = df_processed['last_exit_time'].dt.hour
        df_processed['exit_minute'] = df_processed['last_exit_time'].dt.minute
        df_processed['exit_time_numeric'] = df_processed['exit_hour'] + df_processed['exit_minute'] / 60

        # Remove intermediate hour/minute columns to keep only numeric time representations
        drop_cols = ['entry_hour', 'entry_minute', 'exit_hour', 'exit_minute']
        df_processed = df_processed.drop(columns=[col for col in drop_cols if col in df_processed.columns])

        return df_processed
    
    def create_employee_features(self, df):
        """
        Create essential employee-related features.
        
        Args:
            df (DataFrame): Input dataframe
            
        Returns:
            DataFrame: Dataframe with new employee features
        """
        df_processed = df.copy()
        
        country_name_str = df_processed['country_name'].astype(str) if 'country_name' in df_processed.columns else None
        employee_origin_str = df_processed['employee_origin_country'].astype(str) if 'employee_origin_country' in df_processed.columns else None
        
        # Check if employee works in their country of origin
        if country_name_str is not None and employee_origin_str is not None:
            df_processed['is_employee_in_origin_country'] = (
                country_name_str == employee_origin_str
            ).astype(int)

        df_processed['is_new_employee'] = (df_processed['employee_seniority_years'] < 1).astype(int)
        df_processed['is_veteran_employee'] = (df_processed['employee_seniority_years'] > 10).astype(int)
        
        return df_processed
        
    def create_all_features(self, df):
        """
        Create all new features by applying all feature creation methods.
        
        Args:
            df (DataFrame): Input dataframe
            
        Returns:
            DataFrame: Dataframe with all new features added
        """
        
        df_processed = df.copy()
        df_processed = self.create_temporal_features(df_processed)
        df_processed = self.create_media_features(df_processed)
        df_processed = self.create_employee_features(df_processed)

        return df_processed