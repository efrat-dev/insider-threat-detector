"""
Employee Profile Creator

This module handles the creation of individual employee profiles
with realistic department-position alignment and related attributes.

Responsibilities:
- Assign realistic job positions within departments.
- Match behavioral groups to departments.
- Generate additional employee attributes such as campus, seniority,
  contractor status, classification, and more.
"""

import numpy as np
from config.config import Config


class EmployeeProfileCreator:
    """
    Creates individual employee profiles with realistic attributes.

    Attributes:
        None directly stored; configuration is pulled from Config.
    """
    
    def __init__(self):
        """Initialize the profile creator (no persistent state)."""
        pass
    
    def create_employee_profile(self, department, emp_id):
        """
        Create a single employee profile for a given department.

        Parameters:
            department (str): The department to assign the employee to.
            emp_id (str/int): Unique identifier for the employee.

        Returns:
            dict: A dictionary containing generated employee attributes.

        Process:
            - Randomly selects a position from the department's allowed positions.
            - Assigns a behavioral group according to the department.
            - Randomly determines campus location, seniority, contractor status,
              classification level, citizenship, criminal record, medical history,
              and origin country based on configured probabilities.
        """
        # Select position within department
        position = np.random.choice(Config.DEPARTMENT_POSITIONS[department])
        
        # Assign behavioral group
        behavioral_group = Config.BEHAVIORAL_GROUPS[department]
        
        # Generate employee attributes
        profile = {
            'emp_id': emp_id,
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
        """
        Determine seniority years based on position title.

        Parameters:
            position (str): The employee's job title.

        Returns:
            int: Randomly generated number of years in the role range.

        Logic:
            - Executives have the highest minimum seniority.
            - Managers have medium seniority.
            - Secretaries have specific seniority ranges.
            - All other positions use a default range.
        """
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
        """
        Determine classification level based on department.

        Parameters:
            department (str): The employee's department.

        Returns:
            str: Selected classification level.

        Logic:
            - If department has a custom classification probability set,
              use its distribution.
            - Otherwise, fall back to the default distribution.
        """
        if department in Config.CLASSIFICATION_PROBABILITIES:
            levels = Config.CLASSIFICATION_PROBABILITIES[department]['levels']
            weights = Config.CLASSIFICATION_PROBABILITIES[department]['weights']
        else:
            levels = Config.CLASSIFICATION_PROBABILITIES['default']['levels']
            weights = Config.CLASSIFICATION_PROBABILITIES['default']['weights']
            
        return np.random.choice(levels, p=weights)
