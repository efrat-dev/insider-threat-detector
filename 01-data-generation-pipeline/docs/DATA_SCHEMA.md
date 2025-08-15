# Insider Threat Dataset for Classified Environments

📖 **Navigation**: [← Main README](../README.md) | [Technical Overview](TECHNICAL_OVERVIEW.md) | [User Guide](USER_GUIDE.md)

## Overview
This dataset contains comprehensive employee activity monitoring data designed for behavioral analysis and anomaly detection in organizational security contexts. The dataset tracks multiple dimensions of employee behavior including printing activities, file burning operations, travel patterns, and access control events.

## Dataset Structure

### Core Entity
- **Primary Key**: `employee_id` + `date`
- **Total Fields**: 49 fields covering employee properties, activities, and risk indicators
- **Temporal Coverage**: Complete date range for all employees (including days with no activity)
- **Purpose**: Machine learning models learn from both presence and absence of activities

## Field Definitions

### Employee Static Properties
| Field Name | Type | Description |
|------------|------|-------------|
| `employee_id` | Number | Unique employee identifier |
| `date` | Date | Activity date |
| `employee_department` | Categorical | Employee's department |
| `employee_campus` | Categorical | Employee's assigned campus |
| `employee_position` | Text | Job title/position |
| `employee_seniority_years` | Quantity | Years of service |
| `is_contractor` | Boolean (0/1) | Contractor status |
| `employee_classification` | Categorical (1-4) | Security clearance level |
| `has_foreign_citizenship` | Boolean (0/1) | Foreign citizenship status |
| `has_criminal_record` | Boolean (0/1) | Criminal background indicator |
| `has_medical_history` | Boolean (0/1) | Medical history flag |
| `employee_origin_country` | Categorical | Employee's country of origin |

### Security and Risk Indicators
| Field Name | Type | Description |
|------------|------|-------------|
| `is_malicious` | Boolean (0/1) | Malicious activity indicator |
| `risk_travel_indicator` | Boolean (0/1) | High-risk travel flag |
| `is_emp_malicious` | Boolean (0/1) | Employee malicious behavior flag |

### Printing Activities
| Field Name | Type | Description |
|------------|------|-------------|
| `num_print_commands` | Quantity | Total print commands issued |
| `total_printed_pages` | Quantity | Total pages printed |
| `num_print_commands_off_hours` | Quantity | Print commands during unusual hours |
| `num_printed_pages_off_hours` | Quantity | Pages printed during unusual hours |
| `num_color_prints` | Quantity | Color print count |
| `num_bw_prints` | Quantity | Black & white print count |
| `ratio_color_prints` | Float | Ratio of color to total prints |
| `printed_from_other` | Boolean (0/1) | Printed from non-assigned campus |
| `print_campuses` | Categorical/List | Campuses where printing occurred |

### File Burning/Transfer Operations
| Field Name | Type | Description |
|------------|------|-------------|
| `num_burn_requests` | Quantity | Total burn requests |
| `max_request_classification` | Categorical (1-4) | Highest classification level burned |
| `avg_request_classification` | Float (1-4) | Average classification level |
| `num_burn_requests_off_hours` | Quantity | Burn requests during unusual hours |
| `total_burn_volume_mb` | Quantity | Total data volume burned (MB) |
| `total_files_burned` | Quantity | Total number of files burned |
| `burned_from_other` | Boolean (0/1) | Burned from non-assigned campus |
| `burn_campuses` | Categorical/List | Campuses where burning occurred |

### Travel Information
| Field Name | Type | Description |
|------------|------|-------------|
| `is_abroad` | Boolean (0/1) | Whether employee was abroad |
| `trip_day_number` | Sequential (1,2,3...) | Day N of the trip |
| `country_name` | Categorical | Destination country |
| `is_hostile_country_trip` | Boolean (0/1) | Trip to hostile country |
| `hostility_country_level` | Categorical/Numeric | Level of country hostility |
| `is_official_trip` | Boolean (0/1) | Official business trip |

### Access Control
| Field Name | Type | Description |
|------------|------|-------------|
| `num_entries` | Quantity | Number of facility entries |
| `num_exits` | Quantity | Number of facility exits |
| `first_entry_time` | Datetime | First entry time of day |
| `last_exit_time` | Datetime | Last exit time of day |
| `total_presence_minutes` | Quantity | Total time spent in facility (minutes) |
| `entered_during_night_hours` | Boolean (0/1) | Night entry flag |
| `num_unique_campus` | Quantity | Number of different campuses visited |
| `early_entry_flag` | Boolean (0/1) | Early entry indicator (before 06:00) |
| `late_exit_flag` | Boolean (0/1) | Late exit indicator (after 22:00) |
| `entry_during_weekend` | Boolean (0/1) | Weekend entry flag |

### Data Management
Relevant only with `python main.py --add-noise`:

| Field | Type | Description |
|-------|------|-------------|
| `row_modified` | Boolean (0/1) | Indicates if noise was added to this row |
| `modification_details` | Text | Details of noise/modifications applied |

## Security Classifications

### Employee Classification Levels
1. **Level 1** - Restricted 
2. **Level 2** - Confidential 
3. **Level 3** - Top Secret 
4. **Level 4** - Top Secret – Compartmented

### Campus Designations
- **Campus A, B, C** - Different physical locations 

## Organizational Structure

| Department | Positions |
|------------|-----------|
| **Executive Management** | Chief Executive Officer (CEO), Chief Legal Officer, Chief Human Resources Officer (CHRO), Chief Information Officer (CIO), Chief Technology Officer (CTO), Chief Operating Officer (COO), Chief Financial Officer (CFO), Chief Marketing and Business Development Officer, Chief Information Security Officer (CISO), Secretary |
| **R&D Department** | Head of R&D, Systems Engineer, Development Engineer (Hardware/Software/Mechanical), Algorithm Engineer, Integration and Testing Engineer, Secretary |
| **Engineering Department** | Head of Engineering, Process Engineer, Design Engineer, Systems Engineer, Test Engineer, Secretary |
| **Operations and Manufacturing** | Operations Manager, Manufacturing Engineer, Logistics Manager, Procurement Officer, Warehouse Manager, Secretary |
| **Project Management** | Project Manager, Project Engineer, Project Coordinator, Secretary |
| **Security and Information Security** | Chief Information Security Officer (CISO), Security Officer, Physical Access Control, Information Security Investigator, Cyber Analyst |
| **Human Resources** | HR Manager, Recruitment Coordinator, Employee Welfare Coordinator, Training Coordinator, Secretary |
| **Legal and Regulation** | Regulatory Affairs Officer, Defense Export Compliance Officer, Legal Advisor |
| **Finance** | Finance Manager, Accountant, Financial Analyst, Budget Manager, Secretary |
| **Marketing and Business Development** | Business Development Manager, Account Manager, Bid Coordinator, Marketing Manager, Secretary |
| **Information Technology** | IT Director, Information Security Specialist, Systems and Network Administrator, BI Developer/Data Analyst, Enterprise Systems Developer (ERP/CRM/SAP), Data Scientist, Secretary |

### Risk Profile by Department

#### High-Risk Departments (Access to Sensitive Information)
- **Executive Management**: Strategic decision-making, highest clearance levels
- **R&D Department**: Proprietary technology and intellectual property
- **Security and Information Security**: Security protocols and vulnerability data
- **Legal and Regulation**: Compliance and regulatory sensitive information

#### Medium-Risk Departments
- **Engineering Department**: Technical specifications and designs
- **Information Technology**: System access and data management
- **Project Management**: Cross-departmental information access

#### Standard-Risk Departments
- **Operations and Manufacturing**: Operational data
- **Human Resources**: Personnel information
- **Finance**: Financial data
- **Marketing and Business Development**: Market intelligence

## Time-Based Risk Indicators

### Off-Hours Definition
- **Weekdays**: 21:00-05:00
- **Friday**: Starting from 16:00
- **Saturday**: All day
- **Weekend**: Friday 16:00 through Saturday

### Night Hours Definition
- **22:00-05:00** for access control purposes

## Risk Assessment Framework

### High-Risk Scenarios

### Senior Employee Risk Factors
Senior employees (high `employee_seniority_years`) present unique risks:
- **Accumulated Privileges**: Higher access levels over time
- **System Knowledge**: Understanding of security bypasses
- **Behavioral Changes**: Sudden pattern changes more suspicious
- **Department-Specific Risks**: Executive Management and R&D pose highest insider threat potential
- **Position-Based Access**: C-level executives and department heads have broader system access

#### Travel-Related Risks
The `risk_travel_indicator` is triggered by multiple factors including:
- Unofficial travel to hostile countries
- Data operations during personal travel
- Country hostility level assessments
- Combination of travel and suspicious activities

**Key Risk Scenarios**:
1. **Information Leakage**: Employee collaboration with external parties
2. **Identity Theft**: Unauthorized use of credentials while employee is abroad
3. **Graduated Risk Assessment**: `hostility_country_level` enables nuanced threat evaluation

### Behavioral Anomalies

#### Color Printing Patterns
- Color printing often indicates special document types:
  - Marketing materials
  - Official forms
  - Graphical reports
  - Architectural plans
- Unusual color printing by typically B&W users may signal suspicious activity

### Cross-Campus Activities
- **Printing from other locations**: `printed_from_other` flag and `print_campuses` list
- **Burning from other locations**: `burned_from_other` flag and `burn_campuses` list
- Access patterns inconsistent with job role

#### Enhanced Country Risk Assessment
- **Hostility levels**: `hostility_country_level` provides granular risk classification
- **Travel risk combinations**: Multiple factors determine `risk_travel_indicator`

#### Malicious Activity Detection
- **Individual indicators**: `is_malicious` flags specific incidents
- **Employee-level assessment**: `is_emp_malicious` provides overall employee risk rating
