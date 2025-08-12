# Data Exporter

A comprehensive Python package for analyzing, processing, and exporting insider threat datasets with detailed documentation and reporting capabilities.

## Overview

The Data Exporter package provides tools for:
- Generating data dictionaries and documentation
- Creating comprehensive analysis reports
- Exporting datasets to multiple formats (CSV, Excel)
- Performing statistical analysis and behavioral profiling
- Summarizing employee activities and risk indicators

## Package Structure

```
data_exporter/
├── data_dictionary_generator.py    # Data dictionary creation and documentation
├── report_generator.py            # Analysis report generation
├── data_exporter_base.py          # Main export functionality
└── summary_analyzer.py            # Statistical analysis and summaries
```

## Files Description

### [data_dictionary_generator.py](data_exporter/data_dictionary_generator.py)
Creates comprehensive data dictionaries explaining all dataset columns, behavioral groups, and data structure.

**Key Features:**
- Complete column documentation
- Behavioral group definitions (A-F)
- Data format specifications
- Risk indicator explanations

### [report_generator.py](data_exporter/report_generator.py)
Generates detailed analysis reports with statistics and insights.

**Key Features:**
- Dataset overview and metrics
- Malicious employee analysis
- Department and behavioral group breakdowns
- Activity statistics and off-hours monitoring
- Data quality checks and recommendations

### [data_exporter_base.py](data_exporter/data_exporter_base.py)
Main export functionality for converting datasets to various formats.

**Key Features:**
- Multi-format export (CSV, Excel)
- Multiple Excel sheets with different views
- Automated timestamp naming
- Configurable output paths
- Integration with analysis components

### [summary_analyzer.py](data_exporter/summary_analyzer.py)
Provides statistical analysis and summary creation capabilities.

**Key Features:**
- Behavioral group summaries
- Per-employee activity profiles
- Daily aggregated statistics
- Suspicion scoring algorithms
- Risk indicator calculations

## Usage Examples

### Basic Export
```python
from data_exporter.data_exporter_base import DataExporter

# Initialize exporter
exporter = DataExporter()

# Export to both CSV and Excel
exported_files = exporter.export_dataset(
    df=your_dataframe,
    output_path="./exports/",
    filename_prefix="insider_threat",
    export_format='both',
    include_analysis=True
)
```

### Generate Documentation
```python
from data_exporter.data_dictionary_generator import DataDictionaryGenerator

# Create data dictionary
dict_gen = DataDictionaryGenerator()
dict_gen.create_data_dictionary("data_dictionary.txt")
```

### Create Analysis Report
```python
from data_exporter.report_generator import ReportGenerator

# Generate comprehensive report
behavioral_mapping = {
    'Executive Management': 'A',
    'Engineering Department': 'B',
    # ... other mappings
}

report_gen = ReportGenerator(behavioral_mapping)
report_gen.create_analysis_report(df, "analysis_report.txt")
```

### Statistical Analysis
```python
from data_exporter.summary_analyzer import SummaryAnalyzer

# Create summaries
analyzer = SummaryAnalyzer(behavioral_mapping)

# Group-level analysis
group_summary = analyzer.create_group_summary(df)

# Employee-level analysis
employee_summary = analyzer.create_employee_summary(df)

# Daily trends
daily_summary = analyzer.create_daily_summary(df)
```

## Behavioral Groups

The system categorizes employees into behavioral groups based on their roles:

- **Group A**: Executive Management - Irregular hours, moderate printing
- **Group B**: Developers & Engineers - Technical staff, some late hours
- **Group C**: Office Workers - Regular hours, high printing activity
- **Group D**: Marketing & Business Development - Regular hours, travel
- **Group E**: Security Personnel - 24/7 shifts, high security access
- **Group F**: IT Staff - Technical roles, irregular hours, high burning

## Export Formats

### CSV Export
- Clean dataset without internal behavioral group columns
- Standard comma-separated format
- Timestamped filenames

### Excel Export
Multiple sheets containing:
- **Full_Dataset**: Complete cleaned dataset
- **Malicious_Only**: Records flagged as malicious
- **Group_Summary**: Behavioral group statistics
- **Employee_Summary**: Per-employee profiles
- **Daily_Summary**: Daily aggregated metrics

## Risk Indicators

The system tracks various risk indicators:
- Off-hours activities (printing, document burning)
- Multi-campus access patterns
- Travel to hostile countries
- High-classification document handling
- Weekend and early/late access
- Suspicious activity combinations

## Requirements

- pandas
- openpyxl (for Excel export)
- datetime
- os

## Output Files

When exporting with analysis enabled, the following files are generated:
- Dataset files (CSV/Excel with timestamp)
- `data_dictionary_[timestamp].txt` - Complete data documentation
- `analysis_report_[timestamp].txt` - Comprehensive analysis report

## Data Quality Features

- Missing value detection and reporting
- Logical consistency checks
- Data validation across related fields
- Statistical outlier identification
- Comprehensive data profiling
