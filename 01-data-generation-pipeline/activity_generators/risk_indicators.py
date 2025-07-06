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