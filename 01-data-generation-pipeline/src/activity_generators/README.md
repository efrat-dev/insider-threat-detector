# Activity Generators

This directory contains modules for generating realistic employee activity data for security analysis and simulation purposes. The system simulates various types of employee behaviors and activities within an organizational context.

## Overview

The Activity Generators system creates synthetic data for employee activities including:
- Building access patterns
- Document burning/destruction activities  
- Printing behaviors
- Travel activities
- Risk indicator calculations

Each generator incorporates behavioral patterns that differentiate between regular and potentially malicious employee activities, enabling security analysis and anomaly detection research.

## Module Structure

### [access_activity_generator.py](./access_activity_generator.py)

**Purpose**: Generates building access activity data for employees

**Key Features**:
- Simulates realistic work hour patterns based on behavioral groups
- Models weekend work, absences, and unusual access times
- Differentiates patterns between malicious and non-malicious employees
- Supports multi-campus access scenarios
- Handles special cases like employees working abroad

**Generated Data**:
- Entry/exit counts and timestamps
- Total presence duration
- Night-hour access flags
- Early entry and late exit indicators
- Multi-campus activity metrics

### [burn_activity_generator.py](./burn_activity_generator.py)

**Purpose**: Generates data destruction (burn) activity patterns

**Key Features**:
- Simulates document burning/destruction requests
- Models classification levels of destroyed data
- Tracks off-hours burning activities
- Supports multi-campus burning scenarios
- Adjusts patterns for malicious vs. regular employees

**Generated Data**:
- Number of burn requests
- Data classification levels (max/average)
- Volume of data destroyed (MB)
- File count metrics
- Off-hours activity indicators
- Cross-campus burning flags

### [print_activity_generator.py](./print_activity_generator.py)

**Purpose**: Generates employee printing activity data

**Key Features**:
- Models realistic printing volumes and patterns
- Differentiates between color and black-and-white printing
- Tracks off-hours printing behavior
- Supports multi-campus printing scenarios
- Scales activity based on employee risk profile

**Generated Data**:
- Print command counts and page volumes
- Color vs. black-and-white print ratios
- Off-hours printing metrics
- Cross-campus printing indicators
- Command-to-page relationships

### [travel_activity_generator.py](./travel_activity_generator.py)

**Purpose**: Generates employee travel activity and trip data

**Key Features**:
- Manages ongoing trips with multi-day durations
- Models travel to hostile vs. friendly countries
- Differentiates official vs. unofficial travel
- Tracks trip progression and employee location status
- Adjusts travel patterns for high-risk employees

**Generated Data**:
- Travel status and location information
- Trip duration and day counters
- Country hostility level classifications
- Official vs. unofficial trip indicators
- Origin country relationship flags

### [risk_indicators.py](./risk_indicators.py)

**Purpose**: Calculates composite risk indicators based on activity data

**Key Features**:
- Combines multiple activity types for risk assessment
- Implements rule-based risk detection logic
- Focuses on high-risk combinations (e.g., unofficial travel to hostile countries with suspicious activities)

**Risk Calculations**:
- Travel-based risk indicators combining location, trip type, and concurrent activities
- Cross-activity correlation analysis
- Behavioral anomaly flagging

## Key Concepts

### Behavioral Groups
The system uses behavioral groups (A, B, C, D, E) to categorize employees with different activity patterns:
- Each group has distinct work hour preferences
- Groups vary in travel likelihood and activity volumes
- Security personnel (Group E) have special weekend work patterns

### Malicious vs. Regular Employees
The generators incorporate different probability distributions for potentially malicious employees:
- **Malicious employees** tend to have more extreme behaviors (unusual hours, higher activity volumes, travel to hostile countries)
- **Regular employees** follow more typical organizational patterns
- Risk indicators specifically target suspicious combinations of activities

### Multi-Campus Operations
All generators support multi-campus scenarios where employees may:
- Access buildings at different locations
- Print documents from various campus locations
- Perform data destruction activities across sites

### Configuration Dependencies
The generators rely on configuration constants from `config.Config`:
- Work hour boundaries and duration limits
- Country classifications and hostility levels  
- Travel destination weights and probabilities
- Trip duration ranges

## Dependencies

- `numpy`: Statistical distributions and random number generation
- `datetime`: Date and time handling
- `typing`: Type hints for better code documentation
- `config.config`: Configuration constants and parameters

## Data Output Format

All generators return dictionary objects with standardized field names and data types. Missing or inactive periods return zero-filled dictionaries with consistent structure, enabling seamless data pipeline processing and analysis.
