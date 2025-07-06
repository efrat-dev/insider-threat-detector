import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any

from .data_generator_core import DataGeneratorCore


class DataGenerator(DataGeneratorCore):
    """Main data generation engine that orchestrates all activities"""
    
    def __init__(self, employees: dict, days_range: int = 180, malicious_ratio: float = 0.05):
        super().__init__(employees, days_range, malicious_ratio)
        
        print(f"Using {len(self.employees)} employees")
        print(f"Malicious employees: {self.malicious_employees} ({self.malicious_ratio:.1%})")
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
        return {
            'num_employees': self.num_employees,
            'days_range': self.days_range,
            'malicious_ratio': self.malicious_ratio,
            'malicious_employees': self.malicious_employees,
            'start_date': (datetime.now() - timedelta(days=self.days_range)).date(),
            'end_date': datetime.now().date(),
            'total_expected_records': self.num_employees * self.days_range
        }