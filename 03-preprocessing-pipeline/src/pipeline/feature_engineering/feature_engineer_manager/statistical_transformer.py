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
    
    def apply_statistical_transforms(self, df):
        """החלת טרנספורמציות סטטיסטיות משופרות"""
        df_processed = df.copy()
        
        # זיהוי עמודות מספריות לטרנספורמציה
        numeric_columns = df_processed.select_dtypes(include=[np.number]).columns
        
        # הסרת עמודות מיוחדות
        exclude_cols = ['is_malicious', 'is_emp_malicious', 'date', 'timestamp']
        transform_columns = [col for col in numeric_columns if col not in exclude_cols]
        
        print(f"Applying statistical transforms to {len(transform_columns)} numeric columns")
        
        for col in transform_columns:
            if col in df_processed.columns:
                # בדיקת תקינות הנתונים
                if df_processed[col].isna().all() or df_processed[col].nunique() <= 1:
                    print(f"Skipping column {col} - insufficient data")
                    continue
                    
                try:
                    # טרנספורמציה לוגריתמית
                    if (df_processed[col] >= 0).all():
                        df_processed[f'{col}_log'] = np.log1p(df_processed[col])
                    
                    # טרנספורמציה שורש
                    if (df_processed[col] >= 0).all():
                        df_processed[f'{col}_sqrt'] = np.sqrt(df_processed[col])
                    
                    # Z-score (רק אם יש שונות)
                    if df_processed[col].std() > 0:
                        df_processed[f'{col}_zscore'] = stats.zscore(df_processed[col])
                    
                    # בינארי (מעל/מתחת לממוצע)
                    df_processed[f'{col}_above_mean'] = (df_processed[col] > df_processed[col].mean()).astype(int)
                    
                    # רבעונים עם טיפול טוב יותר
                    unique_values = df_processed[col].nunique()
                    
                    if unique_values >= 4:
                        try:
                            df_processed[f'{col}_quartile'] = pd.qcut(
                                df_processed[col], 
                                q=4, 
                                duplicates='drop'
                            )
                        except:
                            # fallback
                            median_val = df_processed[col].median()
                            df_processed[f'{col}_quartile'] = np.where(
                                df_processed[col] <= median_val, 0, 1
                            )
                    else:
                        df_processed[f'{col}_quartile'] = 0
                        
                except Exception as e:
                    print(f"Error transforming column {col}: {str(e)}")
        
        print("Statistical transformations completed")
        return df_processed