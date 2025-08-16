"""
Synthetic Data Noise Injection Module - Default Low Noise Version
-------------------------------------------------
Adds realistic and controlled synthetic noise to numeric, binary, and entry time fields,
while maintaining consistency between dependent fields.
"""

import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging


class DataNoiseInjector:
    """Class for injecting noise into synthetic data"""
    
    def __init__(self, burn_noise_rate: float = 0.05,
                 print_noise_rate: float = 0.05,
                 entry_time_noise_rate: float = 0.10,
                 use_gaussian: bool = False,
                 random_seed: Optional[int] = None):
        """
        Initialize the noise injection class
        
        Args:
            burn_noise_rate: Percentage of rows affected by burn noise (default: 5%)
            print_noise_rate: Percentage of rows affected by print noise (default: 5%)
            entry_time_noise_rate: Percentage of rows affected by entry time noise (default: 10%)
            use_gaussian: Whether to use Gaussian noise for certain fields
            random_seed: Random seed for reproducibility
        """
        self.burn_noise_rate = burn_noise_rate
        self.print_noise_rate = print_noise_rate
        self.entry_time_noise_rate = entry_time_noise_rate
        self.use_gaussian = use_gaussian
        
        if random_seed is not None:
            random.seed(random_seed)
            np.random.seed(random_seed)
        
        self.logger = logging.getLogger(__name__)
        self.statistics = {
            'total_rows': 0,
            'modified_rows': 0,
            'burn_modifications': 0,
            'print_modifications': 0,
            'entry_time_modifications': 0
        }
    
    def inject_burn_noise(self, row: pd.Series, changes: List[str]) -> pd.Series:
        """Inject burn activity noise - low intensity version"""
        if random.random() < self.burn_noise_rate:
            self.statistics['burn_modifications'] += 1
            
            # Total burn requests 
            if self.use_gaussian:
                delta_burns = max(1, int(np.random.normal(2, 1)))
            else:
                delta_burns = random.randint(1, 3) 
            row['num_burn_requests'] += delta_burns
            changes.append(f"num_burn_requests += {delta_burns}")
            
            # Total files burned 
            if self.use_gaussian:
                delta_files = max(1, int(np.random.normal(6, 4)))
            else:
                delta_files = random.randint(2, 10)  
            row['total_files_burned'] += delta_files
            changes.append(f"total_files_burned += {delta_files}")
            
            # Total burn volume MB 
            if self.use_gaussian:
                delta_mb = max(50, int(np.random.normal(175, 75)))
            else:
                delta_mb = random.randint(50, 300)  
            row['total_burn_volume_mb'] += delta_mb
            changes.append(f"total_burn_volume_mb += {delta_mb}")
            
            # Off-hours burn requests 
            if random.random() < 0.3:
                additional_off_hours = 1
                row['num_burn_requests_off_hours'] += additional_off_hours
                changes.append(f"num_burn_requests_off_hours += {additional_off_hours}")
            
            # Average request classification
            if self.use_gaussian:
                delta_avg = np.random.normal(0, 0.3)
            else:
                delta_avg = round(random.uniform(-0.4, 0.4), 2)
            row['avg_request_classification'] = max(0, min(4, row['avg_request_classification'] + delta_avg))
            changes.append(f"avg_request_classification adjusted by {delta_avg}")
            
            # Max request classification 
            if random.random() < 0.05 and row['max_request_classification'] < 4:
                increment = 1
                row['max_request_classification'] = min(4, row['max_request_classification'] + increment)
                changes.append(f"max_request_classification +{increment}")
            
            # Number of burn campuses 
            if random.random() < 0.03:
                if row['burn_campuses'] < 2:
                    old_campuses = row['burn_campuses']
                    row['burn_campuses'] += 1
                    changes.append(f"burn_campuses: {old_campuses} → {row['burn_campuses']}")
                
                if row['burn_campuses'] > 1:
                    row['burned_from_other'] = 1
                    changes.append("burned_from_other set to 1")
        
        return row
    
    def inject_print_noise(self, row: pd.Series, changes: List[str]) -> pd.Series:
        """Inject print activity noise - low intensity version"""
        if row['num_print_commands'] > 0 and random.random() < self.print_noise_rate:
            self.statistics['print_modifications'] += 1
            
            # Number of print commands 
            if self.use_gaussian:
                noise_factor = max(0.05, np.random.normal(0.15, 0.05))
            else:
                noise_factor = random.uniform(0.05, 0.2)
            delta_prints = max(1, int(row['num_print_commands'] * noise_factor))
            row['num_print_commands'] += delta_prints
            changes.append(f"num_print_commands += {delta_prints}")
            
            # Adjust total printed pages accordingly
            old_prints = max(row['num_print_commands'] - delta_prints, 1)
            pages_per_print = row['total_printed_pages'] / old_prints
            additional_pages = int(delta_prints * pages_per_print)
            row['total_printed_pages'] += additional_pages
            changes.append(f"total_printed_pages += {additional_pages}")
            
            # Ratio of color prints
            if self.use_gaussian:
                color_delta = np.random.normal(0, 0.03)
            else:
                color_delta = random.uniform(-0.05, 0.05)
            row['ratio_color_prints'] = min(1.0, max(0.0, row['ratio_color_prints'] + color_delta))
            changes.append(f"ratio_color_prints adjusted by {color_delta:.3f}")
            
            # Off-hours print commands  
            if random.random() < 0.3:
                additional_off_hours = 1
                row['num_print_commands_off_hours'] += additional_off_hours
                changes.append(f"num_print_commands_off_hours += {additional_off_hours}")
        
        return row
    
    def inject_entry_time_noise(self, row: pd.Series, changes: List[str]) -> pd.Series:
        """Inject noise into first entry time - low intensity version"""
        if pd.notna(row['first_entry_time']) and random.random() < self.entry_time_noise_rate:
            self.statistics['entry_time_modifications'] += 1
            
            try:
                # Modify entry time by a small amount
                t = datetime.strptime(row['first_entry_time'], "%H:%M")
                if self.use_gaussian:
                    delta_minutes = int(np.random.normal(0, 7))
                else:
                    delta_minutes = random.randint(-10, 10)
                
                new_time = (datetime.combine(datetime.today(), t.time()) + timedelta(minutes=delta_minutes)).time()
                row['first_entry_time'] = new_time.strftime("%H:%M")
                changes.append(f"first_entry_time shifted by {delta_minutes} mins")
                
                # Update dependent flags
                hour = new_time.hour
                row['entered_during_night_hours'] = 1 if hour < 6 or hour >= 22 else 0
                row['early_entry_flag'] = 1 if hour < 7 else 0
                changes.append("updated night and early entry flags")
                
            except Exception as e:
                self.logger.warning(f"Failed to parse entry time: {row['first_entry_time']}, error: {e}")
        
        return row
    
    def inject_full_noise(self, row: pd.Series) -> pd.Series:
        """Inject full noise into a single row"""
        changes = []
        
        # Inject noise for all data types
        row = self.inject_burn_noise(row, changes)
        row = self.inject_print_noise(row, changes)
        row = self.inject_entry_time_noise(row, changes)
        
        # Record modifications
        if changes:
            row['row_modified'] = True
            row['modification_details'] = "; ".join(changes)
            self.statistics['modified_rows'] += 1
        else:
            row['row_modified'] = False
            row['modification_details'] = ""
        
        return row
    
    def add_noise_to_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add noise to an entire DataFrame
        
        Args:
            df: Original DataFrame
            
        Returns:
            DataFrame with injected noise
        """
        self.logger.info(f"Starting noise injection for {len(df)} rows")
        self.statistics['total_rows'] = len(df)
        
        # Add documentation columns if missing
        if 'row_modified' not in df.columns:
            df['row_modified'] = False
        if 'modification_details' not in df.columns:
            df['modification_details'] = ""
        
        # Apply noise injection row-wise
        df_noised = df.apply(self.inject_full_noise, axis=1)
        
        self.logger.info(f"Noise injection completed. Modified {self.statistics['modified_rows']} out of {self.statistics['total_rows']} rows")
        return df_noised
    
    def get_statistics(self) -> Dict:
        """Return statistics about the noise added"""
        return self.statistics.copy()