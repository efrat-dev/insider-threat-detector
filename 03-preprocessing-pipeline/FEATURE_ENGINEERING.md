# Feature Engineering Guide

## Overview

This guide provides comprehensive documentation for feature engineering strategies used in the insider threat detection pipeline. The feature engineering component ([`src/pipeline/feature_creator.py`](../src/pipeline/feature_creator.py)) creates domain-specific features that capture behavioral patterns relevant to insider threat detection.

## 🎯 Feature Engineering Philosophy

### Domain-Driven Approach
Features are designed based on security domain knowledge and insider threat research:
- **Behavioral Anomalies**: Unusual patterns in work habits, system usage
- **Temporal Patterns**: Time-based indicators of suspicious activity
- **Access Patterns**: Unusual data access or system interaction patterns
- **Risk Indicators**: Combinations of factors that elevate risk scores

### Feature Categories

```
Feature Engineering
├── Temporal Features
│   ├── Entry/Exit Patterns
│   ├── Work Schedule Analysis
│   └── Calendar-based Features
├── Media/Security Features  
│   ├── Burn Request Analysis
│   ├── Classification Patterns
│   └── Print Command Analysis
└── Employee Behavior Features
    ├── Seniority Analysis
    ├── Location Patterns
    └── Travel Behavior
```

## 🕒 Temporal Features

### Implementation Location
**File**: [`src/pipeline/feature_creator.py`](../src/pipeline/feature_creator.py) - `create_temporal_features()`

### Date and Calendar Features

```python
# Core date features
df_processed['date'] = pd.to_datetime(df_processed['date'], errors='coerce')
df_processed['weekday'] = df_processed['date'].dt.weekday  # 0=Monday, 6=Sunday
df_processed['month'] = df_processed['date'].dt.month

# Business calendar features
df_processed['is_end_of_month'] = (df_processed['date'].dt.day >= 25).astype(int)
df_processed['is_quarter_end'] = df_processed['month'].isin([3, 6, 9, 12]).astype(int)
```

**Business Rationale**:
- End-of-month activities may correlate with financial/reporting cycles
- Quarter-end periods often involve increased legitimate activity
- Weekday patterns help identify unusual weekend access

### Entry/Exit Time Analysis

```python
# Entry time processing
df_processed['first_entry_time'] = pd.to_datetime(df_processed.get('first_entry_time'), errors='coerce')
df_processed['entry_hour'] = df_processed['first_entry_time'].dt.hour
df_processed['entry_minute'] = df_processed['first_entry_time'].dt.minute
df_processed['entry_time_numeric'] = df_processed['entry_hour'] + df_processed['entry_minute'] / 60

# Exit time processing  
df_processed['last_exit_time'] = pd.to_datetime(df_processed.get('last_exit_time'), errors='coerce')
df_processed['exit_hour'] = df_processed['last_exit_time'].dt.hour
df_processed['exit_minute'] = df_processed['last_exit_time'].dt.minute
df_processed['exit_time_numeric'] = df_processed['exit_hour'] + df_processed['exit_minute'] / 60
```

**Key Features Created**:
- `entry_time_numeric`: Decimal hour representation of entry time (e.g., 9.5 = 9:30 AM)
- `exit_time_numeric`: Decimal hour representation of exit time

**Security Significance**:
- Unusual entry/exit times may indicate after-hours unauthorized access
- Numeric representation enables ML algorithms to detect time-based patterns
- Facilitates detection of employees working unusual schedules

### Feature Cleanup Strategy

```python
# Remove intermediate columns to reduce dimensionality
drop_cols = ['entry_hour', 'entry_minute', 'exit_hour', 'exit_minute']
df_processed = df_processed.drop(columns=[col for col in drop_cols if col in df_processed.columns])
```

## 💾 Media and Security Features

### Implementation Location  
**File**: [`src/pipeline/feature_creator.py`](../src/pipeline/feature_creator.py) - `create_media_features()`

### Burn Request Analysis

```python
# Volume and frequency analysis
df_processed['avg_burn_volume_per_request'] = (
    df_processed['total_burn_volume_mb'] / np.maximum(df_processed['num_burn_requests'], 1)
)

# Activity intensity
df_processed['burn_intensity'] = (
    df_processed['num_burn_requests'] / np.maximum(df_processed['total_presence_minutes'] / 60, 1)
)
```

**Key Metrics**:
- `avg_burn_volume_per_request`: Average data volume per burn operation
- `burn_intensity`: Burn requests per hour of presence

**Security Rationale**:
- Large volumes per request may indicate bulk data exfiltration
- High intensity suggests rushed or automated data extraction
- Comparing volume patterns across employees identifies outliers

### Classification Pattern Analysis

```python
# High-risk classification detection
df_processed['high_classification_burn'] = (
    df_processed['max_request_classification'] >= 4
).astype(int)

# Classification consistency analysis
df_processed['classification_variance'] = (
    df_processed['max_request_classification'] / 
    np.maximum(df_processed['avg_request_classification'], 1)
)
```

**Security Indicators**:
- `high_classification_burn`: Binary flag for high-sensitivity data access
- `classification_variance`: Ratio indicating diversity of accessed data sensitivity

### Off-Hours Activity Analysis

```python
# Off-hours behavior patterns
df_processed['off_hours_burn_ratio'] = (
    df_processed['num_burn_requests_off_hours'] / 
    np.maximum(df_processed['num_burn_requests'], 1)
)
```

**Risk Assessment**:
- High off-hours ratios may indicate attempts to avoid detection
- Combined with volume analysis, identifies suspicious patterns

### Behavioral Profiling

```python
# Heavy user identification
df_processed['is_heavy_burner'] = (
    df_processed['num_burn_requests'] > df_processed['num_burn_requests'].quantile(0.8)
).astype(int)
```

**Profiling Logic**:
- Top 20% of users by burn request volume
- Enables detection of unusual activity spikes in typically low-activity users

### Print Command Analysis

```python
# Print behavior analysis
df_processed['avg_pages_per_print'] = (
    df_processed['total_printed_pages'] / np.maximum(df_processed['num_print_commands'], 1)
)

df_processed['print_intensity'] = (
    df_processed['num_print_commands'] / np.maximum(df_processed['total_presence_minutes'] / 60, 1)
)

# Off-hours printing patterns
df_processed['off_hours_ratio'] = (
    df_processed['num_print_commands_off_hours'] / 
    np.maximum(df_processed['num_print_commands'], 1)
)

# Heavy printer identification
df_processed['is_heavy_printer'] = (
    df_processed['num_print_commands'] > df_processed['num_print_commands'].quantile(0.8)
).astype(int)
```

## 👤 Employee Behavior Features

### Implementation Location
**File**: [`src/pipeline/feature_creator.py`](../src/pipeline/feature_creator.py) - `create_employee_features()`

### Geographic Risk Assessment

```python
# Location consistency analysis
country_name_str = df_processed['country_name'].astype(str) if 'country_name' in df_processed.columns else None
employee_origin_str = df_processed['employee_origin_country'].astype(str) if 'employee_origin_country' in df_processed.columns else None

# Geographic risk indicator
if country_name_str is not None and employee_origin_str is not None:
    df_processed['is_employee_in_origin_country'] = (
        country_name_str == employee_origin_str
    ).astype(int)
```

**Security Implications**:
- Employees working outside their origin country may have different risk profiles
- Enables detection of unusual travel or relocation patterns
- Facilitates analysis of cross-border data access patterns

### Seniority-Based Risk Profiling

```python
# Experience-based categorization
df_processed['is_new_employee'] = (df_processed['employee_seniority_years'] < 1).astype(int)
df_processed['is_veteran_employee'] = (df_processed['employee_seniority_years'] > 10).astype(int)
```

**Risk Categories**:
- **New Employees** (`< 1 year`): May lack proper security training, higher accident risk
- **Veteran Employees** (`> 10 years`): May have elevated access, insider knowledge
- **Mid-level Employees** (`1-10 years`): Baseline group for comparison

**Behavioral Assumptions**:
- New employees may exhibit learning-related access patterns
- Veterans may have established routines that, when broken, indicate risk
- Mid-level employees provide behavioral baseline for anomaly detection

## 🔧 Technical Implementation Details

### Safe Division Pattern

Throughout the feature engineering, a consistent pattern is used to prevent division by zero:

```python
# Safe division using np.maximum
result = numerator / np.maximum(denominator, 1)
```

**Why This Approach**:
- Prevents runtime errors from division by zero
- Maintains data type consistency
- Provides sensible default values (0/1 = 0 for rate calculations)

### Error Handling Strategy

```python
# Robust string conversion for categorical comparisons
country_name_str = df_processed['country_name'].astype(str) if 'country_name' in df_processed.columns else None

# Conditional feature creation
if country_name_str is not None and employee_origin_str is not None:
    # Feature creation logic
```

### Memory Efficiency

```python
# Quantile calculation for behavioral profiling
threshold = df_processed['num_burn_requests'].quantile(0.8)
df_processed['is_heavy_burner'] = (df_processed['num_burn_requests'] > threshold).astype(int)
```

**Optimization Benefits**:
- Single quantile calculation per column
- Boolean to integer conversion for consistent data types
- Minimal memory overhead for profiling features

## 📊 Feature Engineering Pipeline Integration

### Pipeline Integration Point
**File**: [`src/pipeline/preprocessing_pipeline.py`](../src/pipeline/preprocessing_pipeline.py)

```python
def fit(self, X_train, y_train=None):
    # ... other preprocessing steps
    
    df_train = self.feature_creator.create_all_features(df_train)
    
    # ... subsequent preprocessing steps
```

### Feature Creation Sequence

```python
def create_all_features(self, df):
    """Create all new features by applying all feature creation methods."""
    df_processed = df.copy()
    df_processed = self.create_temporal_features(df_processed)      # 1st: Time-based features
    df_processed = self.create_media_features(df_processed)        # 2nd: Security features  
    df_processed = self.create_employee_features(df_processed)     # 3rd: Employee profiling
    return df_processed
```

**Order Rationale**:
1. **Temporal features first**: Base time representations needed for other calculations
2. **Media features second**: May depend on presence time calculations
3. **Employee features last**: Profiling features that may use other derived features

## 🎨 Feature Design Patterns

### Rate and Ratio Features
```python
# Pattern: Activity per unit time
activity_rate = activity_count / np.maximum(time_present, 1)

# Pattern: Proportion analysis  
proportion = subset_count / np.maximum(total_count, 1)
```

### Binary Risk Indicators
```python
# Pattern: Threshold-based flags
risk_flag = (risk_metric > threshold).astype(int)

# Pattern: Categorical comparison flags
match_flag = (category_a == category_b).astype(int)
```

### Behavioral Profiling
```python
# Pattern: Percentile-based grouping
high_activity_threshold = data['activity_metric'].quantile(0.8)
is_high_activity = (data['activity_metric'] > high_activity_threshold).astype(int)
```

## 🚀 Extending Feature Engineering

### Adding New Feature Categories

1. **Create new method in FeatureCreator**:
```python
def create_network_features(self, df):
    """Create network-based security features."""
    # Implementation
    return df_processed
```

2. **Add to feature creation pipeline**:
```python
def create_all_features(self, df):
    # ... existing features
    df_processed = self.create_network_features(df_processed)
    return df_processed
```

### Custom Domain Features

```python
def create_custom_domain_features(self, df):
    """Create features specific to your domain."""
    df_processed = df.copy()
    
    # Example: Unusual data access patterns
    df_processed['data_access_entropy'] = calculate_entropy(df_processed['access_patterns'])
    
    # Example: Communication anomalies
    df_processed['comm_anomaly_score'] = detect_communication_anomalies(df_processed)
    
    return df_processed
```

## 📈 Feature Validation and Quality

### Feature Quality Metrics

```python
# Check feature coverage
non_null_ratio = df['new_feature'].count() / len(df)

# Check feature variance
feature_variance = df['new_feature'].var()

# Check feature correlation with target
target_correlation = df['new_feature'].corr(df['target'])
```

### Feature Engineering Best Practices

1. **Domain Knowledge Integration**: Features should encode security expertise
2. **Robustness**: Handle missing data and edge cases gracefully  
3. **Interpretability**: Features should be explainable to security analysts
4. **Scalability**: Efficient computation for large datasets
5. **Validation**: Test features on held-out data

## 🔗 Related Documentation

- **[Main README](../README.md)** - Project overview and setup
- **[Pipeline Architecture](./PIPELINE_ARCHITECTURE.md)** - Overall pipeline design
- **[Data Processing Components](./DATA_PROCESSING.md)** - Other preprocessing components
- **[API Reference](./API_REFERENCE.md)** - Complete method documentation

## 📚 Research References

Feature engineering draws from insider threat research:
- Temporal pattern analysis for anomaly detection
- Behavioral profiling in security contexts
- Risk indicator development from security domain expertise
- Feature engineering for imbalanced security datasets
