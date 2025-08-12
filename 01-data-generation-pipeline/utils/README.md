# Utils Constants Module

Central constants and configuration values for the Advanced Insider Threat Dataset Generator.

## 📁 File Structure
```
utils/
└── constants.py    # Constants and configuration values
```

## 📖 Constants Overview

The [`constants.py`](./constants.py) file contains static configuration values organized into the following categories:

### Application Metadata
```python
APP_NAME = "Advanced Insider Threat Dataset Generator"
APP_DESCRIPTION = "Realistic Behavioral Pattern Simulation"
```

### File and Directory Names
```python
DEFAULT_LOG_FILENAME = "dataset_generation.log"
DEFAULT_OUTPUT_PREFIX = "insider_threat_advanced"
DEFAULT_OUTPUT_DIR = "./output"
```

### Limits and Constraints
```python
MAX_EMPLOYEES = 10000
MAX_DAYS = 1000
MIN_POSITIVE_VALUE = 0
MAX_RATIO = 1.0
```

### Memory Profiling Constants
```python
BYTES_TO_MB = 1024 * 1024
```

### Banner Configuration
```python
BANNER_WIDTH = 70
BANNER_CHAR = "="
```

## 🚀 Usage

### Basic Import
```python
from utils.constants import APP_NAME, MAX_EMPLOYEES, DEFAULT_OUTPUT_DIR
```

### Example Usage
```python
# Application identification
print(f"Running {APP_NAME}")

# Validation using limits
if employee_count > MAX_EMPLOYEES:
    raise ValueError(f"Maximum {MAX_EMPLOYEES} employees allowed")

# File path construction
output_path = f"{DEFAULT_OUTPUT_DIR}/data.csv"

# Memory conversion
memory_mb = memory_bytes / BYTES_TO_MB

# Banner display
print(BANNER_CHAR * BANNER_WIDTH)
```

## 📋 Constants Reference

| Constant | Value | Type | Purpose |
|----------|-------|------|---------|
| `APP_NAME` | "Advanced Insider Threat Dataset Generator" | str | Application name |
| `APP_DESCRIPTION` | "Realistic Behavioral Pattern Simulation" | str | Application description |
| `DEFAULT_LOG_FILENAME` | "dataset_generation.log" | str | Default log file |
| `DEFAULT_OUTPUT_PREFIX` | "insider_threat_advanced" | str | Output file prefix |
| `DEFAULT_OUTPUT_DIR` | "./output" | str | Output directory |
| `MAX_EMPLOYEES` | 10000 | int | Employee limit |
| `MAX_DAYS` | 1000 | int | Days limit |
| `MIN_POSITIVE_VALUE` | 0 | int | Minimum value |
| `MAX_RATIO` | 1.0 | float | Maximum ratio |
| `BYTES_TO_MB` | 1048576 | int | Conversion factor |
| `BANNER_WIDTH` | 70 | int | Banner width |
| `BANNER_CHAR` | "=" | str | Banner character |
