# config.py
"""
Main configuration file that imports all configuration modules.
"""

from .organizational_structure import OrganizationalStructure
from .behavioral_patterns import BehavioralPatterns
from .employee_attributes import EmployeeAttributes
from .geographic_data import GeographicData


class Config(OrganizationalStructure, BehavioralPatterns, EmployeeAttributes, GeographicData):
    """
    Main configuration class that inherits from all configuration modules.
    """
    
    # Default dataset parameters
    DEFAULT_NUM_EMPLOYEES = 1666
    DEFAULT_DAYS_RANGE = 180
    DEFAULT_MALICIOUS_RATIO = 0.05
    
    @classmethod
    def get_department_positions(cls):
        """Get all department positions."""
        return cls.DEPARTMENT_POSITIONS
    
    @classmethod
    def get_behavioral_group(cls, department):
        """Get behavioral group for a department."""
        return cls.BEHAVIORAL_GROUPS.get(department, 'C')
    
    @classmethod
    def get_group_pattern(cls, group):
        """Get behavioral pattern for a group."""
        return cls.GROUP_PATTERNS.get(group, cls.GROUP_PATTERNS['C'])
    
    @classmethod
    def get_classification_probabilities(cls, department):
        """Get classification probabilities for a department."""
        return cls.CLASSIFICATION_PROBABILITIES.get(department, cls.CLASSIFICATION_PROBABILITIES['default'])
    
    @classmethod
    def get_seniority_range(cls, position):
        """Get seniority range based on position type."""
        position_lower = position.lower()
        
        if any(title in position_lower for title in ['chief', 'head of', 'director']):
            return cls.SENIORITY_RANGES['executive']
        elif 'manager' in position_lower:
            return cls.SENIORITY_RANGES['manager']
        elif 'secretary' in position_lower:
            return cls.SENIORITY_RANGES['secretary']
        else:
            return cls.SENIORITY_RANGES['default']