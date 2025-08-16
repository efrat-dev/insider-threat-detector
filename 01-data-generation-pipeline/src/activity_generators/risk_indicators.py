"""
risk_indicators.py - Risk indicator calculation module

This module contains logic for calculating various risk indicators and metrics
based on employee activity data such as travel, printing, and burning activities.
"""

import numpy as np
from typing import Dict, Any


class RiskIndicatorGenerator:
    """Generates risk indicators based on employee activity data."""

    @staticmethod
    def calculate_risk_travel_indicator(
        travel_data: Dict[str, Any],
        print_data: Dict[str, Any],
        burn_data: Dict[str, Any]
    ) -> int:
        """
        Calculate travel-related risk indicator.

        The indicator flags risky travel if all the following conditions are met:
        - Employee is abroad (is_abroad == 1)
        - The trip is unofficial (is_official_trip == 0)
        - The trip is to a hostile country (is_hostile_country_trip == 1)
        - Either burning or printing activities occurred during the trip

        Parameters:
            travel_data (dict): Travel activity details for the employee.
            print_data (dict): Printing activity details for the employee.
            burn_data (dict): Burning activity details for the employee.

        Returns:
            int: 1 if travel risk conditions are met, else 0.
        """
        if (travel_data['is_abroad'] == 1 and
            travel_data['is_official_trip'] == 0 and
            travel_data['is_hostile_country_trip'] == 1 and
            (burn_data['total_files_burned'] > 0 or
             print_data['total_printed_pages'] > 0)):
            return 1
        return 0
