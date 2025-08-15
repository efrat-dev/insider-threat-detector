# Data Generator

A comprehensive synthetic employee activity data generation system designed to create realistic datasets for security analysis, machine learning, and testing purposes.

## Overview

The Data Generator creates synthetic daily activity records for employees across multiple dimensions including printing, file burning, travel, and access patterns. It supports the generation of both normal and malicious behavior patterns with configurable noise injection capabilities.

## Architecture

The system is built with a modular architecture consisting of two main components:

### Core Components

- **[`data_generator_core.py`](./data_generator/data_generator_core.py)** - The foundational class that orchestrates all activity generation
- **[`data_generator.py`](./data_generator/data_generator.py)** - The main interface that extends the core with noise injection and dataset management

## File Structure

```
data_generator/
├── data_generator.py          # Main generator interface
├── data_generator_core.py     # Core generation logic
└── README.md                  # This file
```

## Features

- **Multi-Activity Generation**: Generates printing, burning, travel, and access activities
- **Behavioral Modeling**: Supports different behavioral groups and patterns
- **Malicious Behavior Simulation**: Configurable ratio of malicious employees with distinct activity patterns
- **Noise Injection**: Optional data noise injection for more realistic datasets
- **Progress Tracking**: Real-time progress reporting during dataset generation
- **Department Distribution**: Automatic analysis and reporting of employee department distribution

## Usage

### Basic Usage

```python
from data_generator import DataGenerator

# Initialize with employee data
employees = {
    'emp_001': {
        'department': 'Engineering',
        'campus': 'Main Campus',
        'position': 'Senior Developer',
        'seniority_years': 5,
        'behavioral_group': 1
    },
    # ... more employees
}

# Create generator
generator = DataGenerator(
    employees=employees,
    days_range=180,
    malicious_ratio=0.05,
    add_noise=False
)

# Generate dataset
df = generator.generate_dataset()
```

### Advanced Usage with Noise Injection

```python
# Configure noise injection
noise_config = {
    'burn_rate': 0.1,
    'print_rate': 0.05,
    'entry_time_rate': 0.08,
    'gaussian': True,
    'seed': 42
}

generator = DataGenerator(
    employees=employees,
    days_range=365,
    malicious_ratio=0.08,
    add_noise=True,
    noise_config=noise_config
)

df = generator.generate_dataset()
```

## Configuration Parameters

### DataGenerator Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `employees` | dict | Required | Dictionary of employee profiles keyed by employee ID |
| `days_range` | int | 180 | Number of days to generate data for |
| `malicious_ratio` | float | 0.05 | Fraction of employees marked as malicious (5%) |
| `add_noise` | bool | False | Enable noise injection |
| `noise_config` | dict | None | Configuration for noise injection parameters |

### Noise Configuration Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `burn_rate` | float | Rate of noise injection for burn activities |
| `print_rate` | float | Rate of noise injection for print activities |
| `entry_time_rate` | float | Rate of noise injection for entry/exit times |
| `gaussian` | bool | Use Gaussian distribution for noise |
| `seed` | int | Random seed for reproducible noise |

## Generated Data Structure

The generated dataset includes the following columns:

### Employee Information
- `employee_id` - Unique employee identifier
- `employee_department` - Department name
- `employee_campus` - Campus location
- `employee_position` - Job position
- `employee_seniority_years` - Years of experience
- `employee_classification` - Employee classification
- `behavioral_group` - Behavioral pattern group

### Activity Data
- **Print Activities**: `num_print_commands`, `total_printed_pages`, `num_color_prints`, etc.
- **Burn Activities**: `num_burn_requests`, `total_burn_volume_mb`, `total_files_burned`, etc.
- **Travel Data**: `is_abroad`, `trip_day_number`, travel destinations
- **Access Data**: `num_entries`, `num_exits`, `total_presence_minutes`

### Risk Indicators
- `is_malicious` - Binary flag for malicious employees
- `risk_travel_indicator` - Calculated risk score based on travel and activity patterns

## Dependencies

The Data Generator requires the following components:

- `pandas` - Data manipulation and analysis
- `datetime` - Date and time handling
- `random` - Random number generation
- `typing` - Type hints support

### Internal Dependencies
- `activity_generators` - Various activity generation modules
- `config.config` - Configuration management
- `core.date_noise_injector` - Noise injection functionality

## Output

The `generate_dataset()` method returns a pandas DataFrame with:
- Properly typed columns (dates, integers, floats)
- Sorted records by employee ID and date
- Non-negative count values
- Rounded float values (2 decimal places)
- Progress reporting during generation

## Example Output Statistics

```
Using 1000 employees
Malicious employees: 50 (5.0%)
Noise injection: DISABLED
Department distribution:
  Engineering: 300
  Sales: 200
  HR: 150
  Finance: 150
  Operations: 200
Generating dataset with 1000 employees over 180 days...
Progress: 10% (18000/180000)
...
Dataset generated: 180,000 records
Malicious records: 9,000
```
