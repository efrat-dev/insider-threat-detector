import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class FeatureEngineer:
    """מחלקה מקיפה להנדסת תכונות בסיסיות לזיהוי איומים פנימיים"""
    
    def __init__(self):
        self.encoders = {}
        self.scalers = {}
        self.feature_stats = {}
    
    def extract_time_features(self, df):
        """חילוץ תכונות זמן מקיפות"""
        df_processed = df.copy()
        
        # המרת עמודת התאריך
        df_processed['date'] = pd.to_datetime(df_processed['date'])
        
        # תכונות זמן בסיסיות
        df_processed['year'] = df_processed['date'].dt.year
        df_processed['month'] = df_processed['date'].dt.month
        df_processed['day'] = df_processed['date'].dt.day
        df_processed['weekday'] = df_processed['date'].dt.weekday
        df_processed['quarter'] = df_processed['date'].dt.quarter
        df_processed['day_of_year'] = df_processed['date'].dt.dayofyear
        df_processed['week_of_year'] = df_processed['date'].dt.isocalendar().week
        
        # תכונות זמן מתקדמות
        df_processed['is_weekend'] = df_processed['weekday'].isin([5, 6]).astype(int)
        df_processed['is_monday'] = (df_processed['weekday'] == 0).astype(int)
        df_processed['is_friday'] = (df_processed['weekday'] == 4).astype(int)
        df_processed['is_beginning_of_month'] = (df_processed['day'] <= 5).astype(int)
        df_processed['is_end_of_month'] = (df_processed['day'] >= 25).astype(int)
        df_processed['is_quarter_end'] = df_processed['month'].isin([3, 6, 9, 12]).astype(int)
        
        # תכונות עונתיות
        df_processed['season'] = df_processed['month'].map({
            12: 'winter', 1: 'winter', 2: 'winter',
            3: 'spring', 4: 'spring', 5: 'spring',
            6: 'summer', 7: 'summer', 8: 'summer',
            9: 'autumn', 10: 'autumn', 11: 'autumn'
        })
        
        # עיבוד זמני כניסה ויציאה
        if 'first_entry_time' in df_processed.columns:
            df_processed['first_entry_time'] = pd.to_datetime(df_processed['first_entry_time'], errors='coerce')
            df_processed['entry_hour'] = df_processed['first_entry_time'].dt.hour
            df_processed['entry_minute'] = df_processed['first_entry_time'].dt.minute
            df_processed['entry_time_numeric'] = df_processed['entry_hour'] + df_processed['entry_minute']/60
            
            # תכונות שעות כניסה
            df_processed['is_very_early_entry'] = (df_processed['entry_hour'] < 6).astype(int)
            df_processed['is_early_entry'] = (df_processed['entry_hour'] < 8).astype(int)
            df_processed['is_late_entry'] = (df_processed['entry_hour'] > 10).astype(int)
            df_processed['is_lunch_entry'] = df_processed['entry_hour'].between(12, 14).astype(int)
            df_processed['is_night_entry'] = (df_processed['entry_hour'] >= 20).astype(int)
        
        if 'last_exit_time' in df_processed.columns:
            df_processed['last_exit_time'] = pd.to_datetime(df_processed['last_exit_time'], errors='coerce')
            df_processed['exit_hour'] = df_processed['last_exit_time'].dt.hour
            df_processed['exit_minute'] = df_processed['last_exit_time'].dt.minute
            df_processed['exit_time_numeric'] = df_processed['exit_hour'] + df_processed['exit_minute']/60
            
            # תכונות שעות יציאה
            df_processed['is_early_exit'] = (df_processed['exit_hour'] < 16).astype(int)
            df_processed['is_late_exit'] = (df_processed['exit_hour'] > 19).astype(int)
            df_processed['is_very_late_exit'] = (df_processed['exit_hour'] > 22).astype(int)
            df_processed['is_night_exit'] = (df_processed['exit_hour'] >= 23).astype(int)
            
            # זמן עבודה
            df_processed['work_duration_hours'] = df_processed['total_presence_minutes'] / 60
            df_processed['work_duration_category'] = pd.cut(
                df_processed['work_duration_hours'],
                bins=[0, 4, 8, 12, 24],
                labels=['short', 'normal', 'long', 'very_long']
            )
        
        print("Time features extracted successfully")
        return df_processed
    
    def create_printing_features(self, df):
        """יצירת תכונות מקיפות להדפסה"""
        df_processed = df.copy()
        
        # יחסי הדפסה בסיסיים
        df_processed['avg_pages_per_print'] = df_processed['total_printed_pages'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['print_intensity'] = df_processed['num_print_commands'] / np.maximum(df_processed['total_presence_minutes'] / 60, 1)
        
        # תכונות הדפסה צבעונית
        df_processed['color_print_preference'] = df_processed['num_color_prints'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['bw_print_preference'] = df_processed['num_bw_prints'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['color_vs_bw_ratio'] = df_processed['num_color_prints'] / np.maximum(df_processed['num_bw_prints'], 1)
        
        # תכונות הדפסה מחוץ לשעות
        df_processed['off_hours_print_ratio'] = df_processed['num_print_commands_off_hours'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['off_hours_pages_ratio'] = df_processed['num_printed_pages_off_hours'] / np.maximum(df_processed['total_printed_pages'], 1)
        df_processed['off_hours_avg_pages'] = df_processed['num_printed_pages_off_hours'] / np.maximum(df_processed['num_print_commands_off_hours'], 1)
        
        # תכונות הדפסה מקמפוסים אחרים
        df_processed['prints_from_other_campus'] = (df_processed['printed_from_other'] > 0).astype(int)
        df_processed['print_mobility_score'] = df_processed['print_campuses'] / np.maximum(df_processed['num_unique_campus'], 1)
        
        # תכונות מתקדמות
        df_processed['is_heavy_printer'] = (df_processed['num_print_commands'] > df_processed['num_print_commands'].quantile(0.9)).astype(int)
        df_processed['is_high_volume_printer'] = (df_processed['total_printed_pages'] > df_processed['total_printed_pages'].quantile(0.9)).astype(int)
        df_processed['print_efficiency'] = df_processed['total_printed_pages'] / np.maximum(df_processed['work_duration_hours'], 1)
        
        # תכונות קטגוריות
        df_processed['print_activity_level'] = pd.cut(
            df_processed['num_print_commands'],
            bins=[0, 5, 20, 50, np.inf],
            labels=['low', 'medium', 'high', 'very_high']
        )
        
        print("Printing features created successfully")
        return df_processed
    
    def create_burning_features(self, df):
        """יצירת תכונות מקיפות לשריפה"""
        df_processed = df.copy()
        
        # יחסי שריפה בסיסיים
        df_processed['avg_burn_volume_per_request'] = df_processed['total_burn_volume_mb'] / np.maximum(df_processed['num_burn_requests'], 1)
        df_processed['avg_files_per_burn'] = df_processed['total_files_burned'] / np.maximum(df_processed['num_burn_requests'], 1)
        df_processed['avg_file_size_mb'] = df_processed['total_burn_volume_mb'] / np.maximum(df_processed['total_files_burned'], 1)
        
        # תכונות שריפה מחוץ לשעות
        df_processed['off_hours_burn_ratio'] = df_processed['num_burn_requests_off_hours'] / np.maximum(df_processed['num_burn_requests'], 1)
        df_processed['burn_intensity'] = df_processed['num_burn_requests'] / np.maximum(df_processed['total_presence_minutes'] / 60, 1)
        
        # תכונות סיווג ביטחוני
        df_processed['high_classification_burn'] = (df_processed['max_request_classification'] >= 4).astype(int)
        df_processed['classification_consistency'] = df_processed['max_request_classification'] - df_processed['avg_request_classification']
        df_processed['classification_variance'] = df_processed['max_request_classification'] / np.maximum(df_processed['avg_request_classification'], 1)
        
        # תכונות מיקום שריפה
        df_processed['burns_from_other_campus'] = (df_processed['burned_from_other'] > 0).astype(int)
        df_processed['burn_mobility_score'] = df_processed['burn_campuses'] / np.maximum(df_processed['num_unique_campus'], 1)
        
        # תכונות מתקדמות
        df_processed['is_heavy_burner'] = (df_processed['num_burn_requests'] > df_processed['num_burn_requests'].quantile(0.9)).astype(int)
        df_processed['is_high_volume_burner'] = (df_processed['total_burn_volume_mb'] > df_processed['total_burn_volume_mb'].quantile(0.9)).astype(int)
        df_processed['burn_efficiency'] = df_processed['total_burn_volume_mb'] / np.maximum(df_processed['work_duration_hours'], 1)
        
        # תכונות קטגוריות
        df_processed['burn_activity_level'] = pd.cut(
            df_processed['num_burn_requests'],
            bins=[0, 1, 5, 15, np.inf],
            labels=['none', 'low', 'medium', 'high']
        )
        
        df_processed['burn_volume_category'] = pd.cut(
            df_processed['total_burn_volume_mb'],
            bins=[0, 100, 1000, 10000, np.inf],
            labels=['small', 'medium', 'large', 'huge']
        )
        
        print("Burning features created successfully")
        return df_processed
    
    def create_employee_features(self, df):
        """יצירת תכונות עובד מקיפות"""
        df_processed = df.copy()
        
        # תכונות ותק
        df_processed['seniority_category'] = pd.cut(
            df_processed['employee_seniority_years'],
            bins=[0, 1, 3, 10, np.inf],
            labels=['new', 'junior', 'senior', 'veteran']
        )
        
        df_processed['is_new_employee'] = (df_processed['employee_seniority_years'] < 1).astype(int)
        df_processed['is_veteran_employee'] = (df_processed['employee_seniority_years'] > 10).astype(int)
        
        # תכונות סיכון אישיות
        df_processed['personal_risk_flags'] = (
            df_processed['has_foreign_citizenship'] +
            df_processed['has_criminal_record'] +
            df_processed['has_medical_history']
        )
        
        df_processed['employment_risk_score'] = (
            df_processed['is_contractor'] * 2 +
            df_processed['has_foreign_citizenship'] * 1.5 +
            df_processed['has_criminal_record'] * 3 +
            df_processed['risk_travel_indicator'] * 2
        )
        
        # תכונות מיקום וניידות
        df_processed['is_multi_campus_user'] = (df_processed['num_unique_campus'] > 1).astype(int)
        df_processed['campus_mobility_score'] = df_processed['num_unique_campus']
        
        # תכונות נסיעות
        df_processed['has_travel_history'] = (df_processed['is_abroad'] > 0).astype(int)
        df_processed['hostile_travel_risk'] = (df_processed['is_hostile_country_trip'] > 0).astype(int)
        df_processed['unofficial_travel_risk'] = (df_processed['is_abroad'] & ~df_processed['is_official_trip']).astype(int)
        
        # תכונות קטגוריות למחלקה ותפקיד
        department_risk_map = {
            'IT': 3, 'Security': 4, 'Finance': 3, 'HR': 2,
            'Research': 3, 'Operations': 1, 'Management': 2
        }
        df_processed['department_risk_level'] = df_processed['employee_department'].map(department_risk_map).fillna(1)
        
        print("Employee features created successfully")
        return df_processed
    
    def create_access_features(self, df):
        """יצירת תכונות גישה ונוכחות"""
        df_processed = df.copy()
        
        # תכונות כניסות ויציאות
        df_processed['entry_exit_balance'] = df_processed['num_entries'] - df_processed['num_exits']
        df_processed['avg_presence_per_entry'] = df_processed['total_presence_minutes'] / np.maximum(df_processed['num_entries'], 1)
        df_processed['access_frequency'] = df_processed['num_entries'] + df_processed['num_exits']
        
        # תכונות זמן נוכחות
        df_processed['presence_intensity'] = df_processed['total_presence_minutes'] / (24 * 60)  # יחס מהיום
        df_processed['is_long_presence'] = (df_processed['total_presence_minutes'] > 12 * 60).astype(int)
        df_processed['is_short_presence'] = (df_processed['total_presence_minutes'] < 4 * 60).astype(int)
        
        # תכונות גישה חשודה
        df_processed['suspicious_access_score'] = (
            df_processed['entered_during_night_hours'] * 2 +
            df_processed['early_entry_flag'] * 1 +
            df_processed['late_exit_flag'] * 1 +
            df_processed['entry_during_weekend'] * 2
        )
        
        df_processed['has_suspicious_access'] = (df_processed['suspicious_access_score'] > 0).astype(int)
        
        # תכונות קטגוריות
        df_processed['access_pattern'] = pd.cut(
            df_processed['num_entries'],
            bins=[0, 1, 3, 10, np.inf],
            labels=['rare', 'occasional', 'regular', 'frequent']
        )
        
        print("Access features created successfully")
        return df_processed
    
    def create_interaction_features(self, df):
        """יצירת תכונות אינטראקציה מתקדמות"""
        df_processed = df.copy()
        
        # יחסים בין פעילויות
        df_processed['print_to_burn_ratio'] = df_processed['num_print_commands'] / np.maximum(df_processed['num_burn_requests'], 1)
        df_processed['burn_to_print_ratio'] = df_processed['num_burn_requests'] / np.maximum(df_processed['num_print_commands'], 1)
        df_processed['total_activity_score'] = df_processed['num_print_commands'] + df_processed['num_burn_requests']
        
        # אינטראקציות עם ותק
        df_processed['prints_per_seniority'] = df_processed['num_print_commands'] / np.maximum(df_processed['employee_seniority_years'], 1)
        df_processed['burns_per_seniority'] = df_processed['num_burn_requests'] / np.maximum(df_processed['employee_seniority_years'], 1)
        df_processed['activity_per_seniority'] = df_processed['total_activity_score'] / np.maximum(df_processed['employee_seniority_years'], 1)
        
        # אינטראקציות עם זמן נוכחות
        df_processed['prints_per_hour'] = df_processed['num_print_commands'] / np.maximum(df_processed['work_duration_hours'], 1)
        df_processed['burns_per_hour'] = df_processed['num_burn_requests'] / np.maximum(df_processed['work_duration_hours'], 1)
        df_processed['pages_per_hour'] = df_processed['total_printed_pages'] / np.maximum(df_processed['work_duration_hours'], 1)
        
        # אינטראקציות עם סיכון
        df_processed['risk_activity_interaction'] = df_processed['employment_risk_score'] * df_processed['total_activity_score']
        df_processed['risk_off_hours_interaction'] = df_processed['employment_risk_score'] * df_processed['off_hours_print_ratio']
        
        # אינטראקציות חשודות
        df_processed['suspicious_print_activity'] = (
            df_processed['off_hours_print_ratio'] * df_processed['color_print_preference'] * 
            df_processed['prints_from_other_campus']
        )
        
        df_processed['suspicious_burn_activity'] = (
            df_processed['off_hours_burn_ratio'] * df_processed['high_classification_burn'] * 
            df_processed['burns_from_other_campus']
        )
        
        print("Interaction features created successfully")
        return df_processed
    
    def apply_statistical_transforms(self, df):
        """החלת טרנספורמציות סטטיסטיות"""
        df_processed = df.copy()
        
        # רשימת עמודות לטרנספורמציה
        transform_columns = [
            'num_print_commands', 'total_printed_pages', 'num_burn_requests',
            'total_burn_volume_mb', 'total_files_burned', 'total_presence_minutes',
            'employee_seniority_years', 'total_activity_score'
        ]
        
        for col in transform_columns:
            if col in df_processed.columns:
                # טרנספורמציה לוגריתמית
                df_processed[f'{col}_log'] = np.log1p(df_processed[col])
                
                # טרנספורמציה שורש
                df_processed[f'{col}_sqrt'] = np.sqrt(df_processed[col])
                
                # Z-score
                df_processed[f'{col}_zscore'] = stats.zscore(df_processed[col])
                
                # בינארי (מעל/מתחת לממוצע)
                df_processed[f'{col}_above_mean'] = (df_processed[col] > df_processed[col].mean()).astype(int)
                
                # רבעונים
                df_processed[f'{col}_quartile'] = pd.qcut(df_processed[col], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
        
        print("Statistical transformations applied successfully")
        return df_processed
    
    def encode_categorical_variables(self, df, encoding_method='mixed'):
        """קידוד משתנים קטגוריים מתקדם"""
        df_processed = df.copy()
        
        # זיהוי עמודות קטגוריות
        categorical_columns = df_processed.select_dtypes(include=['category', 'object']).columns
        date_columns = ['date', 'first_entry_time', 'last_exit_time', 'country_name']
        categorical_columns = [col for col in categorical_columns if col not in date_columns]
        
        for col in categorical_columns:
            if col in df_processed.columns:
                unique_values = df_processed[col].nunique()
                
                if unique_values <= 5:
                    # One-hot encoding לעמודות עם cardinality נמוך
                    dummies = pd.get_dummies(df_processed[col], prefix=col)
                    df_processed = pd.concat([df_processed, dummies], axis=1)
                
                elif unique_values <= 20:
                    # Label encoding לעמודות עם cardinality בינוני
                    if col not in self.encoders:
                        self.encoders[col] = LabelEncoder()
                    df_processed[f'{col}_encoded'] = self.encoders[col].fit_transform(df_processed[col].astype(str))
                    
                    # Target encoding אם יש עמודת target
                    if 'is_malicious' in df_processed.columns:
                        target_mean = df_processed.groupby(col)['is_malicious'].mean()
                        df_processed[f'{col}_target_encoded'] = df_processed[col].map(target_mean)
                
                else:
                    # Frequency encoding לעמודות עם cardinality גבוה
                    freq_map = df_processed[col].value_counts().to_dict()
                    df_processed[f'{col}_frequency'] = df_processed[col].map(freq_map)
        
        print(f"Categorical encoding completed using {encoding_method} method")
        return df_processed
    
    def create_all_basic_features(self, df):
        """יצירת כל התכונות הבסיסיות"""
        print("Starting comprehensive basic feature engineering...")
        
        df = self.extract_time_features(df)
        df = self.create_printing_features(df)
        df = self.create_burning_features(df)
        df = self.create_employee_features(df)
        df = self.create_access_features(df)
        df = self.create_interaction_features(df)
        df = self.apply_statistical_transforms(df)
        df = self.encode_categorical_variables(df)
        
        print(f"Basic feature engineering completed! Created {len(df.columns)} features")
        return df
    
    def get_feature_summary(self, df):
        """סיכום התכונות שנוצרו"""
        feature_groups = {
            'time_features': [col for col in df.columns if any(x in col for x in ['year', 'month', 'day', 'hour', 'season', 'quarter'])],
            'printing_features': [col for col in df.columns if 'print' in col],
            'burning_features': [col for col in df.columns if 'burn' in col],
            'employee_features': [col for col in df.columns if any(x in col for x in ['employee', 'seniority', 'risk'])],
            'access_features': [col for col in df.columns if any(x in col for x in ['entry', 'exit', 'presence', 'access'])],
            'interaction_features': [col for col in df.columns if any(x in col for x in ['ratio', 'per_', 'interaction'])],
            'statistical_features': [col for col in df.columns if any(x in col for x in ['_log', '_sqrt', '_zscore', '_quartile'])]
        }
        
        summary = {}
        for group, features in feature_groups.items():
            summary[group] = {
                'count': len(features),
                'features': features[:10]  # הצגת 10 הראשונות
            }
        
        return summary
