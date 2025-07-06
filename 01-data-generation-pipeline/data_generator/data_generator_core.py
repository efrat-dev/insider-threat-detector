import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple, Any

from activity_generators import (
    PrintActivityGenerator,
    BurnActivityGenerator,
    TravelActivityGenerator,
    AccessActivityGenerator,
    RiskIndicatorGenerator
)
from config.config import Config


class DataGeneratorCore:
    """Core data generation functionality"""
    
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
        
        # Initialize behavioral patterns and activity generators
        self.behavioral_patterns = Config.GROUP_PATTERNS
        self.print_generator = PrintActivityGenerator(self.behavioral_patterns)
        self.burn_generator = BurnActivityGenerator(self.behavioral_patterns)
        self.travel_generator = TravelActivityGenerator(self.behavioral_patterns)
        self.access_generator = AccessActivityGenerator(self.behavioral_patterns)
        self.risk_generator = RiskIndicatorGenerator()
    
    def generate_daily_record(self, emp_id: str, date: datetime.date, 
                             is_malicious: bool) -> Dict[str, Any]:
        """Generate a complete daily record for an employee"""
        # Employee static info
        emp_info = self.employees[emp_id]
        
        # Generate travel activity first (affects other activities)
        travel_data = self.travel_generator.generate_travel_activity(
            emp_info, date, is_malicious
        )
        is_abroad = travel_data['is_abroad'] == 1
        
        # Generate all activities
        print_data = self.print_generator.generate_print_activity(
            emp_info, date, is_malicious, is_abroad
        )
        
        burn_data = self.burn_generator.generate_burn_activity(
            emp_info, date, is_malicious, is_abroad
        )
        
        access_data = self.access_generator.generate_access_activity(
            emp_info, date, is_malicious, is_abroad
        )
        
        # Calculate risk indicators
        risk_travel_indicator = self.risk_generator.calculate_risk_travel_indicator(
            travel_data, print_data, burn_data
        )
        
        # Combine all activities into one record
        daily_record = {
            # Employee info
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
            
            # Risk indicators
            'risk_travel_indicator': risk_travel_indicator,
        }
        
        # Add all activity data
        daily_record.update(print_data)
        daily_record.update(burn_data)
        daily_record.update(travel_data)
        daily_record.update(access_data)
        
        return daily_record
    
    def post_process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Post-process the dataframe for better data types and consistency"""
        # Convert trip_day_number to nullable integer
        if 'trip_day_number' in df.columns:
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
            'total_burn_volume_mb', 'total_files_burned', 'num_print_commands_off_hours',
            'num_color_prints', 'num_bw_prints', 'num_burn_requests_off_hours'
        ]
        for col in count_columns:
            if col in df.columns:
                df[col] = df[col].clip(lower=0)
        
        # Sort by employee_id and date for better organization
        df = df.sort_values(['employee_id', 'date']).reset_index(drop=True)
        
        return df