from datetime import datetime
from .data_dictionary_generator import DataDictionaryGenerator

class ReportGenerator:
    """Class for generating analysis reports"""

    def __init__(self, behavioral_groups_mapping):
        """
        Initialize the report generator

        Args:
            behavioral_groups_mapping: Dictionary mapping departments to behavioral groups
        """
        self.behavioral_groups_mapping = behavioral_groups_mapping
        self.dict_generator = DataDictionaryGenerator()

    def create_data_dictionary(self, filename="data_dictionary.txt"):
        """Create a data dictionary explaining all columns"""
        return self.dict_generator.create_data_dictionary(filename)

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
  BW prints vs total prints: {df['num_bw_prints'].sum()} / {df['total_printed_pages'].sum()}

=== RISK INDICATORS ===
High Classification Burning (Level 4): {len(df[df['max_request_classification'] == 4])} incidents
Multi-Campus Access: {len(df[df['num_unique_campus'] > 1])} incidents
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
