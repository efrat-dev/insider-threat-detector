"""
Creates daily labels for suspicious activity detection
This file creates action-level daily labels based on the original employee-level label
"""

import pandas as pd
import numpy as np

def create_daily_labels_from_df(df):
    """
    Creates new daily labels based on anomalous activity from existing DataFrame
    Enhanced version with multi-stage labeling and smart selection for innocent employees
    
    Args:
        df (pandas.DataFrame): Input data with 'is_malicious' column for employees
        
    Returns:
        pandas.DataFrame: Data with new daily labels including sophisticated detection logic
    """
    
    print("Creating daily labels for suspicious activity detection...")
    
    # Create a new copy of the data to avoid modifying the original
    df_labeled = df.copy()
    
    print("Step 1: Creating employee labels and initializing daily labels...")
    # Copy the original label to a new employee-level column
    df_labeled['is_emp_malicious'] = df_labeled['is_malicious']
    
    # Initialize the new daily action-level label
    df_labeled['is_malicious'] = 0
    
    # Convert date column to datetime if needed
    if 'date' in df_labeled.columns:
        df_labeled['date'] = pd.to_datetime(df_labeled['date'])
    
    # Filter malicious and non-malicious employees
    malicious_ids = df_labeled[df_labeled['is_emp_malicious'] == 1]['employee_id'].unique()
    non_malicious_ids = df_labeled[df_labeled['is_emp_malicious'] == 0]['employee_id'].unique()
    
    print(f"Found {len(malicious_ids)} malicious employees")
    print(f"Found {len(non_malicious_ids)} non-malicious employees")
    
    print("Step 2: Calculating thresholds based on non-malicious employees only...")
    # Calculate thresholds based on non-malicious employees only to avoid skewed averages
    non_malicious_df = df_labeled[df_labeled['is_emp_malicious'] == 0]
    
    thresholds = {
        # High anomaly thresholds - for detecting highly suspicious activity
        'prints_95': non_malicious_df['num_print_commands'].quantile(0.95),
        'burns_95': non_malicious_df['num_burn_requests'].quantile(0.95),
        'presence_95': non_malicious_df['total_presence_minutes'].quantile(0.95),
        'trip_days_95': non_malicious_df['trip_day_number'].quantile(0.95),
        
        # Softer thresholds - for marking days before/after severe anomalous activity
        'prints_75': non_malicious_df['num_print_commands'].quantile(0.75),
        'burns_75': non_malicious_df['num_burn_requests'].quantile(0.75),
        'presence_75': non_malicious_df['total_presence_minutes'].quantile(0.75),
    }
    
    print(f"Detection thresholds (95th percentile):")
    print(f"  - Print commands: {thresholds['prints_95']:.2f}")
    print(f"  - Burn requests: {thresholds['burns_95']:.2f}")
    print(f"  - Presence minutes: {thresholds['presence_95']:.2f}")
    print(f"  - Trip days: {thresholds['trip_days_95']:.2f}")
    
    print("Step 3: Identifying highly suspicious days for malicious employees...")
    # Stage 1: Mark malicious actions for pre-identified malicious employees
    high_flag = (
        (df_labeled['employee_id'].isin(malicious_ids)) &
        (
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
    
    print("Step 4: Identifying days before/after suspicious activity...")
    # Stage 2: Mark days before and after for malicious employees
    if 'date' in df_labeled.columns:
        for emp_id in malicious_ids:
            emp_df = df_labeled[df_labeled['employee_id'] == emp_id].sort_values('date')
            flagged_days = emp_df[emp_df['is_malicious'] == 1]['date'].tolist()

            for day in flagged_days:
                for offset in [-1, 1]:  # Day before and after
                    nearby_day = day + pd.Timedelta(days=offset)
                    cond = (
                        (df_labeled['employee_id'] == emp_id) &
                        (df_labeled['date'] == nearby_day) &
                        (
                            (df_labeled['num_print_commands'] > thresholds['prints_75']) |
                            (df_labeled['num_burn_requests'] > thresholds['burns_75']) |
                            (df_labeled['total_presence_minutes'] > thresholds['presence_75']) |
                            (df_labeled['entered_during_night_hours'] == 1) |
                            (df_labeled['is_abroad'] == 1)
                        )
                    )
                    df_labeled.loc[cond, 'is_malicious'] = 1
    
    print("Step 5: Creating false positives from innocent employees...")
    # Stage 3: Mark anomalous actions of innocent employees (compared to themselves)
    # Select 5% of innocent employees randomly to simulate false positives
    selected_ids = np.random.choice(
        non_malicious_ids, 
        size=int(len(non_malicious_ids) * 0.05), 
        replace=False
    )
    
    print(f"Selected {len(selected_ids)} innocent employees for false positive simulation")
    
    for emp_id in selected_ids:
        emp_df = df_labeled[df_labeled['employee_id'] == emp_id].sort_values('date')
        
        # Calculate personal averages for this employee
        avg_prints = emp_df['num_print_commands'].mean()
        avg_burns = emp_df['num_burn_requests'].mean()
        avg_presence = emp_df['total_presence_minutes'].mean()

        # Find candidate days that are anomalous for this employee
        candidate_days = emp_df[
            (emp_df['num_print_commands'] > max(thresholds['prints_95'], 2 * avg_prints)) |
            (emp_df['num_burn_requests'] > max(thresholds['burns_95'], 2 * avg_burns)) |
            (emp_df['total_presence_minutes'] > max(thresholds['presence_95'], 2 * avg_presence)) |
            (emp_df['entered_during_night_hours'] == 1)
        ]

        # Create false positives to simulate real-world detection challenges
        if not candidate_days.empty:
            # Calculate suspicion score for each anomalous day
            candidate_days = candidate_days.copy()
            candidate_days['suspicion_score'] = (
                candidate_days['num_print_commands'].rank(pct=True) +
                candidate_days['num_burn_requests'].rank(pct=True) +
                candidate_days['total_presence_minutes'].rank(pct=True) +
                candidate_days['entered_during_night_hours'] * 0.5 +
                candidate_days['early_entry_flag'] * 0.5
            )
            
            # Smart selection: 80% most suspicious day, 20% random
            if np.random.rand() < 0.8:
                selected_row = candidate_days.sort_values('suspicion_score', ascending=False).index[0]
            else:
                selected_row = candidate_days.sample(1).index[0]

            # Mark the selected day as malicious
            df_labeled.loc[selected_row, 'is_malicious'] = 1
    
    # Calculate comprehensive statistics
    total_days = len(df_labeled)
    malicious_days = df_labeled['is_malicious'].sum()
    malicious_employee_records = df_labeled['is_emp_malicious'].sum()
    
    # Advanced statistics
    malicious_emp_flagged_days = df_labeled[
        (df_labeled['is_emp_malicious'] == 1) & (df_labeled['is_malicious'] == 1)
    ]['is_malicious'].sum()
    
    innocent_emp_flagged_days = df_labeled[
        (df_labeled['is_emp_malicious'] == 0) & (df_labeled['is_malicious'] == 1)
    ]['is_malicious'].sum()
    
    print(f"\nComprehensive daily labels statistics:")
    print(f"  - Total daily records: {total_days}")
    print(f"  - Total malicious employee records: {malicious_employee_records}")
    print(f"  - Total suspicious days identified: {malicious_days}")
    print(f"  - Suspicious days from malicious employees: {malicious_emp_flagged_days}")
    print(f"  - False positive days from innocent employees: {innocent_emp_flagged_days}")
    print(f"  - Overall percentage of suspicious days: {(malicious_days/total_days)*100:.2f}%")
    print(f"  - Detection rate for malicious employees: {(malicious_emp_flagged_days/malicious_employee_records)*100:.2f}%")
    
    return df_labeled