# Advanced Insider Threat Dataset Generator

A sophisticated Python framework for generating realistic behavioral datasets for insider threat detection research and machine learning model development.

## 🎯 Overview

The Advanced Insider Threat Dataset Generator creates comprehensive synthetic datasets that simulate employee behavior patterns in organizational environments. It generates realistic data across multiple dimensions including access patterns, printing activities, data burning (copying), travel behavior, and various risk indicators.

## ✨ Features

### Core Capabilities
- **Realistic Employee Profiles**: Generates diverse employee profiles with department-specific attributes
- **Multi-Activity Simulation**: Simulates printing, data burning, access control, and travel activities
- **Behavioral Pattern Modeling**: Incorporates department-specific behavioral patterns and risk profiles
- **Malicious Actor Simulation**: Configurable percentage of employees exhibiting suspicious behaviors
- **Risk Indicator Calculation**: Automated calculation of travel-based and other risk indicators

### Technical Features
- **Configurable Parameters**: Extensive configuration options for dataset customization
- **Multiple Export Formats**: Support for CSV, Excel, and JSON export formats
- **Comprehensive Analysis**: Built-in statistical analysis and data validation
- **Performance Profiling**: Memory usage monitoring and performance optimization
- **Reproducible Results**: Seed-based random generation for consistent outputs

## 📋 Requirements

### System Requirements
- Python 3.8+
- Memory: 4GB+ RAM (depends on dataset size)
- Storage: Variable (depends on output format and size)

### Dependencies
```
pandas>=1.5.0
numpy>=1.20.0
datetime
random
typing
pathlib
logging
```

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/your-org/synthetic-insider-threat-generator.git
cd synthetic-insider-threat-generator
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python main.py --help
```

## 📖 Usage

### Basic Usage

**Generate a standard dataset**:
```bash
python main.py --employees 1000 --days 180 --malicious-ratio 0.05
```

**Generate with custom parameters**:
```bash
python main.py \
    --employees 5000 \
    --days 365 \
    --malicious-ratio 0.03 \
    --output advanced_dataset \
    --export-format csv \
    --seed 42
```

### Advanced Options

**Analysis-only mode** (analyze existing dataset):
```bash
python main.py --analysis-only --input-file existing_dataset.csv
```

**Performance profiling**:
```bash
python main.py --employees 1000 --days 180 --profile-performance
```

**Verbose logging**:
```bash
python main.py --employees 1000 --days 180 --verbose
```

### Command Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--employees` | 1000 | Number of employees to generate |
| `--days` | 180 | Number of days to simulate |
| `--malicious-ratio` | 0.05 | Percentage of malicious employees (0.0-1.0) |
| `--output` | insider_threat_advanced | Output filename prefix |
| `--output-dir` | ./output | Output directory |
| `--export-format` | csv | Export format (csv, excel, json) |
| `--seed` | None | Random seed for reproducibility |
| `--analysis-only` | False | Run analysis on existing dataset |
| `--skip-analysis` | False | Skip analysis during generation |
| `--validate-data` | False | Run data validation checks |
| `--profile-performance` | False | Enable performance profiling |
| `--verbose` | False | Enable verbose logging |
| `--quiet` | False | Suppress non-error output |

## 🏗️ Architecture

### Core Components

#### 1. **Employee Generator** (`employee_generator/`)
- **EmployeeManager**: Manages employee profile collection
- **EmployeeProfileCreator**: Creates individual employee profiles with realistic attributes

#### 2. **Data Generator** (`data_generator/`)
- **DataGenerator**: Main orchestration engine
- **DataGeneratorCore**: Core data generation functionality

#### 3. **Activity Generators** (`activity_generators/`)
- **PrintActivityGenerator**: Simulates printing behaviors
- **BurnActivityGenerator**: Simulates data copying/burning activities
- **TravelActivityGenerator**: Simulates travel patterns
- **AccessActivityGenerator**: Simulates facility access patterns
- **RiskIndicatorGenerator**: Calculates risk indicators

#### 4. **Analyzers** (`analyzers/`)
- **ComprehensiveAnalyzer**: Statistical analysis and reporting
- **BehavioralAnalyzer**: Behavioral pattern analysis
- **SecurityAnalyzer**: Security-focused analysis

#### 5. **Configuration** (`config/`)
- **Config**: Central configuration management
- **BehavioralPatterns**: Department-specific behavioral patterns
- **EmployeeAttributes**: Employee attribute definitions
- **OrganizationalStructure**: Company structure definitions

### Data Flow

```
Employee Profiles → Activity Generation → Risk Calculation → Analysis → Export
```

## 📊 Generated Data Schema

### Employee Attributes
- `employee_id`: Unique identifier
- `employee_department`: Department assignment
- `employee_position`: Job position
- `employee_seniority_years`: Years of experience
- `behavioral_group`: Behavioral pattern group
- `is_malicious`: Malicious actor flag

### Activity Data
- **Access Activities**: Entry/exit patterns, presence duration
- **Print Activities**: Print commands, page counts, color/BW ratios
- **Burn Activities**: Data copying requests, file volumes
- **Travel Activities**: Travel patterns, foreign travel indicators

### Risk Indicators
- `risk_travel_indicator`: Travel-based risk assessment
- Additional risk metrics based on activity patterns

## ⚙️ Configuration

### Behavioral Patterns
Configure department-specific behavioral patterns in `config/behavioral_patterns.py`:
```python
GROUP_PATTERNS = {
    1: {  # Conservative group
        'base_print_rate': 15,
        'base_burn_rate': 2,
        'travel_probability': 0.15,
        # ... additional parameters
    }
}
```

### Employee Attributes
Customize employee generation in `config/employee_attributes.py`:
```python
DEPARTMENT_WEIGHTS = {
    'Engineering': 0.25,
    'Sales': 0.15,
    'HR': 0.10,
    # ... additional departments
}
```

## 📈 Analysis Features

### Statistical Analysis
- Descriptive statistics for all generated features
- Distribution analysis by department and behavioral group
- Correlation analysis between activities and risk indicators

### Data Validation
- Range validation for all numeric fields
- Consistency checks across related fields
- Outlier detection and reporting

### Export Formats
- **CSV**: Standard comma-separated values
- **Excel**: Multi-sheet workbooks with analysis tabs
- **JSON**: Structured data format for API consumption

## 🔧 Customization

### Adding New Activity Types
1. Create new generator in `activity_generators/`
2. Implement required methods following existing patterns
3. Integrate with `DataGeneratorCore`
4. Update configuration as needed

### Custom Risk Indicators
1. Add calculation logic to `RiskIndicatorGenerator`
2. Update data schema in `DataGeneratorCore`
3. Include in analysis modules

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Generate a small test dataset:
```bash
python main.py --employees 100 --days 30 --output test_dataset
```

## 📝 Performance Considerations

### Memory Usage
- Memory usage scales with: `employees × days × activities_per_day`
- Recommended: 4GB RAM for 1000 employees × 365 days
- Use `--profile-performance` to monitor memory usage

### Generation Time
- Typical generation rate: ~1000 records/second
- Large datasets (10K+ employees, 365+ days) may take several minutes
- Progress indicators show completion status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: This generator creates synthetic data for research purposes. Always comply with organizational policies and legal requirements when working with insider threat detection systems.
