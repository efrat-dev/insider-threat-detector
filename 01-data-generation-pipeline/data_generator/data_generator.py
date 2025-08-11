import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from .data_generator_core import DataGeneratorCore
from core.date_noise_injector import DataNoiseInjector


class DataGenerator(DataGeneratorCore):
    """Main data generation engine that orchestrates all activities"""
    
    def __init__(self, employees: dict, days_range: int = 180, malicious_ratio: float = 0.05,
                 add_noise: bool = False, noise_config: Optional[Dict[str, Any]] = None):
        super().__init__(employees, days_range, malicious_ratio)
        
        # Initialize noise injector if requested
        self.add_noise = add_noise
        self.noise_injector = None
        
        if add_noise:
            if noise_config:
                mapped_config = {}
                param_mapping = {
                    'burn_rate': 'burn_noise_rate',
                    'print_rate': 'print_noise_rate', 
                    'entry_time_rate': 'entry_time_noise_rate',
                    'gaussian': 'use_gaussian',
                    'seed': 'random_seed'
                }
                # Map old param names to new ones
                for old_name, new_name in param_mapping.items():
                    if old_name in noise_config:
                        mapped_config[new_name] = noise_config[old_name]
                # Also add any params already with correct names
                for param in ['burn_noise_rate', 'print_noise_rate', 'entry_time_noise_rate', 'use_gaussian', 'random_seed']:
                    if param in noise_config:
                        mapped_config[param] = noise_config[param]
                self.noise_injector = DataNoiseInjector(**mapped_config)
            else:
                self.noise_injector = DataNoiseInjector()
        
        print(f"Using {len(self.employees)} employees")
        print(f"Malicious employees: {self.malicious_employees} ({self.malicious_ratio:.1%})")
        print(f"Noise injection: {'ENABLED' if add_noise else 'DISABLED'}")
        self._print_department_distribution()
    
    def _print_department_distribution(self):
        """Print distribution of employees by department"""
        dept_counts = {}
        for emp in self.employees.values():
            dept_counts[emp['department']] = dept_counts.get(emp['department'], 0) + 1
        
        print("Department distribution:")
        for dept, count in sorted(dept_counts.items()):
            print(f"  {dept}: {count}")
    
    def generate_dataset(self) -> pd.DataFrame:
        """Generate the complete dataset with all activities"""
        print(f"Generating dataset with {self.num_employees} employees over {self.days_range} days...")
        
        data = []
        start_date = datetime.now() - timedelta(days=self.days_range)
        
        total_iterations = self.num_employees * self.days_range
        completed = 0
        
        for emp_id in self.employees.keys():
            is_malicious = emp_id in self.malicious_employee_ids
            
            for day in range(self.days_range):
                current_date = start_date + timedelta(days=day)
                
                completed += 1
                if completed % (total_iterations // 10) == 0:
                    progress = (completed / total_iterations) * 100
                    print(f"Progress: {progress:.0f}% ({completed}/{total_iterations})")
                
                daily_record = self.generate_daily_record(emp_id, current_date.date(), is_malicious)
                data.append(daily_record)
        
        df = pd.DataFrame(data)
        df = self.post_process_dataframe(df)
        
        if self.add_noise and self.noise_injector:
            print("Applying noise injection...")
            df = self.noise_injector.add_noise_to_dataframe(df)
            
            if 'row_modified' in df.columns:
                modified_count = df['row_modified'].sum()
                print(f"Noise applied to {modified_count:,} records ({modified_count/len(df):.1%})")
        
        print(f"Dataset generated: {len(df)} records")
        print(f"Malicious records: {df['is_malicious'].sum()}")
        
        return df
    