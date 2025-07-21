"""
Display utilities for the Advanced Insider Threat Dataset Generator.

This module handles all user interface display functionality including:
- Banner printing
- Configuration display
- Final statistics reporting

Author: Advanced Security Analytics Team
Date: 2024
"""

def print_configuration(args):
    """Print current configuration"""
    print("Configuration:")
    print(f"  Employees: {args.employees:,}")
    print(f"  Days: {args.days:,}")
    print(f"  Malicious ratio: {args.malicious_ratio:.1%}")
    print(f"  Expected malicious employees: {int(args.employees * args.malicious_ratio)}")
    print(f"  Expected total records: {args.employees * args.days:,}")
    print(f"  Output format: {args.export_format}")
    print(f"  Output directory: {args.output_dir}")
    if args.seed:
        print(f"  Random seed: {args.seed}")
    
    # הצגת הגדרות רעש
    if args.add_noise:
        print(f"  Noise injection: ENABLED")
        print(f"    - Burn noise rate: {args.burn_noise_rate:.1%}")
        print(f"    - Print noise rate: {args.print_noise_rate:.1%}")
        print(f"    - Entry time noise rate: {args.entry_time_noise_rate:.1%}")
        print(f"    - Use Gaussian distribution: {args.use_gaussian}")
    else:
        print(f"  Noise injection: DISABLED")
    
    print()


def print_final_statistics(df, logger):
    """Print final dataset statistics"""
    logger.info("=== FINAL DATASET STATISTICS ===")
    logger.info(f"Total records: {len(df):,}")
    logger.info(f"Total employees: {df['employee_id'].nunique():,}")
    logger.info(f"Date range: {df['date'].min()} to {df['date'].max()}")
    logger.info(f"Malicious employees: {df[df['is_malicious']==1]['employee_id'].nunique()}")
    logger.info(f"Malicious records: {df['is_malicious'].sum():,} ({df['is_malicious'].mean():.1%})")
    
    # הצגת סטטיסטיקות רעש אם קיימות
    if 'row_modified' in df.columns:
        modified_count = df['row_modified'].sum()
        logger.info(f"Records with noise: {modified_count:,} ({modified_count/len(df):.1%})")
    
    # Department distribution
    logger.info("Department distribution:")
    dept_counts = df.groupby('employee_department')['employee_id'].nunique().sort_values(ascending=False)
    for dept, count in dept_counts.items():
        logger.info(f"  {dept}: {count} employees")
    
    # Behavioral group distribution
    logger.info("Behavioral group distribution:")
    group_counts = df.groupby('behavioral_group')['employee_id'].nunique().sort_index()
    for group, count in group_counts.items():
        logger.info(f"  Group {group}: {count} employees")


def print_success_message(exported_files=None):
    """Print success message with file information"""
    print("\n" + "=" * 50)
    print("Dataset generation completed successfully!")
    if exported_files:
        print("Files created:")
        for file_type, filename in exported_files.items():
            print(f"  {file_type}: {filename}")
    print("=" * 50)