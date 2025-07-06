"""
Employee Profile Generator
Handles creation of realistic employee profiles with proper department-position alignment
"""

import numpy as np
import random
from config.config import Config


class EmployeeGenerator:
    def __init__(self, num_employees=1000):
        self.num_employees = num_employees
        self.employees = {}
        
    def generate_employee_profiles(self):
        """Generate all employee profiles"""
        print(f"Generating {self.num_employees} employee profiles...")
        
        num_digits = len(str(self.num_employees))
        departments = list(Config.DEPARTMENT_WEIGHTS.keys())
        weights = list(Config.DEPARTMENT_WEIGHTS.values())
        
        for i in range(self.num_employees):
            emp_id = str(i + 1).zfill(num_digits)
            
            # Select department based on realistic distribution
            department = np.random.choice(departments, p=weights)
            
            # Generate employee profile
            employee_profile = self._generate_single_employee(department)
            employee_profile['emp_id'] = emp_id
            
            self.employees[emp_id] = employee_profile
            
        self._print_generation_summary()
        return self.employees
    
    def _generate_single_employee(self, department):
        """Generate a single employee profile"""
        # Select position within department
        position = np.random.choice(Config.DEPARTMENT_POSITIONS[department])
        
        # Assign behavioral group
        behavioral_group = Config.BEHAVIORAL_GROUPS[department]
        
        # Generate employee attributes
        profile = {
            'department': department,
            'position': position,
            'behavioral_group': behavioral_group,
            'campus': np.random.choice(Config.CAMPUSES),
            'seniority_years': self._get_seniority_years(position),
            'is_contractor': np.random.choice(
                Config.EMPLOYEE_PROBABILITIES['contractor']['values'],
                p=Config.EMPLOYEE_PROBABILITIES['contractor']['weights']
            ),
            'classification': self._get_classification_level(department),
            'foreign_citizenship': np.random.choice(
                Config.EMPLOYEE_PROBABILITIES['foreign_citizenship']['values'],
                p=Config.EMPLOYEE_PROBABILITIES['foreign_citizenship']['weights']
            ),
            'criminal_record': np.random.choice(
                Config.EMPLOYEE_PROBABILITIES['criminal_record']['values'],
                p=Config.EMPLOYEE_PROBABILITIES['criminal_record']['weights']
            ),
            'medical_history': np.random.choice(
                Config.EMPLOYEE_PROBABILITIES['medical_history']['values'],
                p=Config.EMPLOYEE_PROBABILITIES['medical_history']['weights']
            ),
            'origin_country': np.random.choice(
                Config.ORIGIN_COUNTRIES,
                p=Config.ORIGIN_COUNTRY_WEIGHTS
            )
        }
        
        return profile
    
    def _get_seniority_years(self, position):
        """Determine seniority years based on position"""
        if any(title in position for title in ['Chief', 'Head of', 'Director']):
            min_years, max_years = Config.SENIORITY_RANGES['executive']
        elif 'Manager' in position:
            min_years, max_years = Config.SENIORITY_RANGES['manager']
        elif 'Secretary' in position:
            min_years, max_years = Config.SENIORITY_RANGES['secretary']
        else:
            min_years, max_years = Config.SENIORITY_RANGES['default']
            
        return np.random.randint(min_years, max_years + 1)
    
    def _get_classification_level(self, department):
        """Determine classification level based on department"""
        if department in Config.CLASSIFICATION_PROBABILITIES:
            levels = Config.CLASSIFICATION_PROBABILITIES[department]['levels']
            weights = Config.CLASSIFICATION_PROBABILITIES[department]['weights']
        else:
            levels = Config.CLASSIFICATION_PROBABILITIES['default']['levels']
            weights = Config.CLASSIFICATION_PROBABILITIES['default']['weights']
            
        return np.random.choice(levels, p=weights)
    
    def _print_generation_summary(self):
        """Print summary of generated employees"""
        print(f"Generated {len(self.employees)} employees")
        print("Department distribution:")
        
        dept_counts = {}
        for emp in self.employees.values():
            dept = emp['department']
            dept_counts[dept] = dept_counts.get(dept, 0) + 1
            
        for dept, count in sorted(dept_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {dept}: {count}")
    
    def get_employee(self, emp_id):
        """Get employee profile by ID"""
        return self.employees.get(emp_id)
    
    def get_all_employees(self):
        """Get all employee profiles"""
        return self.employees
    
    def get_employees_by_department(self, department):
        """Get all employees in a specific department"""
        return {emp_id: emp for emp_id, emp in self.employees.items() 
                if emp['department'] == department}
    
    def get_employees_by_behavioral_group(self, group):
        """Get all employees in a specific behavioral group"""
        return {emp_id: emp for emp_id, emp in self.employees.items() 
                if emp['behavioral_group'] == group}
    
    def select_malicious_employees(self, malicious_ratio=0.05):
        """Select random employees to be malicious"""
        num_malicious = int(len(self.employees) * malicious_ratio)
        malicious_ids = set(random.sample(list(self.employees.keys()), num_malicious))
        
        print(f"Selected {len(malicious_ids)} malicious employees ({malicious_ratio:.1%})")
        return malicious_ids
