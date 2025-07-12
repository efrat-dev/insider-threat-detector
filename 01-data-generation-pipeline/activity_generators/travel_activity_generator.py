"""
travel_activity_generator.py - Travel activity generation
Contains logic for generating daily travel activities for employees
"""

import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional
from config.config import Config


class TravelActivityGenerator:
    """Class for generating travel activities"""
    
    def __init__(self, behavioral_patterns: Dict[str, Any]):
        self.patterns = behavioral_patterns
        self.employee_trips = {}  # Track active trips
    
    def generate_travel_activity(self, employee: Dict[str, Any], date: datetime.date,
                               is_malicious: bool) -> Dict[str, Any]:
        """Generate daily travel activity for employee"""
        emp_id = employee['emp_id']
        
        # Check if employee is on active trip
        if emp_id in self.employee_trips:
            return self._handle_existing_trip(emp_id, date)
        
        # Check if starting new trip
        if self._should_start_new_trip(employee, is_malicious):
            return self._start_new_trip(employee, date, is_malicious)
        
        return self._no_travel_activity()
    
    def _handle_existing_trip(self, emp_id: str, date: datetime.date) -> Dict[str, Any]:
        """Handle existing trip"""
        trip = self.employee_trips[emp_id]
        days_since_start = (date - trip['start_date']).days
        
        if days_since_start < trip['duration']:
            hostility_level = self._get_hostility_level(trip['country'])
            return {
                'is_abroad': 1,
                'trip_day_number': days_since_start + 1,
                'country_name': trip['country'],
                'is_hostile_country_trip': 1 if hostility_level > 0 else 0,
                'hostility_country_level': hostility_level,
                'is_official_trip': trip['is_official']
            }
        else:
            # End trip
            del self.employee_trips[emp_id]
            return self._no_travel_activity()
    
    def _should_start_new_trip(self, employee: Dict[str, Any], is_malicious: bool) -> bool:
        """Check if should start new trip"""
        group = employee['behavioral_group']
        pattern = self.patterns[group]
        
        travel_likelihood = pattern['travel_likelihood']
        if is_malicious:
            travel_likelihood *= 1.5
        
        return np.random.random() < travel_likelihood
    
    def _start_new_trip(self, employee: Dict[str, Any], date: datetime.date,
                       is_malicious: bool) -> Dict[str, Any]:
        """Start new trip"""
        emp_id = employee['emp_id']
        origin_country = employee['origin_country']
        
        # Choose destination based on malicious behavior
        country = self._choose_destination(is_malicious)
        
        # Determine if official trip
        is_official = np.random.choice([0, 1], p=[0.3, 0.7])
        
        # Check if trip to origin country
        is_origin_trip = 1 if country == origin_country else 0
        
        if is_origin_trip and np.random.random() < 0.6:
            is_official = 0  # Origin country trips less official
        
        # For hostile countries, reduce official trip likelihood
        hostility_level = self._get_hostility_level(country)
        if hostility_level > 0:
            # More hostile = less likely to be official
            official_reduction = 0.8 ** hostility_level
            if np.random.random() > official_reduction:
                is_official = 0
        
        # Trip duration - add missing Config variables
        min_duration = getattr(Config, 'MIN_TRIP_DURATION', 1)
        max_duration = getattr(Config, 'MAX_TRIP_DURATION', 14)
        duration = np.random.randint(min_duration, max_duration + 1)
        
        # Save trip
        self.employee_trips[emp_id] = {
            'country': country,
            'start_date': date,
            'duration': duration,
            'is_official': is_official,
            'origin_country': origin_country
        }
        
        return {
            'is_abroad': 1,
            'trip_day_number': 1,
            'country_name': country,
            'is_hostile_country_trip': 1 if hostility_level > 0 else 0,
            'hostility_country_level': hostility_level,
            'is_official_trip': is_official
        }
    
    def _choose_destination(self, is_malicious: bool) -> str:
        """Choose travel destination based on malicious behavior"""
        if is_malicious:
            # Malicious users more likely to visit hostile countries
            rand_val = np.random.random()
            
            if rand_val < 0.15:  # 15% chance for level 3 (most hostile)
                return np.random.choice(Config.HOSTILE_COUNTRIES[3])
            elif rand_val < 0.25:  # 10% chance for level 2
                return np.random.choice(Config.HOSTILE_COUNTRIES[2])
            elif rand_val < 0.35:  # 10% chance for level 1 (least hostile)
                return np.random.choice(Config.HOSTILE_COUNTRIES[1])
            else:  # 65% chance for regular countries
                return np.random.choice(Config.TRAVEL_COUNTRIES)
        else:
            # Non-malicious users rarely visit hostile countries
            rand_val = np.random.random()
            
            if rand_val < 0.02:  # 2% chance for level 1 (least hostile)
                return np.random.choice(Config.HOSTILE_COUNTRIES[1])
            elif rand_val < 0.03:  # 1% chance for level 2
                return np.random.choice(Config.HOSTILE_COUNTRIES[2])
            elif rand_val < 0.035:  # 0.5% chance for level 3 (most hostile)
                return np.random.choice(Config.HOSTILE_COUNTRIES[3])
            else:  # 96.5% chance for regular countries
                return np.random.choice(
                                Config.TRAVEL_COUNTRIES,
                                p=Config.TRAVEL_COUNTRY_WEIGHTS
                            )  
              
    def _get_hostility_level(self, country: str) -> int:
        """Get hostility level for a country (0 = not hostile, 1-3 = hostile levels)"""
        for level, countries in Config.HOSTILE_COUNTRIES.items():
            if country in countries:
                return level
        return 0
    
    def _no_travel_activity(self) -> Dict[str, Any]:
        """Return empty travel activity"""
        return {
            'is_abroad': 0,
            'trip_day_number': None,
            'country_name': None,
            'is_hostile_country_trip': 0,
            'hostility_country_level': 0,
            'is_official_trip': 0
        }