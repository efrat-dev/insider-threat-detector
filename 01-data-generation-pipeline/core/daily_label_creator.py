"""
Creates daily action-level labels for suspicious activity detection based on employee-level labels.

This module transforms an input DataFrame containing employee-level maliciousness labels into a
daily-labeled dataset by applying multi-stage anomaly detection logic. It includes:

- Threshold calculation based on non-malicious employee behavior
- Identification of highly suspicious days for known malicious employees
- Extension of suspicious labels to adjacent days based on softer thresholds
- Simulation of false positives by selecting a subset of innocent employees
- Detailed statistical reporting of labeling outcomes

Functions:
-----------
create_daily_labels_from_df(df):
    Processes the input DataFrame and returns an enhanced DataFrame with daily-level 'is_malicious' labels.
"""

import pandas as pd
import numpy as np

def create_daily_labels_from_df(df):
    """
    Generate refined daily-level suspicious activity labels from employee-level data.

    The function performs multi-step labeling by:
      1. Preserving original employee malicious labels and initializing daily labels.
      2. Computing anomaly detection thresholds from non-malicious employees only.
      3. Marking suspicious days for pre-identified malicious employees based on strict thresholds.
      4. Expanding suspicious flags to days immediately before and after detected anomalies using softer thresholds.
      5. Introducing false positives by randomly selecting a fraction of innocent employees and marking anomalous days relative to their own baseline behavior.
      6. Calculating and printing comprehensive statistics on labeling results.

    Args:
        df (pandas.DataFrame): Input dataset containing employee activity data and an 'is_malicious' employee-level label.

    Returns:
        pandas.DataFrame: Copy of the input DataFrame augmented with:
          - 'is_emp_malicious': original employee-level malicious label.
          - 'is_malicious': new daily-level suspicious activity label.
    """
    
    print("Starting creation of daily suspicious activity labels...")

    # Step 1: Initialize labels
    df_labeled = df.copy()
    df_labeled['is_emp_malicious'] = df_labeled['is_malicious']
    df_labeled['is_malicious'] = 0

    # Ensure 'date' column is datetime for temporal operations
    if 'date' in df_labeled.columns:
        df_labeled['date'] = pd.to_datetime(df_labeled['date'])

    # Identify malicious and non-malicious employee IDs
    malicious_ids = df_labeled.loc[df_labeled['is_emp_malicious'] == 1, 'employee_id'].unique()
    non_malicious_ids = df_labeled.loc[df_labeled['is_emp_malicious'] == 0, 'employee_id'].unique()

    print(f"Detected {len(malicious_ids)} malicious employees and {len(non_malicious_ids)} non-malicious employees.")

    # Step 2: Calculate detection thresholds from non-malicious employee activity
    non_malicious_df = df_labeled[df_labeled['is_emp_malicious'] == 0]

    thresholds = {
        'prints_95': non_malicious_df['num_print_commands'].quantile(0.95),
        'burns_95': non_malicious_df['num_burn_requests'].quantile(0.95),
        'presence_95': non_malicious_df['total_presence_minutes'].quantile(0.95),
        'trip_days_95': non_malicious_df['trip_day_number'].quantile(0.95),
        'prints_75': non_malicious_df['num_print_commands'].quantile(0.75),
        'burns_75': non_malicious_df['num_burn_requests'].quantile(0.75),
        'presence_75': non_malicious_df['total_presence_minutes'].quantile(0.75),
    }

    print("Calculated detection thresholds (95th percentile):")
    for key in ['prints_95', 'burns_95', 'presence_95', 'trip_days_95']:
        print(f"  - {key}: {thresholds[key]:.2f}")

    # Step 3: Label highly suspicious days for malicious employees
    high_flag = (
        (df_labeled['employee_id'].isin(malicious_ids)) & (
            (df_labeled['num_print_commands'] > thresholds['prints_95']) |
            (df_labeled['num_print_commands_off_hours'] > 0) |
            (df_labeled['num_burn_requests'] > thresholds['burns_95']) |
            (df_labeled['num_burn_requests_off_hours'] > 0) |
            (df_labeled['total_presence_minutes'] > thresholds['presence_95']) |
            (df_labeled['entered_during_night_hours'] == 1) |
            (df_labeled['early_entry_flag'] == 1) |
            (df_labeled['late_exit_flag'] == 1) |
            (df_labeled['is_abroad'] == 1) |
            (df_labeled['trip_day_number'] > thresholds['trip_days_95']) |
            (df_labeled['is_hostile_country_trip'] == 1)
        )
    )
    df_labeled.loc[high_flag, 'is_malicious'] = 1

    # Step 4: Label days adjacent to suspicious activity for malicious employees
    if 'date' in df_labeled.columns:
        for emp_id in malicious_ids:
            emp_data = df_labeled[df_labeled['employee_id'] == emp_id].sort_values('date')
            suspicious_days = emp_data.loc[emp_data['is_malicious'] == 1, 'date'].tolist()

            for day in suspicious_days:
                for offset in [-1, 1]:
                    adjacent_day = day + pd.Timedelta(days=offset)
                    cond = (
                        (df_labeled['employee_id'] == emp_id) &
                        (df_labeled['date'] == adjacent_day) & (
                            (df_labeled['num_print_commands'] > thresholds['prints_75']) |
                            (df_labeled['num_burn_requests'] > thresholds['burns_75']) |
                            (df_labeled['total_presence_minutes'] > thresholds['presence_75']) |
                            (df_labeled['entered_during_night_hours'] == 1) |
                            (df_labeled['is_abroad'] == 1)
                        )
                    )
                    df_labeled.loc[cond, 'is_malicious'] = 1

    # Step 5: Simulate false positives among innocent employees
    selected_ids = np.random.choice(non_malicious_ids, size=int(len(non_malicious_ids) * 0.05), replace=False)
    print(f"Simulating false positives for {len(selected_ids)} randomly selected innocent employees.")

    for emp_id in selected_ids:
        emp_data = df_labeled[df_labeled['employee_id'] == emp_id].sort_values('date')
        avg_prints = emp_data['num_print_commands'].mean()
        avg_burns = emp_data['num_burn_requests'].mean()
        avg_presence = emp_data['total_presence_minutes'].mean()

        candidate_days = emp_data[
            (emp_data['num_print_commands'] > max(thresholds['prints_95'], 2 * avg_prints)) |
            (emp_data['num_burn_requests'] > max(thresholds['burns_95'], 2 * avg_burns)) |
            (emp_data['total_presence_minutes'] > max(thresholds['presence_95'], 2 * avg_presence)) |
            (emp_data['entered_during_night_hours'] == 1)
        ]

        if not candidate_days.empty:
            candidate_days = candidate_days.copy()
            candidate_days['suspicion_score'] = (
                candidate_days['num_print_commands'].rank(pct=True) +
                candidate_days['num_burn_requests'].rank(pct=True) +
                candidate_days['total_presence_minutes'].rank(pct=True) +
                candidate_days['entered_during_night_hours'] * 0.5 +
                candidate_days['early_entry_flag'] * 0.5
            )

            if np.random.rand() < 0.8:
                selected_idx = candidate_days.sort_values('suspicion_score', ascending=False).index[0]
            else:
                selected_idx = candidate_days.sample(1).index[0]

            df_labeled.loc[selected_idx, 'is_malicious'] = 1

    # Summary statistics
    total_records = len(df_labeled)
    total_suspicious = df_labeled['is_malicious'].sum()
    total_malicious_employees = df_labeled['is_emp_malicious'].sum()

    malicious_suspicious_days = df_labeled[(df_labeled['is_emp_malicious'] == 1) & (df_labeled['is_malicious'] == 1)]['is_malicious'].sum()
    false_positive_days = df_labeled[(df_labeled['is_emp_malicious'] == 0) & (df_labeled['is_malicious'] == 1)]['is_malicious'].sum()

    print("\nDaily labeling statistics summary:")
    print(f"  Total records: {total_records}")
    print(f"  Total malicious employees: {total_malicious_employees}")
    print(f"  Total suspicious days: {total_suspicious}")
    print(f"  Suspicious days for malicious employees: {malicious_suspicious_days}")
    print(f"  False positive suspicious days: {false_positive_days}")
    print(f"  Suspicious days rate: {(total_suspicious / total_records) * 100:.2f}%")
    print(f"  Detection rate for malicious employees: {(malicious_suspicious_days / total_malicious_employees) * 100:.2f}%")

    return df_labeled
