import pandas as pd
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer


class SecurityAnalyzer(BaseAnalyzer):
    """
    Specialized analyzer for security and malicious behavior detection.
    
    Provides metrics and comparative analysis between malicious and normal employees,
    risk assessments, anomaly detection, and identification of suspicious activity patterns.
    """
    
    def analyze_security_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Main method to run comprehensive security-related analyses on the dataset.
        
        Returns a dictionary including:
        - Basic security metrics
        - Malicious vs normal behavior analysis
        - Risk assessment results
        - Detected security anomalies
        """
        analysis = {}
        analysis['basic_security_metrics'] = self._generate_basic_security_metrics(df)
        analysis['malicious_behavior'] = self._generate_malicious_analysis(df)
        analysis['risk_assessment'] = self._generate_risk_assessment(df)
        analysis['anomalies'] = self._detect_security_anomalies(df)
        return analysis
    
    def _generate_basic_security_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate basic security metrics, such as total and malicious employees,
        high-risk travel incidents, and counts of security-sensitive activities.
        """
        metrics = {}
        if 'is_malicious' in df.columns:
            metrics['total_employees'] = len(df)
            metrics['malicious_employees'] = df['is_malicious'].sum()
            metrics['malicious_percentage'] = (metrics['malicious_employees'] / len(df)) * 100
        
        if 'risk_travel_indicator' in df.columns:
            metrics['high_risk_travel_incidents'] = df['risk_travel_indicator'].sum()
        
        security_columns = ['num_print_commands_off_hours', 'num_burn_requests', 'is_hostile_country_trip']
        for col in security_columns:
            if col in df.columns:
                metrics[f'{col}_total'] = df[col].sum()
                metrics[f'{col}_employees_involved'] = (df[col] > 0).sum()
        
        return metrics
    
    def _generate_malicious_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Compare behavioral differences between malicious and normal employees.
        
        Returns metrics on printing, burning, travel, work patterns,
        and risk indicator comparisons.
        """
        if 'is_malicious' not in df.columns:
            return {'error': 'Missing malicious indicator column'}
        
        malicious_df = df[df['is_malicious'] == 1]
        normal_df = df[df['is_malicious'] == 0]
        
        analysis = {
            'activity_comparison': {
                'printing': self._compare_printing_activity(malicious_df, normal_df),
                'burning': self._compare_burning_activity(malicious_df, normal_df),
                'travel': self._compare_travel_activity(malicious_df, normal_df),
                'work_patterns': self._compare_work_patterns(malicious_df, normal_df)
            },
            'risk_indicators': self._analyze_risk_indicators(df, malicious_df, normal_df)
        }
        return analysis
    
    def _generate_risk_assessment(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Assess security risks based on various factors such as travel,
        off-hours activity, and data exfiltration via burning media.
        """
        risk_assessment = {}
        if 'is_abroad' in df.columns and 'is_hostile_country_trip' in df.columns:
            abroad = df[df['is_abroad'] == 1]
            if len(abroad) > 0:
                risk_assessment['travel_risk'] = {
                    'employees_traveled_abroad': len(abroad),
                    'hostile_country_visits': abroad['is_hostile_country_trip'].sum(),
                    'hostile_country_percentage': (abroad['is_hostile_country_trip'].sum() / len(abroad)) * 100
                }
        
        if 'num_print_commands_off_hours' in df.columns:
            risk_assessment['off_hours_printing'] = {
                'employees_printing_off_hours': (df['num_print_commands_off_hours'] > 0).sum(),
                'total_off_hours_print_commands': df['num_print_commands_off_hours'].sum()
            }
        
        if 'num_burn_requests' in df.columns:
            burning = df[df['num_burn_requests'] > 0]
            if len(burning) > 0:
                risk_assessment['data_exfiltration_risk'] = {
                    'employees_burning_media': len(burning),
                    'total_burn_requests': df['num_burn_requests'].sum(),
                    'avg_burn_volume_mb': burning.get('total_burn_volume_mb', pd.Series([0])).mean()
                }
        return risk_assessment
    
    def _detect_security_anomalies(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect potential security anomalies such as unusual night work,
        multiple campus accesses, and high-volume printing.
        """
        anomalies = {}
        if 'entered_during_night_hours' in df.columns:
            night_workers = df[df['entered_during_night_hours'] > 0]
            anomalies['night_work_anomalies'] = {
                'employees_working_nights': len(night_workers),
                'percentage_night_workers': (len(night_workers) / len(df)) * 100
            }
        
        if 'num_unique_campus' in df.columns:
            multi_campus = df[df['num_unique_campus'] > 1]
            anomalies['multi_campus_access'] = {
                'employees_multi_campus': len(multi_campus),
                'max_campus_access': df['num_unique_campus'].max(),
                'avg_campus_access': df['num_unique_campus'].mean()
            }
        
        if 'total_printed_pages' in df.columns:
            high_volume_threshold = df['total_printed_pages'].quantile(0.95)
            high_volume_printers = df[df['total_printed_pages'] > high_volume_threshold]
            anomalies['high_volume_printing'] = {
                'threshold_pages': high_volume_threshold,
                'employees_above_threshold': len(high_volume_printers),
                'max_pages_printed': df['total_printed_pages'].max()
            }
        
        return anomalies
    
    def _compare_printing_activity(self, malicious_df: pd.DataFrame, normal_df: pd.DataFrame) -> Dict[str, Any]:
        """Compare printing activity between malicious and normal employees."""
        if 'total_printed_pages' not in malicious_df.columns:
            return {'error': 'No printing data available'}
        
        return {
            'malicious_print_freq': (malicious_df['total_printed_pages'] > 0).mean(),
            'normal_print_freq': (normal_df['total_printed_pages'] > 0).mean(),
            'malicious_avg_pages': malicious_df[malicious_df['total_printed_pages'] > 0]['total_printed_pages'].mean(),
            'normal_avg_pages': normal_df[normal_df['total_printed_pages'] > 0]['total_printed_pages'].mean(),
            'malicious_off_hours_ratio': (malicious_df.get('num_print_commands_off_hours', pd.Series([0])).sum() /
                                         max(malicious_df.get('num_print_commands', pd.Series([1])).sum(), 1)),
            'normal_off_hours_ratio': (normal_df.get('num_print_commands_off_hours', pd.Series([0])).sum() /
                                       max(normal_df.get('num_print_commands', pd.Series([1])).sum(), 1))
        }
    
    def _compare_burning_activity(self, malicious_df: pd.DataFrame, normal_df: pd.DataFrame) -> Dict[str, Any]:
        """Compare burning activity between malicious and normal employees."""
        if 'num_burn_requests' not in malicious_df.columns:
            return {'error': 'No burning data available'}
        
        return {
            'malicious_burn_freq': (malicious_df['num_burn_requests'] > 0).mean(),
            'normal_burn_freq': (normal_df['num_burn_requests'] > 0).mean(),
            'malicious_avg_volume': malicious_df[malicious_df['num_burn_requests'] > 0].get('total_burn_volume_mb', pd.Series([0])).mean(),
            'normal_avg_volume': normal_df[normal_df['num_burn_requests'] > 0].get('total_burn_volume_mb', pd.Series([0])).mean(),
            'malicious_avg_classification': malicious_df[malicious_df['num_burn_requests'] > 0].get('avg_request_classification', pd.Series([0])).mean(),
            'normal_avg_classification': normal_df[normal_df['num_burn_requests'] > 0].get('avg_request_classification', pd.Series([0])).mean()
        }
    
    def _compare_travel_activity(self, malicious_df: pd.DataFrame, normal_df: pd.DataFrame) -> Dict[str, Any]:
        """Compare travel activity between malicious and normal employees."""
        if 'is_abroad' not in malicious_df.columns:
            return {'error': 'No travel data available'}
        
        return {
            'malicious_travel_freq': (malicious_df['is_abroad'] == 1).mean(),
            'normal_travel_freq': (normal_df['is_abroad'] == 1).mean(),
            'malicious_hostile_country_ratio': malicious_df[malicious_df['is_abroad'] == 1].get('is_hostile_country_trip', pd.Series([0])).mean(),
            'normal_hostile_country_ratio': normal_df[normal_df['is_abroad'] == 1].get('is_hostile_country_trip', pd.Series([0])).mean()
        }
    
    def _compare_work_patterns(self, malicious_df: pd.DataFrame, normal_df: pd.DataFrame) -> Dict[str, Any]:
        """Compare work patterns such as weekend work, night entry, and multi-campus access."""
        if 'num_entries' not in malicious_df.columns:
            return {'error': 'No work entry data available'}
        
        malicious_work = malicious_df[malicious_df['num_entries'] > 0]
        normal_work = normal_df[normal_df['num_entries'] > 0]
        
        return {
            'malicious_weekend_work': malicious_work.get('entry_during_weekend', pd.Series([0])).mean(),
            'normal_weekend_work': normal_work.get('entry_during_weekend', pd.Series([0])).mean(),
            'malicious_night_entry': malicious_work.get('entered_during_night_hours', pd.Series([0])).mean(),
            'normal_night_entry': normal_work.get('entered_during_night_hours', pd.Series([0])).mean(),
            'malicious_multi_campus': malicious_work.get('num_unique_campus', pd.Series([0])).mean(),
            'normal_multi_campus': normal_work.get('num_unique_campus', pd.Series([0])).mean()
        }
    
    def _analyze_risk_indicators(self, df: pd.DataFrame, malicious_df: pd.DataFrame, normal_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze risk indicators such as travel risk across malicious and normal groups."""
        risk_indicators = {}
        
        if 'risk_travel_indicator' in df.columns:
            risk_indicators.update({
                'malicious_risk_travel': malicious_df['risk_travel_indicator'].mean(),
                'normal_risk_travel': normal_df['risk_travel_indicator'].mean(),
                'total_risk_travel_incidents': df['risk_travel_indicator'].sum()
            })
        
        return risk_indicators