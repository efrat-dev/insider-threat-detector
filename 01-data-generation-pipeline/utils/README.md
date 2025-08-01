# Utils Directory

This directory contains utility functions and configurations for the **Advanced Insider Threat Dataset Generator**. The utilities provide essential functionality for performance monitoring, constant definitions, and shared configurations across the application.

## Overview

The utils package is designed to support the main application with:
- Performance profiling and memory monitoring
- Application-wide constants and configuration values
- Shared utility functions for logging and system monitoring

## Files Structure

```
utils/
├── __init__.py              # Package initialization and exports
├── constants.py             # Application constants and configuration
└── performance_profiler.py  # Memory and performance monitoring utilities
```

## Module Documentation

### `constants.py`

Contains all application-wide constants and configuration values used throughout the Advanced Insider Threat Dataset Generator.

#### Application Metadata
- `APP_NAME`: "Advanced Insider Threat Dataset Generator"
- `APP_DESCRIPTION`: "Realistic Behavioral Pattern Simulation"

#### File and Directory Configuration
- `DEFAULT_LOG_FILENAME`: "dataset_generation.log"
- `DEFAULT_OUTPUT_PREFIX`: "insider_threat_advanced"
- `DEFAULT_OUTPUT_DIR`: "./output"

#### System Limits and Constraints
- `MAX_EMPLOYEES`: 10,000 (maximum number of employees in simulation)
- `MAX_DAYS`: 1,000 (maximum simulation duration in days)
- `MIN_POSITIVE_VALUE`: 0 (minimum allowed positive value)
- `MAX_RATIO`: 1.0 (maximum ratio value)

#### Performance and Display Constants
- `BYTES_TO_MB`: 1,048,576 (conversion factor from bytes to megabytes)
- `BANNER_WIDTH`: 70 (width for console banner display)
- `BANNER_CHAR`: "=" (character used for banner formatting)

### `performance_profiler.py`

Provides memory and performance monitoring capabilities for the application.

#### Functions

##### `profile_memory_usage()`
Profiles current memory usage of the application process.

**Returns:**
- `dict`: Memory usage information containing:
  - `rss_mb`: Resident Set Size in megabytes
  - `vms_mb`: Virtual Memory Size in megabytes
  - `percent`: Memory usage percentage
- `None`: If psutil is not available

**Dependencies:**
- `psutil`: Optional dependency for memory profiling

##### `log_memory_usage(logger, stage_name, memory_info)`
Logs memory usage information for a specific application stage.

**Parameters:**
- `logger`: Logger instance for output
- `stage_name` (str): Name of the current processing stage
- `memory_info` (dict): Memory information from `profile_memory_usage()`

**Behavior:**
- Logs memory usage at INFO level if profiling data is available
- Logs debug message if memory profiling is unavailable

## Usage Examples

### Basic Import and Usage

```python
from utils import (
    profile_memory_usage,
    log_memory_usage,
    APP_NAME,
    MAX_EMPLOYEES,
    DEFAULT_OUTPUT_DIR
)

# Profile memory usage
memory_info = profile_memory_usage()
if memory_info:
    print(f"Current memory usage: {memory_info['rss_mb']:.1f} MB")

# Use application constants
print(f"Application: {APP_NAME}")
print(f"Max employees: {MAX_EMPLOYEES}")
print(f"Output directory: {DEFAULT_OUTPUT_DIR}")
```

### Memory Profiling with Logging

```python
import logging
from utils import profile_memory_usage, log_memory_usage

# Setup logging
logger = logging.getLogger(__name__)

# Profile and log memory usage
memory_info = profile_memory_usage()
log_memory_usage(logger, "Data Generation", memory_info)
```

### Configuration Usage

```python
from utils import (
    DEFAULT_OUTPUT_DIR,
    MAX_EMPLOYEES,
    MAX_DAYS,
    BANNER_WIDTH,
    BANNER_CHAR
)

# Create output directory
import os
os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)

# Validate input parameters
def validate_parameters(num_employees, num_days):
    if num_employees > MAX_EMPLOYEES:
        raise ValueError(f"Number of employees cannot exceed {MAX_EMPLOYEES}")
    if num_days > MAX_DAYS:
        raise ValueError(f"Number of days cannot exceed {MAX_DAYS}")

# Create formatted banner
def create_banner(title):
    banner = BANNER_CHAR * BANNER_WIDTH
    return f"{banner}\n{title.center(BANNER_WIDTH)}\n{banner}"
```

## Dependencies

### Required Dependencies
- `os`: Standard library (built-in)

### Optional Dependencies
- `psutil`: Required for memory profiling functionality
  - Install with: `pip install psutil`
  - If not available, memory profiling functions will return `None`

## Exported Functions and Constants

The package exports the following items through `__init__.py`:

**Functions:**
- `profile_memory_usage`
- `log_memory_usage`

**Constants:**
- `APP_NAME`
- `APP_DESCRIPTION`
- `DEFAULT_LOG_FILENAME`
- `DEFAULT_OUTPUT_PREFIX`
- `DEFAULT_OUTPUT_DIR`
- `MAX_EMPLOYEES`
- `MAX_DAYS`
- `MIN_POSITIVE_VALUE`
- `MAX_RATIO`
- `BYTES_TO_MB`
- `BANNER_WIDTH`
- `BANNER_CHAR`

## Error Handling

The utils package handles errors gracefully:
- Memory profiling functions return `None` if `psutil` is not available
- All functions include appropriate error handling for system-level operations
- Constants are defined with sensible defaults for various system configurations

## Performance Considerations

- Memory profiling has minimal overhead when `psutil` is available
- Constants are loaded once at import time
- No persistent state is maintained within the utility functions
