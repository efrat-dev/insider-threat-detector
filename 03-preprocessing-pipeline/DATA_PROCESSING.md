# Data Processing Components Guide

## Overview

This guide provides detailed documentation for each data processing component in the preprocessing pipeline. Each component handles a specific aspect of data preparation and follows the fit-transform paradigm for proper train-test separation.

## 🧹 Data Cleaning Component

### Implementation
**File**: [`src/pipeline/data_cleaning.py`](../src/pipeline/data_cleaning.py)

The `DataCleaner` class handles missing values and outliers using domain-specific strategies learned from training data.

### Missing Value Handling

#### Strategy Selection
```python
def fit_handle_missing_values(self, df):
    """Fit missing value handling parameters on training data."""
    
    # Domain-specific strategies
    travel_columns = ['trip_day_number', 'country_name']
    time_columns = ['first_entry_time', 'last_exit_time']
    derived_time_columns = ['entry_time_numeric', 'exit_time_numeric', 
                           'entry_time_numeric_zscore', 'exit_time_numeric_zscore']
```

#### Imputation Strategies by Column Type

**Travel-Related Columns**:
```python
# Trip day number: 0 indicates no travel
self.fitted_params['missing_values']['trip_day_number'] = {'method': 'fill_zero', 'value': 0}

# Country name: 'No_Travel' for non-traveling employees
self.fitted_params['missing_values']['country_name'] = {'method': 'fill_constant', 'value': 'No_Travel'}
```

**Time Columns**:
```python
# Use pandas NaT (Not a Time) for missing datetime values
self.fitted_params['missing_values'][col] = {'method': 'fill_datetime', 'value': pd.NaT}

# For derived numeric time features, use 0
self.fitted_params['missing_values'][col] = {'method': 'fill_zero', 'value': 0}
```

**Numeric Columns**:
```python
# Use median imputation for robust central tendency
median_val = df[col].median()
self.fitted_params['missing_values'][col] = {'method': 'fill_median', 'value': median_val}
```

**Categorical Columns**:
```python
# Use mode (most frequent value) or 'Unknown' as fallback
mode_val = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
self.fitted_params['missing_values'][col] = {'method': 'fill_mode', 'value': mode_val}
```

#### Transform Implementation
```python
def transform_handle_missing_values(self, df):
    """Apply missing value handling parameters to new data."""
    
    for col, params in self.fitted_params['missing_values'].items():
        if col in df_processed.columns and df_processed[col].isnull().sum() > 0:
            method = params['method']
            value = params['value']
            
            if method == 'fill_datetime':
                default_date = pd.Timestamp('1900-01-01')  # Sentinel date
                df_processed[col] = df_processed[col].fillna(default_date)
```

### Outlier Detection and Handling

#### IQR-Based Detection
```python
def fit_handle_outliers(self, df, method='cap', threshold=0.05):
    """Fit outlier handling parameters using IQR method."""
    
    for col in numeric_columns:
        # Calculate IQR bounds
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        self.fitted_params['outliers']['bounds'][col] = {
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }
```

#### Outlier Handling Methods
```python
def transform_handle_outliers(self, df):
    """Apply outlier handling using learned bounds."""
    
    if method == 'cap':
        # Cap values to bounds (Winsorization)
        df_processed[col] = np.where(df_processed[col] < lower_bound, lower_bound, df_processed[col])
        df_processed[col] = np.where(df_processed[col] > upper_bound, upper_bound, df_processed[col])
    elif method == 'remove':
        # Mark outliers as NaN (don't delete rows in transform)
        df_processed[col] = np.where(
            (df_processed[col] < lower_bound) | (df_processed[col] > upper_bound),
            np.nan, df_processed[col]
        )
```

**Key Design Decisions**:
- Protected columns (timestamps) are excluded from outlier detection
- Transform phase doesn't remove rows to maintain data alignment
- Configurable handling methods for different use cases

## 🔄 Data Type Converter

### Implementation
**File**: [`src/pipeline/data_type_converter.py`](../src/pipeline/data_type_converter.py)

Static converter for optimizing data types and memory usage.

### DateTime Conversion
```python
def convert_data_types(df):
    """Convert data types with robust error handling."""
    
    date_columns = ['date', 'first_entry_time', 'last_exit_time']
    for col in date_columns:
        if col in df_processed.columns:
            try:
                df_processed[col] = pd.to_datetime(df_processed[col], errors='coerce')
            except:
                print(f"Could not convert {col} to datetime")
```

### Boolean Optimization
```python
# Explicit boolean columns for memory efficiency
boolean_columns = ['is_contractor', 'has_foreign_citizenship', 'has_criminal_record', 
                  'has_medical_history', 'is_malicious', 'is_emp_malicios', 'is_abroad', 
                  'is_hostile_country_trip', 'is_official_trip', 'entered_during_night_hours', 
                  'early_entry_flag', 'late_exit_flag', 'entry_during_weekend']

for col in boolean_columns:
    if col in df_processed.columns:
        df_processed[col] = df_processed[col].astype(bool)
```

### Categorical Memory Optimization
```python
# Use category dtype for memory efficiency
categorical_columns = ['employee_department', 'employee_campus', 'employee_position', 
                     'employee_classification', 'employee_origin_country', 'country_name']

for col in categorical_columns:
    if col in df_processed.columns:
        df_processed[col] = df_processed[col].astype('category')
```

**Memory Benefits**:
- Category dtype uses integer codes internally
- Significant memory reduction for high-cardinality string columns
- Faster operations on categorical data

## 🎯 Categorical Encoder

### Implementation
**File**: [`src/pipeline/categorical_encoder.py`](../src/pipeline/categorical_encoder.py)

Advanced categorical encoding with cardinality-based strategy selection.

### Automatic Column Detection
```python
def identify_all_categorical_columns(self, df):
    """Identify categorical columns using multiple heuristics."""
    
    for col in df.columns:
        # Skip protected columns
        if col in protected_columns:
            continue
        
        dtype = df[col].dtype
        
        # Explicit categorical/object types
        if dtype in ['object', 'category']:
            categorical_columns.append(col)
            continue
        
        # Numeric columns that might be categorical
        if dtype in ['int64', 'int32', 'float64', 'float32']:
            unique_values = df[col].nunique()
            total_values = len(df[col])
            
            # Low cardinality heuristic
            if unique_values <= 50 and unique_values < total_values * 0.1:
                categorical_columns.append(col)
```

### Strategy Selection Logic

```python
def fit_encode(self, df, target_col='is_malicious'):
    """Learn encoding parameters with cardinality-based strategy selection."""
    
    for col in self.categorical_columns:
        unique_values = col_data.nunique()
        
        if unique_values == 1:
            self.encoding_strategies[col] = 'skip'
            
        elif unique_values == 2:
            self.encoding_strategies[col] = 'binary'
            # Use LabelEncoder for binary encoding
            
        elif unique_values <= self.max_onehot_categories:  # ≤3
            self.encoding_strategies[col] = 'onehot_only'
            
        elif unique_values <= self.max_categories_for_detailed_encoding:  # ≤10
            self.encoding_strategies[col] = 'target_freq'
            # Learn target encoding + frequency encoding parameters
            
        else:
            # High cardinality - attempt rare category grouping
            rare_grouping = self.group_rare_categories(df_work, col, min_frequency=50)
            self.encoding_strategies[col] = 'target_freq' or 'minimal'
```

### Encoding Implementations

#### Binary Encoding
```python
if strategy == 'binary':
    encoder = self.encoders[col]
    known_values = encoder.classes_
    # Handle unknown categories gracefully
    col_data_safe = col_data.apply(lambda x: x if x in known_values else 'missing')
    df_processed[f'{col}_binary'] = encoder.transform(col_data_safe)
```

#### One-Hot Encoding
```python
elif strategy == 'onehot_only':
    unique_train_values = self.encoders[col].classes_
    for val in unique_train_values:
        if val != 'missing': 
            df_processed[f'{col}_cat_{val}'] = (col_data == val).astype(int)
```

#### Target + Frequency Encoding
```python
elif strategy == 'target_freq':
    # Target encoding: map to target mean
    if col in self.target_encodings:
        target_map = self.target_encodings[col]
        global_mean = self.target_encodings[f'{col}_global_mean']
        df_processed[f'{col}_target'] = col_data.map(target_map).fillna(global_mean)
    
    # Frequency encoding: map to occurrence frequency  
    if col in self.frequency_encodings:
        freq_map = self.frequency_encodings[col]
        df_processed[f'{col}_freq'] = col_data.map(freq_map).fillna(0)
```

### Rare Category Grouping
```python
def group_rare_categories(self, df, col, min_frequency=100):
    """Group infrequent categories to reduce dimensionality."""
    
    value_counts = df[col].value_counts()
    rare_categories = value_counts[value_counts < min_frequency].index.tolist()
    
    if len(rare_categories) > 1:
        grouping_map = {}
        for cat in rare_categories:
            grouping_map[cat] = 'OTHER_RARE'
        return grouping_map
    return {}
```

## 📊 Statistical Transformer

### Implementation
**File**: [`src/pipeline/statistical_transformer.py`](../src/pipeline/statistical_transformer.py)

Creates z-score transformations for numerical features.

### Z-Score Parameter Learning
```python
def fit(self, df):
    """Fit statistical transformation parameters."""
    
    for col in transform_columns:
        col_params = {}
        col_params['std'] = df[col].std()
        col_params['has_variance'] = col_params['std'] > 0
        
        if col_params['has_variance']:
            scaler = StandardScaler()
            scaler.fit(df[col].values.reshape(-1, 1))
            self.scalers[col] = scaler
        
        self.fitted_params[col] = col_params
```

### Z-Score Application
```python
def transform(self, df):
    """Apply z-score transformations using fitted scalers."""
    
    for col in transform_columns:
        col_params = self.fitted_params[col]
        
        if col_params.get('has_variance', False) and col in self.scalers:
            try:
                df_processed[f'{col}_zscore'] = self.scalers[col].transform(
                    df_processed[col].values.reshape(-1, 1)
                ).flatten()
            except Exception as e:
                print(f"Error applying Z-score to {col}: {str(e)}")
```

**Key Features**:
- Only transforms columns with non-zero variance
- Creates new z-score columns (doesn't replace originals)
- Robust error handling for edge cases

## 🎛️ Variance Correlation Filter

### Implementation
**File**: [`src/pipeline/variance_correlation_filter.py`](../src/pipeline/variance_correlation_filter.py)

Feature selection based on variance and correlation analysis.

### Variance Filtering
```python
def fit_variance_filtering(self, df, threshold=0.01):
    """Filter features with low variance."""
    
    # Separate protected columns (e.g., zscore features)
    protected_cols = [col for col in numeric_cols if self._is_protected_column(col)]
    regular_cols = [col for col in numeric_cols if not self._is_protected_column(col)]
    
    # Apply variance filtering only to regular columns
    self.variance_threshold = VarianceThreshold(threshold=threshold)
    self.variance_threshold.fit(df[regular_cols])
    
    # Combine filtered regular + protected + non-numeric columns
    selected_regular = [col for col, selected in 
                       zip(regular_cols, self.variance_threshold.get_support()) 
                       if selected]
    
    self.variance_filtered_features_ = selected_regular + protected_cols + non_numeric_cols
```

### Correlation Filtering
```python
def fit_correlation_filtering(self, df, threshold=0.95):
    """Filter highly correlated features."""
    
    # Calculate correlation matrix for regular columns only
    corr_matrix = df[regular_cols].corr().abs()
    
    # Find highly correlated pairs using upper triangle
    upper_tri = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )
    
    # Identify columns to drop
    to_drop = [column for column in upper_tri.columns 
              if any(upper_tri[column] > threshold)]
    
    # Keep remaining regular + all protected columns
    remaining_regular = [col for col in regular_cols if col not in to_drop]
    self.correlation_filtered_features_ = remaining_regular + protected_cols + non_numeric_cols
```

### Protected Column Logic
```python
def _is_protected_column(self, col_name):
    """Check if column should be protected from filtering."""
    return 'zscore' in col_name.lower()
```

**Design Rationale**:
- Z-score features are protected because they provide normalized views
- Target columns are automatically excluded
- Non-numeric columns pass through unchanged

## 📏 Feature Normalizer

### Implementation  
**File**: [`src/pipeline/feature_normalizer.py`](../src/pipeline/feature_normalizer.py)

Final scaling step to ensure features are on similar scales.

### Scaler Selection and Fitting
```python
def fit_normalize_features(self, df, method='standard'):
    """Fit normalization parameters on training data."""
    
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    exclude_cols = ['employee_id', 'is_malicious', 'is_emp_malicious_binary', 'target', 
                   'date', 'first_entry_time', 'last_exit_time']
    numeric_columns = [col for col in numeric_columns if col not in exclude_cols]
    
    # Fit appropriate scaler
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
```

### Normalization Application
```python
def transform_normalize_features(self, df):
    """Apply normalization using fitted parameters."""
    
    method = self.fitted_params['normalization']['method']
    columns_to_normalize = self.fitted_params['normalization']['columns_to_normalize']
    
    # Handle missing columns gracefully
    available_columns = [col for col in columns_to_normalize if col in df_processed.columns]
    
    scaler = self.scalers.get(method)
    if scaler is None:
        raise ValueError(f"Scaler for method '{method}' not found")
    
    df_processed[available_columns] = scaler.transform(df_processed[available_columns])
```

**Scaling Methods**:
- **StandardScaler**: Mean=0, std=1 (default, best for normally distributed data)
- **MinMaxScaler**: Scale to [0,1] range (good for bounded features)
- **RobustScaler**: Uses median and IQR (robust to outliers)

## 🔗 Component Integration

### Pipeline Orchestration
**File**: [`src/pipeline/preprocessing_pipeline.py`](../src/pipeline/preprocessing_pipeline.py)

```python
class PreprocessingPipeline:
    def __init__(self):
        # Initialize all components
        self.data_cleaner = DataCleaner()
        self.data_type_converter = DataTypeConverter()
        self.feature_creator = FeatureCreator()
        self.categorical_encoder = CategoricalEncoder()
        self.statistical_transformer = StatisticalTransformer()
        self.variance_correlation_filter = VarianceCorrelationFilter()
        self.feature_normalizer = FeatureNormalizer()
    
    def fit(self, X_train, y_train=None):
        """Fit all components in sequence."""
        df_train = X_train.copy()
        if y_train is not None:
            df_train['target'] = y_train
        
        # Sequential fitting and transformation
        df_train = self.data_cleaner.fit_handle_missing_values(df_train)
        df_train = self.data_type_converter.convert_data_types(df_train)
        df_train = self.feature_creator.create_all_features(df_train)
        df_train = self._remove_original_columns(df_train)
        df_train = self._standardize_data_types(df_train)
        df_train = self.categorical_encoder.fit_encode(df_train)
        df_train = self.statistical_transformer.fit_transform(df_train)
        df_train = self.data_cleaner.fit_handle_outliers(df_train, method='cap')
        df_train = self.variance_correlation_filter.fit_variance_filtering(df_train)
        df_train = self.variance_correlation_filter.fit_correlation_filtering(df_train)
        self.feature_normalizer.fit_normalize_features(df_train)
        
        return self
```

### Data Flow Validation
```python
def transform(self, X):
    """Apply all transformations in sequence."""
    if not self.is_fitted:
        raise ValueError("Pipeline must be fitted before transform")
    
    # Apply same sequence without fitting
    df = self.data_cleaner.transform_handle_missing_values(X.copy())
    df = self.data_type_converter.convert_data_types(df)
    # ... continue sequence
    
    return df
```

## ⚡ Performance Considerations

### Memory Optimization Strategies

1. **Data Type Optimization**:
```python
# Convert float64 to float32 where appropriate
float_cols = df.select_dtypes(include=['float64']).columns
df = df.astype({col: 'float32' for col in float_cols})
```

2. **Category Dtype Usage**:
```python
# Use category for string columns with limited unique values
df[col] = df[col].astype('category')
```

3. **Selective Processing**:
```python
# Process only columns that need transformation
transform_columns = [col for col in numeric_columns if col not in exclude_cols]
```

### Computational Efficiency

1. **Vectorized Operations**:
```python
# Use numpy/pandas vectorized operations
df_processed[new_col] = df[col1] / np.maximum(df[col2], 1)
```

2. **Early Termination**:
```python
# Skip processing for edge cases
if len(numeric_columns) == 0:
    return df  # No processing needed
```

3. **Single-Pass Calculations**:
```python
# Calculate statistics once and reuse
Q1 = df[col].quantile(0.25)
Q3 = df[col].quantile(0.75)
IQR = Q3 - Q1
```

## 🔧 Error Handling Patterns

### Graceful Degradation
```python
try:
    # Primary processing logic
    result = complex_processing(data)
except Exception as e:
    print(f"Primary processing failed: {e}")
    # Fallback to simpler approach
    result = simple_processing(data)
```

### Missing Column Handling
```python
# Filter to available columns
available_columns = [col for col in expected_columns if col in df.columns]

# Warn about missing columns
if len(available_columns) != len(expected_columns):
    missing_cols = set(expected_columns) - set(available_columns)
    print(f"Warning: {len(missing_cols)} columns missing")
```

### State Validation
```python
def transform(self, df):
    if not self.is_fitted:
        raise ValueError("Component must be fitted before transform")
    
    # Proceed with transformation
```

## 🔗 Related Documentation

- **[Main README](../README.md)** - Project overview and quick start
- **[Pipeline Architecture](./PIPELINE_ARCHITECTURE.md)** - Overall system design
- **[Feature Engineering Guide](./FEATURE_ENGINEERING.md)** - Feature creation strategies
- **[API Reference](./API_REFERENCE.md)** - Complete method documentation

## 🧪 Testing and Validation

### Component Testing Strategy
```python
# Test individual components
data_cleaner = DataCleaner()
clean_data = data_cleaner.fit_handle_missing_values(train_data)

# Validate transformations maintain data integrity
assert len(clean_data) == len(train_data)  # No rows lost
assert clean_data.isnull().sum().sum() == 0  # No missing values remain
```

### Integration Testing
```python
# Test full pipeline
pipeline = PreprocessingPipeline()
pipeline.fit(X_train, y_train)
X_processed = pipeline.transform(X_test)

# Validate pipeline output
assert not X_processed.isnull().any().any()  # No missing values
assert X_processed.dtypes.apply(lambda x: x.kind in 'biufc').all()  # All numeric
```
