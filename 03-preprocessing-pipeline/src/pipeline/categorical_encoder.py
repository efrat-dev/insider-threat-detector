import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class CategoricalEncoder:
    """מחלקה מיוחדת לקידוד משתנים קטגוריים"""
    
    def __init__(self):
        self.encoders = {}
        self.categorical_columns = []
        self.encoding_strategies = {}
        self.target_encodings = {}
        self.frequency_encodings = {}
        self.is_fitted = False
    
    def identify_all_categorical_columns(self, df):
        """זיהוי כל העמודות הקטגוריות/טקסטואליות ללא יצירת הגבלות"""
        categorical_columns = []
        
        # הגדרת עמודות שאסור לקודד (רק עמודות שבאמת לא צריכות קידוד)
        protected_columns = [
            'is_malicious',  # target column
            'is_emp_malicios',  # target column
            'target',        # target column
            'date',          # date columns שצריכות טיפול מיוחד
            'timestamp'      # timestamp columns
        ]
        
        # בדיקת כל עמודה
        for col in df.columns:
            if col in protected_columns:
                continue
                
            # בדיקת סוג הנתונים
            dtype = df[col].dtype
            
            # עמודות טקסט מפורשות
            if dtype in ['object', 'category']:
                categorical_columns.append(col)
                continue
            
            # עמודות מספריות שעשויות להיות קטגוריות
            if dtype in ['int64', 'int32', 'float64', 'float32']:
                unique_values = df[col].nunique()
                total_values = len(df[col])
                
                # אם יש מעט ערכים ייחודיים ביחס לכמות הנתונים
                if unique_values <= 50 and unique_values < total_values * 0.1:
                    sample_values = df[col].dropna().unique()[:10]
                    
                    # אם הערכים נראים כמו קטגוריות
                    if any(isinstance(val, (str, bool)) for val in sample_values):
                        categorical_columns.append(col)
                    elif unique_values <= 10:  # מספרים עם מעט ערכים
                        categorical_columns.append(col)
        
        return categorical_columns
    
    def fit_encode(self, df, target_col='is_malicious'):
        """למידת פרמטרי הקידוד מנתוני האימון"""
        print("Fitting categorical encoder...")
        
        # זיהוי כל העמודות הקטגוריות
        self.categorical_columns = self.identify_all_categorical_columns(df)
        
        # הוספת כל עמודות object שלא נתפסו
        object_columns = df.select_dtypes(include=['object']).columns
        for col in object_columns:
            if col not in self.categorical_columns and col not in ['is_malicious', 'is_emp_malicios', 'target', 'date', 'timestamp']:
                self.categorical_columns.append(col)
        
        print(f"Found {len(self.categorical_columns)} categorical columns to encode:")
        print(self.categorical_columns[:10])  # הצגת 10 הראשונות
        
        # למידת פרמטרי הקידוד לכל עמודה
        for col in self.categorical_columns:
            if col not in df.columns:
                continue
            
            print(f"Learning encoding for column: {col}")
            
            # המרה לטקסט
            col_data = df[col].astype(str)
            unique_values = col_data.nunique()
            
            try:
                if unique_values == 1:
                    # עמודה עם ערך יחיד - נסמן לדילוג
                    self.encoding_strategies[col] = 'skip'
                    print(f"  Column {col} has only one unique value, will skip")
                    
                elif unique_values == 2:
                    # קידוד בינארי פשוט
                    self.encoding_strategies[col] = 'binary'
                    encoder = LabelEncoder()
                    encoder.fit(col_data.fillna('missing'))
                    self.encoders[col] = encoder
                    
                elif unique_values <= 10:
                    # One-hot encoding + label encoding
                    self.encoding_strategies[col] = 'onehot_label'
                    encoder = LabelEncoder()
                    encoder.fit(col_data.fillna('missing'))
                    self.encoders[col] = encoder
                    
                elif unique_values <= 50:
                    # Label + Target + Frequency encoding
                    self.encoding_strategies[col] = 'multi'
                    encoder = LabelEncoder()
                    encoder.fit(col_data.fillna('missing'))
                    self.encoders[col] = encoder
                    
                    # למידת target encoding
                    if target_col in df.columns:
                        target_mean = df.groupby(col)[target_col].mean()
                        global_mean = df[target_col].mean()
                        self.target_encodings[col] = target_mean.to_dict()
                        self.target_encodings[f'{col}_global_mean'] = global_mean
                    
                    # למידת frequency encoding
                    freq_map = col_data.value_counts().to_dict()
                    self.frequency_encodings[col] = freq_map
                    
                else:
                    # עמודות עם cardinality גבוה
                    self.encoding_strategies[col] = 'high_cardinality'
                    
                    # למידת frequency encoding
                    freq_map = col_data.value_counts().to_dict()
                    self.frequency_encodings[col] = freq_map
                    
                    # למידת target encoding
                    if target_col in df.columns:
                        target_mean = df.groupby(col)[target_col].mean()
                        global_mean = df[target_col].mean()
                        self.target_encodings[col] = target_mean.to_dict()
                        self.target_encodings[f'{col}_global_mean'] = global_mean
                
                print(f"  Successfully learned encoding for {col} with {unique_values} unique values")
                
            except Exception as e:
                print(f"  Error learning encoding for column {col}: {str(e)}")
                # fallback strategy
                self.encoding_strategies[col] = 'fallback'
                try:
                    encoder = LabelEncoder()
                    encoder.fit(col_data.fillna('missing'))
                    self.encoders[col] = encoder
                except:
                    print(f"  Failed to learn encoding for {col} even with fallback method")
                    self.encoding_strategies[col] = 'skip'
        
        self.is_fitted = True
        print("Categorical encoder fitting completed!")
        
        # החלת הקידוד על נתוני האימון
        return self.transform_encode(df)
    
    def transform_encode(self, df):
        """החלת הקידוד על נתונים חדשים"""
        if not self.is_fitted:
            raise ValueError("Encoder must be fitted before transform")
        
        print("Transforming categorical variables...")
        df_processed = df.copy()
        
        encoded_features = []
        columns_to_drop = []
        
        for col in self.categorical_columns:
            if col not in df_processed.columns:
                continue
            
            strategy = self.encoding_strategies.get(col, 'skip')
            
            if strategy == 'skip':
                columns_to_drop.append(col)
                continue
            
            print(f"Transforming column: {col} with strategy: {strategy}")
            
            # המרה לטקסט
            col_data = df_processed[col].astype(str).fillna('missing')
            
            try:
                if strategy == 'binary':
                    # קידוד בינארי
                    encoder = self.encoders[col]
                    # טיפול בערכים לא מוכרים
                    known_values = encoder.classes_
                    col_data_safe = col_data.apply(lambda x: x if x in known_values else 'missing')
                    df_processed[f'{col}_binary'] = encoder.transform(col_data_safe)
                    encoded_features.append(f'{col}_binary')
                    columns_to_drop.append(col)
                    
                elif strategy == 'onehot_label':
                    # One-hot encoding
                    # טיפול בערכים לא מוכרים עבור one-hot
                    unique_train_values = self.encoders[col].classes_
                    for val in unique_train_values:
                        if val != 'missing':
                            df_processed[f'{col}_cat_{val}'] = (col_data == val).astype(int)
                            encoded_features.append(f'{col}_cat_{val}')
                    
                    # Label encoding
                    encoder = self.encoders[col]
                    col_data_safe = col_data.apply(lambda x: x if x in encoder.classes_ else 'missing')
                    df_processed[f'{col}_label'] = encoder.transform(col_data_safe)
                    encoded_features.append(f'{col}_label')
                    columns_to_drop.append(col)
                    
                elif strategy == 'multi':
                    # Label encoding
                    encoder = self.encoders[col]
                    col_data_safe = col_data.apply(lambda x: x if x in encoder.classes_ else 'missing')
                    df_processed[f'{col}_label'] = encoder.transform(col_data_safe)
                    encoded_features.append(f'{col}_label')
                    
                    # Target encoding
                    if col in self.target_encodings:
                        target_map = self.target_encodings[col]
                        global_mean = self.target_encodings[f'{col}_global_mean']
                        df_processed[f'{col}_target'] = col_data.map(target_map).fillna(global_mean)
                        encoded_features.append(f'{col}_target')
                    
                    # Frequency encoding
                    if col in self.frequency_encodings:
                        freq_map = self.frequency_encodings[col]
                        df_processed[f'{col}_freq'] = col_data.map(freq_map).fillna(0)
                        encoded_features.append(f'{col}_freq')
                    
                    columns_to_drop.append(col)
                    
                elif strategy == 'high_cardinality':
                    # Frequency encoding
                    if col in self.frequency_encodings:
                        freq_map = self.frequency_encodings[col]
                        df_processed[f'{col}_freq'] = col_data.map(freq_map).fillna(0)
                        encoded_features.append(f'{col}_freq')
                    
                    # Target encoding
                    if col in self.target_encodings:
                        target_map = self.target_encodings[col]
                        global_mean = self.target_encodings[f'{col}_global_mean']
                        df_processed[f'{col}_target'] = col_data.map(target_map).fillna(global_mean)
                        encoded_features.append(f'{col}_target')
                    
                    # Hash encoding לעמודות עם cardinality גבוה מאוד
                    unique_values = col_data.nunique()
                    if unique_values > 100:
                        df_processed[f'{col}_hash'] = col_data.apply(lambda x: hash(str(x)) % 1000)
                        encoded_features.append(f'{col}_hash')
                    
                    columns_to_drop.append(col)
                    
                elif strategy == 'fallback':
                    # fallback - רק label encoding
                    encoder = self.encoders[col]
                    col_data_safe = col_data.apply(lambda x: x if x in encoder.classes_ else 'missing')
                    df_processed[f'{col}_fallback'] = encoder.transform(col_data_safe)
                    encoded_features.append(f'{col}_fallback')
                    columns_to_drop.append(col)
                
                print(f"  Successfully transformed {col}")
                
            except Exception as e:
                print(f"  Error transforming column {col}: {str(e)}")
                columns_to_drop.append(col)
        
        # מחיקת העמודות המקוריות
        existing_columns_to_drop = [col for col in columns_to_drop if col in df_processed.columns]
        if existing_columns_to_drop:
            df_processed = df_processed.drop(columns=existing_columns_to_drop)
            print(f"Dropped {len(existing_columns_to_drop)} original categorical columns")
        
        print(f"Categorical encoding completed! Created {len(encoded_features)} new encoded features")
        return df_processed