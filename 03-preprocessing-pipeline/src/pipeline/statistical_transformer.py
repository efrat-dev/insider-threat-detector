import numpy as np
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class StatisticalTransformer:
    """מחלקה מיוחדת לטרנספורמציות סטטיסטיות - Z-score ורבעונים בהתאם לסוג המודל"""
    
    def __init__(self, model_type='isolation-forest'):
        self.model_type = model_type
        self.scalers = {}
        self.fitted_params = {}
        self.is_fitted = False
        
    def fit(self, df):
        """אימון פרמטרי הטרנספורמציות הסטטיסטיות על נתוני הטריין"""
        print(f"Fitting statistical transformations parameters for {self.model_type} model...")
        
        # איפוס פרמטרים
        self.fitted_params = {}
        self.scalers = {}
        
        # זיהוי עמודות מספריות לטרנספורמציה
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        # הסרת עמודות מיוחדות
        exclude_cols = ['is_malicious', 'is_emp_malicious', 'target', 'date', 'timestamp', 'employee_id']
        transform_columns = [col for col in numeric_columns if col not in exclude_cols]
        
        self.fitted_params['transform_columns'] = transform_columns
        
        print(f"Fitting statistical parameters for {len(transform_columns)} numeric columns")
        
        successful_fits = 0
        
        for col in transform_columns:
            if col in df.columns:
                # בדיקת תקינות הנתונים
                if df[col].isna().all():
                    print(f"Skipping column {col} - all values are NaN")
                    continue
                
                # שמירת פרמטרים לכל עמודה
                col_params = {}
                
                try:
                    # פרמטרים בסיסיים
                    col_params['std'] = df[col].std()
                    col_params['has_variance'] = col_params['std'] > 0
                    col_params['unique_values'] = df[col].nunique()
                    col_params['min_val'] = df[col].min()
                    col_params['max_val'] = df[col].max()
                    
                    if col_params['has_variance']:
                        scaler = StandardScaler()
                        scaler.fit(df[col].values.reshape(-1, 1))
                        self.scalers[col] = scaler
                    
                    self.fitted_params[col] = col_params
                    successful_fits += 1
                    
                except Exception as e:
                    print(f"Error fitting parameters for column {col}: {str(e)}")
                    continue
        
        self.is_fitted = True
        
        print(f"Statistical fitting completed for {successful_fits} columns")
        print(f"  - Z-score transformations: {len(self.scalers)}")
        
        return df  
    
    def transform(self, df):
        """החלת הטרנספורמציות הסטטיסטיות עם פרמטרים מהטריין"""
        if not self.is_fitted:
            raise ValueError("StatisticalTransformer must be fitted before transform")
        
        print(f"Transforming data using fitted statistical parameters for {self.model_type} model...")
        df_processed = df.copy()
        
        transform_columns = self.fitted_params.get('transform_columns', [])
        zscore_successes = 0
        
        for col in transform_columns:
            if col not in df_processed.columns or col not in self.fitted_params:
                continue
            
            col_params = self.fitted_params[col]
            
            try:
                if col_params.get('has_variance', False) and col in self.scalers:
                    try:
                        df_processed[f'{col}_zscore'] = self.scalers[col].transform(
                            df_processed[col].values.reshape(-1, 1)
                        ).flatten()
                        zscore_successes += 1
                    except Exception as e:
                        print(f"Error applying Z-score to {col}: {str(e)}")
                        continue
                
            except Exception as e:
                print(f"Error transforming column {col}: {str(e)}")
                continue
        
        print(f"Statistical transformations completed - Z-score: {zscore_successes} columns")
        
        return df_processed
    
    def fit_transform(self, df):
        """fit + transform במקום אחד"""
        self.fit(df)
        return self.transform(df)