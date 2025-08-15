import pandas as pd
from datetime import datetime
import os

class DataExporter:
    """Class for exporting datasets to various formats."""

    def __init__(self, behavioral_groups_mapping=None):
        """
        Initialize the exporter with behavioral groups mapping.

        Args:
            behavioral_groups_mapping: Dictionary mapping departments to behavioral groups.
        """
        if behavioral_groups_mapping is None:
            # Default mapping based on typical organizational departments
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

    def _remove_behavioral_group_column(self, df):
        """
        Remove the behavioral_group column from the DataFrame before export.

        Args:
            df: DataFrame to clean.

        Returns:
            DataFrame without the behavioral_group column.
        """
        df_export = df.copy()
        if 'behavioral_group' in df_export.columns:
            df_export = df_export.drop('behavioral_group', axis=1)
        return df_export

    def export_dataset(self, df, output_path, filename_prefix, export_format='both', include_analysis=True):
        """
        Export dataset to specified formats with optional analysis reports.

        Args:
            df: DataFrame to export.
            output_path: Output directory path.
            filename_prefix: Prefix for exported filenames.
            export_format: One of 'csv', 'excel', or 'both'.
            include_analysis: Whether to include additional analysis reports.

        Returns:
            dict: Paths of exported files.
        """
        exported_files = {}
        os.makedirs(output_path, exist_ok=True)
        df_export = self._remove_behavioral_group_column(df)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if export_format in ['csv', 'both']:
            csv_filename = f"{filename_prefix}_{timestamp}.csv"
            csv_path = os.path.join(output_path, csv_filename)
            df_export.to_csv(csv_path, index=False)
            exported_files['CSV'] = csv_path
            print(f"Dataset exported to {csv_path}")

        if export_format in ['excel', 'both']:
            excel_filename = f"{filename_prefix}_{timestamp}.xlsx"
            excel_path = os.path.join(output_path, excel_filename)

            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df_export.to_excel(writer, sheet_name='Full_Dataset', index=False)
                malicious_df = df_export[df_export['is_malicious'] == 1]
                if len(malicious_df) > 0:
                    malicious_df.to_excel(writer, sheet_name='Malicious_Only', index=False)

                if include_analysis:
                    from .summary_analyzer import SummaryAnalyzer
                    analyzer = SummaryAnalyzer(self.behavioral_groups_mapping)

                    summary_df = analyzer.create_group_summary(df)
                    summary_df.to_excel(writer, sheet_name='Group_Summary', index=False)

                    employee_summary = analyzer.create_employee_summary(df)
                    employee_summary_export = self._remove_behavioral_group_column(employee_summary)
                    employee_summary_export.to_excel(writer, sheet_name='Employee_Summary', index=False)

                    daily_summary = analyzer.create_daily_summary(df)
                    daily_summary.to_excel(writer, sheet_name='Daily_Summary', index=False)

            exported_files['Excel'] = excel_path
            print(f"Dataset exported to {excel_path}")

        if include_analysis:
            from .report_generator import ReportGenerator
            report_gen = ReportGenerator(self.behavioral_groups_mapping)

            dict_filename = f"data_dictionary_{timestamp}.txt"
            dict_path = os.path.join(output_path, dict_filename)
            report_gen.create_data_dictionary(dict_path)
            exported_files['Data_Dictionary'] = dict_path

            report_filename = f"analysis_report_{timestamp}.txt"
            report_path = os.path.join(output_path, report_filename)
            report_gen.create_analysis_report(df, report_path)
            exported_files['Analysis_Report'] = report_path

        return exported_files

    def export_to_csv(self, df, filename_prefix="insider_threat_advanced"):
        """
        Export dataset to CSV file.

        Args:
            df: pandas DataFrame to export.
            filename_prefix: Filename prefix.

        Returns:
            str: Generated CSV filename.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"{filename_prefix}_{timestamp}.csv"
        df_export = self._remove_behavioral_group_column(df)
        df_export.to_csv(csv_filename, index=False)
        print(f"Dataset exported to {csv_filename}")
        return csv_filename

    def export_to_excel(self, df, filename_prefix="insider_threat_advanced"):
        """
        Export dataset to Excel with multiple sheets.

        Args:
            df: pandas DataFrame to export.
            filename_prefix: Filename prefix.

        Returns:
            str: Generated Excel filename.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = f"{filename_prefix}_{timestamp}.xlsx"
        df_export = self._remove_behavioral_group_column(df)

        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            df_export.to_excel(writer, sheet_name='Full_Dataset', index=False)
            malicious_df = df_export[df_export['is_malicious'] == 1]
            if len(malicious_df) > 0:
                malicious_df.to_excel(writer, sheet_name='Malicious_Only', index=False)

            from .summary_analyzer import SummaryAnalyzer
            analyzer = SummaryAnalyzer(self.behavioral_groups_mapping)

            summary_df = analyzer.create_group_summary(df)
            summary_df.to_excel(writer, sheet_name='Group_Summary', index=False)

            employee_summary = analyzer.create_employee_summary(df)
            employee_summary_export = self._remove_behavioral_group_column(employee_summary)
            employee_summary_export.to_excel(writer, sheet_name='Employee_Summary', index=False)

            daily_summary = analyzer.create_daily_summary(df)
            daily_summary.to_excel(writer, sheet_name='Daily_Summary', index=False)

        print(f"Dataset exported to {excel_filename} with multiple sheets")
        return excel_filename
