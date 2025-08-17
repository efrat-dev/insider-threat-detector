# Sample Record Analysis - Insider Threat Dataset

📖 **Navigation**: [← Main README](../README.md) | [Technical Overview](./docs/TECHNICAL_OVERVIEW.md) | [User Guide](./docs/USER_GUIDE.md)

This document demonstrates how to interpret individual records from the insider threat dataset through detailed analysis of a sample employee record.

---

## Sample Record: Test Engineer with Normal Activity Pattern

### Complete Record:
```
employee_id: 0008
date: 2025-04-01
employee_department: Engineering Department
employee_campus: Campus B
employee_position: Test Engineer
employee_seniority_years: 24
is_contractor: 0
employee_classification: 2
has_foreign_citizenship: 0
has_criminal_record: 0
has_medical_history: 0
employee_origin_country: Israel
is_malicious: 0
risk_travel_indicator: 0
num_print_commands: 0
total_printed_pages: 0
num_print_commands_off_hours: 0
num_printed_pages_off_hours: 0
num_color_prints: 0
num_bw_prints: 0
ratio_color_prints: 0.0
printed_from_other: 0
print_campuses: 0
num_burn_requests: 0
max_request_classification: 0
avg_request_classification: 0.0
num_burn_requests_off_hours: 0
total_burn_volume_mb: 0
total_files_burned: 0
burned_from_other: 0
burn_campuses: 0
is_abroad: 0
trip_day_number: 
country_name: 
is_hostile_country_trip: 0
hostility_country_level: 0
is_official_trip: 0
num_entries: 2
num_exits: 2
first_entry_time: 08:06
last_exit_time: 18:57
total_presence_minutes: 651
entered_during_night_hours: 0
num_unique_campus: 1
early_entry_flag: 0
late_exit_flag: 0
entry_during_weekend: 0
row_modified: False
modification_details: 
is_emp_malicious: 0
```

## What is a Test Engineer?

**Test Engineers** are critical personnel responsible for:
- Quality assurance and functional testing of products and systems
- Development of testing procedures and validation protocols
- Operation of advanced testing equipment and measurement systems
- Documentation of test results and quality compliance reports
- **Security Relevance:** Access to technical specifications, performance data, and sensitive design details

Test Engineers often have access to:
- Detailed product specifications and blueprints
- Performance benchmarks and failure analysis data
- Manufacturing processes and quality control procedures
- Customer requirements and contractual specifications

---

## Field-by-Field Analysis:

### Personal Background & Citizenship
```
has_foreign_citizenship: 0
employee_origin_country: Israel
has_criminal_record: 0
```
**Key Insights:** Domestic employee with Israeli origin, no foreign citizenship, clean criminal background - represents low personal risk profile for security purposes.

### Printing Activities
```
num_print_commands: 0
total_printed_pages: 0
num_print_commands_off_hours: 0
num_printed_pages_off_hours: 0
num_color_prints: 0
num_bw_prints: 0
ratio_color_prints: 0.0
printed_from_other: 0
print_campuses: 0
```
**Key Insights:** Zero printing activity throughout the day. This suggests either digital-only workflow or no need for hard-copy documentation on this particular day. Normal for modern engineering environments.

### File Burning/Transfer Operations
```
num_burn_requests: 0
max_request_classification: 0
avg_request_classification: 0.0
num_burn_requests_off_hours: 0
total_burn_volume_mb: 0
total_files_burned: 0
burned_from_other: 0
burn_campuses: 0
```
**Key Insights:** No file burning or data transfer activities. Indicates no sensitive data movement on this date - typical for routine testing work that doesn't involve data export.

### Travel Information
```
is_abroad: 0
trip_day_number: 
country_name: 
is_hostile_country_trip: 0
hostility_country_level: 0
is_official_trip: 0
risk_travel_indicator: 0
```
**Key Insights:** Employee remained domestic throughout the day. No travel-related risk factors present.

### Physical Access Control
```
num_entries: 2
num_exits: 2
first_entry_time: 08:06
last_exit_time: 18:57
total_presence_minutes: 651
entered_during_night_hours: 0
num_unique_campus: 1
early_entry_flag: 0
late_exit_flag: 0
entry_during_weekend: 0
```
**Key Insights:** 
- **Multiple entries/exits:** 2 entries and 2 exits indicate a midday break (likely lunch or external meeting)
- **Extended workday:** 651 minutes (10.85 hours) from 08:06 to 18:57 shows dedicated work ethic
- **Regular schedule:** No early/late flags, normal weekday activity
- **Single campus:** All activity confined to assigned Campus B

### Employee Profile & Risk Assessment
```
employee_seniority_years: 24
is_contractor: 0
employee_classification: 2
is_malicious: 0
is_emp_malicious: 0
```
**Key Insights:**
- **Highly experienced:** 24 years of service indicates deep institutional knowledge and established trust
- **Permanent employee:** Full-time staff member (not contractor), suggesting long-term commitment
- **Mid-level clearance:** Classification Level 2 (Confidential) appropriate for engineering role
- **Clean security record:** No malicious activity flags at individual or aggregate level

### Data Integrity
```
row_modified: False
modification_details: 
```
**Key Insights:** This is authentic data - no artificial noise or modifications added. Represents genuine employee behavior pattern.

---

## Risk Assessment Summary

### ✅ Low-Risk Indicators:
- **Established employee:** 24-year tenure with clean record
- **Normal work pattern:** Regular hours with appropriate break
- **No suspicious activities:** Zero printing, burning, or travel anomalies
- **Domestic status:** Israeli origin with no foreign complications
- **Authentic data:** Unmodified record representing real behavior

### 📊 Notable Patterns:
- **Long workday:** 10.85 hours suggests project commitment or deadline pressure
- **Digital workflow:** No printing activity aligns with modern engineering practices
- **Routine behavior:** Consistent with senior engineer's typical daily activities

### 🎯 Security Context:
This record exemplifies a **baseline normal** employee profile. Senior Test Engineers like this individual are valuable assets who:
- Possess extensive institutional knowledge
- Have established trust through long tenure
- Maintain consistent, predictable work patterns
- Operate within appropriate security boundaries

---

## Learning Objectives

This sample demonstrates how the dataset captures:
1. **Multi-dimensional behavior tracking** across printing, burning, travel, and access activities
2. **Temporal patterns** showing work schedule and break behavior
3. **Security clearance context** appropriate for role and seniority
4. **Baseline establishment** for anomaly detection algorithms
5. **Data authenticity markers** distinguishing real from synthetic records

For machine learning applications, records like this serve as **negative examples** (non-malicious) that help models understand normal employee behavior patterns and distinguish them from potential insider threats.
