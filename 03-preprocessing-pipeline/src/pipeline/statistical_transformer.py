import pandas as pd
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
    
    def _safe_quartile_binning(self, data, column_name):
        """
        פונקציה בטוחה ליצירת רבעונים עם טיפול בגבולות כפולים
        """
        try:
            # ניסיון ראשון עם qcut (המדויק ביותר)
            quartiles = pd.qcut(data, q=4, labels=[0, 1, 2, 3], duplicates='drop')
            return quartiles.astype(int)
            
        except ValueError as e:
            # אם qcut נכשל, נשתמש בגישות חלופיות
            print(f"Warning: Column {column_name} - using alternative binning method")
            
            # בדיקת מספר ערכים ייחודיים
            unique_values = data.dropna().unique()
            n_unique = len(unique_values)
            
            if n_unique <= 1:
                # כל הערכים זהים
                return pd.Series([0] * len(data), index=data.index)
            
            elif n_unique == 2:
                # שני ערכים ייחודיים - חלוקה בינארית
                median_val = np.median(unique_values)
                return pd.cut(data, bins=[-np.inf, median_val, np.inf], 
                             labels=[0, 1], include_lowest=True).astype(int)
            
            elif n_unique == 3:
                # שלושה ערכים ייחודיים
                sorted_vals = np.sort(unique_values)
                bins = [-np.inf, 
                       (sorted_vals[0] + sorted_vals[1])/2,
                       (sorted_vals[1] + sorted_vals[2])/2, 
                       np.inf]
                return pd.cut(data, bins=bins, labels=[0, 1, 2], 
                             include_lowest=True).astype(int)
            
            else:
                # מספיק ערכים - השתמש ב-cut עם 4 bins
                try:
                    return pd.cut(data, bins=4, labels=[0, 1, 2, 3], 
                                 include_lowest=True).astype(int)
                except ValueError:
                    # אם גם cut נכשל, חזור לחלוקה פשוטה
                    quantiles = data.quantile([0.33, 0.66]).values
                    bins = [-np.inf] + quantiles.tolist() + [np.inf]
                    return pd.cut(data, bins=bins, labels=[0, 1, 2], 
                                 include_lowest=True).astype(int)
    
    def _can_create_quartiles(self, data):
        """
        בדיקה האם ניתן ליצור רבעונים משמעותיים עבור העמודה
        """
        # בדיקות בסיסיות
        if data.isna().all() or data.nunique() <= 1:
            return False, "insufficient_variance"
        
        # בדיקה לערכים כפולים ברבעונים
        try:
            quartiles = data.quantile([0.25, 0.5, 0.75]).values
            unique_quartiles = len(np.unique(quartiles))
            
            if unique_quartiles < 3:  # לפחות 3 גבולות ייחודיים
                return False, "duplicate_quartiles"
            
            return True, "ok"
            
        except Exception:
            return False, "calculation_error"
    
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
        quartile_successes = 0
        
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
                    
                    # פרמטרים לרבעונים (רק עבור isolation-forest)
                    if self.model_type == 'isolation-forest':
                        can_quartile, reason = self._can_create_quartiles(df[col])
                        
                        if can_quartile:
                            try:
                                # בדיקה מעמיקה - נסה ליצור רבעונים בפועל
                                test_quartiles = self._safe_quartile_binning(df[col], col)
                                
                                if test_quartiles is not None and len(test_quartiles.unique()) > 1:
                                    col_params['use_quartiles'] = True
                                    col_params['quartile_method'] = 'safe_binning'
                                    quartile_successes += 1
                                else:
                                    col_params['use_quartiles'] = False
                                    col_params['quartile_skip_reason'] = 'binning_failed'
                                    
                            except Exception as e:
                                col_params['use_quartiles'] = False
                                col_params['quartile_skip_reason'] = f'error: {str(e)}'
                                print(f"Quartile creation failed for {col}: {str(e)}")
                        else:
                            col_params['use_quartiles'] = False
                            col_params['quartile_skip_reason'] = reason
                    else:
                        col_params['use_quartiles'] = False
                    
                    # שמירת פרמטרי Z-score (לכל סוגי המודלים)
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
        
        # הדפסת סיכום מפורט
        if self.model_type == 'lstm':
            print(f"Statistical fitting completed for {successful_fits} columns (Z-score only for LSTM)")
        else:
            print(f"Statistical fitting completed for {successful_fits} columns")
            print(f"  - Z-score transformations: {len(self.scalers)}")
            print(f"  - Quartile transformations: {quartile_successes}")
            if successful_fits - quartile_successes > 0:
                print(f"  - Skipped quartiles (low variance/duplicates): {successful_fits - quartile_successes}")
        
        return df  
    
    def transform(self, df):
        """החלת הטרנספורמציות הסטטיסטיות עם פרמטרים מהטריין"""
        if not self.is_fitted:
            raise ValueError("StatisticalTransformer must be fitted before transform")
        
        print(f"Transforming data using fitted statistical parameters for {self.model_type} model...")
        df_processed = df.copy()
        
        transform_columns = self.fitted_params.get('transform_columns', [])
        zscore_successes = 0
        quartile_successes = 0
        
        for col in transform_columns:
            if col not in df_processed.columns or col not in self.fitted_params:
                continue
            
            col_params = self.fitted_params[col]
            
            try:
                # Z-score עם scaler מהטריין (לכל סוגי המודלים)
                if col_params.get('has_variance', False) and col in self.scalers:
                    try:
                        df_processed[f'{col}_zscore'] = self.scalers[col].transform(
                            df_processed[col].values.reshape(-1, 1)
                        ).flatten()
                        zscore_successes += 1
                    except Exception as e:
                        print(f"Error applying Z-score to {col}: {str(e)}")
                        continue
                
                # רבעונים רק עבור isolation-forest
                if (self.model_type == 'isolation-forest' and 
                    col_params.get('use_quartiles', False)):
                    try:
                        quartile_result = self._safe_quartile_binning(df_processed[col], col)
                        if quartile_result is not None:
                            df_processed[f'{col}_quartile'] = quartile_result
                            quartile_successes += 1
                        else:
                            print(f"Failed to create quartiles for {col}")
                            
                    except Exception as e:
                        print(f"Error applying quartiles to {col}: {str(e)}")
                        continue
                        
            except Exception as e:
                print(f"Error transforming column {col}: {str(e)}")
                continue
        
        # סיכום התוצאות
        if self.model_type == 'lstm':
            print(f"Statistical transformations completed - Z-score: {zscore_successes} columns")
        else:
            print(f"Statistical transformations completed - Z-score: {zscore_successes}, Quartiles: {quartile_successes} columns")
        
        return df_processed
    
    def fit_transform(self, df):
        """fit + transform במקום אחד"""
        self.fit(df)
        return self.transform(df)