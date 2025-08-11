"""
Print Activity Generator

This module contains logic for generating daily printing activities for employees.
It simulates realistic printing behavior, including:
- Number of print commands and pages
- Distribution of color vs. black-and-white prints
- Off-hours printing tendencies
- Multi-campus printing scenarios
"""

import datetime
import numpy as np
from typing import Dict, Any, Tuple

class PrintActivityGenerator:
    """
    Generates printing activities for employees.

    Attributes:
        patterns (dict): Behavioral patterns configuration for employee groups.
    """

    def __init__(self, behavioral_patterns: Dict[str, Any]):
        """
        Initialize the generator.

        Parameters:
            behavioral_patterns (dict): Mapping of behavioral groups to print activity parameters.
        """
        self.patterns = behavioral_patterns

    def generate_print_activity(
        self,
        employee: Dict[str, Any],
        date: datetime.date,
        is_malicious: bool,
        is_abroad: bool
    ) -> Dict[str, Any]:
        """
        Generate daily print activity for an employee.

        Parameters:
            employee (dict): Employee profile.
            date (datetime.date): Target date for activity generation.
            is_malicious (bool): Whether the employee is flagged as malicious.
            is_abroad (bool): Whether the employee is abroad on this date.

        Returns:
            dict: Printing activity details for the given date.
        """
        # Low probability of printing when abroad
        if is_abroad and not is_malicious and np.random.random() < 0.98:
            return self._empty_print_activity()
        if is_abroad and is_malicious and np.random.random() < 0.85:
            return self._empty_print_activity()

        group = employee['behavioral_group']
        pattern = self.patterns[group]

        # Determine if the employee prints today
        if np.random.random() > pattern['print_likelihood']:
            return self._empty_print_activity()

        multiplier = self._get_malicious_multiplier(is_malicious)

        base_commands = max(1, int(np.random.poisson(pattern['print_volume']['commands_mean'])))

        # Pages follow a right-skewed distribution using gamma
        if is_malicious:
            pages_base = pattern['print_volume']['pages_mean'] * 5
        else:
            pages_base = pattern['print_volume']['pages_mean']

        shape = 1.2  # Controls skewness
        scale = pages_base / shape
        total_pages = max(1, int(np.random.gamma(shape, scale) * multiplier))

        if total_pages > pages_base * 2:
            num_commands = base_commands + np.random.poisson(1)
        else:
            num_commands = base_commands

        color_ratio = self._calculate_color_ratio(pattern['print_volume']['color_ratio'])

        off_hours_commands, off_hours_pages = self._calculate_off_hours_printing(
            num_commands, total_pages, pattern, is_malicious)

        print_campuses, printed_from_other = self._calculate_multi_campus_printing(
            employee, is_malicious)

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
        """
        Return multiplier for malicious employees printing volume.

        Returns:
            float: Multiplier to scale printed pages.
        """
        if is_malicious:
            return np.random.uniform(0.8, 1.2)
        return np.random.uniform(0.7, 1.3)

    def _calculate_color_ratio(self, base_ratio: float) -> float:
        """
        Calculate color print ratio with some noise.

        Returns:
            float: Adjusted color print ratio between 0 and 1.
        """
        return max(0, min(1, np.random.normal(base_ratio, 0.1)))

    def _calculate_off_hours_printing(
        self,
        num_commands: int,
        total_pages: int,
        pattern: Dict[str, Any],
        is_malicious: bool
    ) -> Tuple[int, int]:
        """
        Calculate off-hours printing commands and pages.

        Returns:
            tuple: (num_off_hours_commands, num_off_hours_pages)
        """
        off_hours_tendency = pattern.get('off_hours_tendency', 0.1)

        if is_malicious:
            off_hours_tendency = min(0.4, off_hours_tendency * 1.8)

        if np.random.random() < off_hours_tendency:
            if is_malicious:
                off_hours_ratio = np.random.uniform(0.3, 0.7)
            else:
                off_hours_ratio = np.random.uniform(0.1, 0.4)

            off_hours_commands = max(0, int(num_commands * off_hours_ratio))
            off_hours_pages = max(0, int(total_pages * off_hours_ratio))
            return off_hours_commands, off_hours_pages

        return 0, 0

    def _calculate_multi_campus_printing(
        self,
        employee: Dict[str, Any],
        is_malicious: bool
    ) -> Tuple[int, int]:
        """
        Calculate multi-campus printing characteristics.

        Returns:
            tuple: (number_of_campuses_printed_from, printed_from_other_campus_flag)
        """
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
        """
        Return empty print activity indicating no prints.

        Returns:
            dict: Empty print activity data.
        """
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