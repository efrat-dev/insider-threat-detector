import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class BaseFeatureEngineer:
    """מחלקת בסיס להנדסת תכונות"""
    
    def __init__(self):
        self.encoders = {}
        self.scalers = {}
        self.feature_stats = {}
    
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
                # בדיקת תקינות הנתונים
                if df_processed[col].isna().all():
                    print(f"Warning: Column {col} contains only NaN values, skipping transformations")
                    continue
                    
                # טרנספורמציה לוגריתמית
                df_processed[f'{col}_log'] = np.log1p(df_processed[col])
                
                # טרנספורמציה שורש
                df_processed[f'{col}_sqrt'] = np.sqrt(df_processed[col])
                
                # Z-score (רק אם יש שונות)
                if df_processed[col].std() > 0:
                    df_processed[f'{col}_zscore'] = stats.zscore(df_processed[col])
                else:
                    df_processed[f'{col}_zscore'] = 0
                
                # בינארי (מעל/מתחת לממוצע)
                df_processed[f'{col}_above_mean'] = (df_processed[col] > df_processed[col].mean()).astype(int)
                
                # רבעונים - עם טיפול בערכים כפולים
                try:
                    # בדיקת מספר ערכים ייחודיים
                    unique_values = df_processed[col].nunique()
                    
                    if unique_values >= 4:
                        # ניסיון ליצור רבעונים עם טיפול בערכים כפולים
                        df_processed[f'{col}_quartile'] = pd.qcut(
                            df_processed[col], 
                            q=4, 
                            duplicates='drop'  # ללא labels כדי להימנע מבעיות
                        )
                    elif unique_values >= 2:
                        # אם יש פחות מ-4 ערכים ייחודיים, נשתמש בחלוקה פשוטה יותר
                        df_processed[f'{col}_quartile'] = pd.cut(
                            df_processed[col], 
                            bins=min(unique_values, 4)
                        )
                    else:
                        # אם יש רק ערך אחד ייחודי
                        df_processed[f'{col}_quartile'] = 'Single_Value'
                        
                except Exception as e:
                    # יצירת חלוקה פשוטה במקרה של שגיאה
                    median_val = df_processed[col].median()
                    df_processed[f'{col}_quartile'] = np.where(
                        df_processed[col] <= median_val, 'Below_Median', 'Above_Median'
                    )
        
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