import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict


class BaseAnalyzer:
    """Base class for data analysis with common utilities"""
    
    def __init__(self, behavioral_groups_mapping: Optional[Dict[str, str]] = None):
        """
        Initialize the BaseAnalyzer
        
        Args:
            behavioral_groups_mapping: Optional mapping of behavioral group codes to names
        """
        self.behavioral_groups_mapping = behavioral_groups_mapping or {}
        self.reverse_mapping = {v: k for k, v in self.behavioral_groups_mapping.items()}
        
        # Default behavioral group names if mapping is not provided
        self.default_group_names = {
            0: "Standard Employee",
            1: "High Activity Employee", 
            2: "Suspicious Activity Employee",
            3: "Travel-Heavy Employee",
            4: "After-Hours Worker",
            5: "Multi-Campus Employee",
            6: "Security-Risk Employee",
            7: "Malicious Insider"
        }
    
    def _get_group_name(self, group_code: int) -> str:
        """Get human-readable name for behavioral group"""
        if self.behavioral_groups_mapping:
            return self.reverse_mapping.get(group_code, f"Group_{group_code}")
        return self.default_group_names.get(group_code, f"Group_{group_code}")
    
    def _generate_basic_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate basic dataset statistics"""
        stats = {
            'total_records': len(df),
            'total_employees': df['employee_id'].nunique(),
            'date_range': {
                'start': df['date'].min(),
                'end': df['date'].max(),
                'days': (pd.to_datetime(df['date'].max()) - pd.to_datetime(df['date'].min())).days + 1
            },
            'malicious_stats': {
                'total_malicious_employees': df[df['is_malicious'] == 1]['employee_id'].nunique(),
                'total_malicious_records': df['is_malicious'].sum(),
                'malicious_ratio': df['is_malicious'].mean()
            }
        }
        
        # Department distribution
        if 'employee_department' in df.columns:
            stats['department_distribution'] = df.groupby('employee_department')['employee_id'].nunique().to_dict()
        
        # Campus distribution
        if 'employee_campus' in df.columns:
            stats['campus_distribution'] = df.groupby('employee_campus')['employee_id'].nunique().to_dict()
        
        # Behavioral group distribution
        if 'behavioral_group' in df.columns:
            stats['behavioral_group_distribution'] = df.groupby('behavioral_group')['employee_id'].nunique().to_dict()
        
        return stats
    
    def _generate_data_quality_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data quality and consistency"""
        quality = {}
        
        # Missing value analysis
        quality['missing_values'] = df.isnull().sum().to_dict()
        
        # Logical consistency checks
        consistency_checks = {}
        
        # Check abroad employees with building access
        if 'is_abroad' in df.columns and 'num_entries' in df.columns:
            abroad_data = df[df['is_abroad'] == 1]
            if len(abroad_data) > 0:
                consistency_checks['abroad_with_access'] = {
                    'total_abroad_records': len(abroad_data),
                    'abroad_with_building_access': (abroad_data['num_entries'] > 0).sum(),
                    'suspicious_abroad_access_ratio': (abroad_data['num_entries'] > 0).mean()
                }
        
        # Check off-hours activity ratios
        total_activities = {}
        if 'num_print_commands' in df.columns:
            total_activities['print_commands'] = df['num_print_commands'].sum()
        if 'num_burn_requests' in df.columns:
            total_activities['burn_requests'] = df['num_burn_requests'].sum()
        if 'num_print_commands_off_hours' in df.columns:
            total_activities['off_hours_print'] = df['num_print_commands_off_hours'].sum()
        if 'num_burn_requests_off_hours' in df.columns:
            total_activities['off_hours_burn'] = df['num_burn_requests_off_hours'].sum()
        
        if total_activities:
            consistency_checks['off_hours_ratios'] = {
                'print_off_hours_ratio': (total_activities.get('off_hours_print', 0) / 
                                        max(total_activities.get('print_commands', 1), 1)),
                'burn_off_hours_ratio': (total_activities.get('off_hours_burn', 0) / 
                                       max(total_activities.get('burn_requests', 1), 1))
            }
        
        # Check classification levels
        classification_checks = {}
        if 'employee_classification' in df.columns:
            classification_checks['avg_employee_classification'] = df['employee_classification'].mean()
        if 'avg_request_classification' in df.columns:
            classification_checks['avg_burn_classification'] = df[df['num_burn_requests'] > 0]['avg_request_classification'].mean()
        
        consistency_checks['classification_levels'] = classification_checks
        quality['consistency_checks'] = consistency_checks
        
        return quality
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Run comprehensive data validation checks"""
        validation_results = {}
        
        # Check for required columns
        required_columns = ['employee_id', 'date', 'is_malicious']
        missing_columns = [col for col in required_columns if col not in df.columns]
        validation_results['missing_required_columns'] = missing_columns
        
        # Check data types
        validation_results['data_types'] = df.dtypes.to_dict()
        
        # Check for duplicates
        validation_results['duplicate_records'] = df.duplicated().sum()
        
        # Check date range consistency
        if 'date' in df.columns:
            try:
                dates = pd.to_datetime(df['date'])
                validation_results['date_range_valid'] = True
                validation_results['date_range'] = {
                    'min': dates.min(),
                    'max': dates.max(),
                    'gaps': len(pd.date_range(dates.min(), dates.max())) - dates.nunique()
                }
            except:
                validation_results['date_range_valid'] = False
        
        # Check employee ID consistency
        if 'employee_id' in df.columns:
            validation_results['employee_id_stats'] = {
                'unique_employees': df['employee_id'].nunique(),
                'records_per_employee': df.groupby('employee_id').size().describe().to_dict()
            }
        
        return validation_results