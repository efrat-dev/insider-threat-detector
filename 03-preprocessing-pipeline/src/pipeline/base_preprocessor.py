import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class InsiderThreatPreprocessor:
    """מחלקה עיקרית לעיבוד מקדים של נתוני Insider Threat"""
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.feature_names = None
        self.selected_features = None
        self.pca = None
        self.imputers = {}
        
    def load_data(self, filepath):
        """טעינת הנתונים מקובץ"""
        try:
            if filepath.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif filepath.endswith('.xlsx'):
                df = pd.read_excel(filepath)
            else:
                raise ValueError("Unsupported file format")
            
            print(f"Data loaded successfully: {df.shape}")
            print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def analyze_missing_values(self, df):
        """ניתוח ערכים חסרים"""
        missing_info = pd.DataFrame({
            'Column': df.columns,
            'Missing_Count': df.isnull().sum(),
            'Missing_Percentage': (df.isnull().sum() / len(df)) * 100
        })
        missing_info = missing_info[missing_info['Missing_Count'] > 0].sort_values('Missing_Percentage', ascending=False)
        
        print("Missing Values Analysis:")
        print(missing_info)
        return missing_info
    
    def split_dataset(self, df, test_size=0.2, val_size=0.1, random_state=42):
        """חלוקת הנתונים לטיפול בלתי מאוזן"""
        if 'is_malicious' not in df.columns:
            raise ValueError("Target column 'is_malicious' not found")
        
        X = df.drop('is_malicious', axis=1)
        y = df['is_malicious']
        
        # חלוקה ראשונה לטריין וטסט
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # חלוקה שנייה לטריין וולידציה
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=val_size/(1-test_size), random_state=random_state, stratify=y_train
        )
        
        print(f"Dataset split completed:")
        print(f"  Training set: {X_train.shape[0]} samples")
        print(f"  Validation set: {X_val.shape[0]} samples")
        print(f"  Test set: {X_test.shape[0]} samples")
        print(f"  Malicious cases - Train: {y_train.sum()}, Val: {y_val.sum()}, Test: {y_test.sum()}")
        
        return X_train, X_val, X_test, y_train, y_val, y_test