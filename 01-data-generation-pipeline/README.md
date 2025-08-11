# Synthetic Insider Threat Dataset Generator

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Active Development](https://img.shields.io/badge/Status-Active%20Development-green.svg)]()

## 🎯 Overview

The **Synthetic Insider Threat Dataset Generator** is a comprehensive tool designed to simulate realistic insider threat scenarios within **classified organizational environments** for cybersecurity research, machine learning model training, and security system evaluation. When real-world labeled data is limited or too sensitive to use, this tool provides high-quality synthetic datasets that mimic authentic organizational behavior patterns and security incidents in **high-security, classified settings** where traditional data collection is restricted.
Key Features

- 🔒 **Classified Environment Simulation:** Specifically designed for high-security, classified organizational settings with security clearance levels and sensitive data handling
- 🏢 **Realistic Organizational Structure:** Simulates 11 different departments with authentic position hierarchies typical of defense/security organizations
- 👥 **Behavioral Modeling:** Six distinct behavioral groups with characteristic activity patterns for classified environments
- 📊 **Advanced Analytics:** Built-in statistical analysis and data quality validation for security-focused datasets
- 🔄 **Noise Injection:** Configurable synthetic noise to simulate real-world data anomalies in classified systems
- 📈 **Scalable Generation:** Support for datasets ranging from hundreds to thousands of employees with security classifications
- 🎲 **Reproducible Results:** Seed-based random generation for consistent outputs in research environments
- 📋 **Multiple Export Formats:** CSV and Excel output options with comprehensive security-aware reporting


## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Dataset Structure](#-dataset-structure)
- [Behavioral Groups](#-behavioral-groups)
- [Command Line Arguments](#-command-line-arguments)
- [Output Files](#-output-files)
- [Project Structure](#-project-structure)
- [Advanced Features](#-advanced-features)
- [License](#-license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/your-username/synthetic-insider-threat-generator.git
cd synthetic-insider-threat-generator

# Install required packages
pip install -r requirements.txt
```

## ⚡ Quick Start

Generate a basic dataset with default settings:

```bash
python main.py
```

This will create:
- 1,666 employees across 11 departments
- 180 days of activity simulation  
- 5% malicious employee ratio
- Output files in `./output/` directory

## 💡 Usage Examples

### Basic Dataset Generation

```bash
# Generate default dataset
python main.py

# Custom employee count and duration
python main.py -e 500 -d 90

# Adjust malicious employee ratio
python main.py -m 0.08  # 8% malicious employees
```

### Advanced Generation Options

```bash
# Generate with specific random seed for reproducibility
python main.py --seed 42

# Export only to Excel format
python main.py --export-format excel

# Custom output directory and filename
python main.py -o my_dataset --output-dir ./custom_output
```

### Analysis and Noise Injection

```bash
# Add synthetic noise to simulate real-world anomalies
python main.py --add-noise --burn-noise-rate 0.1 --print-noise-rate 0.05

# Analysis-only mode on existing data
python main.py --analysis-only --input-file ./data/existing_dataset.csv

# Comprehensive data validation
python main.py --validate-data --verbose
```

## ⚙️ Configuration

The generator uses a sophisticated configuration system with multiple components:

### Organizational Structure

**11 Departments Supported:**
- Executive Management
- R&D Department  
- Engineering Department
- Information Technology
- Operations and Manufacturing
- Marketing and Business Development
- Project Management
- Finance
- Human Resources
- Security and Information Security
- Legal and Regulation

### Behavioral Groups

The system models **6 distinct behavioral patterns** (A-F):

| Group | Profile | Characteristics |
|-------|---------|-----------------|
| **A** | Executive Management | Late start/end times, high travel, strategic printing |
| **B** | Developers & Engineers | Flexible hours, technical focus, moderate off-hours work |
| **C** | Office Workers & Secretaries | Standard hours, high printing activity, minimal travel |
| **D** | Marketing & Business Development | Standard hours, high color printing, moderate travel |
| **E** | Security Personnel | Variable shifts, weekend work, minimal printing |
| **F** | IT Staff | Extended hours, high burning activity, off-hours maintenance |

### Employee Attributes

Each employee is generated with:
- **Personal Information**: Name, department, position, seniority
- **Geographic Data**: Origin country, campus location, travel patterns
- **Security Profile**: Classification level, contractor status, background flags
- **Behavioral Classification**: Activity patterns, work schedule preferences

## 📊 Dataset Structure

The generated dataset contains comprehensive employee activity records with the following key fields:

### Core Fields
- `employee_id`: Unique employee identifier
- `date`: Activity date
- `behavioral_group`: Employee behavior classification (A-F)
- `is_malicious`: Binary flag indicating insider threat status

### Employee Demographics
- `employee_name`, `employee_department`, `employee_position`
- `employee_seniority`, `employee_classification_level`
- `employee_origin_country`, `employee_campus`

### Activity Metrics
- `entry_time`, `exit_time`: Daily work schedule
- `print_*`: Printing activity (commands, pages, color ratio)
- `burn_*`: Data burning/disposal activity
- `travel_*`: Business travel information

### Security Indicators
- Background check flags (contractor, foreign citizenship, criminal record)
- Classification levels and security clearances
- Anomaly detection features

## 🎛️ Command Line Arguments

### Dataset Parameters
```bash
-e, --employees        Number of employees (default: 1666)
-d, --days            Simulation duration in days (default: 180)  
-m, --malicious-ratio  Ratio of malicious employees (default: 0.05)
```

### Output Options
```bash
-o, --output          Output filename prefix
--export-format       csv, excel, or both (default: both)
--output-dir          Output directory (default: ./output)
```

### Analysis Options
```bash
--analysis-only       Run analysis on existing dataset
--input-file          Input CSV file for analysis
--skip-analysis       Skip statistical analysis generation
--validate-data       Run comprehensive data validation
```

### Technical Options
```bash
--seed               Random seed for reproducibility
--verbose            Enable detailed logging
--quiet              Suppress non-error output
```

### Noise Injection Options
```bash
--add-noise                    Enable synthetic noise injection
--burn-noise-rate             Burn activity noise percentage (default: 0.05)
--print-noise-rate            Print activity noise percentage (default: 0.05)
--entry-time-noise-rate       Entry time noise percentage (default: 0.10)
--use-gaussian                Use Gaussian noise distribution
```

## 📁 Output Files

The generator creates several output files:

### Dataset Files
- `{prefix}.csv`: Main dataset in CSV format
- `{prefix}.xlsx`: Excel workbook with multiple sheets
- `{prefix}_with_noise.csv/xlsx`: Noise-injected variants (if enabled)

### Analysis Reports
- Statistical summaries and distributions
- Data quality validation reports
- Behavioral pattern analysis
- Anomaly detection metrics

## 🏗️ Project Structure

```
synthetic-insider-threat-generator/
├── main.py                          # Main application entry point
├── requirements.txt                 # Python dependencies
├── README.md                       # This file
├── LICENSE                         # License information
│
├── cli/                            # Command line interface
│   ├── __init__.py
│   ├── argument_parser.py          # Argument parsing and validation
│   └── display_utils.py            # User interface utilities
│
├── config/                         # Configuration system  
│   ├── __init__.py
│   ├── config.py                   # Main configuration aggregator
│   ├── behavioral_patterns.py     # Employee behavior definitions
│   ├── organizational_structure.py # Company structure and positions
│   ├── employee_attributes.py     # Employee characteristic definitions
│   └── geographic_data.py          # Location and travel data
│
├── core/                           # Core generation logic
│   ├── __init__.py
│   └── [generation modules]
│
├── data_generator/                 # Data generation components
├── employee_generator/             # Employee creation logic
├── activity_generators/            # Activity pattern generators
├── analyzers/                      # Data analysis modules
├── data_exporter/                  # Export functionality
├── utils/                          # Utility functions
└── output/                         # Generated datasets (created at runtime)
```

## 🔧 Advanced Features

### Noise Injection System

The built-in noise injection system simulates real-world data imperfections:

- **Burn Noise**: Simulates variations in data destruction patterns
- **Print Noise**: Adds realistic printing activity variations  
- **Entry Time Noise**: Models irregular work schedule patterns
- **Gaussian Distribution**: Optional statistical noise distribution

### Data Validation

Comprehensive validation includes:
- Statistical consistency checks
- Behavioral pattern verification
- Data quality assessments
- Anomaly detection validation

### Reproducible Generation

- Seed-based random generation ensures consistent outputs
- Version control friendly for research reproducibility
- Configurable parameters for systematic experimentation

### Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/synthetic-insider-threat-generator.git
cd synthetic-insider-threat-generator

# Create development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
---

**Note**: This tool is designed for research, educational, and testing purposes. Ensure compliance with your organization's data privacy and security policies when using synthetic datasets for security system evaluation.
