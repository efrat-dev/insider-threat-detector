# employee_attributes.py
"""
Employee attributes, security classifications, and seniority definitions.
"""

class EmployeeAttributes:
    # Classification probabilities by department
    CLASSIFICATION_PROBABILITIES = {
        'Executive Management': {
            'levels': [3, 4],
            'weights': [0.3, 0.7]
        },
        'Security and Information Security': {
            'levels': [2, 3, 4],
            'weights': [0.2, 0.5, 0.3]
        },
        'Legal and Regulation': {
            'levels': [2, 3, 4],
            'weights': [0.2, 0.5, 0.3]
        },
        'R&D Department': {
            'levels': [2, 3],
            'weights': [0.6, 0.4]
        },
        'Engineering Department': {
            'levels': [2, 3],
            'weights': [0.6, 0.4]
        },
        'default': {
            'levels': [1, 2, 3],
            'weights': [0.5, 0.4, 0.1]
        }
    }

    # Seniority ranges by position type
    SENIORITY_RANGES = {
        'executive': (8, 31),    # Chief, Head of, Director
        'manager': (5, 21),      # Manager
        'secretary': (1, 16),    # Secretary
        'default': (0, 26)       # All others
    }

    # Employee attribute probabilities
    EMPLOYEE_PROBABILITIES = {
        'contractor': {'values': [0, 1], 'weights': [0.85, 0.15]},
        'foreign_citizenship': {'values': [0, 1], 'weights': [0.85, 0.15]},
        'criminal_record': {'values': [0, 1], 'weights': [0.95, 0.05]},
        'medical_history': {'values': [0, 1], 'weights': [0.85, 0.15]}
    }