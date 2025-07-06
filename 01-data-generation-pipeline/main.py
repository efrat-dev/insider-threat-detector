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
from datetime import datetime

# Import our modules
from cli import parse_arguments, validate_arguments, print_banner, print_configuration, print_final_statistics, print_success_message
from core import setup_logging, setup_random_seed, run_analysis_only, run_full_generation
from utils import profile_memory_usage, log_memory_usage


def main():
    """Main application entry point"""
    try:
        # Parse and validate arguments
        args = parse_arguments()
        validate_arguments(args)
        
        # Setup logging
        logger = setup_logging(args.verbose, args.quiet)
        
        # Print banner and configuration unless quiet
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
            log_memory_usage(logger, "Final", final_memory)
        
        # Success message
        if not args.quiet:
            print_success_message(exported_files)
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        if 'args' in locals() and hasattr(args, 'verbose') and args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())