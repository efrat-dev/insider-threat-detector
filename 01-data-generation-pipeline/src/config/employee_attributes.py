"""
Definitions of employee attributes, security classification probabilities, and seniority ranges.

This module contains probabilistic distributions and ranges used to simulate realistic
employee characteristics across different departments and position types.

- Classification probabilities specify security clearance or classification levels by department.
- Seniority ranges define expected years of experience for different roles.
- Employee attribute probabilities model binary attributes such as contractor status,
  foreign citizenship, criminal record, and medical history.
"""

class EmployeeAttributes:
    # Security classification level probabilities per department
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

    # Seniority (years of experience) ranges by employee position category
    SENIORITY_RANGES = {
        'executive': (8, 31),    # Chief, Head of, Director roles
        'manager': (5, 21),      # Managers
        'secretary': (1, 16),    # Secretaries
        'default': (0, 26)       # Other roles
    }

    # Probabilistic binary employee attributes with weights for 0/1 values
    EMPLOYEE_PROBABILITIES = {
        'contractor': {'values': [0, 1], 'weights': [0.85, 0.15]},
        'foreign_citizenship': {'values': [0, 1], 'weights': [0.85, 0.15]},
        'criminal_record': {'values': [0, 1], 'weights': [0.95, 0.05]},
        'medical_history': {'values': [0, 1], 'weights': [0.85, 0.15]}
    }