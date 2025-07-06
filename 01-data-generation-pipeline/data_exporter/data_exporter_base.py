import pandas as pd
from datetime import datetime
import os

class DataExporter:
    """Class for exporting datasets to various formats"""
    
    def __init__(self, behavioral_groups_mapping=None):
        """
        Initialize the exporter with behavioral groups mapping
        
        Args:
            behavioral_groups_mapping: Dictionary mapping departments to behavioral groups
        """
        if behavioral_groups_mapping is None:
            # Default mapping based on your data
            self.behavioral_groups_mapping = {
                'Executive Management': 'A',
                'Engineering Department': 'B', 
                'R&D Department': 'B',
                'Operations and Manufacturing': 'C',
                'Finance': 'C',
                'Human Resources': 'C',
                'Project Management': 'C',
                'Marketing and Business Development': 'D',
                'Information Technology': 'F',
                'Security and Information Security': 'E',
                'Legal and Regulation': 'C'
            }
        else:
            self.behavioral_groups_mapping = behavioral_groups_mapping
    
    def export_dataset(self, df, output_path, filename_prefix, export_format='both', include_analysis=True):
        """
        Export dataset with specified format and options
        
        Args:
            df: DataFrame to export
            output_path: Path to output directory
            filename_prefix: Prefix for filenames
            export_format: 'csv', 'excel', or 'both'
            include_analysis: Whether to include analysis reports
            
        Returns:
            dict: Dictionary of exported files
        """
        import os
        exported_files = {}
        
        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)
        
        # Generate full file paths
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if export_format in ['csv', 'both']:
            csv_filename = f"{filename_prefix}_{timestamp}.csv"
            csv_path = os.path.join(output_path, csv_filename)
            df.to_csv(csv_path, index=False)
            exported_files['CSV'] = csv_path
            print(f"Dataset exported to {csv_path}")
        
        if export_format in ['excel', 'both']:
            excel_filename = f"{filename_prefix}_{timestamp}.xlsx"
            excel_path = os.path.join(output_path, excel_filename)
            
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                # Full dataset
                df.to_excel(writer, sheet_name='Full_Dataset', index=False)
                
                # Malicious employees only
                malicious_df = df[df['is_malicious'] == 1]
                if len(malicious_df) > 0:
                    malicious_df.to_excel(writer, sheet_name='Malicious_Only', index=False)
                
                # Summary by behavioral group
                if include_analysis:
                    from .summary_analyzer import SummaryAnalyzer
                    analyzer = SummaryAnalyzer(self.behavioral_groups_mapping)
                    
                    summary_df = analyzer.create_group_summary(df)
                    summary_df.to_excel(writer, sheet_name='Group_Summary', index=False)
                    
                    # Employee summary
                    employee_summary = analyzer.create_employee_summary(df)
                    employee_summary.to_excel(writer, sheet_name='Employee_Summary', index=False)
                    
                    # Daily aggregations
                    daily_summary = analyzer.create_daily_summary(df)
                    daily_summary.to_excel(writer, sheet_name='Daily_Summary', index=False)
            
            exported_files['Excel'] = excel_path
            print(f"Dataset exported to {excel_path}")
        
        # Create additional analysis files if requested
        if include_analysis:
            from .report_generator import ReportGenerator
            report_gen = ReportGenerator(self.behavioral_groups_mapping)
            
            # Data dictionary
            dict_filename = f"data_dictionary_{timestamp}.txt"
            dict_path = os.path.join(output_path, dict_filename)
            report_gen.create_data_dictionary(dict_path)
            exported_files['Data_Dictionary'] = dict_path
            
            # Analysis report
            report_filename = f"analysis_report_{timestamp}.txt"
            report_path = os.path.join(output_path, report_filename)
            report_gen.create_analysis_report(df, report_path)
            exported_files['Analysis_Report'] = report_path
        
        return exported_files

    def export_to_csv(self, df, filename_prefix="insider_threat_advanced"):
        """
        Export dataset to CSV format
        
        Args:
            df: pandas DataFrame to export
            filename_prefix: Prefix for filename
            
        Returns:
            str: Generated filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"{filename_prefix}_{timestamp}.csv"
        
        df.to_csv(csv_filename, index=False)
        print(f"Dataset exported to {csv_filename}")
        
        return csv_filename
    
    def export_to_excel(self, df, filename_prefix="insider_threat_advanced"):
        """
        Export dataset to Excel format with multiple sheets
        
        Args:
            df: pandas DataFrame to export
            filename_prefix: Prefix for filename
            
        Returns:
            str: Generated filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = f"{filename_prefix}_{timestamp}.xlsx"
        
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            # Full dataset
            df.to_excel(writer, sheet_name='Full_Dataset', index=False)
            
            # Malicious employees only
            malicious_df = df[df['is_malicious'] == 1]
            if len(malicious_df) > 0:
                malicious_df.to_excel(writer, sheet_name='Malicious_Only', index=False)
            
            # Summary by behavioral group
            from .summary_analyzer import SummaryAnalyzer
            analyzer = SummaryAnalyzer(self.behavioral_groups_mapping)
            
            summary_df = analyzer.create_group_summary(df)
            summary_df.to_excel(writer, sheet_name='Group_Summary', index=False)
            
            # Employee summary
            employee_summary = analyzer.create_employee_summary(df)
            employee_summary.to_excel(writer, sheet_name='Employee_Summary', index=False)
            
            # Daily aggregations
            daily_summary = analyzer.create_daily_summary(df)
            daily_summary.to_excel(writer, sheet_name='Daily_Summary', index=False)
        
        print(f"Dataset exported to {excel_filename} with multiple sheets")
        return excel_filename
    
    def export_datasets(self, df, filename_prefix="insider_threat_advanced"):
        """
        Export dataset to both CSV and Excel formats
        
        Args:
            df: pandas DataFrame to export
            filename_prefix: Prefix for filenames
            
        Returns:
            tuple: (csv_filename, excel_filename)
        """
        csv_file = self.export_to_csv(df, filename_prefix)
        excel_file = self.export_to_excel(df, filename_prefix)
        
        return csv_file, excel_file
    
    def export_malicious_only(self, df, filename_prefix="malicious_employees"):
        """
        Export only malicious employee data
        
        Args:
            df: pandas DataFrame to export
            filename_prefix: Prefix for filenames
            
        Returns:
            tuple: (csv_filename, excel_filename)
        """
        malicious_df = df[df['is_malicious'] == 1]
        
        if len(malicious_df) == 0:
            print("No malicious employees found in dataset")
            return None, None
        
        csv_file = self.export_to_csv(malicious_df, filename_prefix)
        excel_file = self.export_to_excel(malicious_df, filename_prefix)
        
        return csv_file, excel_file