# Core Module

The `core` module contains the essential infrastructure components for the Advanced Insider Threat Dataset Generator. This module provides configuration management, workflow orchestration, and data processing utilities that support the entire system.

## Overview

This module handles system-wide configuration, logging setup, workflow management, and specialized data processing tasks including daily-level suspicious activity labeling and synthetic noise injection for enhanced dataset realism.

## Module Components

### Configuration Management
- **[config_manager.py](./config_manager.py)** - System configuration and setup utilities
  - Logging configuration with multiple verbosity levels
  - Random seed initialization for reproducible results
  - Output directory creation and management

### Workflow Orchestration
- **[workflow_manager.py](./workflow_manager.py)** - Main business logic coordination
  - Analysis-only mode execution for existing datasets
  - Full dataset generation process orchestration
  - Data validation and export coordination

### Data Processing
- **[daily_label_creator.py](./daily_label_creator.py)** - Daily-level suspicious activity labeling
  - Transforms employee-level malicious labels to daily-level labels
  - Multi-stage anomaly detection with threshold calculation
  - False positive simulation for realistic evaluation scenarios

- **[data_noise_injector.py](./data_noise_injector.py)** - Synthetic noise injection
  - Controlled noise addition to numeric, binary, and temporal fields
  - Maintains consistency between dependent fields
  - Configurable noise rates and distribution types

## Key Features

### Configuration Management
- **Flexible Logging**: Supports multiple verbosity levels (quiet, normal, verbose)
- **Reproducible Results**: Optional random seed configuration
- **File Output**: Automatic log file generation alongside console output

### Workflow Management
- **Dual Operating Modes**: Analysis-only and full generation workflows
- **Comprehensive Analysis**: Behavioral pattern analysis and data quality validation
- **Export Coordination**: Multi-format dataset export with analysis results

### Daily Label Creation
- **Anomaly Detection**: Multi-threshold suspicious activity identification
- **Temporal Expansion**: Adjacent day labeling based on softer thresholds
- **False Positive Simulation**: Realistic evaluation scenarios with innocent employee flagging
- **Statistical Reporting**: Detailed labeling outcome metrics

### Noise Injection
- **Controlled Realism**: Low-intensity noise injection by default (5-10% modification rates)
- **Field-Specific Processing**: Specialized noise for burn requests, print commands, and entry times
- **Dependency Preservation**: Maintains logical relationships between related fields
- **Statistical Tracking**: Comprehensive modification statistics and logging

## Usage Examples

### Configuration Setup
```python
from core.config_manager import setup_logging, setup_random_seed, create_output_directory

# Setup logging
logger = setup_logging(verbose=True)

# Set random seed for reproducibility
setup_random_seed(42)

# Create output directory
output_path = create_output_directory("output/results")
```

### Workflow Execution
```python
from core.workflow_manager import run_full_generation, run_analysis_only

# Run full dataset generation
df, files = run_full_generation(args, logger)

# Or run analysis on existing data
df = run_analysis_only(args, logger)
```

### Daily Label Creation
```python
from core.daily_label_creator import create_daily_labels_from_df

# Transform employee-level to daily-level labels
df_with_daily_labels = create_daily_labels_from_df(df)
```

### Noise Injection
```python
from core.data_noise_injector import DataNoiseInjector

# Initialize noise injector with custom parameters
injector = DataNoiseInjector(
    burn_noise_rate=0.05,
    print_noise_rate=0.05,
    entry_time_noise_rate=0.10,
    use_gaussian=False
)

# Apply noise to dataset
df_noisy = injector.add_noise_to_dataframe(df)

# Get modification statistics
stats = injector.get_statistics()
```

## Configuration Parameters

### Logging Configuration
- **verbose**: Enable debug-level logging
- **quiet**: Suppress all but error messages
- **log_file**: Automatic generation of `dataset_generation.log`

### Noise Injection Parameters
- **burn_noise_rate**: Percentage of rows affected by burn activity noise (default: 5%)
- **print_noise_rate**: Percentage of rows affected by print activity noise (default: 5%)
- **entry_time_noise_rate**: Percentage of rows affected by entry time modifications (default: 10%)
- **use_gaussian**: Enable Gaussian distribution for noise generation (default: False)

### Daily Labeling Thresholds
- **95th percentile thresholds**: Strict detection for high-confidence suspicious activity
- **75th percentile thresholds**: Softer thresholds for adjacent day expansion
- **False positive rate**: 5% of innocent employees selected for anomaly simulation

## Output and Statistics

### Daily Label Creation Statistics
- Total records processed
- Malicious employee count
- Suspicious days identified
- Detection rates and false positive counts

### Noise Injection Statistics
- Total and modified row counts
- Field-specific modification counts
- Detailed change logging per record

## Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations and random number generation
- **logging**: System logging functionality
- **pathlib**: File system path handling
- **datetime**: Date and time operations

## Integration

The `core` module integrates with:
- **Employee Generator**: Provides configuration for employee profile creation
- **Data Generator**: Supplies workflow coordination and noise injection
- **Analyzers**: Receives configuration and workflow management
- **Data Exporter**: Coordinated through workflow management

This module serves as the foundation for the entire dataset generation system, providing essential infrastructure services while maintaining modularity and configurability.
