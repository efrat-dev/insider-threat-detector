#!/usr/bin/env python3
"""
Main entry point for the Advanced Insider Threat Dataset Generator.

This script orchestrates the entire dataset generation process including:
- Employee profile generation
- Behavioral pattern simulation
- Activity data generation
- Statistical analysis
- Data export

Author: Advanced Security Analytics Team
Date: 2024
"""

import sys
import argparse
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path

# Import our modules
from config.config import Config
from employee_generator import EmployeeGenerator
from data_generator import DataGenerator
from analyzers.comprehensive_analyzer import ComprehensiveAnalyzer as DataAnalyzer
from exporter import DataExporter


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Advanced Insider Threat Dataset Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Generate default dataset
  python main.py -e 500 -d 90 -m 0.08    # 500 employees, 90 days, 8% malicious
  python main.py --analysis-only          # Only run analysis on existing data
  python main.py --export-format excel    # Export only to Excel
  python main.py --seed 42                # Use specific random seed
        """
    )
    
    # Dataset parameters
    parser.add_argument(
        '-e', '--employees',
        type=int,
        default=Config.DEFAULT_NUM_EMPLOYEES,
        help=f'Number of employees to generate (default: {Config.DEFAULT_NUM_EMPLOYEES})'
    )
    
    parser.add_argument(
        '-d', '--days',
        type=int,
        default=Config.DEFAULT_DAYS_RANGE,
        help=f'Number of days to simulate (default: {Config.DEFAULT_DAYS_RANGE})'
    )
    
    parser.add_argument(
        '-m', '--malicious-ratio',
        type=float,
        default=Config.DEFAULT_MALICIOUS_RATIO,
        help=f'Ratio of malicious employees (default: {Config.DEFAULT_MALICIOUS_RATIO})'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='insider_threat_advanced',
        help='Output filename prefix (default: insider_threat_advanced)'
    )
    
    parser.add_argument(
        '--export-format',
        choices=['csv', 'excel', 'both'],
        default='both',
        help='Export format (default: both)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./output',
        help='Output directory (default: ./output)'
    )
    
    # Analysis options
    parser.add_argument(
        '--analysis-only',
        action='store_true',
        help='Only run analysis on existing dataset (requires --input-file)'
    )
    
    parser.add_argument(
        '--input-file',
        type=str,
        help='Input CSV file for analysis-only mode'
    )
    
    parser.add_argument(
        '--skip-analysis',
        action='store_true',
        help='Skip statistical analysis and summary generation'
    )
    
    # Technical options
    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed for reproducibility'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress all output except errors'
    )
    
    # Validation options
    parser.add_argument(
        '--validate-data',
        action='store_true',
        help='Run comprehensive data validation checks'
    )
    
    parser.add_argument(
        '--profile-performance',
        action='store_true',
        help='Profile performance and memory usage'
    )
    
    return parser.parse_args()


def setup_logging(verbose=False, quiet=False):
    """Setup logging configuration"""
    import logging
    
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('dataset_generation.log')
        ]
    )
    
    return logging.getLogger(__name__)


def validate_arguments(args):
    """Validate command line arguments"""
    errors = []
    
    # Validate employee count
    if args.employees <= 0:
        errors.append("Number of employees must be positive")
    elif args.employees > 10000:
        errors.append("Number of employees exceeds maximum (10,000)")
    
    # Validate days range
    if args.days <= 0:
        errors.append("Number of days must be positive")
    elif args.days > 1000:
        errors.append("Number of days exceeds maximum (1,000)")
    
    # Validate malicious ratio
    if not (0 <= args.malicious_ratio <= 1):
        errors.append("Malicious ratio must be between 0 and 1")
    
    # Validate analysis-only mode
    if args.analysis_only and not args.input_file:
        errors.append("Analysis-only mode requires --input-file")
    
    # Validate input file exists
    if args.input_file and not Path(args.input_file).exists():
        errors.append(f"Input file does not exist: {args.input_file}")
    
    # Validate conflicting options
    if args.verbose and args.quiet:
        errors.append("Cannot specify both --verbose and --quiet")
    
    if errors:
        print("ERROR: Invalid arguments:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


def print_banner():
    """Print application banner"""
    print("בס\"ד")
    print("=" * 70)
    print("    Advanced Insider Threat Dataset Generator")
    print("    Realistic Behavioral Pattern Simulation")
    print("=" * 70)
    print()


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
    print()


def setup_random_seed(seed=None):
    """Setup random seed for reproducibility"""
    if seed is not None:
        import random
        import numpy as np
        
        random.seed(seed)
        np.random.seed(seed)
        print(f"Random seed set to: {seed}")
    else:
        print("Using random seed")


def create_output_directory(output_dir):
    """Create output directory if it doesn't exist"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def profile_memory_usage():
    """Profile memory usage if profiling is enabled"""
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,  # Resident Set Size
            'vms_mb': memory_info.vms / 1024 / 1024,  # Virtual Memory Size
            'percent': process.memory_percent()
        }
    except ImportError:
        return None


def run_analysis_only(args, logger):
    """Run analysis on existing dataset"""
    logger.info("Running analysis-only mode")
    
    # Load existing dataset
    logger.info(f"Loading dataset from {args.input_file}")
    df = pd.read_csv(args.input_file)
    
    # Create analyzer
    analyzer = DataAnalyzer()
    
    # Run analysis
    logger.info("Running behavioral analysis...")
    analyzer.generate_summary_statistics(df)
    
    # Validate data if requested
    if args.validate_data:
        logger.info("Running data validation...")
        analyzer.validate_data_quality(df)
    
    # Export analysis results
    output_path = create_output_directory(args.output_dir)
    analysis_file = output_path / f"{args.output}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    analyzer.export_analysis_results(df, str(analysis_file))
    logger.info(f"Analysis results exported to {analysis_file}")
    
    return df


def run_full_generation(args, logger):
    """Run full dataset generation process"""
    logger.info("Starting full dataset generation")
    
    # Profile initial memory usage
    if args.profile_performance:
        initial_memory = profile_memory_usage()
        if initial_memory:
            logger.info(f"Initial memory usage: {initial_memory['rss_mb']:.1f} MB")
    
    # Generate employee profiles
    logger.info("Generating employee profiles...")
    employee_gen = EmployeeGenerator(args.employees)
    employees = employee_gen.generate_employee_profiles()
        
    # Generate dataset
    logger.info("Generating behavioral dataset...")
    data_gen = DataGenerator(
        employees=employees,
        days_range=args.days,
        malicious_ratio=args.malicious_ratio
    )
    
    df = data_gen.generate_dataset()
    
    # Profile memory usage after generation
    if args.profile_performance:
        post_gen_memory = profile_memory_usage()
        if post_gen_memory:
            logger.info(f"Memory usage after generation: {post_gen_memory['rss_mb']:.1f} MB")
    
    # Run analysis unless skipped
    if not args.skip_analysis:
        logger.info("Running behavioral analysis...")
        analyzer = DataAnalyzer()
        analyzer.generate_summary_statistics(df)
        
        # Run data validation if requested
        if args.validate_data:
            logger.info("Running data validation...")
            analyzer.validate_data_quality(df)
    
    # Export dataset
    logger.info("Exporting dataset...")
    output_path = create_output_directory(args.output_dir)
    
    exporter = DataExporter()
    exported_files = exporter.export_dataset(
        df=df,
        output_path=str(output_path),
        filename_prefix=args.output,
        export_format=args.export_format,
        include_analysis=not args.skip_analysis
    )
    
    logger.info("Export completed:")
    for file_type, filename in exported_files.items():
        logger.info(f"  {file_type}: {filename}")
    
    return df, exported_files


def print_final_statistics(df, logger):
    """Print final dataset statistics"""
    logger.info("=== FINAL DATASET STATISTICS ===")
    logger.info(f"Total records: {len(df):,}")
    logger.info(f"Total employees: {df['employee_id'].nunique():,}")
    logger.info(f"Date range: {df['date'].min()} to {df['date'].max()}")
    logger.info(f"Malicious employees: {df[df['is_malicious']==1]['employee_id'].nunique()}")
    logger.info(f"Malicious records: {df['is_malicious'].sum():,} ({df['is_malicious'].mean():.1%})")
    
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


def main():
    """Main application entry point"""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Validate arguments
        validate_arguments(args)
        
        # Setup logging
        logger = setup_logging(args.verbose, args.quiet)
        
        # Print banner unless quiet
        if not args.quiet:
            print_banner()
            print_configuration(args)
        
        # Setup random seed
        setup_random_seed(args.seed)
        
        # Record start time
        start_time = datetime.now()
        logger.info(f"Starting dataset generation at {start_time}")
        
        # Run generation or analysis
        if args.analysis_only:
            df = run_analysis_only(args, logger)
            exported_files = {}
        else:
            df, exported_files = run_full_generation(args, logger)
        
        # Print final statistics
        if not args.quiet:
            print_final_statistics(df, logger)
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = end_time - start_time
        logger.info(f"Execution completed in {execution_time}")
        
        # Profile final memory usage
        if args.profile_performance:
            final_memory = profile_memory_usage()
            if final_memory:
                logger.info(f"Final memory usage: {final_memory['rss_mb']:.1f} MB")
        
        # Success message
        if not args.quiet:
            print("\n" + "=" * 50)
            print("Dataset generation completed successfully!")
            if exported_files:
                print("Files created:")
                for file_type, filename in exported_files.items():
                    print(f"  {file_type}: {filename}")
            print("=" * 50)
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Advanced Insider Threat Dataset Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Generate default dataset
  python main.py -e 500 -d 90 -m 0.08    # 500 employees, 90 days, 8% malicious
  python main.py --analysis-only          # Only run analysis on existing data
  python main.py --export-format excel    # Export only to Excel
  python main.py --seed 42                # Use specific random seed
        """
    )
    
    # Dataset parameters
    parser.add_argument(
        '-e', '--employees',
        type=int,
        default=Config.DEFAULT_NUM_EMPLOYEES,
        help=f'Number of employees to generate (default: {Config.DEFAULT_NUM_EMPLOYEES})'
    )
    
    parser.add_argument(
        '-d', '--days',
        type=int,
        default=Config.DEFAULT_DAYS_RANGE,
        help=f'Number of days to simulate (default: {Config.DEFAULT_DAYS_RANGE})'
    )
    
    parser.add_argument(
        '-m', '--malicious-ratio',
        type=float,
        default=Config.DEFAULT_MALICIOUS_RATIO,
        help=f'Ratio of malicious employees (default: {Config.DEFAULT_MALICIOUS_RATIO})'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='insider_threat_advanced',
        help='Output filename prefix (default: insider_threat_advanced)'
    )
    
    parser.add_argument(
        '--export-format',
        choices=['csv', 'excel', 'both'],
        default='both',
        help='Export format (default: both)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./output',
        help='Output directory (default: ./output)'
    )
    
    # Analysis options
    parser.add_argument(
        '--analysis-only',
        action='store_true',
        help='Only run analysis on existing dataset (requires --input-file)'
    )
    
    parser.add_argument(
        '--input-file',
        type=str,
        help='Input CSV file for analysis-only mode'
    )
    
    parser.add_argument(
        '--skip-analysis',
        action='store_true',
        help='Skip statistical analysis and summary generation'
    )
    
    # Technical options
    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed for reproducibility'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress all output except errors'
    )
    
    # Validation options
    parser.add_argument(
        '--validate-data',
        action='store_true',
        help='Run comprehensive data validation checks'
    )
    
    parser.add_argument(
        '--profile-performance',
        action='store_true',
        help='Profile performance and memory usage'
    )
    
    return parser.parse_args()


def setup_logging(verbose=False, quiet=False):
    """Setup logging configuration"""
    import logging
    
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('dataset_generation.log')
        ]
    )
    
    return logging.getLogger(__name__)


def validate_arguments(args):
    """Validate command line arguments"""
    errors = []
    
    # Validate employee count
    if args.employees <= 0:
        errors.append("Number of employees must be positive")
    elif args.employees > 10000:
        errors.append("Number of employees exceeds maximum (10,000)")
    
    # Validate days range
    if args.days <= 0:
        errors.append("Number of days must be positive")
    elif args.days > 1000:
        errors.append("Number of days exceeds maximum (1,000)")
    
    # Validate malicious ratio
    if not (0 <= args.malicious_ratio <= 1):
        errors.append("Malicious ratio must be between 0 and 1")
    
    # Validate analysis-only mode
    if args.analysis_only and not args.input_file:
        errors.append("Analysis-only mode requires --input-file")
    
    # Validate input file exists
    if args.input_file and not Path(args.input_file).exists():
        errors.append(f"Input file does not exist: {args.input_file}")
    
    # Validate conflicting options
    if args.verbose and args.quiet:
        errors.append("Cannot specify both --verbose and --quiet")
    
    if errors:
        print("ERROR: Invalid arguments:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


def print_banner():
    """Print application banner"""
    print("בס\"ד")
    print("=" * 70)
    print("    Advanced Insider Threat Dataset Generator")
    print("    Realistic Behavioral Pattern Simulation")
    print("=" * 70)
    print()


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
    print()


def setup_random_seed(seed=None):
    """Setup random seed for reproducibility"""
    if seed is not None:
        import random
        import numpy as np
        
        random.seed(seed)
        np.random.seed(seed)
        print(f"Random seed set to: {seed}")
    else:
        print("Using random seed")


def create_output_directory(output_dir):
    """Create output directory if it doesn't exist"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def profile_memory_usage():
    """Profile memory usage if profiling is enabled"""
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,  # Resident Set Size
            'vms_mb': memory_info.vms / 1024 / 1024,  # Virtual Memory Size
            'percent': process.memory_percent()
        }
    except ImportError:
        return None


def run_analysis_only(args, logger):
    """Run analysis on existing dataset"""
    logger.info("Running analysis-only mode")
    
    # Load existing dataset
    logger.info(f"Loading dataset from {args.input_file}")
    df = pd.read_csv(args.input_file)
    
    # Create analyzer
    analyzer = DataAnalyzer()
    
    # Run analysis
    logger.info("Running behavioral analysis...")
    analyzer.generate_summary_statistics(df)
    
    # Validate data if requested
    if args.validate_data:
        logger.info("Running data validation...")
        analyzer.validate_data_quality(df)
    
    # Export analysis results
    output_path = create_output_directory(args.output_dir)
    analysis_file = output_path / f"{args.output}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    analyzer.export_analysis_results(df, str(analysis_file))
    logger.info(f"Analysis results exported to {analysis_file}")
    
    return df


def run_full_generation(args, logger):
    """Run full dataset generation process"""
    logger.info("Starting full dataset generation")
    
    # Profile initial memory usage
    if args.profile_performance:
        initial_memory = profile_memory_usage()
        if initial_memory:
            logger.info(f"Initial memory usage: {initial_memory['rss_mb']:.1f} MB")
    
    # Generate employee profiles
    logger.info("Generating employee profiles...")
    employee_gen = EmployeeGenerator(args.employees)
    employees = employee_gen.generate_employee_profiles()
        
    # Generate dataset
    logger.info("Generating behavioral dataset...")
    data_gen = DataGenerator(
        employees=employees,
        days_range=args.days,
        malicious_ratio=args.malicious_ratio
    )
    
    df = data_gen.generate_dataset()
    
    # Profile memory usage after generation
    if args.profile_performance:
        post_gen_memory = profile_memory_usage()
        if post_gen_memory:
            logger.info(f"Memory usage after generation: {post_gen_memory['rss_mb']:.1f} MB")
    
    # Run analysis unless skipped
    if not args.skip_analysis:
        logger.info("Running behavioral analysis...")
        analyzer = DataAnalyzer()
        analyzer.generate_summary_statistics(df)
        
        # Run data validation if requested
        if args.validate_data:
            logger.info("Running data validation...")
            analyzer.validate_data_quality(df)
    
    # Export dataset
    logger.info("Exporting dataset...")
    output_path = create_output_directory(args.output_dir)
    
    exporter = DataExporter()
    exported_files = exporter.export_dataset(
        df=df,
        output_path=str(output_path),
        filename_prefix=args.output,
        export_format=args.export_format,
        include_analysis=not args.skip_analysis
    )
    
    logger.info("Export completed:")
    for file_type, filename in exported_files.items():
        logger.info(f"  {file_type}: {filename}")
    
    return df, exported_files


def print_final_statistics(df, logger):
    """Print final dataset statistics"""
    logger.info("=== FINAL DATASET STATISTICS ===")
    logger.info(f"Total records: {len(df):,}")
    logger.info(f"Total employees: {df['employee_id'].nunique():,}")
    logger.info(f"Date range: {df['date'].min()} to {df['date'].max()}")
    logger.info(f"Malicious employees: {df[df['is_malicious']==1]['employee_id'].nunique()}")
    logger.info(f"Malicious records: {df['is_malicious'].sum():,} ({df['is_malicious'].mean():.1%})")
    
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


def main():
    """Main application entry point"""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Validate arguments
        validate_arguments(args)
        
        # Setup logging
        logger = setup_logging(args.verbose, args.quiet)
        
        # Print banner unless quiet
        if not args.quiet:
            print_banner()
            print_configuration(args)
        
        # Setup random seed
        setup_random_seed(args.seed)
        
        # Record start time
        start_time = datetime.now()
        logger.info(f"Starting dataset generation at {start_time}")
        
        # Run generation or analysis
        if args.analysis_only:
            df = run_analysis_only(args, logger)
            exported_files = {}
        else:
            df, exported_files = run_full_generation(args, logger)
        
        # Print final statistics
        if not args.quiet:
            print_final_statistics(df, logger)
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = end_time - start_time
        logger.info(f"Execution completed in {execution_time}")
        
        # Profile final memory usage
        if args.profile_performance:
            final_memory = profile_memory_usage()
            if final_memory:
                logger.info(f"Final memory usage: {final_memory['rss_mb']:.1f} MB")
        
        # Success message
        if not args.quiet:
            print("\n" + "=" * 50)
            print("Dataset generation completed successfully!")
            if exported_files:
                print("Files created:")
                for file_type, filename in exported_files.items():
                    print(f"  {file_type}: {filename}")
            print("=" * 50)
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())