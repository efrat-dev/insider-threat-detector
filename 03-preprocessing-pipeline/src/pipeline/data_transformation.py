import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

class DataTransformer:
    """מחלקה לטרנספורמציות נתונים"""
    
    def __init__(self):
        self.scaler = None        
        self.fitted_params = {}
        self.scalers = {}
        
    
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