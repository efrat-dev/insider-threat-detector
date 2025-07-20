import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from typing import List  

class DataTransformer:
    """מחלקה לטרנספורמציות נתונים"""
    
    def __init__(self):
        self.scalers = {}
        self.pca = None
    
    
    def feature_filtering(self, df: pd.DataFrame, method: str = 'correlation', threshold: float = 0.95) -> pd.DataFrame:
        """
        סינון תכונות מתקדם עם תמיכה בשיטות שונות
        
        Args:
            df: DataFrame עם הנתונים
            method: שיטת הסינון - 'correlation', 'variance', 'both'
            threshold: סף לסינון
        
        Returns:
            DataFrame מסונן
        """
        df_processed = df.copy()
        
        if method == 'correlation':
            redundant_features = self.identify_redundant_features_many_columns(df_processed, threshold)
            df_processed = df_processed.drop(columns=redundant_features)
            print(f"Dropped {len(redundant_features)} highly correlated features")
            
        elif method == 'variance':
            numeric_columns = df_processed.select_dtypes(include=[np.number]).columns
            variances = df_processed[numeric_columns].var()
            low_variance_cols = variances[variances < threshold].index.tolist()
            df_processed = df_processed.drop(columns=low_variance_cols)
            print(f"Dropped {len(low_variance_cols)} low variance features")
            
        elif method == 'both':
            # תחילה הסרת correlation
            redundant_features = self.identify_redundant_features_many_columns(df_processed, threshold)
            df_processed = df_processed.drop(columns=redundant_features)
            print(f"Dropped {len(redundant_features)} highly correlated features")
            
            # לאחר מכן הסרת variance נמוכה
            numeric_columns = df_processed.select_dtypes(include=[np.number]).columns
            variances = df_processed[numeric_columns].var()
            low_variance_cols = variances[variances < threshold].index.tolist()
            df_processed = df_processed.drop(columns=low_variance_cols)
            print(f"Dropped {len(low_variance_cols)} low variance features")
        
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
                corr_matrix = df_sample[chunk].corr().abs()
                
                # בדיקת כל זוגות עמודות בchunk
                for j in range(len(chunk)):
                    for k in range(j+1, len(chunk)):
                        if corr_matrix.iloc[j, k] > correlation_threshold:
                            col1, col2 = chunk[j], chunk[k]
                            redundant_features.add(col1 if len(col1) > len(col2) else col2)
        
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
    
    def normalize_features(self, df, method='standard'):
        """נורמליזציה/סטנדרטיזציה של תכונות"""
        df_processed = df.copy()
        numeric_columns = df_processed.select_dtypes(include=[np.number]).columns
        
        # הוצאת עמודות שלא צריכות נורמליזציה
        exclude_cols = ['employee_id', 'is_malicious']
        numeric_columns = [col for col in numeric_columns if col not in exclude_cols]
        
        if method == 'standard':
            scaler = StandardScaler()
            df_processed[numeric_columns] = scaler.fit_transform(df_processed[numeric_columns])
            self.scalers['standard'] = scaler
        
        elif method == 'minmax':
            scaler = MinMaxScaler()
            df_processed[numeric_columns] = scaler.fit_transform(df_processed[numeric_columns])
            self.scalers['minmax'] = scaler
        
        elif method == 'robust':
            scaler = RobustScaler()
            df_processed[numeric_columns] = scaler.fit_transform(df_processed[numeric_columns])
            self.scalers['robust'] = scaler
        
        print(f"Features normalized using {method} method")
        return df_processed