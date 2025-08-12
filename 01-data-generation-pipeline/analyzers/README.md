# Analyzers Directory

This directory contains a comprehensive suite of Python classes for analyzing insider threat datasets. The analyzers provide statistical insights, behavioral pattern detection, security risk assessment, and data quality validation for employee activity data.

## File Structure

```
analyzers/
├── base_analyzer.py          # Base class with common utilities
├── behavioral_analyzer.py    # Behavioral group analysis
├── comprehensive_analyzer.py # Integrated comprehensive analysis
└── security_analyzer.py     # Security and malicious behavior analysis
```

## Overview

The analyzer suite is designed to process employee activity datasets containing information about:
- Building access patterns
- Printing and document activities
- Secure document burning/destruction
- Travel activities
- Work schedule patterns
- Security classifications and risk indicators

## Core Components

### [base_analyzer.py](analyzers/base_analyzer.py)

**BaseAnalyzer** - Foundation class providing:

- **Behavioral Group Mapping**: Configurable mapping from group codes to human-readable names
- **Basic Statistics Generation**: Dataset overview including employee counts, date ranges, malicious activity ratios
- **Data Quality Analysis**: Missing value detection, consistency checks, logical validation
- **Validation Framework**: Comprehensive data integrity verification

**Key Features:**
- Default behavioral group classifications (Standard Employee, High Activity, Suspicious Activity, etc.)
- Automated data type and structure validation
- Off-hours activity ratio calculations
- Classification level analysis

### [behavioral_analyzer.py](analyzers/behavioral_analyzer.py)

**BehavioralAnalyzer** - Specialized analysis by behavioral groups:

- **Work Pattern Analysis**: Entry/exit times, early/late patterns, weekend and night work
- **Printing Pattern Analysis**: Frequency, volume, color ratios, off-hours printing, multi-campus activity
- **Burning Pattern Analysis**: Secure destruction frequency, classification levels, volume analysis
- **Travel Pattern Analysis**: Trip frequency, official vs unofficial travel, hostile country visits

**Key Metrics:**
- Group-specific malicious employee ratios
- Activity pattern distributions
- Cross-campus behavior analysis
- Temporal activity patterns

### [security_analyzer.py](analyzers/security_analyzer.py)

**SecurityAnalyzer** - Security-focused threat detection:

- **Malicious vs Normal Comparison**: Comparative analysis between employee types
- **Risk Assessment**: Travel risk, off-hours activity, data exfiltration indicators
- **Anomaly Detection**: Unusual patterns in night work, multi-campus access, high-volume activities
- **Security Metrics**: Classification levels, hostile country travel, suspicious activity indicators

**Key Capabilities:**
- Threat indicator correlation
- Behavioral deviation detection
- Risk scoring and assessment
- Security pattern identification

### [comprehensive_analyzer.py](analyzers/comprehensive_analyzer.py)

**ComprehensiveAnalyzer** - Integrated analysis orchestrator:

- **Multi-Analyzer Integration**: Combines behavioral and security analyses
- **Temporal Trend Analysis**: Monthly and weekly activity patterns
- **Activity Pattern Mapping**: Daily, weekly, and cross-campus activity distributions
- **Export Functionality**: Excel export with multiple analysis sheets

**Integration Features:**
- Unified analysis results
- Cross-referenced insights
- Comprehensive reporting
- Data export capabilities

## Usage Example

```python
from analyzers.comprehensive_analyzer import ComprehensiveAnalyzer
import pandas as pd

# Load your dataset
df = pd.read_csv('employee_activity_data.csv')

# Initialize the comprehensive analyzer
analyzer = ComprehensiveAnalyzer()

# Generate complete analysis
results = analyzer.generate_comprehensive_analysis(df)

# Export results to Excel
analyzer.export_analysis_results(df, 'analysis_report.xlsx')

# Access specific analysis components
basic_stats = results['basic_stats']
behavioral_insights = results['behavioral_analysis']
security_patterns = results['security_analysis']
```

## Required Dataset Columns

### Core Required Columns
- `employee_id`: Unique employee identifier
- `date`: Activity date
- `is_malicious`: Binary indicator (0/1) for malicious employees

### Optional Behavioral Columns
- `behavioral_group`: Numeric group classification
- `employee_department`: Department assignment
- `employee_campus`: Primary campus location
- `employee_classification`: Security clearance level

### Work Pattern Columns
- `num_entries`: Daily building access count
- `first_entry_time`: First building entry time (HH:MM)
- `last_exit_time`: Last building exit time (HH:MM)
- `early_entry_flag`: Early arrival indicator
- `late_exit_flag`: Late departure indicator
- `entry_during_weekend`: Weekend work indicator
- `entered_during_night_hours`: Night access indicator
- `num_unique_campus`: Number of different campuses accessed

### Printing Activity Columns
- `total_printed_pages`: Daily page count
- `num_print_commands`: Print command count
- `num_print_commands_off_hours`: Off-hours printing
- `ratio_color_prints`: Color printing ratio
- `printed_from_other`: Cross-campus printing indicator

### Burning/Destruction Columns
- `num_burn_requests`: Secure destruction requests
- `num_burn_requests_off_hours`: Off-hours burning
- `total_burn_volume_mb`: Data volume destroyed (MB)
- `total_files_burned`: File count destroyed
- `avg_request_classification`: Average security classification
- `max_request_classification`: Highest security classification
- `burned_from_other`: Cross-campus burning indicator

### Travel Columns
- `is_abroad`: International travel indicator
- `is_official_trip`: Official business travel flag
- `is_hostile_country_trip`: Hostile nation travel flag
- `is_origin_country_trip`: Origin country visit flag
- `trip_day_number`: Sequential trip day number
- `risk_travel_indicator`: Travel risk assessment

## Output Structure

The analysis results are organized into hierarchical dictionaries containing:

- **Basic Statistics**: Employee counts, date ranges, activity distributions
- **Behavioral Analysis**: Group-specific patterns and comparisons
- **Security Analysis**: Threat indicators, risk assessments, anomaly detection
- **Temporal Analysis**: Time-based trends and patterns
- **Data Quality**: Validation results and consistency checks

## Dependencies

```python
pandas>=1.3.0
numpy>=1.20.0
openpyxl>=3.0.0  # For Excel export functionality
```

## License

This analyzer suite is designed for insider threat research and security analysis purposes. Please ensure compliance with your organization's data privacy and security policies when processing employee activity data.
