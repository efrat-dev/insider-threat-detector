import pandas as pd

class SummaryAnalyzer:
    """Class for creating summary statistics and analysis"""

    def __init__(self, behavioral_groups_mapping):
        """
        Initialize the analyzer with behavioral groups mapping

        Args:
            behavioral_groups_mapping: Dictionary mapping departments to behavioral groups
        """
        self.behavioral_groups_mapping = behavioral_groups_mapping

    def create_group_summary(self, df):
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

    def create_employee_summary(self, df):
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
                'suspicious_activity_score': self.calculate_suspicion_score(emp_data)
            }
            employee_stats.append(stats)

        return pd.DataFrame(employee_stats)

    def create_daily_summary(self, df):
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

        # Add day of week and weekend flag
        daily_stats['day_of_week'] = pd.to_datetime(daily_stats['date']).dt.day_name()
        daily_stats['is_weekend'] = pd.to_datetime(daily_stats['date']).dt.dayofweek >= 5

        return daily_stats

    def calculate_suspicion_score(self, emp_data):
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