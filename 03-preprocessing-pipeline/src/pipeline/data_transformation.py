import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from typing import List  

class DataTransformer:
    """מחלקה לטרנספורמציות נתונים"""
    
    def __init__(self):
        self.scalers = {}
        self.pca = None
        self.fitted_params = {}
        self.is_fitted = False
    
    def fit_feature_filtering(self, df: pd.DataFrame, method: str = 'correlation', threshold: float = 0.95):
        """אימון פרמטרי סינון התכונות על נתוני הטריין"""
        print(f"Fitting feature filtering parameters with method: {method}, threshold: {threshold}")
        
        # שמירת פרמטרי הסינון
        self.fitted_params['filtering'] = {
            'method': method,
            'threshold': threshold
        }
        
        df_processed = df.copy()
        
        # זיהוי כל עמודות הטרנספורמציות הסטטיסטיות לצורך הגנה עליהן
        statistical_transformations = ['zscore', 'quartile']
        protected_columns = []
        
        for col in df_processed.columns:
            # בדיקה אם העמודה מסתיימת באחת מהטרנספורמציות הסטטיסטיות
            if any(col.endswith(f'_{transform}') for transform in statistical_transformations):
                protected_columns.append(col)
        
        # הוספת עמודות חשובות נוספות שלא רוצים למחוק
        essential_columns = ['employee_id', 'is_malicious', 'is_emp_malicious_binary', 'date']
        for col in essential_columns:
            if col in df_processed.columns and col not in protected_columns:
                protected_columns.append(col)
        
        self.fitted_params['filtering']['protected_columns'] = protected_columns
        print(f"Protected columns ({len(protected_columns)}): {protected_columns[:10]}..." if len(protected_columns) > 10 else protected_columns)
        
        # רשימת עמודות לשמירה
        columns_to_keep = list(df_processed.columns)
        
        if method == 'correlation':
            redundant_features = self.identify_redundant_features_many_columns(df_processed, threshold)
            # הסרת עמודות מוגנות מרשימת העמודות למחיקה
            redundant_features = [col for col in redundant_features if col not in protected_columns]
            columns_to_keep = [col for col in columns_to_keep if col not in redundant_features]
            print(f"Will drop {len(redundant_features)} highly correlated features (statistical transformations protected)")
            
        elif method == 'variance':
            numeric_columns = df_processed.select_dtypes(include=[np.number]).columns
            variances = df_processed[numeric_columns].var()
            low_variance_cols = variances[variances < threshold].index.tolist()
            # הסרת עמודות מוגנות מרשימת העמודות למחיקה
            low_variance_cols = [col for col in low_variance_cols if col not in protected_columns]
            columns_to_keep = [col for col in columns_to_keep if col not in low_variance_cols]
            print(f"Will drop {len(low_variance_cols)} low variance features (statistical transformations protected)")
            
        elif method == 'both':
            # תחילה הסרת correlation
            redundant_features = self.identify_redundant_features_many_columns(df_processed, threshold)
            redundant_features = [col for col in redundant_features if col not in protected_columns]
            columns_to_keep = [col for col in columns_to_keep if col not in redundant_features]
            print(f"Will drop {len(redundant_features)} highly correlated features (statistical transformations protected)")
            
            # לאחר מכן הסרת variance נמוכה
            remaining_df = df_processed[columns_to_keep]
            numeric_columns = remaining_df.select_dtypes(include=[np.number]).columns
            variances = remaining_df[numeric_columns].var()
            low_variance_cols = variances[variances < threshold].index.tolist()
            low_variance_cols = [col for col in low_variance_cols if col not in protected_columns]
            columns_to_keep = [col for col in columns_to_keep if col not in low_variance_cols]
            print(f"Will drop {len(low_variance_cols)} low variance features (statistical transformations protected)")
        
        # שמירת רשימת העמודות הסופית
        self.fitted_params['filtering']['selected_columns'] = columns_to_keep
        
        # החזרת הדאטה המסונן
        df_filtered = df[columns_to_keep].copy()
        
        print(f"Feature filtering fitted: {len(df.columns)} -> {len(columns_to_keep)} columns")
        
        # הדפסת סיכום של מה שהוסר
        removed_columns = [col for col in df.columns if col not in columns_to_keep]
        if removed_columns:
            print(f"Removed columns ({len(removed_columns)}): {removed_columns[:10]}..." if len(removed_columns) > 10 else removed_columns)
        
        return df_filtered
    
    def transform_feature_filtering(self, df: pd.DataFrame):
        """החלת סינון התכונות עם פרמטרים מהטריין"""
        if not self.fitted_params.get('filtering'):
            raise ValueError("Feature filtering must be fitted before transform")
        
        print("Transforming features using fitted filtering parameters...")
        
        selected_columns = self.fitted_params['filtering']['selected_columns']
        
        # שמירה על עמודות שקיימות בדאטה החדש
        available_columns = [col for col in selected_columns if col in df.columns]
        
        if len(available_columns) != len(selected_columns):
            missing_cols = set(selected_columns) - set(available_columns)
            print(f"Warning: {len(missing_cols)} columns from training are missing in transform data")
        
        df_processed = df[available_columns].copy()
        print(f"Feature filtering applied: {len(df.columns)} -> {len(df_processed.columns)} columns")
        
        return df_processed
    
    def fit_normalize_features(self, df, method='standard'):
        """אימון פרמטרי הנורמליזציה על נתוני הטריין"""
        print(f"Fitting normalization parameters with method: {method}")
        
        # שמירת פרמטרי הנורמליזציה
        self.fitted_params['normalization'] = {
            'method': method
        }
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        # הוצאת עמודות שלא צריכות נורמליזציה
        exclude_cols = ['employee_id', 'is_malicious', 'is_emp_malicious_binary', 'target']
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
    
    def identify_redundant_features_many_columns(self, df: pd.DataFrame, 
                                                correlation_threshold: float = 0.95,
                                                chunk_size: int = 50) -> List[str]:
        """זיהוי תכונות מיותרות - chunks עם בדיקה מלאה"""
        
        numerical_features = df.select_dtypes(include=[np.number]).columns
        
        if len(numerical_features) < 2:
            return []
        
        print(f"Processing {len(numerical_features)} features in chunks of {chunk_size}")
        
        # דגימת שורות (לא עמודות) אם הנתונים גדולים
        if len(df) > 10000:
            df_sample = df.sample(n=10000, random_state=42)
        else:
            df_sample = df
        
        redundant_features = set()
        
        # יצירת רשימת chunks
        chunks = []
        for i in range(0, len(numerical_features), chunk_size):
            chunks.append(numerical_features[i:i+chunk_size])
        
        print(f"Created {len(chunks)} chunks")
        
        # שלב 1: בדיקה בתוך כל chunk
        for chunk_idx, chunk in enumerate(chunks):
            if len(chunk) > 1:
                print(f"Processing within chunk {chunk_idx + 1}/{len(chunks)}")
                try:
                    corr_matrix = df_sample[chunk].corr().abs()
                    
                    # בדיקת כל זוגות עמודות בchunk
                    for j in range(len(chunk)):
                        for k in range(j+1, len(chunk)):
                            if corr_matrix.iloc[j, k] > correlation_threshold:
                                col1, col2 = chunk[j], chunk[k]
                                redundant_features.add(col1 if len(col1) > len(col2) else col2)
                except Exception as e:
                    print(f"Warning: Could not process chunk {chunk_idx + 1}: {e}")
                    continue
        
        # שלב 2: בדיקה בין כל זוגות chunks (בדיקה מלאה!)
        for i in range(len(chunks)):
            for j in range(i+1, len(chunks)):
                print(f"Checking between chunks {i+1} and {j+1}")
                
                chunk1, chunk2 = chunks[i], chunks[j]
                combined = list(chunk1) + list(chunk2)
                
                try:
                    corr_matrix = df_sample[combined].corr().abs()
                    
                    # בדיקת כל זוגות עמודות בין הchunks
                    for col1 in chunk1:
                        for col2 in chunk2:
                            if corr_matrix.loc[col1, col2] > correlation_threshold:
                                redundant_features.add(col1 if len(col1) > len(col2) else col2)
                
                except Exception as e:
                    print(f"Warning: Could not process chunks {i+1} and {j+1}: {e}")
                    continue
        
        print(f"Found {len(redundant_features)} redundant features")
        return list(redundant_features)
    
    def _process_features_standard(self, df_sample, numerical_features, correlation_threshold):
        """עבודה רגילה למספר קטן של עמודות (עד 100)"""
        corr_matrix = df_sample[numerical_features].corr().abs()
        
        # יצירת מטריצה משולשת עליונה
        upper_triangle = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        
        # מציאת עמודות עם correlation גבוה
        redundant_features = []
        for column in upper_triangle.columns:
            if any(upper_triangle[column] > correlation_threshold):
                redundant_features.append(column)
        
        return redundant_features