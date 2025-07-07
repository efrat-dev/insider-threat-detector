"""
access_activity_generator.py - Access activity generation
Contains logic for generating daily building access activities for employees
"""

import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional
from config.config import Config


class AccessActivityGenerator:
    """Class for generating building access activities"""
    
    def __init__(self, behavioral_patterns: Dict[str, Any]):
        self.patterns = behavioral_patterns
    
    def generate_access_activity(self, employee: Dict[str, Any], date: datetime.date,
                               is_malicious: bool, is_abroad: bool) -> Dict[str, Any]:
        """Generate daily access activity for employee"""
        
        # Handle employee abroad
        if is_abroad:
            if is_malicious and np.random.random() < 0.05:
                pass  # Suspicious access from abroad
            elif not is_malicious and np.random.random() < 0.001:
                pass  # Legitimate rare access
            else:
                return self._empty_access_activity()
        
        # Check for absence
        if np.random.random() < 0.05:
            return self._empty_access_activity()
        
        # Get work hours
        start_hour, end_hour = self._get_work_hours(employee, date, is_malicious)
        
        # Check weekend work
        if not self._should_work_weekend(employee, date, is_malicious):
            return self._empty_access_activity()
        
        # Generate access activity
        return self._generate_access_data(employee, date, start_hour, end_hour, is_malicious)
    
    def _get_work_hours(self, employee: Dict[str, Any], date: datetime.date,
                       is_malicious: bool) -> Tuple[float, float]:
        """Calculate work hours by behavior pattern"""
        group = employee['behavioral_group']
        pattern = self.patterns[group]
        
        # Basic work hours
        start_hour = np.random.normal(
            pattern['work_hours']['start_mean'],
            pattern['work_hours']['start_std']
        )
        end_hour = np.random.normal(
            pattern['work_hours']['end_mean'],
            pattern['work_hours']['end_std']
        )
        
        # Boundary limits - add missing Config variables
        min_work_hour = getattr(Config, 'MIN_WORK_HOUR', 6)
        max_work_hour = getattr(Config, 'MAX_WORK_HOUR', 22)
        min_work_duration = getattr(Config, 'MIN_WORK_DURATION', 4)
        
        start_hour = max(min_work_hour, min(12, start_hour))
        end_hour = max(start_hour + min_work_duration, 
                      min(max_work_hour, end_hour))
        
        # Malicious employees - more unusual hours
        # if is_malicious and np.random.random() < 0.3:
        #     if np.random.random() < 0.5:
        #         start_hour = np.random.uniform(5, 7)  # Very early
        #     else:
        #         end_hour = np.random.uniform(20, 23)  # Very late

# זדוניים - 1% סיכוי לשעות לילה
        if is_malicious and np.random.random() < 0.01:  # 1% במקום 30%
            if np.random.random() < 0.5:
                start_hour = np.random.uniform(5, 7)  # Very early
            else:
                end_hour = np.random.uniform(20, 23)  # Very late

        # רגילים - 0.8% סיכוי לשעות לילה (קרוב לזדוניים אבל קצת פחות)
        elif not is_malicious and np.random.random() < 0.008:  # 0.8%
            if np.random.random() < 0.5:
                start_hour = np.random.uniform(5, 7)  # Very early
            else:
                end_hour = np.random.uniform(20, 23)  # Very late
                
        return start_hour, end_hour
    
    def _should_work_weekend(self, employee: Dict[str, Any], date: datetime.date,
                           is_malicious: bool) -> bool:
        """Check if employee should work weekend"""
        if date.weekday() < 4:  # Weekdays
            return True
        
        group = employee['behavioral_group']
        pattern = self.patterns[group]
        
        # Security always works
        if group == 'E':
            return np.random.random() < pattern.get('weekend_work', 0.6)
        
        # Malicious employees - more weekend work
        if is_malicious and np.random.random() < 0.3:
            return True
        
        # Regular employees - rare weekend work
        return np.random.random() < 0.05
    
    def _generate_access_data(self, employee: Dict[str, Any], date: datetime.date,
                            start_hour: float, end_hour: float, is_malicious: bool) -> Dict[str, Any]:
        """Generate detailed access data"""
        base_date = datetime.combine(date, datetime.min.time())
        first_entry = base_date + timedelta(hours=start_hour)
        last_exit = base_date + timedelta(hours=end_hour)
        
        # Number of entries/exits
        if is_malicious and np.random.random() < 0.2:
            num_entries = np.random.choice([2, 3, 4], p=[0.5, 0.3, 0.2])
        else:
            num_entries = np.random.choice([1, 2], p=[0.8, 0.2])
        
        num_exits = num_entries
        
        # Presence time
        total_minutes = int((last_exit - first_entry).total_seconds() / 60)
        
        # Flags
        early_entry = 1 if first_entry.hour < 6 else 0
        late_exit = 1 if last_exit.hour > 22 else 0
        night_entry = 1 if first_entry.hour <= 5 or first_entry.hour >= 22 else 0
        weekend_entry = 1 if date.weekday() >= 4 else 0
        
        # Multi-campus access
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
        """Return empty access activity"""
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