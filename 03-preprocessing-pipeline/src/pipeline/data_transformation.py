import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.decomposition import PCA
from typing import List, Dict, Tuple, Optional  # הוספת הimports החסרים

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
                                            correlation_threshold: float = 0.95) -> List[str]:
        """זיהוי תכונות מיותרות - מטפל ביעילות במאות עמודות"""
        
        numerical_features = df.select_dtypes(include=[np.number]).columns
        
        if len(numerical_features) < 2:
            return []
        
        print(f"Processing {len(numerical_features)} numerical features")
        
        # דגימה חכמה לפי גודל הנתונים
        if len(df) > 50000:
            sample_size = 15000
        elif len(df) > 20000:
            sample_size = 10000
        elif len(df) > 10000:
            sample_size = 5000
        else:
            sample_size = len(df)
        
        if len(df) > sample_size:
            df_sample = df.sample(n=sample_size, random_state=42)
        else:
            df_sample = df
        
        # **גישה 1: עבודה בחלקים (chunks) למספר גדול של עמודות**
        if len(numerical_features) > 300:
            print("Using chunked processing for large number of features")
            return self._process_features_in_chunks(df_sample, numerical_features, correlation_threshold)
        
        # **גישה 2: אלגוריתם מיון מהיר לעמודות בינוניות**
        elif len(numerical_features) > 100:
            print("Using optimized processing for medium number of features")
            return self._process_features_optimized(df_sample, numerical_features, correlation_threshold)
        
        # **גישה 3: עבודה רגילה למספר קטן של עמודות**
        else:
            print("Using standard processing")
            return self._process_features_standard(df_sample, numerical_features, correlation_threshold)

    def _process_features_in_chunks(self, df_sample, numerical_features, correlation_threshold):
        """עבודה בחלקים - למאות עמודות"""
        chunk_size = 150
        all_redundant = set()
        
        # שלב 1: בדיקת correlation בתוך כל chunk
        for i in range(0, len(numerical_features), chunk_size):
            chunk_features = numerical_features[i:i+chunk_size]
            print(f"Processing chunk {i//chunk_size + 1}: columns {i} to {min(i+chunk_size, len(numerical_features))}")
            
            chunk_corr = df_sample[chunk_features].corr().abs()
            
            # מציאת redundant features בchunk זה
            mask = np.triu(np.ones(chunk_corr.shape, dtype=bool), k=1)
            high_corr_indices = np.where((chunk_corr.values > correlation_threshold) & mask)
            
            for idx_i, idx_j in zip(high_corr_indices[0], high_corr_indices[1]):
                col1 = chunk_features[idx_i]
                col2 = chunk_features[idx_j]
                
                if len(col1) > len(col2):
                    all_redundant.add(col1)
                else:
                    all_redundant.add(col2)
        
        # שלב 2: בדיקת correlation בין chunks (אופציונלי)
        if len(all_redundant) < len(numerical_features) * 0.5:  # אם לא מצאנו הרבה redundant
            print("Checking cross-chunk correlations...")
            all_redundant.update(self._check_cross_chunk_correlations(
                df_sample, numerical_features, correlation_threshold, chunk_size
            ))
        
        return list(all_redundant)

    def _check_cross_chunk_correlations(self, df_sample, numerical_features, correlation_threshold, chunk_size):
        """בדיקת correlation בין chunks שונים"""
        cross_redundant = set()
        
        # בדיקה רק של דגימה מכל chunk
        for i in range(0, len(numerical_features), chunk_size):
            chunk1 = numerical_features[i:i+min(50, chunk_size)]  # דגימה מהchunk הראשון
            
            for j in range(i+chunk_size, len(numerical_features), chunk_size):
                chunk2 = numerical_features[j:j+min(50, chunk_size)]  # דגימה מהchunk השני
                
                if len(chunk1) > 0 and len(chunk2) > 0:
                    combined_features = list(chunk1) + list(chunk2)
                    combined_corr = df_sample[combined_features].corr().abs()
                    
                    # בדיקה רק בין החלקים
                    for col1 in chunk1:
                        for col2 in chunk2:
                            if combined_corr.loc[col1, col2] > correlation_threshold:
                                if len(col1) > len(col2):
                                    cross_redundant.add(col1)
                                else:
                                    cross_redundant.add(col2)
        
        return cross_redundant
    
    def _process_features_optimized(self, df_sample, numerical_features, correlation_threshold):
        """אלגוריתם מותאם לעמודות בינוניות (100-300)"""
        redundant_features = set()
        
        # חישוב correlation matrix בחלקים קטנים יותר
        batch_size = 50
        processed_pairs = set()
        
        for i in range(0, len(numerical_features), batch_size):
            batch1 = numerical_features[i:i+batch_size]
            
            for j in range(i, len(numerical_features), batch_size):
                batch2 = numerical_features[j:j+batch_size]
                
                # אם זה אותו batch, נבדק רק את המשולש העליון
                if i == j:
                    batch_corr = df_sample[batch1].corr().abs()
                    mask = np.triu(np.ones(batch_corr.shape, dtype=bool), k=1)
                    high_corr_indices = np.where((batch_corr.values > correlation_threshold) & mask)
                    
                    for idx_i, idx_j in zip(high_corr_indices[0], high_corr_indices[1]):
                        col1 = batch1[idx_i]
                        col2 = batch1[idx_j]
                        
                        if len(col1) > len(col2):
                            redundant_features.add(col1)
                        else:
                            redundant_features.add(col2)
                
                # אם זה batches שונים, נבדק את כל הצירופים
                elif i < j:
                    combined_features = list(batch1) + list(batch2)
                    combined_corr = df_sample[combined_features].corr().abs()
                    
                    for col1 in batch1:
                        for col2 in batch2:
                            if combined_corr.loc[col1, col2] > correlation_threshold:
                                if len(col1) > len(col2):
                                    redundant_features.add(col1)
                                else:
                                    redundant_features.add(col2)
        
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
    
    def get_feature_importance_report(self, df: pd.DataFrame, removed_features: List[str]) -> dict:
        """דוח על התכונות שהוסרו"""
        report = {
            'original_features': len(df.columns),
            'removed_features': len(removed_features),
            'remaining_features': len(df.columns) - len(removed_features),
            'removal_percentage': (len(removed_features) / len(df.columns)) * 100,
            'removed_feature_names': removed_features
        }
        
        return report

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
    
    def dimensionality_reduction(self, df, method='pca', n_components=0.95):
        """הפחתת מימדיות"""
        df_processed = df.copy()
        
        # הכנת הנתונים
        feature_columns = df_processed.select_dtypes(include=[np.number]).columns
        exclude_cols = ['employee_id', 'is_malicious']
        feature_columns = [col for col in feature_columns if col not in exclude_cols]
        
        X = df_processed[feature_columns]
        
        if method == 'pca':
            self.pca = PCA(n_components=n_components)
            X_transformed = self.pca.fit_transform(X)
            
            # יצירת DataFrame חדש עם הרכיבים העיקריים
            pca_columns = [f'PC{i+1}' for i in range(X_transformed.shape[1])]
            df_pca = pd.DataFrame(X_transformed, columns=pca_columns, index=df_processed.index)
            
            # שמירת עמודות לא נומריות
            non_numeric_cols = df_processed.select_dtypes(exclude=[np.number]).columns
            for col in non_numeric_cols:
                df_pca[col] = df_processed[col]
            
            # שמירת עמודות חשובות
            for col in exclude_cols:
                if col in df_processed.columns:
                    df_pca[col] = df_processed[col]
            
            print(f"PCA completed: {X_transformed.shape[1]} components explain {self.pca.explained_variance_ratio_.sum():.3f} of variance")
            return df_pca
        
        return df_processed