"""
Access Activity Generator

This module contains logic for generating daily building access activity data
for employees. It simulates realistic work patterns, including:
- Standard work hours based on behavioral groups.
- Variations for malicious and non-malicious employees.
- Handling weekend work, absences, and rare night-hour access.
- Optional simulation of multi-campus activity.
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple
from config.config import Config


class AccessActivityGenerator:
    """
    Generates building access activities for employees.

    Attributes:
        patterns (dict): Behavioral patterns configuration for employee groups.
    """

    def __init__(self, behavioral_patterns: Dict[str, Any]):
        """
        Initialize the generator.

        Parameters:
            behavioral_patterns (dict): Mapping of behavioral groups to activity parameters.
        """
        self.patterns = behavioral_patterns
    
    def generate_access_activity(
        self,
        employee: Dict[str, Any],
        date: datetime.date,
        is_malicious: bool,
        is_abroad: bool
    ) -> Dict[str, Any]:
        """
        Generate daily access activity for an employee.

        Parameters:
            employee (dict): Employee profile.
            date (datetime.date): Target date for activity generation.
            is_malicious (bool): Whether the employee is flagged as malicious.
            is_abroad (bool): Whether the employee is abroad on this date.

        Returns:
            dict: Access activity details for the given date.
        """
        # Handle employee abroad cases
        if is_abroad:
            if is_malicious and np.random.random() < 0.05:
                pass  # Suspicious access from abroad
            elif not is_malicious and np.random.random() < 0.001:
                pass  # Rare legitimate access
            else:
                return self._empty_access_activity()
        
        # Simulate random absences
        if np.random.random() < 0.05:
            return self._empty_access_activity()
        
        # Determine work hours
        start_hour, end_hour = self._get_work_hours(employee, date, is_malicious)
        
        # Weekend check
        if not self._should_work_weekend(employee, date, is_malicious):
            return self._empty_access_activity()
        
        # Generate detailed access data
        return self._generate_access_data(employee, date, start_hour, end_hour, is_malicious)
    
    def _get_work_hours(
        self,
        employee: Dict[str, Any],
        date: datetime.date,
        is_malicious: bool
    ) -> Tuple[float, float]:
        """
        Determine start and end work hours based on behavior patterns.

        Includes:
            - Normal variation using Gaussian distribution.
            - Night-hour anomalies (different probabilities for malicious vs. regular).

        Returns:
            tuple: (start_hour, end_hour) in decimal hours.
        """
        group = employee['behavioral_group']
        pattern = self.patterns[group]
        
        # Base hours from pattern
        start_hour = np.random.normal(pattern['work_hours']['start_mean'],
                                      pattern['work_hours']['start_std'])
        end_hour = np.random.normal(pattern['work_hours']['end_mean'],
                                    pattern['work_hours']['end_std'])
        
        # Safety boundaries
        min_work_hour = getattr(Config, 'MIN_WORK_HOUR', 6)
        max_work_hour = getattr(Config, 'MAX_WORK_HOUR', 22)
        min_work_duration = getattr(Config, 'MIN_WORK_DURATION', 4)
        
        start_hour = max(min_work_hour, min(12, start_hour))
        end_hour = max(start_hour + min_work_duration, min(max_work_hour, end_hour))

        # Malicious: 1% chance of extreme early/late hours
        if is_malicious and np.random.random() < 0.01:
            if np.random.random() < 0.5:
                start_hour = np.random.uniform(5, 7)  # Very early
            else:
                end_hour = np.random.uniform(20, 23)  # Very late

        # Regular: 0.8% chance of extreme early/late hours
        elif not is_malicious and np.random.random() < 0.008:
            if np.random.random() < 0.5:
                start_hour = np.random.uniform(5, 7)
            else:
                end_hour = np.random.uniform(20, 23)
                
        return start_hour, end_hour
    
    def _should_work_weekend(
        self,
        employee: Dict[str, Any],
        date: datetime.date,
        is_malicious: bool
    ) -> bool:
        """
        Determine if an employee should work on weekends.

        Logic:
            - Weekdays always return True.
            - Security group (E) has higher weekend work probability.
            - Malicious employees more likely to work weekends.
            - Regular employees rarely work weekends.
        """
        if date.weekday() < 4:  # Monday–Thursday
            return True
        
        group = employee['behavioral_group']
        pattern = self.patterns[group]
        
        if group == 'E':  # Security staff
            return np.random.random() < pattern.get('weekend_work', 0.6)
        
        if is_malicious and np.random.random() < 0.3:
            return True
        
        return np.random.random() < 0.05
    
    def _generate_access_data(
        self,
        date: datetime.date,
        start_hour: float,
        end_hour: float,
        is_malicious: bool
    ) -> Dict[str, Any]:
        """
        Generate a detailed access record for the day.

        Returns:
            dict: Access record including entry/exit times, flags, and anomalies.
        """
        base_date = datetime.combine(date, datetime.min.time())
        first_entry = base_date + timedelta(hours=start_hour)
        last_exit = base_date + timedelta(hours=end_hour)
        
        # Number of daily entries
        if is_malicious and np.random.random() < 0.2:
            num_entries = np.random.choice([2, 3, 4], p=[0.5, 0.3, 0.2])
        else:
            num_entries = np.random.choice([1, 2], p=[0.8, 0.2])
        
        num_exits = num_entries
        
        # Calculate total presence time
        total_minutes = int((last_exit - first_entry).total_seconds() / 60)
        
        # Flags
        early_entry = int(first_entry.hour < 6)
        late_exit = int(last_exit.hour > 22)
        night_entry = int(first_entry.hour <= 5 or first_entry.hour >= 22)
        weekend_entry = int(date.weekday() >= 4)
        
        # Multi-campus activity
        num_unique_campus = 1
        if is_malicious and np.random.random() < 0.15:
            num_unique_campus = np.random.choice([2, 3])
        
        return {
            'num_entries': num_entries,
            'num_exits': num_exits,
            'first_entry_time': first_entry.strftime('%H:%M'),
            'last_exit_time': last_exit.strftime('%H:%M'),
            'total_presence_minutes': total_minutes,
            'entered_during_night_hours': night_entry,
            'num_unique_campus': num_unique_campus,
            'early_entry_flag': early_entry,
            'late_exit_flag': late_exit,
            'entry_during_weekend': weekend_entry
        }
    
    def _empty_access_activity(self) -> Dict[str, Any]:
        """
        Return an empty (no access) activity record.
        """
        return {
            'num_entries': 0,
            'num_exits': 0,
            'first_entry_time': None,
            'last_exit_time': None,
            'total_presence_minutes': 0,
            'entered_during_night_hours': 0,
            'num_unique_campus': 0,
            'early_entry_flag': 0,
            'late_exit_flag': 0,
            'entry_during_weekend': 0
        }