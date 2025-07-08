"""
Data Quality Validator for Insider Threat Dataset
מאמת איכות נתונים עבור נתוני איומים פנימיים
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

class DataQualityValidator:
    """מאמת איכות נתונים מתקדם"""
    
    def __init__(self):
        self.validation_results = {}
        self.critical_issues = []
        self.warnings = []
        
    def validate_data_completeness(self, df: pd.DataFrame) -> Dict:
        """בדיקת שלמות הנתונים"""
        completeness_report = {}
        
        # בדיקת ערכים חסרים
        missing_counts = df.isnull().sum()
        missing_percentages = (missing_counts / len(df)) * 100
        
        completeness_report['missing_values'] = {
            'counts': missing_counts.to_dict(),
            'percentages': missing_percentages.to_dict(),
            'columns_with_missing': missing_counts[missing_counts > 0].index.tolist()
        }
        
        # בדיקת עמודות ריקות לחלוטין
        empty_columns = df.columns[df.isnull().all()].tolist()
        if empty_columns:
            completeness_report['empty_columns'] = empty_columns
            self.critical_issues.append(f"Found completely empty columns: {empty_columns}")
        
        # בדיקת שורות ריקות לחלוטין
        empty_rows = df.index[df.isnull().all(axis=1)].tolist()
        if empty_rows:
            completeness_report['empty_rows'] = len(empty_rows)
            self.critical_issues.append(f"Found {len(empty_rows)} completely empty rows")
        
        return completeness_report
    
    def validate_data_consistency(self, df: pd.DataFrame) -> Dict:
        """בדיקת עקביות הנתונים"""
        consistency_report = {}
        
        # בדיקת עקביות לוגית
        logical_issues = []
        
        # בדיקה: מספר הדפסות צריך להיות >= מספר הדפסות בצבע + שחור-לבן
        if all(col in df.columns for col in ['total_printed_pages', 'num_color_prints', 'num_bw_prints']):
            inconsistent_prints = df[
                df['total_printed_pages'] < (df['num_color_prints'] + df['num_bw_prints'])
            ]
            if len(inconsistent_prints) > 0:
                logical_issues.append(f"Found {len(inconsistent_prints)} rows with inconsistent print counts")
        
        # בדיקה: מספר כניסות צריך להיות >= מספר יציאות או שווה
        if all(col in df.columns for col in ['num_entries', 'num_exits']):
            inconsistent_entries = df[df['num_entries'] < df['num_exits']]
            if len(inconsistent_entries) > 0:
                logical_issues.append(f"Found {len(inconsistent_entries)} rows where exits > entries")
        
        # בדיקה: זמן נוכחות צריך להיות הגיוני
        if 'total_presence_minutes' in df.columns:
            unrealistic_presence = df[
                (df['total_presence_minutes'] > 24 * 60) |  # יותר מ-24 שעות
                (df['total_presence_minutes'] < 0)  # שלילי
            ]
            if len(unrealistic_presence) > 0:
                logical_issues.append(f"Found {len(unrealistic_presence)} rows with unrealistic presence time")
        
        # בדיקה: יחס הדפסות צבע צריך להיות בין 0 ל-1
        if 'ratio_color_prints' in df.columns:
            invalid_ratios = df[
                (df['ratio_color_prints'] < 0) | (df['ratio_color_prints'] > 1)
            ]
            if len(invalid_ratios) > 0:
                logical_issues.append(f"Found {len(invalid_ratios)} rows with invalid color print ratios")
        
        consistency_report['logical_issues'] = logical_issues
        
        return consistency_report
    
    def validate_data_types(self, df: pd.DataFrame) -> Dict:
        """בדיקת סוגי נתונים"""
        dtype_report = {}
        
        # בדיקת סוגי נתונים צפויים
        expected_types = {
            'employee_id': 'int64',
            'date': 'datetime64[ns]',
            'employee_seniority_years': 'int64',
            'is_contractor': 'int64',
            'is_malicious': 'int64',
            'num_print_commands': 'int64',
            'total_printed_pages': 'int64',
            'ratio_color_prints': 'float64'
        }
        
        type_mismatches = []
        for col, expected_type in expected_types.items():
            if col in df.columns:
                actual_type = str(df[col].dtype)
                if actual_type != expected_type and not (
                    expected_type == 'datetime64[ns]' and 'datetime' in actual_type
                ):
                    type_mismatches.append({
                        'column': col,
                        'expected': expected_type,
                        'actual': actual_type
                    })
        
        dtype_report['type_mismatches'] = type_mismatches
        
        # בדיקת ערכים לא חוקיים בעמודות בינאריות
        binary_columns = [
            'is_contractor', 'has_foreign_citizenship', 'has_criminal_record',
            'has_medical_history', 'is_malicious', 'printed_from_other',
            'burned_from_other', 'is_abroad'
        ]
        
        invalid_binary_values = {}
        for col in binary_columns:
            if col in df.columns:
                unique_values = df[col].dropna().unique()
                invalid_values = [v for v in unique_values if v not in [0, 1]]
                if invalid_values:
                    invalid_binary_values[col] = invalid_values
        
        dtype_report['invalid_binary_values'] = invalid_binary_values
        
        return dtype_report
    
    def validate_data_ranges(self, df: pd.DataFrame) -> Dict:
        """בדיקת טווחי נתונים"""
        range_report = {}
        
        # בדיקת ערכים שליליים בעמודות שצריכות להיות חיוביות
        positive_columns = [
            'employee_seniority_years', 'num_print_commands', 'total_printed_pages',
            'num_burn_requests', 'total_burn_volume_mb', 'total_files_burned',
            'num_entries', 'num_exits', 'total_presence_minutes'
        ]
        
        negative_value_issues = {}
        for col in positive_columns:
            if col in df.columns:
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    negative_value_issues[col] = negative_count
        
        range_report['negative_value_issues'] = negative_value_issues
        
        # בדיקת ערכים קיצוניים
        extreme_values = {}
        for col in df.select_dtypes(include=[np.number]).columns:
            if col in df.columns:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 3 * iqr
                upper_bound = q3 + 3 * iqr
                
                extreme_low = (df[col] < lower_bound).sum()
                extreme_high = (df[col] > upper_bound).sum()
                
                if extreme_low > 0 or extreme_high > 0:
                    extreme_values[col] = {
                        'extreme_low_count': extreme_low,
                        'extreme_high_count': extreme_high,
                        'bounds': (lower_bound, upper_bound)
                    }
        
        range_report['extreme_values'] = extreme_values
        
        return range_report
    
    def validate_duplicates(self, df: pd.DataFrame) -> Dict:
        """בדיקת כפילויות"""
        duplicate_report = {}
        
        # בדיקת שורות כפולות
        duplicate_rows = df.duplicated().sum()
        duplicate_report['duplicate_rows'] = duplicate_rows
        
        # בדיקת כפילויות לפי employee_id ותאריך
        if all(col in df.columns for col in ['employee_id', 'date']):
            duplicate_employee_date = df.duplicated(subset=['employee_id', 'date']).sum()
            duplicate_report['duplicate_employee_date'] = duplicate_employee_date
        
        # בדיקת כפילויות לפי employee_id בלבד
        if 'employee_id' in df.columns:
            duplicate_employee_id = df.duplicated(subset=['employee_id']).sum()
            duplicate_report['duplicate_employee_id'] = duplicate_employee_id
        
        return duplicate_report
    
    def validate_categorical_data(self, df: pd.DataFrame) -> Dict:
        """בדיקת נתונים קטגוריים"""
        categorical_report = {}
        
        categorical_columns = df.select_dtypes(include=['object']).columns
        
        for col in categorical_columns:
            col_report = {}
            
            # מספר קטגוריות יניקות
            unique_count = df[col].nunique()
            col_report['unique_count'] = unique_count
            
            # קטגוריות עם תדירות נמוכה
            value_counts = df[col].value_counts()
            rare_categories = value_counts[value_counts < 5].index.tolist()
            col_report['rare_categories'] = rare_categories
            
            # קטגוריות עם תדירות גבוהה מאוד
            dominant_categories = value_counts[value_counts > len(df) * 0.95].index.tolist()
            col_report['dominant_categories'] = dominant_categories
            
            # בדיקת אורך מחרוזות חריג
            if df[col].dtype == 'object':
                string_lengths = df[col].astype(str).str.len()
                unusual_lengths = string_lengths[
                    (string_lengths > string_lengths.quantile(0.99)) |
                    (string_lengths < string_lengths.quantile(0.01))
                ]
                col_report['unusual_length_count'] = len(unusual_lengths)
            
            categorical_report[col] = col_report
        
        return categorical_report
    
    def generate_quality_score(self, df: pd.DataFrame) -> Dict:
        """חישוב ציון איכות כולל"""
        total_issues = 0
        max_possible_issues = 0
        
        # ספירת בעיות מכל הבדיקות
        completeness = self.validate_data_completeness(df)
        consistency = self.validate_data_consistency(df)
        dtypes = self.validate_data_types(df)
        ranges = self.validate_data_ranges(df)
        duplicates = self.validate_duplicates(df)
        
        # חישוב ציון איכות (0-100)
        missing_percentage = sum(completeness['missing_values']['percentages'].values())
        consistency_issues = len(consistency['logical_issues'])
        type_issues = len(dtypes['type_mismatches'])
        range_issues = len(ranges['negative_value_issues'])
        duplicate_issues = duplicates['duplicate_rows']
        
        # נוסחת ציון איכות
        quality_score = max(0, 100 - (
            missing_percentage * 0.5 +
            consistency_issues * 5 +
            type_issues * 3 +
            range_issues * 2 +
            duplicate_issues * 0.01
        ))
        
        return {
            'overall_quality_score': round(quality_score, 2),
            'missing_data_impact': round(missing_percentage, 2),
            'consistency_issues': consistency_issues,
            'type_issues': type_issues,
            'range_issues': range_issues,
            'duplicate_issues': duplicate_issues,
            'quality_level': (
                'Excellent' if quality_score >= 90 else
                'Good' if quality_score >= 75 else
                'Fair' if quality_score >= 50 else
                'Poor'
            )
        }
    
    def run_full_validation(self, df: pd.DataFrame) -> Dict:
        """הרצת בדיקת איכות מלאה"""
        print("Running comprehensive data quality validation...")
        
        validation_results = {}
        
        print("1. Validating data completeness...")
        validation_results['completeness'] = self.validate_data_completeness(df)
        
        print("2. Validating data consistency...")
        validation_results['consistency'] = self.validate_data_consistency(df)
        
        print("3. Validating data types...")
        validation_results['data_types'] = self.validate_data_types(df)
        
        print("4. Validating data ranges...")
        validation_results['ranges'] = self.validate_data_ranges(df)
        
        print("5. Validating duplicates...")
        validation_results['duplicates'] = self.validate_duplicates(df)
        
        print("6. Validating categorical data...")
        validation_results['categorical'] = self.validate_categorical_data(df)
        
        print("7. Generating quality score...")
        validation_results['quality_score'] = self.generate_quality_score(df)
        
        self.validation_results = validation_results
        
        print("Data quality validation completed!")
        print(f"Overall Quality Score: {validation_results['quality_score']['overall_quality_score']}")
        print(f"Quality Level: {validation_results['quality_score']['quality_level']}")
        
        return validation_results
    
    def get_recommendations(self) -> List[str]:
        """קבלת המלצות לשיפור איכות הנתונים"""
        recommendations = []
        
        if self.validation_results:
            # המלצות בהתבסס על תוצאות הבדיקה
            quality_score = self.validation_results.get('quality_score', {})
            
            if quality_score.get('missing_data_impact', 0) > 10:
                recommendations.append("Consider imputation strategies for missing values")
            
            if quality_score.get('consistency_issues', 0) > 0:
                recommendations.append("Address logical inconsistencies in the data")
            
            if quality_score.get('type_issues', 0) > 0:
                recommendations.append("Convert columns to appropriate data types")
            
            if quality_score.get('duplicate_issues', 0) > 100:
                recommendations.append("Remove or investigate duplicate records")
            
            if quality_score.get('overall_quality_score', 100) < 75:
                recommendations.append("Comprehensive data cleaning is recommended")
        
        return recommendations