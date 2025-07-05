import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict


class DataAnalyzer:
    """Comprehensive analysis of the generated insider threat dataset"""
    
    def __init__(self, behavioral_groups_mapping: Optional[Dict[str, str]] = None):
        """
        Initialize the DataAnalyzer
        
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
    
    def generate_comprehensive_analysis(self, df: pd.DataFrame, 
                                      malicious_employee_ids: Optional[set] = None) -> Dict[str, Any]:
        """Generate comprehensive analysis of the dataset"""
        analysis = {}
        
        # Basic statistics
        analysis['basic_stats'] = self._generate_basic_statistics(df)
        
        # Behavioral group analysis
        analysis['behavioral_analysis'] = self._generate_behavioral_analysis(df)
        
        # Malicious vs Normal comparison
        analysis['malicious_analysis'] = self._generate_malicious_analysis(df)
        
        # Activity pattern analysis
        analysis['activity_patterns'] = self._generate_activity_patterns(df)
        
        # Data quality analysis
        analysis['data_quality'] = self._generate_data_quality_analysis(df)
        
        # Temporal analysis
        analysis['temporal_analysis'] = self._generate_temporal_analysis(df)
        
        return analysis
    
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
            if 'first_entry_time' in group_data.columns:
                work_data = group_data[group_data['first_entry_time'].notna()]
                if len(work_data) > 0:
                    try:
                        entry_times = pd.to_datetime(work_data['first_entry_time'], format='%H:%M', errors='coerce').dt.hour
                        exit_times = pd.to_datetime(work_data['last_exit_time'], format='%H:%M', errors='coerce').dt.hour
                        
                        group_stats['work_patterns'] = {
                            'avg_entry_time': entry_times.mean() if not entry_times.isna().all() else 0,
                            'avg_exit_time': exit_times.mean() if not exit_times.isna().all() else 0,
                            'early_entry_rate': work_data.get('early_entry_flag', pd.Series([0])).mean(),
                            'late_exit_rate': work_data.get('late_exit_flag', pd.Series([0])).mean(),
                            'weekend_work_rate': work_data.get('entry_during_weekend', pd.Series([0])).mean(),
                            'night_entry_rate': work_data.get('entered_during_night_hours', pd.Series([0])).mean()
                        }
                    except Exception as e:
                        group_stats['work_patterns'] = {'error': f"Error processing work patterns: {str(e)}"}
            
            # Printing patterns
            if 'total_printed_pages' in group_data.columns:
                print_data = group_data[group_data['total_printed_pages'] > 0]
                if len(print_data) > 0:
                    group_stats['printing_patterns'] = {
                        'printing_frequency': len(print_data) / len(group_data),
                        'avg_pages_per_print_day': print_data['total_printed_pages'].mean(),
                        'avg_commands_per_print_day': print_data.get('num_print_commands', pd.Series([0])).mean(),
                        'color_print_ratio': print_data.get('ratio_color_prints', pd.Series([0])).mean(),
                        'off_hours_print_ratio': (print_data.get('num_print_commands_off_hours', pd.Series([0])).sum() / 
                                                max(print_data.get('num_print_commands', pd.Series([1])).sum(), 1)),
                        'multi_campus_print_rate': print_data.get('printed_from_other', pd.Series([0])).mean()
                    }
            
            # Burning patterns
            if 'num_burn_requests' in group_data.columns:
                burn_data = group_data[group_data['num_burn_requests'] > 0]
                if len(burn_data) > 0:
                    group_stats['burning_patterns'] = {
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
            
            # Travel patterns
            if 'is_abroad' in group_data.columns:
                travel_data = group_data[group_data['is_abroad'] == 1]
                if len(travel_data) > 0:
                    group_stats['travel_patterns'] = {
                        'travel_frequency': len(travel_data) / len(group_data),
                        'official_travel_ratio': travel_data.get('is_official_trip', pd.Series([0])).mean(),
                        'hostile_country_visit_ratio': travel_data.get('is_hostile_country_trip', pd.Series([0])).mean(),
                        'origin_country_visit_ratio': travel_data.get('is_origin_country_trip', pd.Series([0])).mean(),
                        'avg_trip_duration': travel_data.groupby('employee_id')['trip_day_number'].max().mean() if 'trip_day_number' in travel_data.columns else 0
                    }
            
            analysis[group] = group_stats
        
        return analysis
    
    def _generate_malicious_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compare malicious vs normal employee behavior"""
        malicious_df = df[df['is_malicious'] == 1]
        normal_df = df[df['is_malicious'] == 0]
        
        analysis = {}
        
        # Activity level comparison
        activity_comparison = {}
        
        # Printing activity
        if 'total_printed_pages' in df.columns:
            activity_comparison['printing'] = {
                'malicious_print_freq': (malicious_df['total_printed_pages'] > 0).mean(),
                'normal_print_freq': (normal_df['total_printed_pages'] > 0).mean(),
                'malicious_avg_pages': malicious_df[malicious_df['total_printed_pages'] > 0]['total_printed_pages'].mean(),
                'normal_avg_pages': normal_df[normal_df['total_printed_pages'] > 0]['total_printed_pages'].mean(),
                'malicious_off_hours_ratio': (malicious_df.get('num_print_commands_off_hours', pd.Series([0])).sum() / 
                                            max(malicious_df.get('num_print_commands', pd.Series([1])).sum(), 1)),
                'normal_off_hours_ratio': (normal_df.get('num_print_commands_off_hours', pd.Series([0])).sum() / 
                                         max(normal_df.get('num_print_commands', pd.Series([1])).sum(), 1))
            }
        
        # Burning activity
        if 'num_burn_requests' in df.columns:
            activity_comparison['burning'] = {
                'malicious_burn_freq': (malicious_df['num_burn_requests'] > 0).mean(),
                'normal_burn_freq': (normal_df['num_burn_requests'] > 0).mean(),
                'malicious_avg_volume': malicious_df[malicious_df['num_burn_requests'] > 0].get('total_burn_volume_mb', pd.Series([0])).mean(),
                'normal_avg_volume': normal_df[normal_df['num_burn_requests'] > 0].get('total_burn_volume_mb', pd.Series([0])).mean(),
                'malicious_avg_classification': malicious_df[malicious_df['num_burn_requests'] > 0].get('avg_request_classification', pd.Series([0])).mean(),
                'normal_avg_classification': normal_df[normal_df['num_burn_requests'] > 0].get('avg_request_classification', pd.Series([0])).mean()
            }
        
        # Travel activity
        if 'is_abroad' in df.columns:
            activity_comparison['travel'] = {
                'malicious_travel_freq': (malicious_df['is_abroad'] == 1).mean(),
                'normal_travel_freq': (normal_df['is_abroad'] == 1).mean(),
                'malicious_hostile_country_ratio': malicious_df[malicious_df['is_abroad'] == 1].get('is_hostile_country_trip', pd.Series([0])).mean(),
                'normal_hostile_country_ratio': normal_df[normal_df['is_abroad'] == 1].get('is_hostile_country_trip', pd.Series([0])).mean()
            }
        
        # Work patterns
        if 'num_entries' in df.columns:
            malicious_work = malicious_df[malicious_df['num_entries'] > 0]
            normal_work = normal_df[normal_df['num_entries'] > 0]
            
            activity_comparison['work_patterns'] = {
                'malicious_weekend_work': malicious_work.get('entry_during_weekend', pd.Series([0])).mean(),
                'normal_weekend_work': normal_work.get('entry_during_weekend', pd.Series([0])).mean(),
                'malicious_night_entry': malicious_work.get('entered_during_night_hours', pd.Series([0])).mean(),
                'normal_night_entry': normal_work.get('entered_during_night_hours', pd.Series([0])).mean(),
                'malicious_multi_campus': malicious_work.get('num_unique_campus', pd.Series([0])).mean(),
                'normal_multi_campus': normal_work.get('num_unique_campus', pd.Series([0])).mean()
            }
        
        analysis['activity_comparison'] = activity_comparison
        
        # Risk indicators
        if 'risk_travel_indicator' in df.columns:
            analysis['risk_indicators'] = {
                'malicious_risk_travel': malicious_df['risk_travel_indicator'].mean(),
                'normal_risk_travel': normal_df['risk_travel_indicator'].mean(),
                'total_risk_travel_incidents': df['risk_travel_indicator'].sum()
            }
        
        return analysis
    
    def _generate_activity_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze activity patterns across the dataset"""
        patterns = {}
        
        # Daily activity distribution
        daily_activity = {}
        if 'num_entries' in df.columns:
            daily_activity['total_work_days'] = (df['num_entries'] > 0).sum()
        if 'total_printed_pages' in df.columns:
            daily_activity['total_print_days'] = (df['total_printed_pages'] > 0).sum()
        if 'num_burn_requests' in df.columns:
            daily_activity['total_burn_days'] = (df['num_burn_requests'] > 0).sum()
        if 'is_abroad' in df.columns:
            daily_activity['total_travel_days'] = (df['is_abroad'] == 1).sum()
        
        patterns['daily_activity'] = daily_activity
        
        # Weekly patterns
        try:
            df['weekday'] = pd.to_datetime(df['date']).dt.day_name()
            weekly_patterns = {}
            
            if 'num_entries' in df.columns:
                weekly_patterns['work_by_weekday'] = df[df['num_entries'] > 0]['weekday'].value_counts().to_dict()
            if 'total_printed_pages' in df.columns:
                weekly_patterns['print_by_weekday'] = df[df['total_printed_pages'] > 0]['weekday'].value_counts().to_dict()
            if 'num_burn_requests' in df.columns:
                weekly_patterns['burn_by_weekday'] = df[df['num_burn_requests'] > 0]['weekday'].value_counts().to_dict()
            
            patterns['weekly_patterns'] = weekly_patterns
        except Exception as e:
            patterns['weekly_patterns'] = {'error': f"Error processing weekly patterns: {str(e)}"}
        
        # Multi-campus activity
        multi_campus = {}
        if 'num_unique_campus' in df.columns:
            multi_campus['employees_using_multiple_campuses'] = df[df['num_unique_campus'] > 1]['employee_id'].nunique()
        if 'printed_from_other' in df.columns:
            multi_campus['print_from_other_campus'] = df['printed_from_other'].sum()
        if 'burned_from_other' in df.columns:
            multi_campus['burn_from_other_campus'] = df['burned_from_other'].sum()
        
        patterns['multi_campus'] = multi_campus
        
        return patterns
    
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
    
    def _generate_temporal_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze temporal patterns in the data"""
        temporal = {}
        
        try:
            # Monthly aggregation
            df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
            monthly_agg = {}
            
            if 'is_malicious' in df.columns:
                monthly_agg['is_malicious'] = df.groupby('month')['is_malicious'].sum().to_dict()
            if 'total_printed_pages' in df.columns:
                monthly_agg['total_printed_pages'] = df.groupby('month')['total_printed_pages'].sum().to_dict()
            if 'num_burn_requests' in df.columns:
                monthly_agg['num_burn_requests'] = df.groupby('month')['num_burn_requests'].sum().to_dict()
            if 'is_abroad' in df.columns:
                monthly_agg['is_abroad'] = df.groupby('month')['is_abroad'].sum().to_dict()
            
            monthly_agg['employee_id'] = df.groupby('month')['employee_id'].nunique().to_dict()
            
            temporal['monthly_trends'] = monthly_agg
            
            # Weekly aggregation
            df['week'] = pd.to_datetime(df['date']).dt.to_period('W')
            weekly_agg = {}
            
            if 'is_malicious' in df.columns:
                weekly_agg['is_malicious'] = df.groupby('week')['is_malicious'].sum().to_dict()
            if 'total_printed_pages' in df.columns:
                weekly_agg['total_printed_pages'] = df.groupby('week')['total_printed_pages'].sum().to_dict()
            if 'num_burn_requests' in df.columns:
                weekly_agg['num_burn_requests'] = df.groupby('week')['num_burn_requests'].sum().to_dict()
            if 'is_abroad' in df.columns:
                weekly_agg['is_abroad'] = df.groupby('week')['is_abroad'].sum().to_dict()
            
            temporal['weekly_trends'] = weekly_agg
            
        except Exception as e:
            temporal['error'] = f"Error processing temporal analysis: {str(e)}"
        
        return temporal
    
    def generate_summary_statistics(self, df: pd.DataFrame):
        """Generate and print summary statistics"""
        analysis = self.generate_comprehensive_analysis(df)
        self.print_analysis_summary(analysis)
        return analysis
    
    def print_analysis_summary(self, analysis: Dict[str, Any]):
        """Print a comprehensive analysis summary"""
        print("\n=== COMPREHENSIVE DATASET ANALYSIS ===")
        
        # Basic statistics
        basic = analysis['basic_stats']
        print(f"\n--- Basic Statistics ---")
        print(f"Total Records: {basic['total_records']:,}")
        print(f"Total Employees: {basic['total_employees']:,}")
        print(f"Date Range: {basic['date_range']['start']} to {basic['date_range']['end']}")
        print(f"Malicious Employees: {basic['malicious_stats']['total_malicious_employees']}")
        print(f"Malicious Records: {basic['malicious_stats']['total_malicious_records']:,} ({basic['malicious_stats']['malicious_ratio']:.1%})")
        
        # Department distribution
        if 'department_distribution' in basic:
            print(f"\n--- Department Distribution ---")
            for dept, count in sorted(basic['department_distribution'].items()):
                print(f"  {dept}: {count} employees")
        
        # Behavioral group analysis
        if 'behavioral_analysis' in analysis and 'error' not in analysis['behavioral_analysis']:
            print(f"\n--- Behavioral Group Analysis ---")
            for group, stats in analysis['behavioral_analysis'].items():
                print(f"\nGroup {group} - {stats['group_name']}:")
                print(f"  Employees: {stats['total_employees']}")
                print(f"  Malicious: {stats['malicious_employees']} ({stats['malicious_ratio']:.1%})")
                
                if 'work_patterns' in stats and 'error' not in stats['work_patterns']:
                    wp = stats['work_patterns']
                    print(f"  Work: {wp['avg_entry_time']:.1f}:00 - {wp['avg_exit_time']:.1f}:00")
                    print(f"  Off-hours: {wp['early_entry_rate']:.1%} early, {wp['late_exit_rate']:.1%} late")
                    print(f"  Weekend work: {wp['weekend_work_rate']:.1%}")
                
                if 'printing_patterns' in stats:
                    pp = stats['printing_patterns']
                    print(f"  Printing: {pp['printing_frequency']:.1%} frequency, {pp['avg_pages_per_print_day']:.1f} pages/day")
                
                if 'burning_patterns' in stats:
                    bp = stats['burning_patterns']
                    print(f"  Burning: {bp['burning_frequency']:.1%} frequency, {bp['avg_volume_mb']:.0f} MB/day")
        
        # Malicious vs Normal comparison
        if 'malicious_analysis' in analysis:
            print(f"\n--- Malicious vs Normal Comparison ---")
            malicious = analysis['malicious_analysis']
            
            if 'activity_comparison' in malicious:
                ac = malicious['activity_comparison']
                
                if 'printing' in ac:
                    print("Printing Activity:")
                    print(f"  Malicious: {ac['printing']['malicious_print_freq']:.1%} frequency")
                    print(f"  Normal: {ac['printing']['normal_print_freq']:.1%} frequency")
                
                if 'burning' in ac:
                    print("Burning Activity:")
                    print(f"  Malicious: {ac['burning']['malicious_burn_freq']:.1%} frequency")
                    print(f"  Normal: {ac['burning']['normal_burn_freq']:.1%} frequency")
                
                if 'travel' in ac:
                    print("Travel Activity:")
                    print(f"  Malicious: {ac['travel']['malicious_travel_freq']:.1%} frequency")
                    print(f"  Normal: {ac['travel']['normal_travel_freq']:.1%} frequency")
        
        # Data quality
        if 'data_quality' in analysis:
            print(f"\n--- Data Quality ---")
            quality = analysis['data_quality']
            missing = quality['missing_values']
            if any(v > 0 for v in missing.values()):
                print("Missing values:")
                for col, count in missing.items():
                    if count > 0:
                        print(f"  {col}: {count}")
            else:
                print("No missing values detected")
            
            # Risk indicators
            if 'malicious_analysis' in analysis and 'risk_indicators' in analysis['malicious_analysis']:
                risk = analysis['malicious_analysis']['risk_indicators']
                print(f"Risk Travel Incidents: {risk.get('total_risk_travel_incidents', 0)}")
    
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
    
    def export_analysis_results(self, df: pd.DataFrame, output_file: str):
        """Export analysis results to Excel file"""
        try:
            analysis = self.generate_comprehensive_analysis(df)
            
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Basic statistics
                basic_stats_df = pd.DataFrame([analysis['basic_stats']])
                basic_stats_df.to_excel(writer, sheet_name='Basic_Statistics', index=False)
                
                # Behavioral analysis
                if 'behavioral_analysis' in analysis and 'error' not in analysis['behavioral_analysis']:
                    behavioral_data = []
                    for group, stats in analysis['behavioral_analysis'].items():
                        row = {'group': group, 'group_name': stats['group_name']}
                        row.update(stats)
                        behavioral_data.append(row)
                    
                    behavioral_df = pd.DataFrame(behavioral_data)
                    behavioral_df.to_excel(writer, sheet_name='Behavioral_Analysis', index=False)
                
                # Activity patterns
                if 'activity_patterns' in analysis:
                    activity_df = pd.DataFrame([analysis['activity_patterns']['daily_activity']])
                    activity_df.to_excel(writer, sheet_name='Activity_Patterns', index=False)
                
                # Data quality
                if 'data_quality' in analysis:
                    quality_df = pd.DataFrame([analysis['data_quality']['missing_values']])
                    quality_df.to_excel(writer, sheet_name='Data_Quality', index=False)
            
            print(f"Analysis results exported to {output_file}")
            
        except Exception as e:
            print(f"Error exporting analysis results: {str(e)}")