import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class StatisticalTransformer:
    """מחלקה מיוחדת לטרנספורמציות סטטיסטיות"""
    
    def __init__(self):
        self.scalers = {}
        self.feature_stats = {}
        self.fitted_params = {}
        self.is_fitted = False
    
    def fit(self, df):
        """אימון פרמטרי הטרנספורמציות הסטטיסטיות על נתוני הטריין"""
        print("Fitting statistical transformations parameters...")
        
        # איפוס פרמטרים
        self.fitted_params = {}
        self.scalers = {}
        self.feature_stats = {}
        
        # זיהוי עמודות מספריות לטרנספורמציה
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        # הסרת עמודות מיוחדות
        exclude_cols = ['is_malicious', 'is_emp_malicious', 'target', 'date', 'timestamp', 'employee_id']
        transform_columns = [col for col in numeric_columns if col not in exclude_cols]
        
        self.fitted_params['transform_columns'] = transform_columns
        
        print(f"Fitting statistical parameters for {len(transform_columns)} numeric columns")
        
        for col in transform_columns:
            if col in df.columns:
                # בדיקת תקינות הנתונים
                if df[col].isna().all() or df[col].nunique() <= 1:
                    print(f"Skipping column {col} - insufficient data")
                    continue
                
                # שמירת פרמטרים לכל עמודה
                col_params = {}
                
                try:
                    # פרמטרים בסיסיים
                    col_params['mean'] = df[col].mean()
                    col_params['median'] = df[col].median()
                    col_params['std'] = df[col].std()
                    col_params['min_val'] = df[col].min()
                    col_params['max_val'] = df[col].max()
                    
                    # בדיקות לטרנספורמציות
                    col_params['can_log'] = (df[col] >= 0).all()
                    col_params['has_variance'] = col_params['std'] > 0
                    col_params['unique_values'] = df[col].nunique()
                    
                    # פרמטרים לרבעונים
                    if col_params['unique_values'] >= 4:
                        try:
                            # שמירת quartile boundaries
                            quartiles = df[col].quantile([0.25, 0.5, 0.75]).values
                            col_params['quartile_bounds'] = quartiles
                            col_params['use_quartiles'] = True
                        except:
                            col_params['use_quartiles'] = False
                            col_params['quartile_bounds'] = None
                    else:
                        col_params['use_quartiles'] = False
                        col_params['quartile_bounds'] = None
                    
                    # שמירת פרמטרי Z-score
                    if col_params['has_variance']:
                        scaler = StandardScaler()
                        scaler.fit(df[col].values.reshape(-1, 1))
                        self.scalers[col] = scaler
                    
                    self.fitted_params[col] = col_params
                    
                except Exception as e:
                    print(f"Error fitting parameters for column {col}: {str(e)}")
                    continue
        
        self.is_fitted = True
        print(f"Statistical fitting completed for {len(self.fitted_params)} columns")
        return df  
    
    def transform(self, df):
        """החלת הטרנספורמציות הסטטיסטיות עם פרמטרים מהטריין"""
        if not self.is_fitted:
            raise ValueError("StatisticalTransformer must be fitted before transform")
        
        print("Transforming data using fitted statistical parameters...")
        df_processed = df.copy()
        
        transform_columns = self.fitted_params.get('transform_columns', [])
        
        for col in transform_columns:
            if col not in df_processed.columns or col not in self.fitted_params:
                continue
            
            col_params = self.fitted_params[col]
            
            try:
                # טרנספורמציה לוגריתמית
                if col_params.get('can_log', False):
                    df_processed[f'{col}_log'] = np.log1p(df_processed[col])
                                
                # Z-score עם scaler מהטריין
                if col_params.get('has_variance', False) and col in self.scalers:
                    try:
                        df_processed[f'{col}_zscore'] = self.scalers[col].transform(
                            df_processed[col].values.reshape(-1, 1)
                        ).flatten()
                    except:
                        # fallback manual calculation
                        df_processed[f'{col}_zscore'] = (
                            df_processed[col] - col_params['mean']
                        ) / col_params['std']
                
                # בינארי (מעל/מתחת לממוצע מהטריין)
                df_processed[f'{col}_above_mean'] = (
                    df_processed[col] > col_params['mean']
                ).astype(int)
                
                # רבעונים עם boundaries מהטריין
                if col_params.get('use_quartiles', False) and col_params.get('quartile_bounds') is not None:
                    try:
                        bounds = col_params['quartile_bounds']
                        df_processed[f'{col}_quartile'] = pd.cut(
                            df_processed[col],
                            bins=[-np.inf] + bounds.tolist() + [np.inf],
                            labels=[0, 1, 2, 3],
                            include_lowest=True
                        ).astype(int)
                    except:
                        # fallback לבינארי מול median
                        median_val = col_params['median']
                        df_processed[f'{col}_quartile'] = np.where(
                            df_processed[col] <= median_val, 0, 1
                        )
                else:
                    df_processed[f'{col}_quartile'] = 0
                        
            except Exception as e:
                print(f"Error transforming column {col}: {str(e)}")
                continue
        
        print("Statistical transformations completed")
        return df_processed
    
    def fit_transform(self, df):
        """fit + transform במקום אחד"""
        self.fit(df)
        return self.transform(df)