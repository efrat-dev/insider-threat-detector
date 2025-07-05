# Add these imports at the top of your data_generator.py file
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple, Any

# Option 1: Update the DataGenerator class to match main.py expectations
class DataGenerator:
    """Main data generation engine that orchestrates all activities"""
    
    def __init__(self, employees: dict, days_range: int = 180, malicious_ratio: float = 0.05):
        self.employees = employees
        self.num_employees = len(employees)
        self.days_range = days_range
        self.malicious_ratio = malicious_ratio
        self.malicious_employees = int(self.num_employees * malicious_ratio)
        
        # Select malicious employees
        self.malicious_employee_ids = set(random.sample(
            list(self.employees.keys()), self.malicious_employees
        ))
        
        # Initialize trip tracking for travel generator
        self.employee_trips = {}
        
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
                daily_record = self._generate_daily_record(
                    emp_id, current_date.date(), is_malicious
                )
                data.append(daily_record)
        
        df = pd.DataFrame(data)
        
        # Post-process the dataframe
        df = self._post_process_dataframe(df)
        
        print(f"Dataset generated: {len(df)} records")
        print(f"Malicious records: {df['is_malicious'].sum()}")
        
        return df
    
    def _generate_daily_record(self, emp_id: str, date: datetime.date, 
                             is_malicious: bool) -> Dict[str, Any]:
        """Generate a complete daily record for an employee"""
        # Employee static info
        emp_info = self.employees[emp_id]
        
        # For now, create minimal records since activity_generators aren't available
        # You'll need to add your activity generators here
        
        # Basic daily record structure
        daily_record = {
            'employee_id': emp_id,
            'date': date,
            'employee_department': emp_info['department'],
            'employee_campus': emp_info.get('campus', 'Main Campus'),
            'employee_position': emp_info.get('position', 'Employee'),
            'employee_seniority_years': emp_info.get('seniority_years', 1),
            'is_contractor': emp_info.get('is_contractor', False),
            'employee_classification': emp_info.get('classification', 'Regular'),
            'has_foreign_citizenship': emp_info.get('foreign_citizenship', False),
            'has_criminal_record': emp_info.get('criminal_record', False),
            'has_medical_history': emp_info.get('medical_history', False),
            'employee_origin_country': emp_info.get('origin_country', 'Unknown'),
            'behavioral_group': emp_info.get('behavioral_group', 1),
            'is_malicious': 1 if is_malicious else 0,
            
            # Placeholder activity data - replace with actual activity generators
            'num_entries': random.randint(0, 3),
            'num_exits': random.randint(0, 3),
            'total_presence_minutes': random.randint(0, 600),
            'num_print_commands': random.randint(0, 10),
            'total_printed_pages': random.randint(0, 50),
            'num_burn_requests': random.randint(0, 2),
            'total_burn_volume_mb': random.randint(0, 100),
            'total_files_burned': random.randint(0, 5),
            'is_abroad': random.choice([0, 1]) if random.random() < 0.1 else 0,
            'is_official_trip': random.choice([0, 1]),
            'is_hostile_country_trip': random.choice([0, 1]) if random.random() < 0.05 else 0,
            'trip_day_number': None,
            'risk_travel_indicator': 0
        }
        
        # Calculate risk travel indicator
        daily_record['risk_travel_indicator'] = 1 if (
            daily_record['is_abroad'] == 1 and
            daily_record['is_official_trip'] == 0 and
            daily_record['is_hostile_country_trip'] == 1 and
            (daily_record['total_files_burned'] > 0 or 
             daily_record['total_printed_pages'] > 0)
        ) else 0
        
        return daily_record
    
    def _post_process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Post-process the dataframe for better data types and consistency"""
        # Convert trip_day_number to nullable integer
        df['trip_day_number'] = df['trip_day_number'].astype('Int64')
        
        # Ensure date is datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Round floating point values to reasonable precision
        float_columns = [
            'avg_request_classification', 'ratio_color_prints'
        ]
        for col in float_columns:
            if col in df.columns:
                df[col] = df[col].round(2)
        
        # Ensure non-negative values for count columns
        count_columns = [
            'num_entries', 'num_exits', 'total_presence_minutes',
            'num_print_commands', 'total_printed_pages', 'num_burn_requests',
            'total_burn_volume_mb', 'total_files_burned'
        ]
        for col in count_columns:
            if col in df.columns:
                df[col] = df[col].clip(lower=0)
        
        # Sort by employee_id and date for better organization
        df = df.sort_values(['employee_id', 'date']).reset_index(drop=True)
        
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