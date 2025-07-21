"""
Employee Manager
Manages collection of employee profiles and provides access methods
"""

import numpy as np
import random
from config.config import Config
from .employee_profile_creator import EmployeeProfileCreator


class EmployeeManager:
    """Manages the collection of employee profiles"""
    
    def __init__(self, num_employees=1000):
        self.num_employees = num_employees
        self.employees = {}
        self.profile_creator = EmployeeProfileCreator()
        
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
            employee_profile = self.profile_creator.create_employee_profile(department, emp_id)
            
            self.employees[emp_id] = employee_profile
            
        self._print_generation_summary()
        return self.employees
    
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
    
    def select_malicious_employees(self, malicious_ratio=0.05):
        """Select random employees to be malicious"""
        num_malicious = int(len(self.employees) * malicious_ratio)
        malicious_ids = set(random.sample(list(self.employees.keys()), num_malicious))
        
        print(f"Selected {len(malicious_ids)} malicious employees ({malicious_ratio:.1%})")
        return malicious_ids