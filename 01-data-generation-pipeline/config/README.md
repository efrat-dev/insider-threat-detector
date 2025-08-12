# Configuration Directory

This directory contains all configuration modules used for synthetic employee dataset generation and behavioral analysis. The configuration system is designed to simulate realistic organizational structures, employee behaviors, and characteristics for security research and testing purposes.

## Files Overview

### [`config.py`](config/config.py)
Main configuration aggregator module that serves as the central access point for all configuration components. This module consolidates organizational structure, behavioral patterns, employee attributes, and geographic data into a single unified configuration class.

**Key Features:**
- Unified `Config` class combining all configuration aspects through multiple inheritance
- Default dataset parameters (employee count, time range, malicious ratio)
- Central import point for all configuration modules

### [`behavioral_patterns.py`](config/behavioral_patterns.py)
Defines behavioral characteristics and patterns for different employee groups used in synthetic data generation and behavioral analysis.

**Employee Groups:**
- **Group A**: Executive Management
- **Group B**: Developers & Engineers  
- **Group C**: Office Workers & Secretaries
- **Group D**: Marketing & Business Development
- **Group E**: Security Personnel
- **Group F**: IT Staff

**Pattern Attributes:**
- Work hours distributions (start/end times with statistical parameters)
- Print activity likelihood and volume parameters
- Data burning activity probabilities and parameters
- Travel likelihood probabilities
- Off-hours and weekend work tendencies
- Classification level flags for sensitive activities

### [`organizational_structure.py`](config/organizational_structure.py)
Contains organizational hierarchy definitions, department structures, position titles, and behavioral group mappings.

**Key Components:**
- **Department Positions**: Complete mapping of departments to their respective job titles
- **Behavioral Groups**: Links departments to behavioral pattern groups (A-F)
- **Department Weights**: Relative size weights for realistic employee distribution

**Departments Included:**
- Executive Management
- R&D Department
- Engineering Department
- Operations and Manufacturing
- Project Management
- Security and Information Security
- Human Resources
- Legal and Regulation
- Finance
- Marketing and Business Development
- Information Technology

### [`employee_attributes.py`](config/employee_attributes.py)
Defines probabilistic distributions for employee characteristics, security classifications, and seniority ranges.

**Configuration Areas:**
- **Security Classification**: Department-specific probability distributions for security clearance levels (1-4)
- **Seniority Ranges**: Years of experience ranges by position category (executive, manager, secretary, default)
- **Employee Probabilities**: Binary attribute probabilities for:
  - Contractor status
  - Foreign citizenship
  - Criminal record
  - Medical history

### [`geographic_data.py`](config/geographic_data.py)
Contains geographic information for employee origins, campus locations, travel patterns, and security threat assessments.

**Geographic Components:**
- **Campus Locations**: List of available campus sites
- **Origin Countries**: Employee origin countries with weighted probability distributions
- **Travel Destinations**: Common business travel countries with frequency weights
- **Hostile Countries**: Security threat classification by country (levels 1-3)

## Usage Example

```python
from config.config import Config

# Access unified configuration
config = Config()

# Get behavioral patterns
executive_patterns = config.GROUP_PATTERNS['A']  # Executive Management
developer_patterns = config.GROUP_PATTERNS['B']   # Developers & Engineers

# Access organizational structure
departments = config.DEPARTMENT_POSITIONS
behavioral_mapping = config.BEHAVIORAL_GROUPS

# Get employee attribute configurations
classification_probs = config.CLASSIFICATION_PROBABILITIES
seniority_ranges = config.SENIORITY_RANGES

# Access geographic data
origin_countries = config.ORIGIN_COUNTRIES
hostile_countries = config.HOSTILE_COUNTRIES

# Use default parameters
num_employees = config.DEFAULT_NUM_EMPLOYEES      # 1666
days_range = config.DEFAULT_DAYS_RANGE           # 180
malicious_ratio = config.DEFAULT_MALICIOUS_RATIO # 0.05
```

## Configuration Design Principles

### Realistic Modeling
The configuration system is designed to generate synthetic data that closely resembles real organizational behavior patterns while maintaining statistical targets (mean-median gaps, standard deviations).

### Modular Architecture
Each configuration aspect is separated into its own module for maintainability and extensibility, while being unified through the main `Config` class.

### Probabilistic Distributions
Most parameters use probabilistic distributions rather than fixed values to simulate natural variance in employee behavior and characteristics.

### Security-Aware Design
The system includes security classification levels, hostile country definitions, and sensitive activity patterns to support security research applications.

## Customization

To modify the configuration:

1. **Add new behavioral groups**: Extend `GROUP_PATTERNS` in `behavioral_patterns.py`
2. **Add departments**: Update `DEPARTMENT_POSITIONS`, `BEHAVIORAL_GROUPS`, and `DEPARTMENT_WEIGHTS` in `organizational_structure.py`
3. **Modify employee attributes**: Adjust probabilities and ranges in `employee_attributes.py`
4. **Update geographic data**: Modify country lists and weights in `geographic_data.py`
5. **Change defaults**: Update default parameters in `config.py`

## Dependencies

The configuration system is self-contained and doesn't require external dependencies beyond Python's standard library. All modules use relative imports and are designed to work together as a cohesive configuration package.
