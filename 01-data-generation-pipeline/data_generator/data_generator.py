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
        
        # Initialize noise injection if requested
        self.add_noise = add_noise
        self.noise_injector = None
        if add_noise:
            # מיפוי שמות פרמטרים מה-config לשמות הנכונים במחלקה
            if noise_config:
                mapped_config = {}
                # מיפוי שמות פרמטרים
                param_mapping = {
                    'burn_rate': 'burn_noise_rate',
                    'print_rate': 'print_noise_rate', 
                    'entry_time_rate': 'entry_time_noise_rate',
                    'gaussian': 'use_gaussian',
                    'seed': 'random_seed'
                }
                
                for old_name, new_name in param_mapping.items():
                    if old_name in noise_config:
                        mapped_config[new_name] = noise_config[old_name]
                
                # הוספת פרמטרים נוספים שעלולים להיות בשמות הנכונים
                for param in ['burn_noise_rate', 'print_noise_rate', 'entry_time_noise_rate', 'use_gaussian', 'random_seed']:
                    if param in noise_config:
                        mapped_config[param] = noise_config[param]
                
                self.noise_injector = DataNoiseInjector(**mapped_config)
            else:
                self.noise_injector = DataNoiseInjector()
        
        print(f"Using {len(self.employees)} employees")
        print(f"Malicious employees: {self.malicious_employees} ({self.malicious_ratio:.1%})")
        if add_noise:
            print(f"Noise injection: ENABLED")
        else:
            print(f"Noise injection: DISABLED")
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
        
        # Progress tracking
        total_iterations = len(self.employees) * self.days_range
        completed = 0
        
        for emp_id in list(self.employees.keys()):
            is_malicious = emp_id in self.malicious_employee_ids
            
            for day in range(self.days_range):
                current_date = start_date + timedelta(days=day)
                
                # Show progress every 10%
                completed += 1
                if completed % (total_iterations // 10) == 0:
                    progress = (completed / total_iterations) * 100
                    print(f"Progress: {progress:.0f}% ({completed}/{total_iterations})")
                
                # Generate daily record
                daily_record = self.generate_daily_record(
                    emp_id, current_date.date(), is_malicious
                )
                data.append(daily_record)
        
        df = pd.DataFrame(data)
        
        # Post-process the dataframe
        df = self.post_process_dataframe(df)
        
        # Apply noise injection if enabled
        if self.add_noise and self.noise_injector:
            print("Applying noise injection...")
            # תיקון: שינוי מ-inject_noise ל-add_noise_to_dataframe
            df = self.noise_injector.add_noise_to_dataframe(df)
            
            # Log noise statistics
            if 'row_modified' in df.columns:
                modified_count = df['row_modified'].sum()
                print(f"Noise applied to {modified_count:,} records ({modified_count/len(df):.1%})")
        
        print(f"Dataset generated: {len(df)} records")
        print(f"Malicious records: {df['is_malicious'].sum()}")
        
        return df
    
    def get_malicious_employees(self) -> set:
        """Get set of malicious employee IDs"""
        return self.malicious_employee_ids
    
    def get_employee_info(self, emp_id: str) -> Dict[str, Any]:
        """Get employee information by ID"""
        return self.employees.get(emp_id, {})
    
    def get_dataset_metadata(self) -> Dict[str, Any]:
        """Get metadata about the generated dataset"""
        metadata = {
            'num_employees': self.num_employees,
            'days_range': self.days_range,
            'malicious_ratio': self.malicious_ratio,
            'malicious_employees': self.malicious_employees,
            'start_date': (datetime.now() - timedelta(days=self.days_range)).date(),
            'end_date': datetime.now().date(),
            'total_expected_records': self.num_employees * self.days_range,
            'noise_injection_enabled': self.add_noise
        }
        
        # Add noise configuration to metadata if enabled
        if self.add_noise and self.noise_injector:
            metadata['noise_config'] = self.noise_injector.get_statistics()
        
        return metadata