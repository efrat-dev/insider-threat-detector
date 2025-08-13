# API Reference Documentation

## Overview

This document provides complete API documentation for all classes and methods in the preprocessing pipeline. Each component follows consistent patterns and interfaces for easy integration and extension.

## 📋 Table of Contents

- [PreprocessingPipeline](#preprocessing-pipeline)
- [DataCleaner](#data-cleaner)
- [DataTypeConverter](#data-type-converter)
- [FeatureCreator](#feature-creator)
- [CategoricalEncoder](#categorical-encoder)
- [StatisticalTransformer](#statistical-transformer)
- [VarianceCorrelationFilter](#variance-correlation-filter)
- [FeatureNormalizer](#feature-normalizer)
- [Utility Functions](#utility-functions)

---

## PreprocessingPipeline

**File**: [`src/pipeline/preprocessing_pipeline.py`](../src/pipeline/preprocessing_pipeline.py)

Main orchestrator class that coordinates all preprocessing steps.

### Class Definition
```python
class PreprocessingPipeline:
    """Complete preprocessing pipeline"""
```

### Constructor
```python
def __init__(self):
    """Initialize all pipeline components."""
```

**Attributes**:
- `data_cleaner` (DataCleaner): Handles missing values and outliers
- `data_type_converter` (DataTypeConverter): Optimizes data types
- `feature_creator` (FeatureCreator): Creates domain-specific features
- `categorical_encoder` (CategoricalEncoder): Encodes categorical variables
- `statistical_transformer` (StatisticalTransformer): Applies statistical transformations
- `variance_correlation_filter` (VarianceCorrelationFilter): Performs feature selection
- `feature_normalizer` (FeatureNormalizer): Normalizes features
- `is_fitted` (bool): Indicates if pipeline has been fitted

### Methods

#### fit()
```python
def fit(self, X_train, y_train=None):
    """
    Fit the pipeline on training data only.
    
    Args:
        X_train (pd.DataFrame): Training features
        y_train (pd.Series, optional): Training target variable
        
    Returns:
        self: Returns the fitted pipeline instance
    """
```

#### transform()
```python
def transform(self, X):
    """
    Apply the fitted pipeline to new data (train or test).
    
    Args:
        X (pd.DataFrame): Data to transform
        
    Returns:
        pd.DataFrame: Transformed data
        
    Raises:
        ValueError: If pipeline hasn't been fitted yet
    """
```

#### fit_transform()
```python
def fit_transform(self, X_train, y_train=None):
    """
    Fit and transform training data in one step.
    
    Args:
        X_train (pd.DataFrame): Training features
        y_train (pd.Series, optional): Training target variable
        
    Returns:
        pd.DataFrame: Fitted and transformed training data
    """
```

### Private Methods

#### _remove_original_columns()
```python
def _remove_original_columns(self, df: pd.DataFrame, columns_to_remove=None) -> pd.DataFrame:
    """
    Remove original columns after feature creation.
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns_to_remove (list, optional): List of columns to remove
        
    Returns:
        pd.DataFrame: Dataframe with specified columns removed
    """
```

#### _standardize_data_types()
```python
def _standardize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize data types across the dataframe.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with standardized data types
    """
```

---

## DataCleaner

**File**: [`src/pipeline/data_cleaning.py`](../src/pipeline/data_cleaning.py)

Handles missing values and outlier detection/treatment.

### Class Definition
```python
class DataCleaner:
    """Class for data cleaning"""
```

### Constructor
```python
def __init__(self):
    """Initialize DataCleaner with empty parameters."""
```

**Attributes**:
- `fitted_params` (dict): Stores fitted parameters
- `is_fitted` (bool): Indicates if cleaner has been fitted

### Methods

#### fit_handle_missing_values()
```python
def fit_handle_missing_values(self, df):
    """
    Fit missing value handling parameters on training data.
    
    Args:
        df (pd.DataFrame): Training dataframe to fit parameters on
        
    Returns:
        pd.DataFrame: Cleaned dataframe with missing values handled
    """
```

**Parameter Storage Structure**:
```python
self.fitted_params['missing_values'] = {
    'column_name': {
        'method': str,  # 'fill_zero', 'fill_constant', 'fill_median', etc.
        'value': Any    # Value to use for filling
    }
}
```

#### transform_handle_missing_values()
```python
def transform_handle_missing_values(self, df):
    """
    Apply missing value handling parameters to new data.
    
    Args:
        df (pd.DataFrame): Dataframe to clean
        
    Returns:
        pd.DataFrame: Cleaned dataframe
        
    Raises:
        ValueError: If DataCleaner hasn't been fitted yet
    """
```

#### fit_handle_outliers()
```python
def fit_handle_outliers(self, df, method='cap', threshold=0.05):
    """
    Fit outlier handling parameters on training data.
    
    Args:
        df (pd.DataFrame): Training dataframe to fit parameters on
        method (str): Method for handling outliers ('cap' or 'remove')
        threshold (float): Threshold parameter (not used in current implementation)
        
    Returns:
        pd.DataFrame: Original dataframe (parameters only stored during fit)
    """
```

**Parameter Storage Structure**:
```python
self.fitted_params['outliers'] = {
    'method': str,  # 'cap' or 'remove'
    'bounds': {
        'column_name': {
            'lower_bound': float,
            'upper_bound': float
        }
    }
}
```

#### transform_handle_outliers()
```python
def transform_handle_outliers(self, df):
    """
    Apply outlier handling parameters to new data.
    
    Args:
        df (pd.DataFrame): Dataframe to process
        
    Returns:
        pd.DataFrame: Dataframe with outliers handled
    """
```

---

## DataTypeConverter

**File**: [`src/pipeline/data_type_converter.py`](../src/pipeline/data_type_converter.py)

Optimizes data types for memory efficiency and proper operations.

### Class Definition
```python
class DataTypeConverter:
    """Class for data type conversion"""
```

### Static Methods

#### convert_data_types()
```python
@staticmethod
def convert_data_types(df):
    """
    Convert data types - static function that doesn't need fit.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with converted data types
    """
```

**Conversion Rules**:
- **Date columns**: Convert to `datetime64` with error handling
- **Boolean columns**: Convert to `bool` dtype
- **Categorical columns**: Convert to `category` dtype for memory efficiency

---

## FeatureCreator

**File**: [`src/pipeline/feature_creator.py`](../src/pipeline/feature_creator.py)

Creates domain-specific features for insider threat detection.

### Class Definition
```python
class FeatureCreator:
    """Class for creating new features from existing data"""
```

### Constructor
```python
def __init__(self):
    """Initialize FeatureCreator."""
```

### Methods

#### create_all_features()
```python
def create_all_features(self, df):
    """
    Create all new features by applying all feature creation methods.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with all new features added
    """
```

#### create_temporal_features()
```python
def create_temporal_features(self, df):
    """
    Create time and presence-related features.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with new temporal features
    """
```

**Features Created**:
- `weekday`: Day of week (0=Monday, 6=Sunday)
- `month`: Month of year (1-12)
- `is_end_of_month`: Binary flag for dates >= 25th
- `is_quarter_end`: Binary flag for quarter-end months
- `entry_time_numeric`: Entry time as decimal hours
- `exit_time_numeric`: Exit time as decimal hours

#### create_media_features()
```python
def create_media_features(self, df):
    """
    Create essential media/burning features.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with new media-related features
    """
```

**Features Created**:
- `avg_burn_volume_per_request`: Average MB per burn request
- `burn_intensity`: Burn requests per hour of presence
- `high_classification_burn`: Binary flag for high-sensitivity data
- `classification_variance`: Ratio of max to avg classification
- `off_hours_burn_ratio`: Proportion of off-hours burn requests
- `is_heavy_burner`: Binary flag for top 20% burn volume users
- `avg_pages_per_print`: Average pages per print command
- `print_intensity`: Print commands per hour of presence
- `off_hours_ratio`: Proportion of off-hours print commands
- `is_heavy_printer`: Binary flag for top 20% print volume users

#### create_employee_features()
```python
def create_employee_features(self, df):
    """
    Create essential employee-related features.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with new employee features
    """
```

**Features Created**:
- `is_employee_in_origin_country`: Binary flag for geographic consistency
- `is_new_employee`: Binary flag for employees with < 1 year seniority
- `is_veteran_employee`: Binary flag for employees with > 10 years seniority

---

## CategoricalEncoder

**File**: [`src/pipeline/categorical_encoder.py`](../src/pipeline/categorical_encoder.py)

Advanced categorical encoding with cardinality-based strategy selection.

### Class Definition
```python
class CategoricalEncoder:
    """
    Specialized class for encoding categorical variables - version optimized for feature reduction.
    
    This encoder uses different strategies based on the cardinality (number of unique values) 
    of categorical columns to minimize the number of output features while preserving information.
    """
```

### Constructor
```python
def __init__(self):
    """
    Initialize the encoder with parameters optimized for feature reduction.
    """
```

**Attributes**:
- `encoders` (dict): Stores sklearn LabelEncoders for specific columns
- `categorical_columns` (list): List of identified categorical column names
- `encoding_strategies` (dict): Maps column names to their encoding strategy
- `target_encodings` (dict): Stores target encoding mappings for each column
- `frequency_encodings` (dict): Stores frequency encoding mappings for each column
- `category_groupings` (dict): Stores rare category groupings for dimensionality reduction
- `is_fitted` (bool): Flag indicating if the encoder has been trained
- `max_onehot_categories` (int): Maximum categories for one-hot encoding (default: 3)
- `max_categories_for_detailed_encoding` (int): Maximum categories for detailed encoding (default: 10)

### Methods

#### identify_all_categorical_columns()
```python
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
```

#### group_rare_categories()
```python
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
```

#### fit_encode()
```python
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
```

#### transform_encode()
```python
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
```

### Encoding Strategies

| Cardinality | Strategy | Features Created | Example |
|-------------|----------|------------------|---------|
| 1 | Skip | None | Constant columns |
| 2 | Binary | `{col}_binary` | Gender: 0/1 |
| ≤3 | One-hot only | `{col}_cat_{value}` | Priority: High, Medium, Low |
| 4-10 | Target + Frequency | `{col}_target`, `{col}_freq` | Department codes |
| >10 | Minimal or Grouped | `{col}_freq` or grouped then strategy | Employee IDs |

---

## StatisticalTransformer

**File**: [`src/pipeline/statistical_transformer.py`](../src/pipeline/statistical_transformer.py)

Creates statistical transformations, primarily z-score normalization.

### Class Definition
```python
class StatisticalTransformer:
    """Special class for statistical transformations - Z-score and quartiles according to model type"""
```

### Constructor
```python
def __init__(self):
    """Initialize StatisticalTransformer with empty parameters."""
```

**Attributes**:
- `scalers` (dict): Stores fitted StandardScaler objects
- `fitted_params` (dict): Stores column-specific parameters
- `is_fitted` (bool): Indicates if transformer has been fitted

### Methods

#### fit()
```python
def fit(self, df):
    """
    Fit statistical transformation parameters on training data.
    
    Args:
        df (pd.DataFrame): Training dataframe to fit parameters on
        
    Returns:
        pd.DataFrame: Original dataframe (unchanged)
    """
```

**Parameter Storage**:
```python
# For each column:
col_params = {
    'std': float,           # Standard deviation
    'has_variance': bool,   # Whether column has non-zero variance
    'unique_values': int,   # Number of unique values
    'min_val': float,      # Minimum value
    'max_val': float       # Maximum value
}
```

#### transform()
```python
def transform(self, df):
    """
    Apply statistical transformations using fitted parameters.
    
    Args:
        df (pd.DataFrame): Dataframe to transform
        
    Returns:
        pd.DataFrame: Transformed dataframe with new statistical features
        
    Raises:
        ValueError: If transformer hasn't been fitted yet
    """
```

#### fit_transform()
```python
def fit_transform(self, df):
    """
    Fit and transform in one step.
    
    Args:
        df (pd.DataFrame): Dataframe to fit and transform
        
    Returns:
        pd.DataFrame: Transformed dataframe
    """
```

**Features Created**:
- `{col}_zscore`: Z-score transformation for columns with variance > 0

---

## VarianceCorrelationFilter

**File**: [`src/pipeline/variance_correlation_filter.py`](../src/pipeline/variance_correlation_filter.py)

Feature selection based on variance and correlation analysis.

### Class Definition
```python
class VarianceCorrelationFilter:
    """Class for filtering features based on variance and correlation"""
```

### Constructor
```python
def __init__(self):
    """Initialize VarianceCorrelationFilter with default parameters."""
```

**Attributes**:
- `variance_threshold` (VarianceThreshold): Sklearn variance threshold object
- `correlation_threshold` (float): Correlation threshold (default: 0.95)
- `variance_filtered_features_` (list): Features remaining after variance filtering
- `correlation_filtered_features_` (list): Features remaining after correlation filtering

### Methods

#### _is_protected_column()
```python
def _is_protected_column(self, col_name):
    """
    Check if column is protected (contains zscore).
    
    Args:
        col_name (str): Column name to check
        
    Returns:
        bool: True if column is protected from filtering
    """
```

#### fit_variance_filtering()
```python
def fit_variance_filtering(self, df, threshold=0.01):
    """
    Filter features with low variance.
    
    Args:
        df (pd.DataFrame): Input dataframe
        threshold (float): Variance threshold for filtering
        
    Returns:
        pd.DataFrame: Dataframe with low variance features removed
    """
```

#### transform_variance_filtering()
```python
def transform_variance_filtering(self, df):
    """
    Apply variance filtering to new data.
    
    Args:
        df (pd.DataFrame): Input dataframe to transform
        
    Returns:
        pd.DataFrame: Filtered dataframe
        
    Raises:
        ValueError: If variance filtering hasn't been fitted yet
    """
```

#### fit_correlation_filtering()
```python
def fit_correlation_filtering(self, df, threshold=0.95):
    """
    Filter features with high correlation.
    
    Args:
        df (pd.DataFrame): Input dataframe
        threshold (float): Correlation threshold for filtering
        
    Returns:
        pd.DataFrame: Dataframe with highly correlated features removed
    """
```

#### transform_correlation_filtering()
```python
def transform_correlation_filtering(self, df):
    """
    Apply correlation filtering to new data.
    
    Args:
        df (pd.DataFrame): Input dataframe to transform
        
    Returns:
        pd.DataFrame: Filtered dataframe
        
    Raises:
        ValueError: If correlation filtering hasn't been fitted yet
    """
```

### Filtering Logic

**Variance Filtering**:
- Removes features with variance below threshold
- Protects z-score features from removal
- Uses sklearn's VarianceThreshold

**Correlation Filtering**:
- Removes one feature from highly correlated pairs (|correlation| > threshold)
- Uses upper triangle of correlation matrix to avoid double-counting
- Protects z-score and target columns

---

## FeatureNormalizer

**File**: [`src/pipeline/feature_normalizer.py`](../src/pipeline/feature_normalizer.py)

Final scaling step to ensure features are on similar scales.

### Class Definition
```python
class FeatureNormalizer:
    """Class for feature normalization"""
```

### Constructor
```python
def __init__(self):
    """Initialize FeatureNormalizer with empty parameters."""
```

**Attributes**:
- `scaler` (object): Main scaler object (deprecated, use `scalers`)
- `fitted_params` (dict): Stores normalization parameters
- `scalers` (dict): Stores fitted scaler objects by method

### Methods

#### fit_normalize_features()
```python
def fit_normalize_features(self, df, method='standard'):
    """
    Fit normalization parameters on training data.
    
    Args:
        df (pd.DataFrame): Training dataframe to fit normalization on
        method (str): Normalization method ('standard', 'minmax', or 'robust')
        
    Returns:
        pd.DataFrame: Original dataframe (unchanged during fit)
    """
```

**Normalization Methods**:
- `'standard'`: StandardScaler (mean=0, std=1)
- `'minmax'`: MinMaxScaler (scale to [0,1])
- `'robust'`: RobustScaler (median-based, outlier-resistant)

#### transform_normalize_features()
```python
def transform_normalize_features(self, df):
    """
    Apply normalization using fitted parameters.
    
    Args:
        df (pd.DataFrame): Dataframe to normalize
        
    Returns:
        pd.DataFrame: Normalized dataframe
        
    Raises:
        ValueError: If normalization hasn't been fitted yet or scaler not found
    """
```

**Parameter Storage**:
```python
self.fitted_params['normalization'] = {
    'method': str,                    # Normalization method
    'columns_to_normalize': list      # Columns to normalize
}
```

---

## Utility Functions

### Main Execution Functions

**File**: [`src/main.py`](../src/main.py)

#### split_data()
```python
def split_data(X, y, employee_col='employee_id', date_col='date'):
    """
    Sorts the dataset by employee and date, then splits it into training, validation, and test sets.
    
    Args:
        X (pd.DataFrame): Feature dataframe
        y (pd.Series): Target series
        employee_col (str): Employee ID column name (default: 'employee_id')
        date_col (str): Date column name (default: 'date')
        
    Returns:
        tuple: (X_train, X_val, X_test, y_train, y_val, y_test)
            - Training set (60%)
            - Validation set (20%) 
            - Test set (20%)
    """
```

**Split Logic**:
- Sorts by employee_col then date_col to maintain temporal order
- 60/20/20 split for train/validation/test
- Maintains employee-date relationships within splits

#### main()
```python
def main():
    """
    Main function to execute the production data processing pipeline.
    
    Process:
    1. Load dataset from 'insider_threat_dataset.csv'
    2. Optimize data types for memory efficiency
    3. Drop irrelevant columns
    4. Fit preprocessing pipeline on full dataset
    5. Transform data through pipeline
    6. Split into train/validation/test sets
    7. Save processed datasets as CSV files
    
    Raises:
        Exception: If pipeline fails at any step
    """
```

## 🔄 Common Usage Patterns

### Basic Pipeline Usage
```python
from pipeline.preprocessing_pipeline import PreprocessingPipeline

# Load data
df = pd.read_csv('data.csv')
X = df.drop(columns=['target'])
y = df['target']

# Initialize and fit pipeline
pipeline = PreprocessingPipeline()
pipeline.fit(X, y)

# Transform data
X_processed = pipeline.transform(X)
```

### Individual Component Usage
```python
from pipeline.categorical_encoder import CategoricalEncoder

# Initialize encoder
encoder = CategoricalEncoder()

# Fit and transform
X_encoded = encoder.fit_encode(X_train, target_col='is_malicious')

# Transform new data
X_test_encoded = encoder.transform_encode(X_test)
```

### Custom Configuration
```python
from pipeline.feature_normalizer import FeatureNormalizer

# Initialize with custom settings
normalizer = FeatureNormalizer()

# Fit with specific method
normalizer.fit_normalize_features(X_train, method='robust')

# Transform
X_normalized = normalizer.transform_normalize_features(X_test)
```

## ⚠️ Error Handling

### Common Exceptions

#### ValueError
- **When**: Component hasn't been fitted before transform
- **Message**: `"Component must be fitted before transform"`
- **Solution**: Call fit() or fit_transform() first

#### KeyError  
- **When**: Expected column missing from dataframe
- **Solution**: Components handle missing columns gracefully with warnings

#### TypeError
- **When**: Invalid data type passed to method
- **Solution**: Ensure input is pandas DataFrame/Series as expected

### Logging and Debugging

```python
import logging

# Enable detailed logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pipeline automatically logs:
logger.info(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
logger.info(f"Data processed: {X_processed.shape}")
logger.warning(f"Column {col} has high cardinality: {nunique}")
logger.error(f"Pipeline failed: {str(e)}")
```

## 🔗 Related Documentation

- **[Main README](../README.md)** - Project overview and quick start guide
- **[Pipeline Architecture](./PIPELINE_ARCHITECTURE.md)** - System design and component interaction
- **[Feature Engineering Guide](./FEATURE_ENGINEERING.md)** - Detailed feature creation strategies
- **[Data Processing Components](./DATA_PROCESSING.md)** - In-depth component documentation

## 📋 Parameter Reference

### Default Parameters Summary

| Component | Parameter | Default Value | Description |
|-----------|-----------|---------------|-------------|
| CategoricalEncoder | max_onehot_categories | 3 | Max categories for one-hot encoding |
| CategoricalEncoder | max_categories_for_detailed_encoding | 10 | Max categories for target+freq encoding |
| VarianceCorrelationFilter | variance_threshold | 0.01 | Minimum variance for feature retention |
| VarianceCorrelationFilter | correlation_threshold | 0.95 | Maximum correlation between features |
| FeatureNormalizer | method | 'standard' | Normalization method |
| DataCleaner | outlier_method | 'cap' | Outlier handling strategy |

### Customization Examples

```python
# Custom categorical encoding thresholds
encoder = CategoricalEncoder()
encoder.max_onehot_categories = 5  # Increase one-hot limit
encoder.max_categories_for_detailed_encoding = 15  # Increase detailed encoding limit

# Custom variance filtering
filter = VarianceCorrelationFilter()
filter.fit_variance_filtering(df, threshold=0.001)  # More aggressive filtering

# Custom normalization
normalizer = FeatureNormalizer()
normalizer.fit_normalize_features(df, method='robust')  # Outlier-resistant scaling
```
