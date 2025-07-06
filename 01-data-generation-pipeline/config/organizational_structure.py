# organizational_structure.py
"""
Organizational structure definitions including departments, positions, and behavioral groups.
"""

class OrganizationalStructure:
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