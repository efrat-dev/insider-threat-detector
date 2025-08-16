from datetime import datetime

class DataDictionaryGenerator:
    """Class for generating data dictionary documentation."""

    def __init__(self):
        """Initialize the data dictionary generator."""
        pass

    def create_data_dictionary(self, filename="data_dictionary.txt"):
        """Create a data dictionary explaining all columns."""
        dictionary_content = """
=== INSIDER THREAT DATASET - DATA DICTIONARY ===

This dataset contains daily records of employee activities for insider threat detection.
Each row represents one employee's activities for one day.

=== EMPLOYEE INFORMATION ===
employee_id: Unique identifier for each employee
date: Date of the record (YYYY-MM-DD format)
employee_department: Department where employee works
employee_campus: Campus location (Campus A, B, or C)
employee_position: Job title/position
employee_seniority_years: Years of employment at company
is_contractor: 1 if contractor, 0 if permanent employee
employee_classification: Employee's security clearance level (1-4, higher = more access)
has_foreign_citizenship: 1 if employee has foreign citizenship
has_criminal_record: 1 if employee has criminal background
has_medical_history: 1 if employee has relevant medical history
employee_origin_country: Country of origin
behavioral_group: Behavioral classification (A-F) based on job role

=== PRINTING ACTIVITIES ===
num_print_commands: Number of print commands issued
total_printed_pages: Total pages printed
num_print_commands_off_hours: Print commands outside normal hours
num_printed_pages_off_hours: Pages printed outside normal hours
num_color_prints: Number of color pages printed
num_bw_prints: Number of black & white pages printed
ratio_color_prints: Ratio of color to total prints
printed_from_other: 1 if printed from campus other than employee's home campus
print_campuses: Number of different campuses where printing occurred

=== DOCUMENT BURNING/DESTRUCTION ===
num_burn_requests: Number of document destruction requests
max_request_classification: Highest classification level of burned documents
avg_request_classification: Average classification level of burned documents
num_burn_requests_off_hours: Burn requests outside normal hours
total_burn_volume_mb: Total volume of data burned (MB)
total_files_burned: Total number of files burned
burned_from_other: 1 if burned from campus other than employee's home campus
burn_campuses: Number of different campuses where burning occurred

=== TRAVEL ACTIVITIES ===
is_abroad: 1 if employee is traveling abroad on this date
trip_day_number: Day number of current trip (null if not traveling)
country_name: Country being visited (null if not traveling)
is_hostile_country_trip: 1 if visiting hostile/suspicious country
is_official_trip: 1 if official business travel, 0 if personal
is_origin_country_trip: 1 if visiting employee's country of origin

=== BUILDING ACCESS ===
num_entries: Number of times employee entered building
num_exits: Number of times employee exited building
first_entry_time: Time of first entry (HH:MM format)
last_exit_time: Time of last exit (HH:MM format)
total_presence_minutes: Total time spent in building (minutes)
entered_during_night_hours: 1 if entered during night hours (22:00-06:00)
num_unique_campus: Number of different campuses accessed
early_entry_flag: 1 if entered before 06:00
late_exit_flag: 1 if exited after 22:00
entry_during_weekend: 1 if entered during weekend (Friday/Saturday)

=== RISK INDICATORS ===
risk_travel_indicator: 1 if suspicious travel activity detected
is_malicious: TARGET VARIABLE - 1 if employee is malicious insider

=== BEHAVIORAL GROUPS ===
A: Executive Management - High-level executives, irregular hours, moderate printing
B: Developers & Engineers - Technical staff, some late hours, moderate burning
C: Office Workers - Regular hours, high printing, low burning
D: Marketing & Business Development - Regular hours, high printing, some travel
E: Security - 24/7 shifts, low printing, high security access
F: IT - Technical staff, some irregular hours, high burning

=== NOTES ===
- All timestamps are in 24-hour format
- Classification levels: 1=Low, 2=Moderate, 3=High, 4=Top Secret
- Hostile countries include: Iran, Russia, China, North Korea, Syria
- Off-hours defined as outside 06:00-22:00 on weekdays
- Weekend defined as Friday-Saturday (local convention)
- null values in trip-related fields indicate no travel
- Behavioral patterns are based on job role and department
"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(dictionary_content)
        
        print(f"Data dictionary created: {filename}")
        return filename
