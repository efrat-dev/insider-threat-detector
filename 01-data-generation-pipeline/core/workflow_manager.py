"""
Workflow management for the Advanced Insider Threat Dataset Generator.

This module orchestrates the main business logic workflows including:
- Analysis-only mode execution
- Full dataset generation process
- Data validation and export coordination

Author: Advanced Security Analytics Team
Date: 2024
"""

import pandas as pd
from datetime import datetime

from employee_generator.employee_manager import EmployeeManager
from data_generator import DataGenerator
from analyzers.comprehensive_analyzer import ComprehensiveAnalyzer as DataAnalyzer
from data_exporter import DataExporter
from core.config_manager import create_output_directory
from utils.performance_profiler import profile_memory_usage, log_memory_usage


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
        log_memory_usage(logger, "Initial", initial_memory)
    
    # Generate employee profiles
    logger.info("Generating employee profiles...")
    employee_manager = EmployeeManager(args.employees)
    employees = employee_manager.generate_employee_profiles()
        
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
        log_memory_usage(logger, "After generation", post_gen_memory)
    
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