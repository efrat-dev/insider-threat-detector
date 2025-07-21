"""
Command-line interface package for the Advanced Insider Threat Dataset Generator.
"""

from .argument_parser import parse_arguments, validate_arguments
from .display_utils import print_configuration, print_final_statistics, print_success_message

__all__ = [
    'parse_arguments',
    'validate_arguments', 
    'print_configuration',
    'print_final_statistics',
    'print_success_message'
]