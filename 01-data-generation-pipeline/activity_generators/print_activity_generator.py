"""
print_activity_generator.py - Print activity generation
Contains logic for generating daily printing activities for employees
"""

import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional
from config.config import Config


class PrintActivityGenerator:
    """Class for generating print activities"""
    
    def __init__(self, behavioral_patterns: Dict[str, Any]):
        self.patterns = behavioral_patterns
    
    def generate_print_activity(self, employee: Dict[str, Any], date: datetime.date, 
                              is_malicious: bool, is_abroad: bool) -> Dict[str, Any]:
        """Generate daily print activity for employee"""
        
        # If employee is abroad - low probability of printing
        if is_abroad and not is_malicious and np.random.random() < 0.98:
            return self._empty_print_activity()
        
        if is_abroad and is_malicious and np.random.random() < 0.85:
            return self._empty_print_activity()
        
        # Get behavior pattern by group
        group = employee['behavioral_group']
        pattern = self.patterns[group]
        
        # Check if employee prints today
        if np.random.random() > pattern['print_likelihood']:
            return self._empty_print_activity()
        
        # Generate print activity
        multiplier = self._get_malicious_multiplier(is_malicious)
        
        num_commands = max(1, int(np.random.poisson(
            pattern['print_volume']['commands_mean']) * multiplier))
        
        total_pages = max(1, int(np.random.poisson(
            pattern['print_volume']['pages_mean'] * num_commands) * multiplier))
        
        color_ratio = self._calculate_color_ratio(pattern['print_volume']['color_ratio'])
        
        # Calculate off-hours printing
        off_hours_commands, off_hours_pages = self._calculate_off_hours_printing(
            num_commands, total_pages, pattern, is_malicious)
        
        # Multi-campus printing
        print_campuses, printed_from_other = self._calculate_multi_campus_printing(
            employee, is_malicious)
        
        # Calculate color and black-white prints
        num_color = int(total_pages * color_ratio)
        num_bw = total_pages - num_color
        
        return {
            'num_print_commands': num_commands,
            'total_printed_pages': total_pages,
            'num_print_commands_off_hours': off_hours_commands,
            'num_printed_pages_off_hours': off_hours_pages,
            'num_color_prints': num_color,
            'num_bw_prints': num_bw,
            'ratio_color_prints': color_ratio if total_pages > 0 else 0,
            'printed_from_other': printed_from_other,
            'print_campuses': print_campuses
        }
    
    def _get_malicious_multiplier(self, is_malicious: bool) -> float:
        """Return multiplier for malicious employees"""
        if is_malicious:
            return np.random.uniform(1.5, 3.0)
        return np.random.uniform(0.8, 1.2)
    
    def _calculate_color_ratio(self, base_ratio: float) -> float:
        """Calculate color print ratio with noise"""
        return max(0, min(1, np.random.normal(base_ratio, 0.1)))
    
    def _calculate_off_hours_printing(self, num_commands: int, total_pages: int,
                                    pattern: Dict[str, Any], is_malicious: bool) -> Tuple[int, int]:
        """Calculate off-hours printing"""
        off_hours_tendency = pattern.get('off_hours_tendency', 0.1)
        if is_malicious:
            off_hours_tendency *= 2
        
        if np.random.random() < off_hours_tendency:
            off_hours_commands = max(0, int(num_commands * np.random.uniform(0.2, 0.8)))
            off_hours_pages = max(0, int(total_pages * np.random.uniform(0.2, 0.8)))
            return off_hours_commands, off_hours_pages
        
        return 0, 0
    
    def _calculate_multi_campus_printing(self, employee: Dict[str, Any], 
                                       is_malicious: bool) -> Tuple[int, int]:
        """Calculate multi-campus printing"""
        print_campuses = 1
        printed_from_other = 0
        
        if is_malicious and np.random.random() < 0.25:
            print_campuses = np.random.choice([2, 3])
            printed_from_other = 1
        elif np.random.random() < 0.05:
            print_campuses = 2
            printed_from_other = 1
        
        return print_campuses, printed_from_other
    
    def _empty_print_activity(self) -> Dict[str, Any]:
        """Return empty print activity"""
        return {
            'num_print_commands': 0,
            'total_printed_pages': 0,
            'num_print_commands_off_hours': 0,
            'num_printed_pages_off_hours': 0,
            'num_color_prints': 0,
            'num_bw_prints': 0,
            'ratio_color_prints': 0,
            'printed_from_other': 0,
            'print_campuses': 0
        }