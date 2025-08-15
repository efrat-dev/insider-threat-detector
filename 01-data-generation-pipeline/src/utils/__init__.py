"""
Utility functions package for the Advanced Insider Threat Dataset Generator.
"""

from .performance_profiler import profile_memory_usage, log_memory_usage
from .constants import *

__all__ = [
    'profile_memory_usage',
    'log_memory_usage',
    'APP_NAME',
    'APP_DESCRIPTION',
    'DEFAULT_LOG_FILENAME',
    'DEFAULT_OUTPUT_PREFIX',
    'DEFAULT_OUTPUT_DIR',
    'MAX_EMPLOYEES',
    'MAX_DAYS',
    'MIN_POSITIVE_VALUE',
    'MAX_RATIO',
    'BYTES_TO_MB',
    'BANNER_WIDTH',
    'BANNER_CHAR'
]