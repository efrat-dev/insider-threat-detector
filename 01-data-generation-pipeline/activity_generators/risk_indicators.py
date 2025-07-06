"""
risk_indicators.py - Risk indicator calculation
Contains logic for calculating various risk indicators and metrics
"""

import numpy as np
from typing import Dict, Any


class RiskIndicatorGenerator:
    """Class for generating risk indicators"""
    
    @staticmethod
    def calculate_risk_travel_indicator(travel_data: Dict[str, Any], 
                                      print_data: Dict[str, Any],
                                      burn_data: Dict[str, Any]) -> int:
        """Calculate travel risk indicator"""
        if (travel_data['is_abroad'] == 1 and 
            travel_data['is_official_trip'] == 0 and 
            travel_data['is_hostile_country_trip'] == 1 and
            (burn_data['total_files_burned'] > 0 or 
             print_data['total_printed_pages'] > 0)):
            return 1
        return 0
    
    @staticmethod
    def calculate_additional_risk_indicators(employee: Dict[str, Any],
                                           all_activities: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate additional risk indicators"""
        
        # Unusual activity score
        unusual_activity_score = 0
        
        # Off-hours activity
        if (all_activities['num_print_commands_off_hours'] > 0 or
            all_activities['num_burn_requests_off_hours'] > 0):
            unusual_activity_score += 1
        
        # Multi-campus activity
        if (all_activities['printed_from_other'] == 1 or
            all_activities['burned_from_other'] == 1):
            unusual_activity_score += 1
        
        # Unusual access
        if (all_activities['entered_during_night_hours'] == 1 or
            all_activities['entry_during_weekend'] == 1):
            unusual_activity_score += 1
        
        return {
            'unusual_activity_score': unusual_activity_score,
            'high_volume_print_flag': 1 if all_activities['total_printed_pages'] > 50 else 0,
            'high_classification_burn_flag': 1 if all_activities['max_request_classification'] >= 4 else 0,
            'multi_campus_activity_flag': 1 if all_activities['num_unique_campus'] > 1 else 0
        }