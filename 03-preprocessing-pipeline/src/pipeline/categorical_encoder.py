import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class CategoricalEncoder:
    """מחלקה מיוחדת לקידוד משתנים קטגוריים - גרסה מותאמת לצמצום תכונות"""
    
    def __init__(self):
        """אתחול המחלקה עם פרמטרים מותאמים לצמצום תכונות"""
        self.encoders = {}
        self.categorical_columns = []
        self.encoding_strategies = {}
        self.target_encodings = {}
        self.frequency_encodings = {}
        self.category_groupings = {}  # לשמירת קיבוצי קטגוריות
        self.is_fitted = False
        # פרמטרים מותאמים לצמצום תכונות
        self.max_onehot_categories = 3  # רק עד 3 ערכים יקבלו one-hot
        self.max_categories_for_detailed_encoding = 10  # רק עד 10 ערכים יקבלו קידוד מפורט
    
    def group_rare_categories(self, df, col, min_frequency=100):
        """קיבוץ קטגוריות נדירות יחד"""
        value_counts = df[col].value_counts()
        rare_categories = value_counts[value_counts < min_frequency].index.tolist()
        
        if len(rare_categories) > 1:
            # יצירת מיפוי לקיבוץ קטגוריות נדירות
            grouping_map = {}
            for cat in rare_categories:
                grouping_map[cat] = 'OTHER_RARE'
            
            return grouping_map
        return {}
        
    def identify_all_categorical_columns(self, df):
        """זיהוי כל העמודות הקטגוריות/טקסטואליות"""
        categorical_columns = []
        
        protected_columns = [
            'is_malicious', 'is_emp_malicios', 'target',
            'date', 'timestamp'
        ]
        
        for col in df.columns:
            if col in protected_columns:
                continue
                
            dtype = df[col].dtype
            
            if dtype in ['object', 'category']:
                categorical_columns.append(col)
                continue
            
            if dtype in ['int64', 'int32', 'float64', 'float32']:
                unique_values = df[col].nunique()
                total_values = len(df[col])
                
                if unique_values <= 50 and unique_values < total_values * 0.1:
                    sample_values = df[col].dropna().unique()[:10]
                    
                    if any(isinstance(val, (str, bool)) for val in sample_values):
                        categorical_columns.append(col)
                    elif unique_values <= 10:
                        categorical_columns.append(col)
        
        return categorical_columns
    
    def fit_encode(self, df, target_col='is_malicious'):
        """למידת פרמטרי הקידוד מנתוני האימון - גרסה מותאמת"""
        print("Fitting categorical encoder...")
        
        self.categorical_columns = self.identify_all_categorical_columns(df)
        
        # הוספת עמודות object
        object_columns = df.select_dtypes(include=['object']).columns
        for col in object_columns:
            if col not in self.categorical_columns and col not in ['is_malicious', 'is_emp_malicios', 'target', 'date', 'timestamp']:
                self.categorical_columns.append(col)
                
        for col in self.categorical_columns:
            if col not in df.columns:
                continue
                        
            # העתקת הנתונים לעבודה
            df_work = df.copy()
            col_data = df_work[col].astype(str)
            unique_values = col_data.nunique()
            
            try:
                if unique_values == 1:
                    self.encoding_strategies[col] = 'skip'
                    
                elif unique_values == 2:
                    # קידוד בינארי פשוט
                    self.encoding_strategies[col] = 'binary'
                    encoder = LabelEncoder()
                    encoder.fit(col_data.fillna('missing'))
                    self.encoders[col] = encoder
                    
                elif unique_values <= self.max_onehot_categories:
                    # One-hot encoding בלבד (ללא label)
                    self.encoding_strategies[col] = 'onehot_only'
                    encoder = LabelEncoder()
                    encoder.fit(col_data.fillna('missing'))
                    self.encoders[col] = encoder
                    
                elif unique_values <= self.max_categories_for_detailed_encoding:
                    # Target encoding + Frequency encoding (ללא one-hot)
                    self.encoding_strategies[col] = 'target_freq'
                    
                    # למידת target encoding
                    if target_col in df.columns:
                        target_mean = df_work.groupby(col)[target_col].mean()
                        global_mean = df_work[target_col].mean()
                        self.target_encodings[col] = target_mean.to_dict()
                        self.target_encodings[f'{col}_global_mean'] = global_mean
                    
                    # למידת frequency encoding
                    freq_map = col_data.value_counts().to_dict()
                    self.frequency_encodings[col] = freq_map
                    
                else:
                    # עמודות עם cardinality גבוה - קיבוץ קטגוריות
                    print(f"  High cardinality column {col} ({unique_values} unique values) - applying grouping")
                    
                    # ניסיון קיבוץ חכם
                    # אם עדיין יותר מדי קטגוריות, קבץ נדירות
                    if unique_values > self.max_categories_for_detailed_encoding:
                        rare_grouping = self.group_rare_categories(df_work, col, min_frequency=50)
                        if rare_grouping:
                            existing_grouping = self.category_groupings.get(col, {})
                            existing_grouping.update(rare_grouping)
                            self.category_groupings[col] = existing_grouping
                            
                            df_work[col] = df_work[col].map(rare_grouping).fillna(df_work[col])
                            col_data = df_work[col].astype(str)
                            unique_values = col_data.nunique()
                            print(f"    Applied rare category grouping, reduced to {unique_values} categories")
                    
                    # קידוד לאחר הקיבוץ
                    if unique_values <= self.max_categories_for_detailed_encoding:
                        self.encoding_strategies[col] = 'target_freq'
                        
                        # למידת target encoding
                        if target_col in df_work.columns:
                            target_mean = df_work.groupby(col)[target_col].mean()
                            global_mean = df_work[target_col].mean()
                            self.target_encodings[col] = target_mean.to_dict()
                            self.target_encodings[f'{col}_global_mean'] = global_mean
                        
                        # למידת frequency encoding
                        freq_map = col_data.value_counts().to_dict()
                        self.frequency_encodings[col] = freq_map
                    else:
                        # אם עדיין יותר מדי - רק frequency ו-hash
                        self.encoding_strategies[col] = 'minimal'
                        freq_map = col_data.value_counts().to_dict()
                        self.frequency_encodings[col] = freq_map
                                
            except Exception as e:
                print(f"  Error learning encoding for column {col}: {str(e)}")
                self.encoding_strategies[col] = 'skip'
        
        self.is_fitted = True
        print("Categorical encoder fitting completed!")
        
        return self.transform_encode(df)
    
    def transform_encode(self, df):
        """החלת הקידוד על נתונים - גרסה מותאמת"""
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
                        
            # החלת קיבוצי קטגוריות אם קיימים
            col_data = df_processed[col].astype(str).fillna('missing')
            if col in self.category_groupings:
                col_data = col_data.map(self.category_groupings[col]).fillna(col_data)
            
            try:
                if strategy == 'binary':
                    encoder = self.encoders[col]
                    known_values = encoder.classes_
                    col_data_safe = col_data.apply(lambda x: x if x in known_values else 'missing')
                    df_processed[f'{col}_binary'] = encoder.transform(col_data_safe)
                    encoded_features.append(f'{col}_binary')
                    columns_to_drop.append(col)
                    
                elif strategy == 'onehot_only':
                    # רק One-hot encoding (ללא label)
                    unique_train_values = self.encoders[col].classes_
                    for val in unique_train_values:
                        if val != 'missing':
                            df_processed[f'{col}_cat_{val}'] = (col_data == val).astype(int)
                            encoded_features.append(f'{col}_cat_{val}')
                    columns_to_drop.append(col)
                    
                elif strategy == 'target_freq':
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
                    
                elif strategy == 'minimal':
                    # רק frequency encoding לעמודות עם cardinality גבוה מאוד
                    if col in self.frequency_encodings:
                        freq_map = self.frequency_encodings[col]
                        df_processed[f'{col}_freq'] = col_data.map(freq_map).fillna(0)
                        encoded_features.append(f'{col}_freq')
                    
                    columns_to_drop.append(col)
                                
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
