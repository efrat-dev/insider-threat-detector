# Pipeline Architecture

## Overview

The preprocessing pipeline follows a modular architecture where each component handles a specific aspect of data preprocessing. The design ensures proper separation of concerns, reusability, and maintainability.

## 🏗️ Architecture Principles

### 1. Fit-Transform Paradigm
All components follow scikit-learn's fit-transform pattern:
- **`fit()`**: Learn parameters from training data only
- **`transform()`**: Apply learned parameters to any dataset
- **`fit_transform()`**: Convenience method combining both operations

### 2. Component Modularity
Each preprocessing step is encapsulated in its own class with clear responsibilities:

```
PreprocessingPipeline
├── DataCleaner
├── DataTypeConverter  
├── FeatureCreator
├── CategoricalEncoder
├── StatisticalTransformer
├── VarianceCorrelationFilter
└── FeatureNormalizer
```

### 3. State Management
Components maintain internal state to ensure consistency between training and inference:
- Fitted parameters are stored for reuse
- Unknown categories and edge cases are handled gracefully
- Pipeline state validation prevents misuse

## 🔄 Pipeline Flow

### Main Pipeline Orchestrator
**File**: [`src/pipeline/preprocessing_pipeline.py`](../src/pipeline/preprocessing_pipeline.py)

The `PreprocessingPipeline` class coordinates all preprocessing steps:

```python
class PreprocessingPipeline:
    def fit(self, X_train, y_train=None):
        """Fit all components on training data"""
        # Sequential fitting of all components
        
    def transform(self, X):
        """Apply all transformations to new data"""
        # Sequential transformation using fitted parameters
        
    def fit_transform(self, X_train, y_train=None):
        """Fit and transform in one step"""
```

### Processing Sequence

#### 1. Data Cleaning ([`data_cleaning.py`](../src/pipeline/data_cleaning.py))
```
Input: Raw dataframe
├── Missing value imputation (fit parameters on training data)
├── Outlier detection and handling (learn bounds from training data)
└── Output: Cleaned dataframe
```

**Key Features**:
- Domain-specific missing value strategies
- IQR-based outlier detection
- Configurable handling methods (cap/remove)

#### 2. Data Type Conversion ([`data_type_converter.py`](../src/pipeline/data_type_converter.py))
```
Input: Cleaned dataframe  
├── DateTime column parsing
├── Boolean column conversion
├── Categorical column optimization
└── Output: Type-optimized dataframe
```

**Key Features**:
- Memory optimization through appropriate data types
- Robust datetime parsing with error handling
- Category dtype for memory efficiency

#### 3. Feature Engineering ([`feature_creator.py`](../src/pipeline/feature_creator.py))
```
Input: Type-optimized dataframe
├── Temporal feature creation
├── Media/security feature engineering
├── Employee behavior analysis
└── Output: Feature-enriched dataframe
```

**Key Features**:
- Domain-specific feature creation
- Derived metrics and ratios
- Time-based pattern recognition

#### 4. Categorical Encoding ([`categorical_encoder.py`](../src/pipeline/categorical_encoder.py))
```
Input: Feature-enriched dataframe
├── Cardinality analysis
├── Strategy selection per column
├── Encoding application
└── Output: Numerically encoded dataframe
```

**Strategy Selection Logic**:
- 1 unique value → Skip (constant)
- 2 unique values → Binary encoding
- ≤3 unique values → One-hot encoding only
- 4-10 unique values → Target + frequency encoding
- >10 unique values → Rare category grouping + appropriate strategy

#### 5. Statistical Transformations ([`statistical_transformer.py`](../src/pipeline/statistical_transformer.py))
```
Input: Encoded dataframe
├── Z-score parameter fitting
├── Statistical feature creation
└── Output: Statistically transformed dataframe
```

**Key Features**:
- StandardScaler integration
- Variance checking before transformation
- Robust error handling

#### 6. Feature Selection ([`variance_correlation_filter.py`](../src/pipeline/variance_correlation_filter.py))
```
Input: Transformed dataframe
├── Variance-based filtering
├── Correlation-based filtering
├── Protected column handling
└── Output: Filtered dataframe
```

**Protection Logic**:
- Z-score features are protected from filtering
- Target columns are automatically excluded
- Configurable protection rules

#### 7. Normalization ([`feature_normalizer.py`](../src/pipeline/feature_normalizer.py))
```
Input: Filtered dataframe
├── Scaler selection and fitting
├── Feature scaling application  
└── Output: Normalized dataframe ready for ML
```

**Scaling Options**:
- StandardScaler (default)
- MinMaxScaler
- RobustScaler

## 🔧 Component Interfaces

### Base Component Pattern
```python
class BasePreprocessor:
    def __init__(self):
        self.is_fitted = False
        self.fitted_params = {}
    
    def fit(self, df, **kwargs):
        """Learn parameters from training data"""
        # Implementation specific to component
        self.is_fitted = True
        return self
    
    def transform(self, df):
        """Apply learned parameters"""
        if not self.is_fitted:
            raise ValueError("Component must be fitted first")
        # Apply transformations
        return transformed_df
    
    def fit_transform(self, df, **kwargs):
        """Convenience method"""
        return self.fit(df, **kwargs).transform(df)
```

### Data Flow Validation
Each component performs validation to ensure data integrity:

```python
def transform(self, df):
    # Validate fitted state
    if not self.is_fitted:
        raise ValueError("Component must be fitted first")
    
    # Handle missing columns gracefully
    available_columns = [col for col in expected_columns if col in df.columns]
    
    # Apply transformations
    return processed_df
```

## 📊 State Management

### Fitted Parameters Storage
Components store various types of fitted parameters:

```python
# Example from CategoricalEncoder
self.fitted_params = {
    'encoding_strategies': {'col1': 'binary', 'col2': 'onehot_only'},
    'target_encodings': {'col1': {category: mean_value}},
    'frequency_encodings': {'col1': {category: frequency}},
    'category_groupings': {'col1': {rare_cat: 'OTHER_RARE'}}
}
```

### Memory Management
- Efficient storage of only necessary parameters
- Cleanup of intermediate variables
- Memory-optimized data type selection

## 🚨 Error Handling Strategy

### Graceful Degradation
```python
try:
    # Attempt primary processing
    result = primary_processing(data)
except Exception as e:
    logger.warning(f"Primary processing failed: {e}")
    # Fall back to simpler approach
    result = fallback_processing(data)
```

### Validation Gates
- Input validation at component entry points
- Intermediate validation during processing
- Output validation before returning results

### Logging Strategy
```python
import logging

logger = logging.getLogger(__name__)

# Progress tracking
logger.info(f"Processing {len(df)} rows")

# Warning for edge cases  
logger.warning(f"Column {col} has high cardinality: {nunique}")

# Error details for debugging
logger.error(f"Failed to process {col}: {str(e)}")
```

## 🔄 Extension Points

### Adding New Components
1. Inherit from base pattern
2. Implement `fit()` and `transform()` methods
3. Add to `PreprocessingPipeline` sequence
4. Update documentation

### Custom Encoding Strategies
Extend `CategoricalEncoder` with new strategies:

```python
def custom_encoding_strategy(self, df, col):
    # Custom implementation
    return encoded_data
```

### Domain-Specific Features
Add new feature creation methods to `FeatureCreator`:

```python
def create_domain_features(self, df):
    # Domain-specific feature engineering
    return feature_enriched_df
```

## 📈 Performance Considerations

### Memory Optimization
- Use of `float32` instead of `float64` where appropriate
- Category dtypes for categorical variables
- Selective column processing

### Computational Efficiency
- Vectorized operations using pandas/numpy
- Early termination for edge cases
- Minimal data copying

### Scalability
- Processing by chunks for large datasets
- Configurable parameters for different data sizes
- Memory usage monitoring

## 🔗 Related Documentation

- **[Main README](../README.md)** - Project overview and quick start
- **[Feature Engineering Guide](./FEATURE_ENGINEERING.md)** - Detailed feature creation strategies
- **[Data Processing Components](./DATA_PROCESSING.md)** - Individual component deep dives
- **[API Reference](./API_REFERENCE.md)** - Complete API documentation

## 🧪 Testing Strategy

### Unit Testing
- Individual component testing
- Edge case validation
- Parameter persistence testing

### Integration Testing
- End-to-end pipeline testing
- Data consistency validation
- Performance regression testing

### Data Validation
- Schema validation
- Data quality checks
- Transformation correctness
