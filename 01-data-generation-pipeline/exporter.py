import pandas as pd
from datetime import datetime
import os

class DataExporter:
    """Class for exporting datasets to various formats"""
    
    def __init__(self, behavioral_groups_mapping=None):
        """
        Initialize the exporter with behavioral groups mapping
        
        Args:
            behavioral_groups_mapping: Dictionary mapping departments to behavioral groups
        """
        if behavioral_groups_mapping is None:
            # Default mapping based on your data
            self.behavioral_groups_mapping = {
                'Executive Management': 'A',
                'Engineering Department': 'B', 
                'R&D Department': 'B',
                'Operations and Manufacturing': 'C',
                'Finance': 'C',
                'Human Resources': 'C',
                'Project Management': 'C',
                'Marketing and Business Development': 'D',
                'Information Technology': 'F',
                'Security and Information Security': 'E',
                'Legal and Regulation': 'C'
            }
        else:
            self.behavioral_groups_mapping = behavioral_groups_mapping
    
    def export_dataset(self, df, output_path, filename_prefix, export_format='both', include_analysis=True):
        """
        Export dataset with specified format and options
        
        Args:
            df: DataFrame to export
            output_path: Path to output directory
            filename_prefix: Prefix for filenames
            export_format: 'csv', 'excel', or 'both'
            include_analysis: Whether to include analysis reports
            
        Returns:
            dict: Dictionary of exported files
        """
        import os
        exported_files = {}
        
        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)
        
        # Generate full file paths
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if export_format in ['csv', 'both']:
            csv_filename = f"{filename_prefix}_{timestamp}.csv"
            csv_path = os.path.join(output_path, csv_filename)
            df.to_csv(csv_path, index=False)
            exported_files['CSV'] = csv_path
            print(f"Dataset exported to {csv_path}")
        
        if export_format in ['excel', 'both']:
            excel_filename = f"{filename_prefix}_{timestamp}.xlsx"
            excel_path = os.path.join(output_path, excel_filename)
            
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                # Full dataset
                df.to_excel(writer, sheet_name='Full_Dataset', index=False)
                
                # Malicious employees only
                malicious_df = df[df['is_malicious'] == 1]
                if len(malicious_df) > 0:
                    malicious_df.to_excel(writer, sheet_name='Malicious_Only', index=False)
                
                # Summary by behavioral group
                if include_analysis:
                    summary_df = self._create_group_summary(df)
                    summary_df.to_excel(writer, sheet_name='Group_Summary', index=False)
                    
                    # Employee summary
                    employee_summary = self._create_employee_summary(df)
                    employee_summary.to_excel(writer, sheet_name='Employee_Summary', index=False)
                    
                    # Daily aggregations
                    daily_summary = self._create_daily_summary(df)
                    daily_summary.to_excel(writer, sheet_name='Daily_Summary', index=False)
            
            exported_files['Excel'] = excel_path
            print(f"Dataset exported to {excel_path}")
        
        # Create additional analysis files if requested
        if include_analysis:
            # Data dictionary
            dict_filename = f"data_dictionary_{timestamp}.txt"
            dict_path = os.path.join(output_path, dict_filename)
            self.create_data_dictionary(dict_path)
            exported_files['Data_Dictionary'] = dict_path
            
            # Analysis report
            report_filename = f"analysis_report_{timestamp}.txt"
            report_path = os.path.join(output_path, report_filename)
            self.create_analysis_report(df, report_path)
            exported_files['Analysis_Report'] = report_path
        
        return exported_files

    def export_to_csv(self, df, filename_prefix="insider_threat_advanced"):
        """
        Export dataset to CSV format
        
        Args:
            df: pandas DataFrame to export
            filename_prefix: Prefix for filename
            
        Returns:
            str: Generated filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"{filename_prefix}_{timestamp}.csv"
        
        df.to_csv(csv_filename, index=False)
        print(f"Dataset exported to {csv_filename}")
        
        return csv_filename
    
    def export_to_excel(self, df, filename_prefix="insider_threat_advanced"):
        """
        Export dataset to Excel format with multiple sheets
        
        Args:
            df: pandas DataFrame to export
            filename_prefix: Prefix for filename
            
        Returns:
            str: Generated filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = f"{filename_prefix}_{timestamp}.xlsx"
        
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            # Full dataset
            df.to_excel(writer, sheet_name='Full_Dataset', index=False)
            
            # Malicious employees only
            malicious_df = df[df['is_malicious'] == 1]
            if len(malicious_df) > 0:
                malicious_df.to_excel(writer, sheet_name='Malicious_Only', index=False)
            
            # Summary by behavioral group
            summary_df = self._create_group_summary(df)
            summary_df.to_excel(writer, sheet_name='Group_Summary', index=False)
            
            # Employee summary
            employee_summary = self._create_employee_summary(df)
            employee_summary.to_excel(writer, sheet_name='Employee_Summary', index=False)
            
            # Daily aggregations
            daily_summary = self._create_daily_summary(df)
            daily_summary.to_excel(writer, sheet_name='Daily_Summary', index=False)
        
        print(f"Dataset exported to {excel_filename} with multiple sheets")
        return excel_filename
    
    def _create_group_summary(self, df):
        """Create summary statistics by behavioral group"""
        summary_stats = []
        
        for group in sorted(df['behavioral_group'].unique()):
            group_data = df[df['behavioral_group'] == group]
            group_name = [k for k, v in self.behavioral_groups_mapping.items() if v == group][0]
            
            stats = {
                'Behavioral_Group': group,
                'Department': group_name,
                'Total_Employees': group_data['employee_id'].nunique(),
                'Total_Records': len(group_data),
                'Malicious_Employees': group_data[group_data['is_malicious'] == 1]['employee_id'].nunique(),
                'Print_Frequency': len(group_data[group_data['total_printed_pages'] > 0]) / len(group_data),
                'Burn_Frequency': len(group_data[group_data['num_burn_requests'] > 0]) / len(group_data),
                'Travel_Frequency': len(group_data[group_data['is_abroad'] == 1]) / len(group_data),
                'Avg_Pages_Per_Day': group_data['total_printed_pages'].mean(),
                'Avg_Burn_Volume_MB': group_data['total_burn_volume_mb'].mean(),
                'Weekend_Work_Rate': group_data['entry_during_weekend'].mean(),
                'Off_Hours_Print_Rate': group_data['num_print_commands_off_hours'].sum() / max(1, group_data['num_print_commands'].sum()),
                'Off_Hours_Burn_Rate': group_data['num_burn_requests_off_hours'].sum() / max(1, group_data['num_burn_requests'].sum()),
                'Multi_Campus_Access_Rate': len(group_data[group_data['num_unique_campus'] > 1]) / len(group_data),
                'Avg_Classification_Level': group_data['avg_request_classification'].mean(),
                'Max_Classification_Level': group_data['max_request_classification'].max(),
                'Foreign_Travel_Rate': len(group_data[group_data['is_abroad'] == 1]) / len(group_data),
                'Hostile_Country_Rate': len(group_data[group_data['is_hostile_country_trip'] == 1]) / len(group_data),
                'Unofficial_Travel_Rate': len(group_data[(group_data['is_abroad'] == 1) & (group_data['is_official_trip'] == 0)]) / len(group_data)
            }
            summary_stats.append(stats)
        
        return pd.DataFrame(summary_stats)
    
    def _create_employee_summary(self, df):
        """Create summary statistics per employee"""
        employee_stats = []
        
        for emp_id in df['employee_id'].unique():
            emp_data = df[df['employee_id'] == emp_id]
            first_record = emp_data.iloc[0]
            
            stats = {
                'employee_id': emp_id,
                'department': first_record['employee_department'],
                'position': first_record['employee_position'],
                'campus': first_record['employee_campus'],
                'behavioral_group': first_record['behavioral_group'],
                'seniority_years': first_record['employee_seniority_years'],
                'classification': first_record['employee_classification'],
                'is_contractor': first_record['is_contractor'],
                'is_malicious': first_record['is_malicious'],
                'origin_country': first_record['employee_origin_country'],
                'has_foreign_citizenship': first_record['has_foreign_citizenship'],
                'has_criminal_record': first_record['has_criminal_record'],
                'has_medical_history': first_record['has_medical_history'],
                
                # Activity summaries
                'total_work_days': len(emp_data[emp_data['num_entries'] > 0]),
                'total_print_pages': emp_data['total_printed_pages'].sum(),
                'total_print_commands': emp_data['num_print_commands'].sum(),
                'total_burn_requests': emp_data['num_burn_requests'].sum(),
                'total_burn_volume_mb': emp_data['total_burn_volume_mb'].sum(),
                'total_files_burned': emp_data['total_files_burned'].sum(),
                'days_abroad': len(emp_data[emp_data['is_abroad'] == 1]),
                'unique_countries_visited': emp_data[emp_data['country_name'].notna()]['country_name'].nunique(),
                'hostile_country_visits': len(emp_data[emp_data['is_hostile_country_trip'] == 1]),
                'unofficial_trips': len(emp_data[(emp_data['is_abroad'] == 1) & (emp_data['is_official_trip'] == 0)]),
                
                # Behavioral flags
                'frequent_off_hours_work': len(emp_data[(emp_data['early_entry_flag'] == 1) | (emp_data['late_exit_flag'] == 1)]) / len(emp_data),
                'weekend_work_frequency': emp_data['entry_during_weekend'].mean(),
                'multi_campus_access': len(emp_data[emp_data['num_unique_campus'] > 1]) / len(emp_data),
                'off_hours_printing': emp_data['num_print_commands_off_hours'].sum() / max(1, emp_data['num_print_commands'].sum()),
                'off_hours_burning': emp_data['num_burn_requests_off_hours'].sum() / max(1, emp_data['num_burn_requests'].sum()),
                'avg_classification_burned': emp_data['avg_request_classification'].mean(),
                'max_classification_burned': emp_data['max_request_classification'].max(),
                
                # Risk indicators
                'risk_travel_incidents': emp_data['risk_travel_indicator'].sum(),
                'suspicious_activity_score': self._calculate_suspicion_score(emp_data)
            }
            employee_stats.append(stats)
        
        return pd.DataFrame(employee_stats)
    
    def _create_daily_summary(self, df):
        """Create daily aggregated statistics"""
        daily_stats = df.groupby('date').agg({
            'employee_id': 'nunique',
            'is_malicious': 'sum',
            'total_printed_pages': 'sum',
            'num_print_commands': 'sum',
            'num_burn_requests': 'sum',
            'total_burn_volume_mb': 'sum',
            'total_files_burned': 'sum',
            'is_abroad': 'sum',
            'entry_during_weekend': 'sum',
            'early_entry_flag': 'sum',
            'late_exit_flag': 'sum',
            'num_print_commands_off_hours': 'sum',
            'num_burn_requests_off_hours': 'sum',
            'risk_travel_indicator': 'sum'
        }).reset_index()
        
        # Rename columns for clarity
        daily_stats.columns = [
            'date', 'active_employees', 'malicious_records', 'total_pages_printed',
            'total_print_commands', 'total_burn_requests', 'total_burn_volume_mb',
            'total_files_burned', 'employees_abroad', 'weekend_entries',
            'early_entries', 'late_exits', 'off_hours_print_commands',
            'off_hours_burn_requests', 'risk_travel_incidents'
        ]
        
        # Add day of week
        daily_stats['day_of_week'] = pd.to_datetime(daily_stats['date']).dt.day_name()
        daily_stats['is_weekend'] = pd.to_datetime(daily_stats['date']).dt.dayofweek >= 5
        
        return daily_stats
    
    def _calculate_suspicion_score(self, emp_data):
        """Calculate a simple suspicion score for an employee"""
        score = 0
        
        # Off-hours activity
        if emp_data['num_print_commands_off_hours'].sum() > 0:
            score += 1
        if emp_data['num_burn_requests_off_hours'].sum() > 0:
            score += 2
        
        # Weekend work
        if emp_data['entry_during_weekend'].sum() > 0:
            score += 1
        
        # Multi-campus access
        if len(emp_data[emp_data['num_unique_campus'] > 1]) > 0:
            score += 1
        
        # High classification burning
        if emp_data['max_request_classification'].max() >= 4:
            score += 2
        
        # Hostile country travel
        if emp_data['is_hostile_country_trip'].sum() > 0:
            score += 3
        
        # Unofficial travel with activity
        unofficial_travel = emp_data[(emp_data['is_abroad'] == 1) & (emp_data['is_official_trip'] == 0)]
        if len(unofficial_travel) > 0:
            if (unofficial_travel['total_printed_pages'].sum() > 0 or 
                unofficial_travel['num_burn_requests'].sum() > 0):
                score += 3
        
        # High volume activities
        if emp_data['total_printed_pages'].sum() > emp_data['total_printed_pages'].quantile(0.9):
            score += 1
        if emp_data['total_burn_volume_mb'].sum() > emp_data['total_burn_volume_mb'].quantile(0.9):
            score += 1
        
        return score
    
    def export_datasets(self, df, filename_prefix="insider_threat_advanced"):
        """
        Export dataset to both CSV and Excel formats
        
        Args:
            df: pandas DataFrame to export
            filename_prefix: Prefix for filenames
            
        Returns:
            tuple: (csv_filename, excel_filename)
        """
        csv_file = self.export_to_csv(df, filename_prefix)
        excel_file = self.export_to_excel(df, filename_prefix)
        
        return csv_file, excel_file
    
    def export_malicious_only(self, df, filename_prefix="malicious_employees"):
        """
        Export only malicious employee data
        
        Args:
            df: pandas DataFrame to export
            filename_prefix: Prefix for filenames
            
        Returns:
            tuple: (csv_filename, excel_filename)
        """
        malicious_df = df[df['is_malicious'] == 1]
        
        if len(malicious_df) == 0:
            print("No malicious employees found in dataset")
            return None, None
        
        csv_file = self.export_to_csv(malicious_df, filename_prefix)
        excel_file = self.export_to_excel(malicious_df, filename_prefix)
        
        return csv_file, excel_file
    
    def create_data_dictionary(self, filename="data_dictionary.txt"):
        """Create a data dictionary explaining all columns"""
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
    
    def create_analysis_report(self, df, filename="analysis_report.txt"):
        """Create a comprehensive analysis report"""
        report_content = f"""
=== INSIDER THREAT DATASET - ANALYSIS REPORT ===
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== DATASET OVERVIEW ===
Total Records: {len(df):,}
Total Employees: {df['employee_id'].nunique():,}
Date Range: {df['date'].min()} to {df['date'].max()}
Total Days: {(df['date'].max() - df['date'].min()).days + 1}

=== MALICIOUS EMPLOYEE ANALYSIS ===
Malicious Employees: {df[df['is_malicious']==1]['employee_id'].nunique()}
Malicious Records: {df['is_malicious'].sum():,} ({df['is_malicious'].mean():.1%})
Malicious Employee Rate: {df[df['is_malicious']==1]['employee_id'].nunique() / df['employee_id'].nunique():.1%}

=== DEPARTMENT DISTRIBUTION ===
"""
        
        dept_counts = df.groupby('employee_department')['employee_id'].nunique().sort_values(ascending=False)
        for dept, count in dept_counts.items():
            malicious_in_dept = df[(df['employee_department'] == dept) & (df['is_malicious'] == 1)]['employee_id'].nunique()
            report_content += f"{dept}: {count} employees ({malicious_in_dept} malicious, {malicious_in_dept/count:.1%})\n"
        
        report_content += f"""
=== BEHAVIORAL GROUP ANALYSIS ===
"""
        
        group_counts = df.groupby('behavioral_group')['employee_id'].nunique().sort_index()
        for group, count in group_counts.items():
            group_name = [k for k, v in self.behavioral_groups_mapping.items() if v == group][0]
            malicious_in_group = df[(df['behavioral_group'] == group) & (df['is_malicious'] == 1)]['employee_id'].nunique()
            report_content += f"Group {group} ({group_name}): {count} employees ({malicious_in_group} malicious, {malicious_in_group/count:.1%})\n"
        
        report_content += f"""
=== ACTIVITY STATISTICS ===
Total Print Commands: {df['num_print_commands'].sum():,}
Total Pages Printed: {df['total_printed_pages'].sum():,}
Total Burn Requests: {df['num_burn_requests'].sum():,}
Total Files Burned: {df['total_files_burned'].sum():,}
Total Days Abroad: {df['is_abroad'].sum():,}
Hostile Country Visits: {df['is_hostile_country_trip'].sum():,}
Risk Travel Incidents: {df['risk_travel_indicator'].sum():,}

=== OFF-HOURS ACTIVITY ===
Off-Hours Print Commands: {df['num_print_commands_off_hours'].sum():,} ({df['num_print_commands_off_hours'].sum()/max(1,df['num_print_commands'].sum()):.1%})
Off-Hours Burn Requests: {df['num_burn_requests_off_hours'].sum():,} ({df['num_burn_requests_off_hours'].sum()/max(1,df['num_burn_requests'].sum()):.1%})
Early Entries: {df['early_entry_flag'].sum():,}
Late Exits: {df['late_exit_flag'].sum():,}
Weekend Entries: {df['entry_during_weekend'].sum():,}

=== DATA QUALITY CHECKS ===
Missing Values:
"""
        
        missing_data = df.isnull().sum()
        for col, missing in missing_data[missing_data > 0].items():
            report_content += f"  {col}: {missing} ({missing/len(df):.1%})\n"
        
        if missing_data[missing_data > 0].empty:
            report_content += "  No missing values detected\n"
        
        report_content += f"""
Logical Consistency:
  Employees abroad with no building access: {len(df[(df['is_abroad'] == 1) & (df['num_entries'] == 0)])} / {len(df[df['is_abroad'] == 1])}
  Color prints vs total prints: {df['num_color_prints'].sum()} / {df['total_printed_pages'].sum()}
  BW prints vs total
=== RISK INDICATORS ===
High Classification Burning (Level 4): {len(df[df['max_request_classification'] == 4])} incidents
Multi-Campus A prints: {df['num_bw_prints'].sum()} / {df['total_printed_pages'].sum()}
  ccess: {len(df[df['num_unique_campus'] > 1])} incidents
Unofficial Travel: {len(df[(df['is_abroad'] == 1) & (df['is_official_trip'] == 0)])} days
Combined Risk Indicators: {df['risk_travel_indicator'].sum()} incidents

=== RECOMMENDATIONS ===
1. Focus monitoring on employees with multiple risk indicators
2. Pay special attention to off-hours activities
3. Monitor travel patterns, especially to hostile countries
4. Track high-classification document access and burning
5. Investigate multi-campus access patterns
6. Review unofficial travel combined with sensitive activities
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"Analysis report created: {filename}")
        return filename