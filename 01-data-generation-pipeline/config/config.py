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