"""
Command line argument parsing and validation for the Advanced Insider Threat Dataset Generator.

This module:
- Defines and parses all CLI arguments (dataset, output, analysis, technical, noise injection).
- Validates provided arguments for logical and technical correctness.
"""

import argparse
import sys
from pathlib import Path
from config.config import Config


def parse_arguments():
    """
    Parse command line arguments.

    Uses argparse to:
    - Organize arguments into categories (dataset parameters, output, analysis, technical, noise injection).
    - Provide help text and usage examples.
    - Apply defaults from the Config object.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
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
  python main.py --add-noise              # Add synthetic noise to dataset
        """
    )
    
    # --- Dataset parameters ---
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
    
    # --- Output options ---
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
    
    # --- Analysis options ---
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
    parser.add_argument(
        '--validate-data',
        action='store_true',
        help='Run comprehensive data validation and quality checks'
    )
    
    # --- Technical options ---
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
    
    # --- Noise injection options ---
    noise_group = parser.add_argument_group('Noise injection options')
    noise_group.add_argument(
        '--add-noise',
        action='store_true',
        help='Add synthetic noise to the generated dataset'
    )
    noise_group.add_argument(
        '--burn-noise-rate',
        type=float,
        default=0.05,
        help='Percentage of rows to add burning noise to (default: 0.05)'
    )
    noise_group.add_argument(
        '--print-noise-rate',
        type=float,
        default=0.05,
        help='Percentage of rows to add printing noise to (default: 0.05)'
    )
    noise_group.add_argument(
        '--entry-time-noise-rate',
        type=float,
        default=0.10,
        help='Percentage of rows to add entry time noise to (default: 0.10)'
    )
    noise_group.add_argument(
        '--use-gaussian',
        action='store_true',
        help='Use Gaussian noise distribution for certain fields'
    )
    
    return parser.parse_args()


def validate_arguments(args):
    """
    Validate command line arguments.

    Performs logical checks such as:
    - Positive ranges for employee count and days.
    - Malicious ratio between 0 and 1.
    - Required input file for analysis-only mode.
    - File existence checks.
    - Conflicting flag detection (e.g., verbose + quiet).
    - Noise rate bounds validation.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
    
    Exits:
        With status code 1 if validation fails.
    """
    errors = []
    
    # Employee count validation
    if args.employees <= 0:
        errors.append("Number of employees must be positive")
    elif args.employees > 10000:
        errors.append("Number of employees exceeds maximum (10,000)")
    
    # Days validation
    if args.days <= 0:
        errors.append("Number of days must be positive")
    elif args.days > 1000:
        errors.append("Number of days exceeds maximum (1,000)")
    
    # Malicious ratio validation
    if not (0 <= args.malicious_ratio <= 1):
        errors.append("Malicious ratio must be between 0 and 1")
    
    # Analysis-only mode requirements
    if args.analysis_only and not args.input_file:
        errors.append("Analysis-only mode requires --input-file")
    
    # Input file existence check
    if args.input_file and not Path(args.input_file).exists():
        errors.append(f"Input file does not exist: {args.input_file}")
    
    # Conflicting verbosity flags
    if args.verbose and args.quiet:
        errors.append("Cannot specify both --verbose and --quiet")
    
    # Noise parameters validation
    if args.add_noise:
        if not (0 <= args.burn_noise_rate <= 1):
            errors.append("Burn noise rate must be between 0 and 1")
        if not (0 <= args.print_noise_rate <= 1):
            errors.append("Print noise rate must be between 0 and 1")
        if not (0 <= args.entry_time_noise_rate <= 1):
            errors.append("Entry time noise rate must be between 0 and 1")
    
    if errors:
        print("ERROR: Invalid arguments:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
