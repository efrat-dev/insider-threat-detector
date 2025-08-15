"""
Employee Manager

This module manages a collection of employee profiles and provides methods
to generate, summarize, and select specific subsets of employees.

Responsibilities:
- Create multiple employee profiles via the EmployeeProfileCreator.
- Maintain an internal dictionary of employee data.
- Provide summary statistics and filtered selections (e.g., malicious employees).
"""

import numpy as np
import random
from config.config import Config
from .employee_profile_creator import EmployeeProfileCreator


class EmployeeManager:
    """
    Manages the collection of employee profiles.

    Attributes:
        num_employees (int): Total number of employees to manage.
        employees (dict): Mapping of employee IDs to their profile dictionaries.
        profile_creator (EmployeeProfileCreator): Helper object for creating profiles.
    """
    
    def __init__(self, num_employees=1000):
        """
        Initialize the EmployeeManager.

        Parameters:
            num_employees (int): Number of employees to generate and manage.
        """
        self.num_employees = num_employees
        self.employees = {}
        self.profile_creator = EmployeeProfileCreator()
        
    def generate_employee_profiles(self):
        """
        Generate all employee profiles.

        Process:
            - Assigns zero-padded numeric IDs to employees.
            - Chooses department distribution based on configured weights.
            - Uses EmployeeProfileCreator to create each employee's profile.
            - Stores profiles in the employees dictionary.

        Returns:
            dict: All generated employee profiles.
        """
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
        """
        Print summary of generated employees.

        Displays:
            - Total number of employees generated.
            - Distribution of employees per department (sorted by count).
        """
        print(f"Generated {len(self.employees)} employees")
        print("Department distribution:")
        
        dept_counts = {}
        for emp in self.employees.values():
            dept = emp['department']
            dept_counts[dept] = dept_counts.get(dept, 0) + 1
            
        for dept, count in sorted(dept_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {dept}: {count}")
    
    def select_malicious_employees(self, malicious_ratio=0.05):
        """
        Select a random subset of employees to be marked as malicious.

        Parameters:
            malicious_ratio (float): Fraction of total employees to mark as malicious.

        Returns:
            set: Employee IDs of malicious employees.

        Example:
            With malicious_ratio=0.05 and 1000 employees, ~50 will be selected.
        """
        num_malicious = int(len(self.employees) * malicious_ratio)
        malicious_ids = set(random.sample(list(self.employees.keys()), num_malicious))
        
        print(f"Selected {len(malicious_ids)} malicious employees ({malicious_ratio:.1%})")
        return malicious_ids