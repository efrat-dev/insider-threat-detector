# Isolation Forest Employee Anomaly Detection

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technical Architecture](#technical-architecture)
  - [Data Flow](#data-flow)
  - [Peer-Relative Features](#peer-relative-features)
  - [Employee Score Aggregation](#employee-score-aggregation)
  - [Thresholding Strategies](#thresholding-strategies)
- [Configuration Parameters](#configuration-parameters)
- [Data Requirements](#data-requirements)
  - [Input Files](#input-files)
  - [Required Columns](#required-columns)
- [Algorithm Details](#algorithm-details)
  - [1. Feature Engineering](#1-feature-engineering)
  - [2. Isolation Forest Training](#2-isolation-forest-training)
  - [3. Score Aggregation](#3-score-aggregation)
  - [4. Threshold Optimization](#4-threshold-optimization)
- [Results Analysis](#results-analysis)
  - [Performance Metrics](#performance-metrics)
  - [Validation Results](#validation-results)
  - [Test Results](#test-results)
  - [Top Anomalous Employees](#top-anomalous-employees)
- [Usage Instructions](#usage-instructions)
  - [1. Environment Setup](#1-environment-setup)
  - [2. Run Complete Pipeline](#2-run-complete-pipeline)
  - [3. Key Outputs](#3-key-outputs)
- [Key Advantages](#key-advantages)
- [Future Improvements](#future-improvements)
- [Implementation Notes](#implementation-notes)

## Project Overview

This project implements a comprehensive anomaly detection system for employee behavior analysis using Isolation Forest with peer-relative feature engineering. The system performs automatic hyperparameter sweeping across multiple configurations to identify the optimal strategy for detecting anomalous employee patterns.

## Key Features

- **Peer-Relative Feature Engineering**: Computes employee anomaly scores relative to their peers (department, position, or combined)
- **Multiple Aggregation Strategies**: Supports various methods for aggregating action-level scores to employee-level scores
- **Automated Hyperparameter Sweep**: Systematically evaluates all parameter combinations
- **Isotonic Calibration**: Optional probability calibration for improved threshold selection
- **Flexible Thresholding**: Global or department-specific thresholds with precision floor constraints
- **Comprehensive Evaluation**: ROC/PR curves, confusion matrices, and threshold stability analysis

## Technical Architecture

### Data Flow
1. **Data Loading**: Train/Val/Test splits with employee mapping (department/position)
2. **Feature Engineering**: Peer-relative features based on statistical comparisons
3. **Model Training**: Isolation Forest trained on relative features
4. **Score Aggregation**: Action-level scores aggregated to employee-level
5. **Threshold Selection**: Optimal thresholds with precision constraints
6. **Evaluation**: Comprehensive performance metrics and visualizations

### Peer-Relative Features

The system computes three types of relative features for each base feature:
- **Mean Difference**: `x - peer_mean`
- **Z-score**: `(x - peer_mean) / peer_std`
- **Median Difference**: `x - peer_median`

#### Peer Group Modes:
- **`dept`**: Department-based peers with global fallback
- **`pos`**: Position-based peers with global fallback
- **`dp`**: Department+Position peers with cascading fallback (dept → global)

### Employee Score Aggregation

Three aggregation methods for converting action-level anomaly scores to employee-level:
- **`top3_mean`**: Mean of top 3 anomaly scores
- **`top3_median`**: Median of top 3 anomaly scores
- **`top5_trimmed_mean`**: Trimmed mean of top 5 scores (excluding highest)

### Thresholding Strategies

- **Global**: Single threshold across all employees
- **Per-Department**: Department-specific thresholds with global fallback
- **Precision Floor**: Ensures minimum precision (default: 0.55)
- **F-beta Optimization**: Optimizes F1 score by default

## Configuration Parameters

```python
# Core Parameters
PEER_MODES = ["dept", "pos", "dp"]                    # Peer group strategies
AGGREGATORS = ["top3_mean", "top3_median", "top5_trimmed_mean"]  # Score aggregation
CALIBRATION = [False, True]                           # Isotonic calibration
THR_MODES = ["global", "per_dept"]                    # Threshold strategies

# Optimization Settings
FBETA_SWEEP = 1.0                                     # F-beta for optimization
P_MIN_FLOOR = 0.55                                    # Minimum precision threshold
MIN_VAL_EMP_PER_DEPT = 8                             # Min employees per dept for thresholding
EMPLOYEE_LABEL_RULE = "ratio>=0.2"                   # Employee labeling rule

# Model Settings
SEED = 42                                             # Random seed
TOP_N = 30                                            # Top anomalous employees to display
```

## Data Requirements

### Input Files
- `train_processed.csv`: Training data
- `val_processed.csv`: Validation data
- `test_processed.csv`: Test data
- `mapping_emp_dep_pos.csv`: Employee-department-position mapping

### Required Columns
- `employee_id`: Unique employee identifier
- `employee_department`: Employee department
- `employee_position`: Employee position
- `is_malicious`: Action-level labels (0/1)
- Numeric feature columns (excluding static/zscore/quartile features)

## Algorithm Details

### 1. Feature Engineering
```python
# Example: Department-based relative features
def build_rel_features(df, feat_cols, mode="dept"):
    # Compute department statistics from training data
    dept_stats = train_df.groupby('department')[feat_cols].agg(['mean', 'std', 'median'])
    
    # For each employee action, compute relative features
    relative_features = {
        f"{col}__diff_grp_mean": df[col] - dept_mean[col],
        f"{col}__z_in_grp": (df[col] - dept_mean[col]) / dept_std[col],
        f"{col}__diff_grp_med": df[col] - dept_median[col]
    }
```

### 2. Isolation Forest Training
```python
iso = IsolationForest(
    n_estimators=300,
    max_samples="auto",
    max_features=1.0,
    contamination="auto",
    random_state=SEED
)
```

### 3. Score Aggregation
```python
def agg_emp(scores, mode="top3_mean"):
    sorted_scores = np.sort(scores)
    if mode == "top3_mean":
        return np.mean(sorted_scores[-3:])
    elif mode == "top5_trimmed_mean":
        top5 = sorted_scores[-5:]
        return np.mean(top5[:-1])  # Exclude highest
```

### 4. Threshold Optimization
```python
def pick_threshold(y_true, scores, beta=1.0, p_min=0.55):
    # Grid search over threshold candidates
    thresholds = np.quantile(scores, np.linspace(0.05, 0.99, 300))
    
    best_fbeta = -1
    for threshold in thresholds:
        predictions = (scores >= threshold).astype(int)
        precision = precision_score(y_true, predictions)
        
        # Apply precision floor constraint
        if precision < p_min:
            continue
            
        fbeta = fbeta_score(y_true, predictions, beta=beta)
        if fbeta > best_fbeta:
            best_fbeta = fbeta
            best_threshold = threshold
```

## Results Analysis

### Performance Metrics
The system achieved optimal performance with:
- **Peer Mode**: Department-based (`dept`)
- **Aggregator**: Top-5 trimmed mean (`top5_trimmed_mean`)
- **Calibration**: Enabled (isotonic calibration)
- **Threshold Mode**: Per-department (`per_dept`)

### Validation Results
- **Precision**: 83.3%
- **Recall**: 76.9%
- **F1-Score**: 80.0%

### Test Results
- **Precision**: 75.0%
- **Recall**: 70.6%
- **F1-Score**: 72.7%

### Top Anomalous Employees
The system identifies the top 30 most anomalous employees with scores ranging from 0.640 to 0.669, providing actionable insights for security teams.

## Usage Instructions

### 1. Environment Setup
```bash
pip install numpy pandas matplotlib scikit-learn gdown
```

### 2. Run Complete Pipeline
```python
# Execute the full pipeline
python isolation_forest_pipeline.py
```

### 3. Key Outputs
- **Console**: Hyperparameter sweep results and performance metrics
- **Plots**: ROC curves, PR curves, confusion matrices, threshold stability
- **CSV**: `if_score_per_employee.csv` with final anomaly scores
- **Directory**: `IF_peer_relative_top3_output/` containing all artifacts

## Key Advantages

1. **Peer-Relative Analysis**: Accounts for normal behavior variations across departments/positions
2. **Robust Aggregation**: Multiple aggregation strategies prevent single-action bias
3. **Automated Optimization**: Systematic hyperparameter search ensures optimal configuration
4. **Precision Control**: Precision floor prevents excessive false positives
5. **Scalable Thresholding**: Department-specific thresholds adapt to organizational structure
6. **Comprehensive Evaluation**: Detailed performance analysis with multiple metrics

## Future Improvements

1. **Consistency Enhancement**: The validation-test performance gap suggests room for improved generalization
2. **Ensemble Methods**: Combining multiple peer modes could reduce noise
3. **Temporal Features**: Incorporating time-based patterns for dynamic anomaly detection
4. **Feature Selection**: Advanced feature selection techniques for improved signal-to-noise ratio
5. **Online Learning**: Adaptive thresholds that evolve with organizational changes

## Implementation Notes

- **Memory Efficiency**: Uses sparse representations and batch processing for large datasets
- **Reproducibility**: Fixed random seeds ensure consistent results
- **Error Handling**: Robust error handling for missing data and edge cases
- **Visualization**: Rich plotting capabilities for result interpretation
- **Export Features**: Automated artifact saving for reporting and analysis

This implementation provides a production-ready anomaly detection system with comprehensive evaluation capabilities and actionable insights for organizational security teams.
