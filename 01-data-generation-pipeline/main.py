#!/usr/bin/env python3
"""
Main entry point for the Advanced Insider Threat Dataset Generator.

This script orchestrates the entire dataset generation process including:
- Employee profile generation
- Behavioral pattern simulation
- Activity data generation
- Statistical analysis
- Data export
- Noise injection (optional)

Author: Advanced Security Analytics Team
Date: 2024
"""

import sys
from datetime import datetime

# Import our modules
from cli import parse_arguments, validate_arguments, print_configuration, print_final_statistics, print_success_message
from core import setup_logging, setup_random_seed, run_analysis_only, run_full_generation, DataNoiseInjector
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
        
        # הוספת רעש אם נדרש
        if args.add_noise:
            logger.info("Adding synthetic noise to dataset...")
                     
            # יצירת מזריק רעש עם הפרמטרים מהCLI
            noise_injector = DataNoiseInjector(
                burn_noise_rate=args.burn_noise_rate,
                print_noise_rate=args.print_noise_rate,
                entry_time_noise_rate=args.entry_time_noise_rate,
                use_gaussian=args.use_gaussian,
                random_seed=args.seed
            )
            
            # הוספת רעש לדאטה
            df = noise_injector.add_noise_to_dataframe(df)
            
            # הדפסת סטטיסטיקות רעש
            noise_stats = noise_injector.get_statistics()
            logger.info(f"Noise injection completed: {noise_stats['modified_rows']}/{noise_stats['total_rows']} rows modified")
            logger.info(f"Burn modifications: {noise_stats['burn_modifications']}")
            logger.info(f"Print modifications: {noise_stats['print_modifications']}")
            logger.info(f"Entry time modifications: {noise_stats['entry_time_modifications']}")
            
            # ייצוא מחדש של הקובץ עם רעש אם היו קבצים מיוצאים
            if exported_files:
                try:
                    from data_exporter import DataExporter
                    from core.config_manager import create_output_directory
                    
                    output_path = create_output_directory(args.output_dir)
                    exporter = DataExporter()
                    
                    # ייצוא עם סיומת מיוחדת לרעש
                    noise_prefix = f"{args.output}_with_noise"
                    exported_files_with_noise = exporter.export_dataset(
                        df=df,
                        output_path=str(output_path),
                        filename_prefix=noise_prefix,
                        export_format=args.export_format,
                        include_analysis=not args.skip_analysis
                    )
                    
                    logger.info("Dataset with noise exported:")
                    for file_type, filename in exported_files_with_noise.items():
                        logger.info(f"  {file_type}: {filename}")
                    
                    # עדכון רשימת הקבצים המיוצאים
                    exported_files.update(exported_files_with_noise)
                    
                except ImportError as e:
                    logger.error(f"Failed to import required modules for export: {e}")
                    logger.info("Dataset with noise was generated but not exported to files")
        
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