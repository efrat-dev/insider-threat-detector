import pandas as pd
from typing import Dict, Any, Optional
from .base_analyzer import BaseAnalyzer
from .behavioral_analyzer import BehavioralAnalyzer
from .security_analyzer import SecurityAnalyzer


class ComprehensiveAnalyzer(BaseAnalyzer):
    """Comprehensive analysis of the generated insider threat dataset"""
    
    def __init__(self):
        """Initialize the comprehensive analyzer with component analyzers"""
        super().__init__()
        self.behavioral_analyzer = BehavioralAnalyzer()
        self.security_analyzer = SecurityAnalyzer()
    
    def generate_comprehensive_analysis(self, df: pd.DataFrame, 
                                      malicious_employee_ids: Optional[set] = None) -> Dict[str, Any]:
        """Generate comprehensive analysis of the dataset"""
        analysis = {}
        
        # Basic statistics
        analysis['basic_stats'] = self._generate_basic_statistics(df)
        
        # Behavioral group analysis
        analysis['behavioral_analysis'] = self.behavioral_analyzer._generate_behavioral_analysis(df)
        
        # Malicious vs Normal comparison
        analysis['malicious_analysis'] = self.security_analyzer._generate_malicious_analysis(df)
        
        # Activity pattern analysis
        analysis['activity_patterns'] = self._generate_activity_patterns(df)
        
        # Data quality analysis
        analysis['data_quality'] = self._generate_data_quality_analysis(df)
        
        # Temporal analysis
        analysis['temporal_analysis'] = self._generate_temporal_analysis(df)
        
        # Security analysis
        analysis['security_analysis'] = self.security_analyzer.analyze_security_patterns(df)
        
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
        
        # Weekly patterns - using temporary DataFrame
        try:
            # יצירת עותק זמני של הדאטה
            df_temp = df.copy()
            df_temp['weekday'] = pd.to_datetime(df_temp['date']).dt.day_name()
            
            weekly_patterns = {}
            
            if 'num_entries' in df.columns:
                weekly_patterns['work_by_weekday'] = df_temp[df_temp['num_entries'] > 0]['weekday'].value_counts().to_dict()
            if 'total_printed_pages' in df.columns:
                weekly_patterns['print_by_weekday'] = df_temp[df_temp['total_printed_pages'] > 0]['weekday'].value_counts().to_dict()
            if 'num_burn_requests' in df.columns:
                weekly_patterns['burn_by_weekday'] = df_temp[df_temp['num_burn_requests'] > 0]['weekday'].value_counts().to_dict()
            
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
    
    def _generate_temporal_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze temporal patterns in the data"""
        temporal = {}
        
        try:
            # יצירת עותק זמני של הדאטה
            df_temp = df.copy()
            
            # Monthly aggregation
            df_temp['month'] = pd.to_datetime(df_temp['date']).dt.to_period('M')
            monthly_agg = {}
            
            if 'is_malicious' in df.columns:
                monthly_agg['is_malicious'] = df_temp.groupby('month')['is_malicious'].sum().to_dict()
            if 'total_printed_pages' in df.columns:
                monthly_agg['total_printed_pages'] = df_temp.groupby('month')['total_printed_pages'].sum().to_dict()
            if 'num_burn_requests' in df.columns:
                monthly_agg['num_burn_requests'] = df_temp.groupby('month')['num_burn_requests'].sum().to_dict()
            if 'is_abroad' in df.columns:
                monthly_agg['is_abroad'] = df_temp.groupby('month')['is_abroad'].sum().to_dict()
            
            monthly_agg['employee_id'] = df_temp.groupby('month')['employee_id'].nunique().to_dict()
            
            temporal['monthly_trends'] = monthly_agg
            
            # Weekly aggregation
            df_temp['week'] = pd.to_datetime(df_temp['date']).dt.to_period('W')
            weekly_agg = {}
            
            if 'is_malicious' in df.columns:
                weekly_agg['is_malicious'] = df_temp.groupby('week')['is_malicious'].sum().to_dict()
            if 'total_printed_pages' in df.columns:
                weekly_agg['total_printed_pages'] = df_temp.groupby('week')['total_printed_pages'].sum().to_dict()
            if 'num_burn_requests' in df.columns:
                weekly_agg['num_burn_requests'] = df_temp.groupby('week')['num_burn_requests'].sum().to_dict()
            if 'is_abroad' in df.columns:
                weekly_agg['is_abroad'] = df_temp.groupby('week')['is_abroad'].sum().to_dict()
            
            temporal['weekly_trends'] = weekly_agg
            
        except Exception as e:
            temporal['error'] = f"Error processing temporal analysis: {str(e)}"
        
        return temporal
    
    def generate_summary_statistics(self, df: pd.DataFrame):
        """Generate and print summary statistics"""
        analysis = self.generate_comprehensive_analysis(df)
        return analysis
    
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