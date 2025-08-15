# Employee Generator

A Python-based employee profile generation system that creates realistic employee datasets for testing, simulation, and analysis purposes. The system generates comprehensive employee profiles with realistic department distributions, job positions, and various attributes.

## 🚀 Features

- **Realistic Profile Generation**: Creates employee profiles with authentic job titles, departments, and attributes
- **Department-Based Organization**: Assigns employees to departments with realistic position hierarchies
- **Behavioral Group Classification**: Maps employees to behavioral groups based on their departments
- **Comprehensive Attributes**: Generates multiple employee characteristics including:
  - Campus locations
  - Seniority levels
  - Contractor status
  - Security classifications
  - Background information
- **Malicious Employee Selection**: Supports selecting random subsets for security testing scenarios
- **Configurable Parameters**: Highly customizable through configuration files

## 📁 Project Structure

```
employee_generator/
├── employee_manager.py           # Main management class for employee collections
├── employee_profile_creator.py   # Individual profile creation logic
```

## Example Output

```python
{
    'emp_id': '001',
    'department': 'IT',
    'position': 'Software Developer',
    'behavioral_group': 'Technical',
    'campus': 'Main Campus',
    'seniority_years': 3,
    'is_contractor': False,
    'classification': 'Level 2',
    'foreign_citizenship': False,
    'criminal_record': False,
    'medical_history': 'None',
    'origin_country': 'United States'
}
```

## 🏗️ Architecture

### Core Components

#### 1. EmployeeManager ([`employee_manager.py`](./employee_manager.py))
The main orchestrator that:
- Manages collections of employee profiles
- Generates multiple employees with realistic distributions
- Provides summary statistics
- Supports malicious employee selection for security scenarios

**Key Methods:**
- `generate_employee_profiles()`: Creates all employee profiles
- `select_malicious_employees(ratio)`: Selects random employees for testing
- `_print_generation_summary()`: Displays generation statistics

#### 2. EmployeeProfileCreator ([`employee_profile_creator.py`](./employee_profile_creator.py))
Handles individual profile creation with:
- Realistic job position assignment within departments
- Behavioral group mapping
- Attribute generation based on configurable probabilities

**Key Methods:**
- `create_employee_profile(department, emp_id)`: Creates single employee profile
- `_get_seniority_years(position)`: Determines experience based on role
- `_get_classification_level(department)`: Assigns security clearance levels

### Configuration System

The system uses a centralized configuration approach through `Config` class that defines:

- **Department Distributions**: Realistic employee counts per department
- **Position Hierarchies**: Job titles within each department
- **Behavioral Groups**: Employee categorization for analysis
- **Probability Weights**: Realistic distributions for all attributes
- **Campus Locations**: Available workplace locations
- **Classification Levels**: Security clearance categories

## ⚙️ Configuration

All system parameters are managed through the `Config` class. Key configuration areas include:

### Department Settings
- Department weights for realistic distribution
- Position lists for each department
- Behavioral group mappings

### Employee Attributes
- Seniority ranges by position type
- Contractor probability distributions
- Classification level assignments
- Background attribute probabilities

### Demographic Settings
- Origin country distributions
- Campus location options
- Citizenship status probabilities

## 🎯 Use Cases

### 1. Security Testing
Generate employee datasets with malicious actors for:
- Insider threat simulation
- Security awareness training
- Access control testing

### 2. HR Analytics
Create realistic employee populations for:
- Workforce planning analysis
- Organizational structure modeling
- Department distribution studies

### 3. System Testing
Generate test data for:
- Employee management systems
- Access control systems
- HR applications

### 4. Research and Simulation
Support academic and business research in:
- Organizational behavior studies
- Security policy analysis
- Workforce demographics modeling

## 🔧 Customization

### Adding New Departments
1. Update `DEPARTMENT_WEIGHTS` in config
2. Add positions to `DEPARTMENT_POSITIONS`
3. Define behavioral group in `BEHAVIORAL_GROUPS`

### Modifying Attributes
1. Adjust probability distributions in `EMPLOYEE_PROBABILITIES`
2. Update classification levels in `CLASSIFICATION_PROBABILITIES`
3. Modify seniority ranges in `SENIORITY_RANGES`

### Changing Distributions
All probability distributions can be customized by modifying the respective arrays and weights in the configuration file.


## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
