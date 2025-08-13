from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class CategoricalEncoder:
    """
    Specialized class for encoding categorical variables - version optimized for feature reduction.
    
    This encoder uses different strategies based on the cardinality (number of unique values) 
    of categorical columns to minimize the number of output features while preserving information.
    """
    
    def __init__(self):
        """
        Initialize the encoder with parameters optimized for feature reduction.
        
        Attributes:
            encoders (dict): Stores sklearn LabelEncoders for specific columns
            categorical_columns (list): List of identified categorical column names
            encoding_strategies (dict): Maps column names to their encoding strategy
            target_encodings (dict): Stores target encoding mappings for each column
            frequency_encodings (dict): Stores frequency encoding mappings for each column
            category_groupings (dict): Stores rare category groupings for dimensionality reduction
            is_fitted (bool): Flag indicating if the encoder has been trained
            max_onehot_categories (int): Maximum categories for one-hot encoding (default: 3)
            max_categories_for_detailed_encoding (int): Maximum categories for detailed encoding (default: 10)
        """
        self.encoders = {}
        self.categorical_columns = []
        self.encoding_strategies = {}
        self.target_encodings = {}
        self.frequency_encodings = {}
        self.category_groupings = {}  
        self.is_fitted = False
        # Parameters optimized for feature reduction
        self.max_onehot_categories = 3  
        self.max_categories_for_detailed_encoding = 10  
    
    def group_rare_categories(self, df, col, min_frequency=100):
        """
        Group rare categories together to reduce feature dimensionality.
        
        This method identifies categories that appear infrequently and groups them
        under a single 'OTHER_RARE' category to prevent creating too many sparse features.
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            col (str): Column name to process
            min_frequency (int): Minimum frequency threshold (default: 100)
            
        Returns:
            dict: Mapping dictionary for rare categories to 'OTHER_RARE', empty dict if no grouping needed
        """
        value_counts = df[col].value_counts()
        rare_categories = value_counts[value_counts < min_frequency].index.tolist()
        
        if len(rare_categories) > 1:
            # Create mapping for grouping rare categories
            grouping_map = {}
            for cat in rare_categories:
                grouping_map[cat] = 'OTHER_RARE'
            
            return grouping_map
        return {}
        
    def identify_all_categorical_columns(self, df):
        """
        Identify all categorical/textual columns in the dataframe.
        
        This method uses multiple heuristics to identify categorical columns:
        1. Object/category dtypes are automatically categorical
        2. Numeric columns with low cardinality (<50 unique values and <10% of total) are considered categorical
        3. Columns containing string or boolean values are categorical
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            list: List of column names identified as categorical
        """
        categorical_columns = []
        
        # Protected columns that should not be encoded
        protected_columns = [
            'is_malicious', 'is_emp_malicios', 'target',
            'date', 'timestamp'
        ]
        
        for col in df.columns:
            if col in protected_columns:
                continue
                
            dtype = df[col].dtype
            
            # Check for explicit categorical/object types
            if dtype in ['object', 'category']:
                categorical_columns.append(col)
                continue
            
            # Check numeric columns that might be categorical
            if dtype in ['int64', 'int32', 'float64', 'float32']:
                unique_values = df[col].nunique()
                total_values = len(df[col])
                
                # Low cardinality heuristic: ≤50 unique values and <10% of total records
                if unique_values <= 50 and unique_values < total_values * 0.1:
                    sample_values = df[col].dropna().unique()[:10]
                    
                    # Check if contains strings or booleans, or very low cardinality
                    if any(isinstance(val, (str, bool)) for val in sample_values):
                        categorical_columns.append(col)
                    elif unique_values <= 10:
                        categorical_columns.append(col)
        
        return categorical_columns
    
    def fit_encode(self, df, target_col='is_malicious'):
        """
        Learn encoding parameters from training data - version optimized for feature reduction.
        
        This method analyzes each categorical column and determines the optimal encoding strategy
        based on its cardinality, then learns the necessary parameters for transformation.
        
        Encoding Strategy Selection:
        - 1 unique value: Skip (constant column)
        - 2 unique values: Binary encoding (LabelEncoder)
        - 3 unique values: One-hot encoding only
        - 4-10 unique values: Target encoding + Frequency encoding
        - >10 unique values: Attempt rare category grouping, then apply appropriate strategy
        
        Args:
            df (pd.DataFrame): Training dataframe
            target_col (str): Target column name for target encoding (default: 'is_malicious')
            
        Returns:
            pd.DataFrame: Transformed dataframe with encoded features
        """
        
        self.categorical_columns = self.identify_all_categorical_columns(df)
        
        # Add any object columns that might have been missed
        object_columns = df.select_dtypes(include=['object']).columns
        for col in object_columns:
            if col not in self.categorical_columns and col not in ['is_malicious', 'is_emp_malicios', 'target', 'date', 'timestamp']:
                self.categorical_columns.append(col)
                
        for col in self.categorical_columns:
            if col not in df.columns:
                continue
                        
            df_work = df.copy()
            col_data = df_work[col].astype(str)
            unique_values = col_data.nunique()
            
            try:
                # Strategy selection based on cardinality
                if unique_values == 1:
                    self.encoding_strategies[col] = 'skip'
                    
                elif unique_values == 2:
                    self.encoding_strategies[col] = 'binary'
                    encoder = LabelEncoder()
                    encoder.fit(col_data.fillna('missing'))
                    self.encoders[col] = encoder
                    
                elif unique_values <= self.max_onehot_categories:
                    # One-hot encoding only (no label encoding to avoid redundancy)
                    self.encoding_strategies[col] = 'onehot_only'
                    encoder = LabelEncoder()
                    encoder.fit(col_data.fillna('missing'))
                    self.encoders[col] = encoder
                    
                elif unique_values <= self.max_categories_for_detailed_encoding:
                    # Target encoding + Frequency encoding (no one-hot to reduce features)
                    self.encoding_strategies[col] = 'target_freq'
                    
                    # Learn target encoding parameters
                    if target_col in df.columns:
                        target_mean = df_work.groupby(col)[target_col].mean()
                        global_mean = df_work[target_col].mean()
                        self.target_encodings[col] = target_mean.to_dict()
                        self.target_encodings[f'{col}_global_mean'] = global_mean
                    
                    # Learn frequency encoding parameters
                    freq_map = col_data.value_counts().to_dict()
                    self.frequency_encodings[col] = freq_map
                    
                else:                    
                    # High cardinality - attempt smart grouping
                    # If still too many categories, group rare ones
                    if unique_values > self.max_categories_for_detailed_encoding:
                        rare_grouping = self.group_rare_categories(df_work, col, min_frequency=50)
                        if rare_grouping:
                            existing_grouping = self.category_groupings.get(col, {})
                            existing_grouping.update(rare_grouping)
                            self.category_groupings[col] = existing_grouping
                            
                            # Apply grouping and recalculate cardinality
                            df_work[col] = df_work[col].map(rare_grouping).fillna(df_work[col])
                            col_data = df_work[col].astype(str)
                            unique_values = col_data.nunique()
                    
                    # Re-evaluate encoding strategy after grouping
                    if unique_values <= self.max_categories_for_detailed_encoding:
                        self.encoding_strategies[col] = 'target_freq'
                        
                        # Learn target encoding parameters
                        if target_col in df_work.columns:
                            target_mean = df_work.groupby(col)[target_col].mean()
                            global_mean = df_work[target_col].mean()
                            self.target_encodings[col] = target_mean.to_dict()
                            self.target_encodings[f'{col}_global_mean'] = global_mean
                        
                        # Learn frequency encoding parameters
                        freq_map = col_data.value_counts().to_dict()
                        self.frequency_encodings[col] = freq_map
                    else:
                        # Still too many categories - minimal encoding (frequency + hash only)
                        self.encoding_strategies[col] = 'minimal'
                        freq_map = col_data.value_counts().to_dict()
                        self.frequency_encodings[col] = freq_map
                                
            except Exception as e:
                print(f"  Error learning encoding for column {col}: {str(e)}")
                self.encoding_strategies[col] = 'skip'
        
        self.is_fitted = True
        
        return self.transform_encode(df)
    
    def transform_encode(self, df):
        """
        Apply learned encoding to data - optimized version for feature reduction.
        
        This method applies the encoding strategies learned during fit_encode to transform
        categorical columns into numerical features using the appropriate method for each column.
        
        Transformation Process:
        1. Apply category groupings if they exist
        2. Apply the appropriate encoding strategy
        3. Handle unknown categories gracefully (fallback to defaults)
        4. Remove original categorical columns
        
        Args:
            df (pd.DataFrame): DataFrame to transform
            
        Returns:
            pd.DataFrame: Transformed dataframe with encoded features
            
        Raises:
            ValueError: If encoder hasn't been fitted yet
        """
        if not self.is_fitted:
            raise ValueError("Encoder must be fitted before transform")
        
        df_processed = df.copy()
        
        encoded_features = []
        columns_to_drop = []
        
        # Process each categorical column according to its learned strategy
        for col in self.categorical_columns:
            if col not in df_processed.columns:
                continue
            
            strategy = self.encoding_strategies.get(col, 'skip')
            
            if strategy == 'skip':
                columns_to_drop.append(col)
                continue
                        
            # Apply category groupings if they exist
            col_data = df_processed[col].astype(str).fillna('missing')
            if col in self.category_groupings:
                col_data = col_data.map(self.category_groupings[col]).fillna(col_data)
            
            try:
                if strategy == 'binary':
                    # Binary encoding: transform to 0/1
                    encoder = self.encoders[col]
                    known_values = encoder.classes_
                    # Handle unknown categories by mapping to 'missing'
                    col_data_safe = col_data.apply(lambda x: x if x in known_values else 'missing')
                    df_processed[f'{col}_binary'] = encoder.transform(col_data_safe)
                    encoded_features.append(f'{col}_binary')
                    columns_to_drop.append(col)
                    
                elif strategy == 'onehot_only':
                    unique_train_values = self.encoders[col].classes_
                    for val in unique_train_values:
                        if val != 'missing': 
                            df_processed[f'{col}_cat_{val}'] = (col_data == val).astype(int)
                            encoded_features.append(f'{col}_cat_{val}')
                    columns_to_drop.append(col)
                    
                elif strategy == 'target_freq':
                    # Target encoding: map categories to their target mean
                    if col in self.target_encodings:
                        target_map = self.target_encodings[col]
                        global_mean = self.target_encodings[f'{col}_global_mean']
                        # Use global mean for unknown categories
                        df_processed[f'{col}_target'] = col_data.map(target_map).fillna(global_mean)
                        encoded_features.append(f'{col}_target')
                    
                    # Frequency encoding: map categories to their frequency
                    if col in self.frequency_encodings:
                        freq_map = self.frequency_encodings[col]
                        # Use 0 for unknown categories
                        df_processed[f'{col}_freq'] = col_data.map(freq_map).fillna(0)
                        encoded_features.append(f'{col}_freq')
                    
                    columns_to_drop.append(col)
                    
                elif strategy == 'minimal':
                    # Minimal encoding: only frequency encoding for very high cardinality columns
                    if col in self.frequency_encodings:
                        freq_map = self.frequency_encodings[col]
                        df_processed[f'{col}_freq'] = col_data.map(freq_map).fillna(0)
                        encoded_features.append(f'{col}_freq')
                    
                    columns_to_drop.append(col)
                                
            except Exception as e:
                # If encoding fails, just drop the column
                print(f"  Error encoding column {col}: {str(e)}")
                columns_to_drop.append(col)
        
        # Remove original categorical columns
        existing_columns_to_drop = [col for col in columns_to_drop if col in df_processed.columns]
        if existing_columns_to_drop:
            df_processed = df_processed.drop(columns=existing_columns_to_drop)
        
        return df_processed