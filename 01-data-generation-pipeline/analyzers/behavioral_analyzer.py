import pandas as pd
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer

class BehavioralAnalyzer(BaseAnalyzer):
    """Specialized analyzer for behavioral group analysis"""
    
    def _generate_behavioral_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate detailed behavioral group analysis"""
        analysis = {}
        
        if 'behavioral_group' not in df.columns:
            analysis['error'] = "No behavioral_group column found in dataset"
            return analysis
        
        for group in sorted(df['behavioral_group'].unique()):
            group_data = df[df['behavioral_group'] == group]
            group_name = self._get_group_name(group)
            
            # Basic group stats
            group_stats = {
                'group_name': group_name,
                'total_employees': group_data['employee_id'].nunique(),
                'total_records': len(group_data),
                'malicious_employees': group_data[group_data['is_malicious'] == 1]['employee_id'].nunique(),
                'malicious_ratio': group_data['is_malicious'].mean()
            }
            
            # Work patterns
            group_stats['work_patterns'] = self._analyze_work_patterns(group_data)
            
            # Printing patterns
            group_stats['printing_patterns'] = self._analyze_printing_patterns(group_data)
            
            # Burning patterns
            group_stats['burning_patterns'] = self._analyze_burning_patterns(group_data)
            
            # Travel patterns
            group_stats['travel_patterns'] = self._analyze_travel_patterns(group_data)
            
            analysis[group] = group_stats
        
        return analysis
    
    def _analyze_work_patterns(self, group_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze work patterns for a behavioral group"""
        if 'first_entry_time' not in group_data.columns:
            return {'error': 'No work time data available'}
        
        work_data = group_data[group_data['first_entry_time'].notna()]
        if len(work_data) == 0:
            return {'error': 'No valid work time data'}
        
        try:
            entry_times = pd.to_datetime(work_data['first_entry_time'], format='%H:%M', errors='coerce').dt.hour
            exit_times = pd.to_datetime(work_data['last_exit_time'], format='%H:%M', errors='coerce').dt.hour
            
            return {
                'avg_entry_time': entry_times.mean() if not entry_times.isna().all() else 0,
                'avg_exit_time': exit_times.mean() if not exit_times.isna().all() else 0,
                'early_entry_rate': work_data.get('early_entry_flag', pd.Series([0])).mean(),
                'late_exit_rate': work_data.get('late_exit_flag', pd.Series([0])).mean(),
                'weekend_work_rate': work_data.get('entry_during_weekend', pd.Series([0])).mean(),
                'night_entry_rate': work_data.get('entered_during_night_hours', pd.Series([0])).mean()
            }
        except Exception as e:
            return {'error': f"Error processing work patterns: {str(e)}"}
    
    def _analyze_printing_patterns(self, group_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze printing patterns for a behavioral group"""
        if 'total_printed_pages' not in group_data.columns:
            return {'error': 'No printing data available'}
        
        print_data = group_data[group_data['total_printed_pages'] > 0]
        if len(print_data) == 0:
            return {'error': 'No printing activity found'}
        
        return {
            'printing_frequency': len(print_data) / len(group_data),
            'avg_pages_per_print_day': print_data['total_printed_pages'].mean(),
            'avg_commands_per_print_day': print_data.get('num_print_commands', pd.Series([0])).mean(),
            'color_print_ratio': print_data.get('ratio_color_prints', pd.Series([0])).mean(),
            'off_hours_print_ratio': (print_data.get('num_print_commands_off_hours', pd.Series([0])).sum() / 
                                    max(print_data.get('num_print_commands', pd.Series([1])).sum(), 1)),
            'multi_campus_print_rate': print_data.get('printed_from_other', pd.Series([0])).mean()
        }
    
    def _analyze_burning_patterns(self, group_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze burning patterns for a behavioral group"""
        if 'num_burn_requests' not in group_data.columns:
            return {'error': 'No burning data available'}
        
        burn_data = group_data[group_data['num_burn_requests'] > 0]
        if len(burn_data) == 0:
            return {'error': 'No burning activity found'}
        
        return {
            'burning_frequency': len(burn_data) / len(group_data),
            'avg_requests_per_burn_day': burn_data['num_burn_requests'].mean(),
            'avg_classification_level': burn_data.get('avg_request_classification', pd.Series([0])).mean(),
            'max_classification_level': burn_data.get('max_request_classification', pd.Series([0])).mean(),
            'avg_volume_mb': burn_data.get('total_burn_volume_mb', pd.Series([0])).mean(),
            'avg_files_per_burn': burn_data.get('total_files_burned', pd.Series([0])).mean(),
            'off_hours_burn_ratio': (burn_data.get('num_burn_requests_off_hours', pd.Series([0])).sum() / 
                                   max(burn_data.get('num_burn_requests', pd.Series([1])).sum(), 1)),
            'multi_campus_burn_rate': burn_data.get('burned_from_other', pd.Series([0])).mean()
        }
    
    def _analyze_travel_patterns(self, group_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze travel patterns for a behavioral group"""
        if 'is_abroad' not in group_data.columns:
            return {'error': 'No travel data available'}
        
        travel_data = group_data[group_data['is_abroad'] == 1]
        if len(travel_data) == 0:
            return {'error': 'No travel activity found'}
        
        return {
            'travel_frequency': len(travel_data) / len(group_data),
            'official_travel_ratio': travel_data.get('is_official_trip', pd.Series([0])).mean(),
            'hostile_country_visit_ratio': travel_data.get('is_hostile_country_trip', pd.Series([0])).mean(),
            'origin_country_visit_ratio': travel_data.get('is_origin_country_trip', pd.Series([0])).mean(),
            'avg_trip_duration': travel_data.groupby('employee_id')['trip_day_number'].max().mean() if 'trip_day_number' in travel_data.columns else 0
        }