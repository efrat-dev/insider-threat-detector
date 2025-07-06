"""
Command line argument parsing and validation for the Advanced Insider Threat Dataset Generator.

This module handles all command-line interface functionality including:
- Argument parsing with argparse
- Argument validation
- Help text and examples

Author: Advanced Security Analytics Team
Date: 2024
"""

import argparse
import sys
from pathlib import Path
from config.config import Config


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