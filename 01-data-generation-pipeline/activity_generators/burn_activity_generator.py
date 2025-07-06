"""
burn_activity_generator.py - Burn activity generation
Contains logic for generating daily burning activities for employees
"""

import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional
from config.config import Config


class BurnActivityGenerator:
    """Class for generating burn activities"""
    
    def __init__(self, behavioral_patterns: Dict[str, Any]):
        self.patterns = behavioral_patterns
    
    def generate_burn_activity(self, employee: Dict[str, Any], date: datetime.date,
                             is_malicious: bool, is_abroad: bool) -> Dict[str, Any]:
        """Generate daily burn activity for employee"""
        
        # If employee is abroad - very low probability of burning
        if is_abroad and not is_malicious and np.random.random() < 0.99:
            return self._empty_burn_activity()
        
        if is_abroad and is_malicious and np.random.random() < 0.90:
            return self._empty_burn_activity()
        
        # Get behavior pattern
        group = employee['behavioral_group']
        pattern = self.patterns[group]
        
        # Burn probability - higher for malicious employees
        base_likelihood = pattern['burn_likelihood']
        if is_malicious:
            base_likelihood *= 3
        
        if np.random.random() > base_likelihood:
            return self._empty_burn_activity()
        
        # Generate burn activity
        burn_params = pattern['burn_params']
        
        if is_malicious:
            num_requests = max(1, int(np.random.poisson(burn_params['requests_mean']) * 
                                    np.random.uniform(1.5, 2.5)))
            volume_mb = np.random.lognormal(burn_params['volume_mean'], 1.5)
            num_files = max(1, int(np.random.poisson(burn_params['files_mean']) * 
                                 np.random.uniform(1.8, 3.0)))
        else:
            num_requests = max(1, np.random.poisson(burn_params['requests_mean']))
            volume_mb = np.random.lognormal(burn_params['volume_mean'], 1.0)
            num_files = max(1, np.random.poisson(burn_params['files_mean']))
        
        # Classification levels
        classifications = self._generate_classifications(
            employee, num_requests, burn_params, is_malicious)
        
        # Off-hours burning
        off_hours_requests = self._calculate_off_hours_burning(
            num_requests, pattern, is_malicious)
        
        # Multi-campus burning
        burn_campuses, burned_from_other = self._calculate_multi_campus_burning(
            is_malicious)
        
        return {
            'num_burn_requests': num_requests,
            'max_request_classification': max(classifications),
            'avg_request_classification': np.mean(classifications),
            'num_burn_requests_off_hours': off_hours_requests,
            'total_burn_volume_mb': int(volume_mb),
            'total_files_burned': num_files,
            'burned_from_other': burned_from_other,
            'burn_campuses': burn_campuses
        }
    
    def _generate_classifications(self, employee: Dict[str, Any], num_requests: int,
                                burn_params: Dict[str, Any], is_malicious: bool) -> list:
        """Generate classification levels for burn requests"""
        employee_classification = employee['classification']
        
        if burn_params['high_classification'] or is_malicious:
            max_classification = min(4, employee_classification + 
                                   np.random.choice([0, 1, 2], p=[0.3, 0.4, 0.3]))
        else:
            max_classification = min(employee_classification, 
                                   np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1]))
        
        return [np.random.randint(1, max_classification + 1) for _ in range(num_requests)]
    
    def _calculate_off_hours_burning(self, num_requests: int, 
                                   pattern: Dict[str, Any], is_malicious: bool) -> int:
        """Calculate off-hours burning"""
        off_hours_tendency = pattern.get('off_hours_tendency', 0.1)
        
        if is_malicious and np.random.random() < off_hours_tendency:
            return max(0, int(num_requests * np.random.uniform(0.3, 0.8)))
        
        return 0
    
    def _calculate_multi_campus_burning(self, is_malicious: bool) -> Tuple[int, int]:
        """Calculate multi-campus burning"""
        burn_campuses = 1
        burned_from_other = 0
        
        if is_malicious and np.random.random() < 0.2:
            burn_campuses = np.random.choice([2, 3])
            burned_from_other = 1
        
        return burn_campuses, burned_from_other
    
    def _empty_burn_activity(self) -> Dict[str, Any]:
        """Return empty burn activity"""
        return {
            'num_burn_requests': 0,
            'max_request_classification': 0,
            'avg_request_classification': 0,
            'num_burn_requests_off_hours': 0,
            'total_burn_volume_mb': 0,
            'total_files_burned': 0,
            'burned_from_other': 0,
            'burn_campuses': 0
        }