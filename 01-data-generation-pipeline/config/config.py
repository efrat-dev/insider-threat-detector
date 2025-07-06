class Config:
    # Department-Position mapping based on organizational structure
    DEPARTMENT_POSITIONS = {
        'Executive Management': [
            'Chief Executive Officer (CEO)',
            'Chief Legal Officer',
            'Chief Human Resources Officer (CHRO)',
            'Chief Information Officer (CIO)',
            'Chief Technology Officer (CTO)',
            'Chief Operating Officer (COO)',
            'Chief Financial Officer (CFO)',
            'Chief Marketing and Business Development Officer',
            'Secretary'
        ],
        'R&D Department': [
            'Head of R&D',
            'Systems Engineer',
            'Development Engineer (Hardware / Software / Mechanical)',
            'Algorithm Engineer',
            'Integration and Testing Engineer',
            'Secretary'
        ],
        'Engineering Department': [
            'Process Engineer',
            'Design Engineer',
            'Head of Engineering',
            'Systems Engineer',
            'Test Engineer',
            'Secretary'
        ],
        'Operations and Manufacturing': [
            'Operations Manager',
            'Manufacturing Engineer',
            'Logistics Manager',
            'Procurement Officer',
            'Warehouse Manager',
            'Secretary'
        ],
        'Project Management': [
            'Project Manager',
            'Project Engineer',
            'Project Coordinator',
            'Secretary'
        ],
        'Security and Information Security': [
            'Physical Access Control',
            'Information Security Investigator',
            'Cyber Analyst',
            'Chief Information Security Officer (CISO)',
            'Security Officer'
        ],
        'Human Resources': [
            'HR Manager',
            'Recruitment Coordinator',
            'Employee Welfare Coordinator',
            'Training Coordinator',
            'Secretary'
        ],
        'Legal and Regulation': [
            'Regulatory Affairs Officer',
            'Defense Export Compliance Officer',
            'Legal Advisor'
        ],
        'Finance': [
            'Accountant',
            'Financial Analyst',
            'Budget Manager',
            'Finance Manager',
            'Secretary'
        ],
        'Marketing and Business Development': [
            'Business Development Manager',
            'Account Manager',
            'Bid Coordinator',
            'Marketing Manager',
            'Secretary'
        ],
        'Information Technology': [
            'IT Director',
            'Information Security Specialist',
            'Systems and Network Administrator',
            'BI Developer / Data Analyst',
            'Enterprise Systems Developer (ERP / CRM / SAP)',
            'Data Scientist',
            'Secretary'
        ]
    }

    # Behavioral groups mapping
    BEHAVIORAL_GROUPS = {
        'Executive Management': 'A',
        'Marketing and Business Development': 'D',
        'R&D Department': 'B',
        'Engineering Department': 'B',
        'Information Technology': 'F',
        'Security and Information Security': 'E',
        'Human Resources': 'C',
        'Finance': 'C',
        'Legal and Regulation': 'C',
        'Operations and Manufacturing': 'C',
        'Project Management': 'C'
    }

    # Behavioral patterns for each group
    GROUP_PATTERNS = {
        'A': {  # Executive Management
            'work_hours': {'start_mean': 7.5, 'start_std': 1.0, 'end_mean': 18.5, 'end_std': 1.5},
            'print_likelihood': 0.4,
            'print_volume': {'commands_mean': 4, 'pages_mean': 8, 'color_ratio': 0.4},
            'burn_likelihood': 0.08,
            'burn_params': {'requests_mean': 2, 'volume_mean': 7.5, 'files_mean': 15, 'high_classification': True},
            'travel_likelihood': 0.015,
            'off_hours_tendency': 0.3
        },
        'B': {  # Developers & Engineers
            'work_hours': {'start_mean': 8.5, 'start_std': 0.8, 'end_mean': 18.0, 'end_std': 2.0},
            'print_likelihood': 0.2,
            'print_volume': {'commands_mean': 2, 'pages_mean': 4, 'color_ratio': 0.1},
            'burn_likelihood': 0.12,
            'burn_params': {'requests_mean': 3, 'volume_mean': 6.8, 'files_mean': 35, 'high_classification': False},
            'travel_likelihood': 0.003,
            'off_hours_tendency': 0.4
        },
        'C': {  # Office Workers & Secretaries
            'work_hours': {'start_mean': 8.0, 'start_std': 0.3, 'end_mean': 16.5, 'end_std': 0.5},
            'print_likelihood': 0.6,
            'print_volume': {'commands_mean': 5, 'pages_mean': 12, 'color_ratio': 0.25},
            'burn_likelihood': 0.03,
            'burn_params': {'requests_mean': 1, 'volume_mean': 5.5, 'files_mean': 8, 'high_classification': False},
            'travel_likelihood': 0.001,
            'off_hours_tendency': 0.05
        },
        'D': {  # Marketing & Business Development
            'work_hours': {'start_mean': 8.2, 'start_std': 1.0, 'end_mean': 17.8, 'end_std': 1.8},
            'print_likelihood': 0.7,
            'print_volume': {'commands_mean': 6, 'pages_mean': 15, 'color_ratio': 0.6},
            'burn_likelihood': 0.06,
            'burn_params': {'requests_mean': 2, 'volume_mean': 6.5, 'files_mean': 20, 'high_classification': False},
            'travel_likelihood': 0.012,
            'off_hours_tendency': 0.2
        },
        'E': {  # Security
            'work_hours': {'start_mean': 8.0, 'start_std': 4.0, 'end_mean': 17.0, 'end_std': 4.0},
            'print_likelihood': 0.15,
            'print_volume': {'commands_mean': 2, 'pages_mean': 3, 'color_ratio': 0.05},
            'burn_likelihood': 0.04,
            'burn_params': {'requests_mean': 1, 'volume_mean': 6.0, 'files_mean': 5, 'high_classification': True},
            'travel_likelihood': 0.001,
            'off_hours_tendency': 0.8,
            'weekend_work': 0.6
        },
        'F': {  # IT
            'work_hours': {'start_mean': 8.5, 'start_std': 1.2, 'end_mean': 17.5, 'end_std': 2.5},
            'print_likelihood': 0.25,
            'print_volume': {'commands_mean': 3, 'pages_mean': 6, 'color_ratio': 0.15},
            'burn_likelihood': 0.15,
            'burn_params': {'requests_mean': 4, 'volume_mean': 7.2, 'files_mean': 45, 'high_classification': False},
            'travel_likelihood': 0.002,
            'off_hours_tendency': 0.35
        }
    }

    # Department size weights for realistic distribution
    DEPARTMENT_WEIGHTS = {
        'R&D Department': 0.25,
        'Engineering Department': 0.20,
        'Information Technology': 0.12,
        'Operations and Manufacturing': 0.15,
        'Marketing and Business Development': 0.08,
        'Project Management': 0.08,
        'Finance': 0.04,
        'Human Resources': 0.03,
        'Security and Information Security': 0.03,
        'Legal and Regulation': 0.015,
        'Executive Management': 0.005
    }

    # Geographic data
    CAMPUSES = ['Campus A', 'Campus B', 'Campus C']
    ORIGIN_COUNTRIES = ['Israel', 'USA', 'Russia', 'China', 'India', 'Germany', 'France', 'UK', 'Canada', 'Australia', 'Other']
    ORIGIN_COUNTRY_WEIGHTS = [0.05, 0.03, 0.02, 0.05, 0.05, 0.2, 0.15, 0.1, 0.1, 0.1, 0.15]

    TRAVEL_COUNTRIES = ['USA', 'Germany', 'France', 'UK', 'Canada', 'Australia', 'Japan', 'South Korea', 'Singapore', 'India', 'China', 'Russia', 'Turkey', 'UAE', 'Other']
    HOSTILE_COUNTRIES = ['Iran', 'Russia', 'China', 'North Korea', 'Syria']

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

    # Default dataset parameters
    DEFAULT_NUM_EMPLOYEES = 1000
    DEFAULT_DAYS_RANGE = 180
    DEFAULT_MALICIOUS_RATIO = 0.05
