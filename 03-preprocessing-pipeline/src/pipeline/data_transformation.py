import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.feature_selection import VarianceThreshold
from typing import List  

class DataTransformer:
    """מחלקה לטרנספורמציות נתונים"""
    
    def __init__(self):
        self.variance_threshold = None
        self.correlation_threshold = 0.95
        self.scaler = None
        self.variance_filtered_features_ = []
        self.correlation_filtered_features_ = []
        self.final_features_ = []
        
        # Initialize fitted_params and scalers dictionaries
        self.fitted_params = {}
        self.scalers = {}
        
    def _is_protected_column(self, col_name):
        """בדיקה האם העמודה מוגנת (מכילה zscore או quartile)"""
        return 'zscore' in col_name.lower() or 'quartile' in col_name.lower()
        
    def fit_variance_filtering(self, df, threshold=0.01):
        """פילטרינג פיצ'רים עם וריאנס נמוך"""
        print(f"Fitting variance filtering with threshold {threshold}...")
        
        # הפרדת פיצ'רים נומריים
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'target' in numeric_cols:
            numeric_cols.remove('target')
        
        if len(numeric_cols) == 0:
            print("No numeric columns found for variance filtering")
            self.variance_filtered_features_ = df.columns.tolist()
            return df
        
        # הפרדה בין עמודות מוגנות לרגילות
        protected_cols = [col for col in numeric_cols if self._is_protected_column(col)]
        regular_cols = [col for col in numeric_cols if not self._is_protected_column(col)]
        
        print(f"Protected columns (will not be filtered): {protected_cols}")
        
        if len(regular_cols) == 0:
            print("No regular numeric columns for variance filtering (all are protected)")
            self.variance_filtered_features_ = df.columns.tolist()
            return df
        
        # יצירת VarianceThreshold רק לעמודות הרגילות
        self.variance_threshold = VarianceThreshold(threshold=threshold)
        
        # אימון על הפיצ'רים הנומריים הרגילים
        self.variance_threshold.fit(df[regular_cols])
        
        # קבלת שמות הפיצ'רים הרגילים שנשארים
        selected_regular = [col for col, selected in 
                           zip(regular_cols, self.variance_threshold.get_support()) 
                           if selected]
        
        # שמירת רשימת הפיצ'רים שנשארים (רגילים + מוגנים + לא נומריים)
        non_numeric_cols = [col for col in df.columns if col not in numeric_cols]
        self.variance_filtered_features_ = selected_regular + protected_cols + non_numeric_cols
        
        removed_count = len(regular_cols) - len(selected_regular)
        print(f"Variance filtering: removed {removed_count} features with low variance")
        print(f"Kept {len(protected_cols)} protected features regardless of variance")
        
        return df[self.variance_filtered_features_]
    
    def transform_variance_filtering(self, df):
        """החלת פילטרינג וריאנס על דאטה חדש"""
        if self.variance_threshold is None:
            raise ValueError("Variance filtering not fitted yet")
        
        # Filter features to only include those that exist in the current dataframe
        available_features = [col for col in self.variance_filtered_features_ if col in df.columns]
        
        if len(available_features) != len(self.variance_filtered_features_):
            missing_features = set(self.variance_filtered_features_) - set(available_features)
            print(f"Warning: {len(missing_features)} features from variance filtering not found in transform data: {missing_features}")
        
        return df[available_features]
    
    def fit_correlation_filtering(self, df, threshold=0.95):
        """פילטרינג פיצ'רים עם קורלציה גבוהה"""
        print(f"Fitting correlation filtering with threshold {threshold}...")
        
        self.correlation_threshold = threshold
        
        # הפרדת פיצ'רים נומריים
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'target' in numeric_cols:
            numeric_cols.remove('target')
        
        if len(numeric_cols) <= 1:
            print("Not enough numeric columns for correlation filtering")
            self.correlation_filtered_features_ = df.columns.tolist()
            return df
        
        # הפרדה בין עמודות מוגנות לרגילות
        protected_cols = [col for col in numeric_cols if self._is_protected_column(col)]
        regular_cols = [col for col in numeric_cols if not self._is_protected_column(col)]
        
        print(f"Protected columns (will not be filtered): {protected_cols}")
        
        if len(regular_cols) <= 1:
            print("Not enough regular numeric columns for correlation filtering")
            self.correlation_filtered_features_ = df.columns.tolist()
            return df
        
        # חישוב מטריצת קורלציה רק לעמודות הרגילות
        corr_matrix = df[regular_cols].corr().abs()
        
        # מציאת זוגות פיצ'רים עם קורלציה גבוהה
        upper_tri = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        
        # פיצ'רים להסרה (רק מהעמודות הרגילות)
        to_drop = [column for column in upper_tri.columns 
                  if any(upper_tri[column] > threshold)]
        
        # שמירת רשימת הפיצ'רים שנשארים
        remaining_regular = [col for col in regular_cols if col not in to_drop]
        non_numeric_cols = [col for col in df.columns if col not in numeric_cols]
        self.correlation_filtered_features_ = remaining_regular + protected_cols + non_numeric_cols
        
        print(f"Correlation filtering: removed {len(to_drop)} highly correlated features")
        print(f"Kept {len(protected_cols)} protected features regardless of correlation")
        if to_drop:
            print(f"Removed features: {to_drop}")
        
        return df[self.correlation_filtered_features_]
    
    def transform_correlation_filtering(self, df):
        """החלת פילטרינג קורלציה על דאטה חדש"""
        if not hasattr(self, 'correlation_filtered_features_'):
            raise ValueError("Correlation filtering not fitted yet")
        
        # Filter features to only include those that exist in the current dataframe
        available_features = [col for col in self.correlation_filtered_features_ if col in df.columns]
        
        if len(available_features) != len(self.correlation_filtered_features_):
            missing_features = set(self.correlation_filtered_features_) - set(available_features)
            print(f"Warning: {len(missing_features)} features from correlation filtering not found in transform data: {missing_features}")
        
        return df[available_features]
    
    def fit_normalize_features(self, df, method='standard'):
        """אfימון פרמטרי הנורמליזציה על נתוני הטריין"""
        print(f"Fitting normalization parameters with method: {method}")
        
        # שמירת פרמטרי הנורמליזציה
        self.fitted_params['normalization'] = {
            'method': method
        }
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        # הוצאת עמודות שלא צריכות נורמליזציה
        exclude_cols = ['employee_id', 'is_malicious', 'is_emp_malicious_binary', 'target', 'date', 'first_entry_time', 'last_exit_time']
        numeric_columns = [col for col in numeric_columns if col not in exclude_cols]
        
        # שמירת רשימת העמודות לנורמליזציה
        self.fitted_params['normalization']['columns_to_normalize'] = numeric_columns
        
        if len(numeric_columns) == 0:
            print("No numeric columns found for normalization")
            return df
        
        # אימון הscaler
        if method == 'standard':
            scaler = StandardScaler()
            scaler.fit(df[numeric_columns])
            self.scalers['standard'] = scaler
        
        elif method == 'minmax':
            scaler = MinMaxScaler()
            scaler.fit(df[numeric_columns])
            self.scalers['minmax'] = scaler
        
        elif method == 'robust':
            scaler = RobustScaler()
            scaler.fit(df[numeric_columns])
            self.scalers['robust'] = scaler
        
        print(f"Normalization fitted for {len(numeric_columns)} columns using {method} method")
        return df  # בפיט לא משנים את הדאטה
    
    def transform_normalize_features(self, df):
        """החלת הנורמליזציה עם פרמטרים מהטריין"""
        if not self.fitted_params.get('normalization'):
            raise ValueError("Normalization must be fitted before transform")
        
        print("Transforming features using fitted normalization parameters...")
        
        df_processed = df.copy()
        method = self.fitted_params['normalization']['method']
        columns_to_normalize = self.fitted_params['normalization']['columns_to_normalize']
        
        # עמודות שקיימות בדאטה החדש
        available_columns = [col for col in columns_to_normalize if col in df_processed.columns]
        
        if len(available_columns) == 0:
            print("No columns available for normalization")
            return df_processed
        
        if len(available_columns) != len(columns_to_normalize):
            missing_cols = set(columns_to_normalize) - set(available_columns)
            print(f"Warning: {len(missing_cols)} normalization columns missing in transform data")
        
        # החלת הscaler המתאים
        scaler = self.scalers.get(method)
        if scaler is None:
            raise ValueError(f"Scaler for method '{method}' not found")
        
        try:
            df_processed[available_columns] = scaler.transform(df_processed[available_columns])
            print(f"Features normalized using {method} method for {len(available_columns)} columns")
        except Exception as e:
            print(f"Error in normalization: {str(e)}")
            
        return df_processed