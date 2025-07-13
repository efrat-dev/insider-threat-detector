import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.decomposition import PCA

class DataTransformer:
    """מחלקה לטרנספורמציות נתונים"""
    
    def __init__(self):
        self.scalers = {}
        self.pca = None
        
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