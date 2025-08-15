#!/usr/bin/env python3
"""
Main entry point for the Advanced Insider Threat Dataset Generator.

Key Features:
- Runs either full dataset generation or analysis-only mode.
- Supports optional synthetic noise injection to simulate anomalies.
- Handles data export with and without noise.
"""

import sys
from datetime import datetime

# Internal modules
from cli import parse_arguments, validate_arguments, print_configuration, print_final_statistics, print_success_message
from core import setup_logging, setup_random_seed, run_analysis_only, run_full_generation, DataNoiseInjector


def main():
    """
    Main application entry point.
    Coordinates argument parsing, dataset generation/analysis,
    optional noise injection, and export.
    """
    try:
        # --- Parse and validate CLI arguments ---
        args = parse_arguments()
        validate_arguments(args)

        # --- Logging setup ---
        logger = setup_logging(args.verbose, args.quiet)

        # --- Display configuration (skip in quiet mode) ---
        if not args.quiet:
            print_configuration(args)

        # --- Ensure reproducibility ---
        setup_random_seed(args.seed)

        # --- Record start time for performance measurement ---
        start_time = datetime.now()
        logger.info(f"Starting dataset generation at {start_time}")

        # --- Select operation mode ---
        if args.analysis_only:
            # Runs analysis without generating new synthetic data
            df = run_analysis_only(args, logger)
            exported_files = {}
        else:
            # Full synthetic dataset generation + export
            df, exported_files = run_full_generation(args, logger)

        # --- Optional synthetic noise injection ---
        if args.add_noise:
            logger.info("Adding synthetic noise to dataset...")

            # Create noise injector with user-defined parameters
            noise_injector = DataNoiseInjector(
                burn_noise_rate=args.burn_noise_rate,
                print_noise_rate=args.print_noise_rate,
                entry_time_noise_rate=args.entry_time_noise_rate,
                use_gaussian=args.use_gaussian,
                random_seed=args.seed
            )

            # Apply noise to the dataset
            df = noise_injector.add_noise_to_dataframe(df)

            # Log statistics about the injected noise
            noise_stats = noise_injector.get_statistics()
            logger.info(
                f"Noise injection completed: {noise_stats['modified_rows']}/{noise_stats['total_rows']} rows modified"
            )

            # If dataset was exported earlier, re-export with noise
            if exported_files:
                try:
                    from data_exporter import DataExporter
                    from core.config_manager import create_output_directory

                    output_path = create_output_directory(args.output_dir)
                    exporter = DataExporter()

                    exported_files_with_noise = exporter.export_dataset(
                        df=df,
                        output_path=str(output_path),
                        filename_prefix=f"{args.output}_with_noise",
                        export_format=args.export_format,
                        include_analysis=not args.skip_analysis
                    )

                    logger.info("Dataset with noise exported:")
                    for file_type, filename in exported_files_with_noise.items():
                        logger.info(f"  {file_type}: {filename}")

                    exported_files.update(exported_files_with_noise)

                except ImportError as e:
                    logger.error(f"Failed to import required modules for export: {e}")
                    logger.info("Dataset with noise was generated but not exported to files")

        # --- Final statistics & success message ---
        if not args.quiet:
            print_final_statistics(df, logger)

        # --- Execution time calculation ---
        end_time = datetime.now()
        execution_time = end_time - start_time
        logger.info(f"Execution completed in {execution_time}")

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
    # Exit code is passed to the OS
    sys.exit(main())
