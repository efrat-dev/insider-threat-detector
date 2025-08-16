"""
Main configuration aggregator module.

This module imports and consolidates all configuration components into a single
comprehensive configuration class. It serves as the central access point for
organizational structure, behavioral patterns, employee attributes, and geographic data.

Additionally, it defines default parameters used across the dataset generation
process, including default number of employees, duration of data (in days),
and the default ratio of malicious employees.
"""

from .organizational_structure import OrganizationalStructure
from .behavioral_patterns import BehavioralPatterns
from .employee_attributes import EmployeeAttributes
from .geographic_data import GeographicData


class Config(OrganizationalStructure, BehavioralPatterns, EmployeeAttributes, GeographicData):
    """
    Unified configuration class combining all configuration aspects
    by multiple inheritance from specific configuration modules.
    """
    
    # Default dataset parameters
    DEFAULT_NUM_EMPLOYEES = 1666
    DEFAULT_DAYS_RANGE = 180
    DEFAULT_MALICIOUS_RATIO = 0.05