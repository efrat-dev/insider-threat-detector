# behavioral_patterns.py
"""
Behavioral patterns definitions for different employee groups.
Updated to achieve target statistics: mean-median gap ~5.54, std ~20.42
"""

class BehavioralPatterns:
    # Behavioral patterns for each group
    GROUP_PATTERNS = {
        'A': {  # Executive Management
            'work_hours': {'start_mean': 7.5, 'start_std': 1.0, 'end_mean': 18.5, 'end_std': 1.5},
            'print_likelihood': 0.4,
            'print_volume': {'commands_mean': 4, 'pages_mean': 12, 'color_ratio': 0.4},  # Increased from 8
            'burn_likelihood': 0.08,
            'burn_params': {'requests_mean': 2, 'volume_mean': 7.5, 'files_mean': 15, 'high_classification': True},
            'travel_likelihood': 0.015,
            'off_hours_tendency': 0.3
        },
        'B': {  # Developers & Engineers
            'work_hours': {'start_mean': 8.5, 'start_std': 0.8, 'end_mean': 18.0, 'end_std': 2.0},
            'print_likelihood': 0.2,
            'print_volume': {'commands_mean': 2, 'pages_mean': 6, 'color_ratio': 0.1},  # Increased from 4
            'burn_likelihood': 0.12,
            'burn_params': {'requests_mean': 3, 'volume_mean': 6.8, 'files_mean': 35, 'high_classification': False},
            'travel_likelihood': 0.003,
            'off_hours_tendency': 0.4
        },
        'C': {  # Office Workers & Secretaries
            'work_hours': {'start_mean': 8.0, 'start_std': 0.3, 'end_mean': 16.5, 'end_std': 0.5},
            'print_likelihood': 0.6,
            'print_volume': {'commands_mean': 5, 'pages_mean': 18, 'color_ratio': 0.25},  # Increased from 12
            'burn_likelihood': 0.03,
            'burn_params': {'requests_mean': 1, 'volume_mean': 5.5, 'files_mean': 8, 'high_classification': False},
            'travel_likelihood': 0.001,
            'off_hours_tendency': 0.05
        },
        'D': {  # Marketing & Business Development
            'work_hours': {'start_mean': 8.2, 'start_std': 1.0, 'end_mean': 17.8, 'end_std': 1.8},
            'print_likelihood': 0.7,
            'print_volume': {'commands_mean': 6, 'pages_mean': 22, 'color_ratio': 0.6},  # Increased from 15
            'burn_likelihood': 0.06,
            'burn_params': {'requests_mean': 2, 'volume_mean': 6.5, 'files_mean': 20, 'high_classification': False},
            'travel_likelihood': 0.012,
            'off_hours_tendency': 0.2
        },
        'E': {  # Security
            'work_hours': {'start_mean': 8.0, 'start_std': 4.0, 'end_mean': 17.0, 'end_std': 4.0},
            'print_likelihood': 0.15,
            'print_volume': {'commands_mean': 2, 'pages_mean': 4, 'color_ratio': 0.05},  # Increased from 3
            'burn_likelihood': 0.04,
            'burn_params': {'requests_mean': 1, 'volume_mean': 6.0, 'files_mean': 5, 'high_classification': True},
            'travel_likelihood': 0.001,
            'off_hours_tendency': 0.3,  # Reduced from 0.8 to be more realistic
            'weekend_work': 0.6
        },
        'F': {  # IT
            'work_hours': {'start_mean': 8.5, 'start_std': 1.2, 'end_mean': 17.5, 'end_std': 2.5},
            'print_likelihood': 0.25,
            'print_volume': {'commands_mean': 3, 'pages_mean': 9, 'color_ratio': 0.15},  # Increased from 6
            'burn_likelihood': 0.15,
            'burn_params': {'requests_mean': 4, 'volume_mean': 7.2, 'files_mean': 45, 'high_classification': False},
            'travel_likelihood': 0.002,
            'off_hours_tendency': 0.35
        }
    }