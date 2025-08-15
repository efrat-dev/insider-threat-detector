#!/usr/bin/env python3
"""
Employee Data Mapper
Extracts and maps employee data from insider_threat_dataset1.csv.
Can be used standalone or as part of preprocessing pipeline.
"""

import pandas as pd
import sys
import os


class EmployeeDataMapper:
    """Maps and extracts unique employee data from insider threat dataset."""
    
    def __init__(self, skip_rows=180):
        """
        Initialize mapper.
        
        Args:
            skip_rows (int): Number of rows to skip per employee (default: 180)
        """
        self.skip_rows = skip_rows
        self.required_columns = ['employee_id', 'employee_department', 'employee_position']
    
    def extract_employee_data(self, input_file):
        """
        Extract unique employee data from CSV file.
        
        Args:
            input_file (str): Path to input CSV file
            
        Returns:
            pd.DataFrame: DataFrame with unique employee records
            
        Raises:
            ValueError: If required columns not found
        """
        df = pd.read_csv(input_file)
        
        # Map actual column names to standardized names (case-insensitive)
        column_mapping = {}
        for req_col in self.required_columns:
            found = False
            for actual_col in df.columns:
                if actual_col.lower().strip() == req_col:
                    column_mapping[actual_col] = req_col
                    found = True
                    break
            
            if not found:
                raise ValueError(f"Required column '{req_col}' not found in CSV file.")
        
        selected_columns = list(column_mapping.keys())
        result_df = df[selected_columns].copy()
        result_df = result_df.rename(columns=column_mapping)
        
        for req_col in self.required_columns:
            if req_col not in result_df.columns:
                result_df[req_col] = "N/A"
        
        result_df = result_df[self.required_columns]
        result_df = result_df.fillna("N/A")
        result_df = result_df.dropna(how='all')
        
        try:
            result_df['employee_id'] = pd.to_numeric(result_df['employee_id'], errors='coerce')
            result_df['employee_id'] = result_df['employee_id'].fillna(0).astype(int)
        except:
            pass
        
        # Take every skip_rows-th row (first record of each employee)
        result_df = result_df.iloc[::self.skip_rows]
        result_df = result_df.reset_index(drop=True)
        
        return result_df
    
    def save_to_csv(self, df, output_file):
        """Save DataFrame to CSV file."""
        df.to_csv(output_file, index=False, encoding='utf-8')


def process_employee_data(input_file):
    """Process CSV and return filtered DataFrame with unique employees."""
    mapper = EmployeeDataMapper()
    return mapper.extract_employee_data(input_file)


def save_to_csv(df, output_file):
    """Save DataFrame to CSV file."""
    df.to_csv(output_file, index=False, encoding='utf-8')


def main():
    input_file = "insider_threat_dataset1.csv"
    output_file = "employee_data.csv"
    
    try:
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found in current directory.")
            print("Please make sure the file exists in the same directory as this script.")
            return 1
        
        result_df = process_employee_data(input_file)
        save_to_csv(result_df, output_file)
        
        print(f"CSV file created: {output_file} ({len(result_df)} employees)")
        return 0
        
    except ValueError as e:
        print(f"Error: {str(e)}")
        return 1
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return 1
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{input_file}' is empty.")
        return 1
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)