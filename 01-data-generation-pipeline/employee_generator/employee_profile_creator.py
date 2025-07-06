"""
Employee Profile Creator
Handles creation of individual employee profiles with proper department-position alignment
"""

import numpy as np
from config.config import Config


class EmployeeProfileCreator:
    """Creates individual employee profiles with realistic attributes"""
    
    def __init__(self):
        pass
    
    def create_employee_profile(self, department, emp_id):
        """Create a single employee profile for given department"""
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