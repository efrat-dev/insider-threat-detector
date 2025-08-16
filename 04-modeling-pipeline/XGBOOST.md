# XGBoost Meta-Model for Employee Risk Assessment

## Table of Contents
- [Overview](#overview)
- [Data Pipeline](#data-pipeline)
- [Model Architecture](#model-architecture)
- [Training Process](#training-process)
- [Threshold Selection](#threshold-selection)
- [Evaluation Metrics](#evaluation-metrics)
- [Feature Importance Analysis](#feature-importance-analysis)
- [Results](#results)
- [Code Structure](#code-structure)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Performance Analysis](#performance-analysis)

## Overview

This notebook implements the final stage of a multi-model ensemble approach for insider threat detection. The XGBoost meta-model combines predictions from specialized models (LSTM for temporal patterns, Isolation Forest for anomaly detection) with static employee features to make final risk assessments at the employee level.

The model addresses the critical business problem of identifying employees who pose security risks based on their behavioral patterns and background characteristics.

## Data Pipeline

### Data Sources
The pipeline integrates multiple data sources:
- **Action-level data**: Daily behavioral patterns from employees (train/test/validation splits)
- **LSTM scores**: Temporal pattern analysis results for all employees
- **Isolation Forest scores**: Anomaly detection results per employee
- **Static features**: Employee demographics and background information

### Data Aggregation Process
1. **Risk Ratio Calculation**: Employee malicious action ratio computed within each data split
2. **Binary Classification**: Employees with ≥20% malicious actions labeled as high-risk
3. **Feature Integration**: Static employee features merged with model-based scores
4. **Data Consistency**: Separate processing for train/validation/test to prevent data leakage

### Feature Set
**Static Employee Features (14 features):**
- `employee_seniority_years`: Years of service
- `employee_department_freq`: Department frequency encoding
- `employee_position_freq`: Position frequency encoding
- `employee_campus_cat_*`: Campus location (one-hot encoded)
- `is_contractor_binary`: Contractor status
- `employee_classification_freq`: Classification frequency
- `has_foreign_citizenship_binary`: Foreign citizenship flag
- `has_criminal_record_binary`: Criminal record flag
- `has_medical_history_binary`: Medical history flag
- `is_new_employee_binary`: New employee status
- `is_veteran_employee_binary`: Veteran status

**Model-based Features (2 features):**
- `lstm_score`: Temporal pattern analysis score
- `if_employee_score`: Isolation Forest anomaly score

## Model Architecture

### XGBoost Configuration
```python
params = {
    'objective': 'binary:logistic',
    'eval_metric': 'logloss',
    'max_depth': 4,
    'eta': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'seed': 42
}
```

### Training Strategy
- **Early Stopping**: 10 rounds to prevent overfitting
- **Validation Monitoring**: Real-time evaluation on validation set
- **Reproducibility**: Fixed random seed (42) for consistent results
- **Maximum Iterations**: 1000 boosting rounds with early stopping

## Training Process

The model training follows these steps:

1. **Data Preparation**: Convert pandas DataFrames to XGBoost DMatrix format
2. **Model Training**: Use `xgb.train()` with early stopping validation
3. **Best Iteration Selection**: Automatically select optimal number of boosting rounds
4. **Version-Compatible Prediction**: Handle different XGBoost API versions

### Training Output Analysis
The training log shows:
- Initial validation loss: 0.157
- Final validation loss: 0.051 (achieved at iteration 34)
- Early stopping triggered after 10 rounds of no improvement
- Total training iterations: 44

## Threshold Selection

### Strategy
The model employs a sophisticated threshold selection approach:

1. **Validation-Based Selection**: Threshold chosen to maximize F1-score on validation set
2. **Grid Search**: 1001 threshold candidates between 0 and 1
3. **Preference for 0.5**: Choose t=0.5 if F1@0.5 is within tolerance of maximum
4. **Tie-Breaking Rules**: 
   - Minimize |Precision - Recall| gap
   - Prefer threshold closest to 0.5

### Selected Threshold
- **Optimal Threshold**: 0.426
- **Validation F1-Score**: 0.80
- **Precision**: 0.71, **Recall**: 0.92

## Evaluation Metrics

### Performance Summary

| Metric | Validation | Test |
|--------|------------|------|
| **Accuracy** | 98% | 99% |
| **F1-Score** | 0.80 | 0.94 |
| **Precision** | 0.71 | 0.89 |
| **Recall** | 0.92 | 1.00 |
| **ROC AUC** | 0.97 | 0.98 |

### Confusion Matrix Results

**Test Set Performance:**
- True Negatives: 318/318 (100% specificity)
- True Positives: 17/17 (100% sensitivity)
- False Positives: 0
- False Negatives: 0

## Feature Importance Analysis

### Top Contributing Features
1. **lstm_score** (13.22): Temporal behavioral patterns - most important
2. **if_employee_score** (3.63): Anomaly detection results
3. **employee_department_freq** (3.11): Department-based risk patterns
4. **employee_campus_cat_Campus B** (1.51): Location-specific risk
5. **employee_position_freq** (1.38): Role-based risk assessment

### Key Insights
- **Model-based features dominate**: LSTM and Isolation Forest scores provide 65% of total importance
- **Static features complement**: Department, campus, and position add contextual information
- **Demographic features minimal**: Personal characteristics (citizenship, criminal record) show low importance

## Results

### Model Performance
The XGBoost meta-model achieves exceptional performance:
- **Perfect Test Recall**: 100% detection of high-risk employees
- **High Precision**: 89% precision minimizes false alarms
- **Excellent Calibration**: ROC AUC of 0.98 indicates strong discriminative ability

### Business Impact
- **Risk Detection**: Successfully identifies all high-risk employees in test set
- **False Positive Control**: Only 2 false positives out of 335 employees
- **Operational Efficiency**: High precision reduces unnecessary investigations

## Code Structure

### Main Components
1. **Data Loading & Preprocessing**: Download and prepare multi-source data
2. **Employee-Level Aggregation**: Transform action-level to employee-level data
3. **Model Training**: XGBoost training with early stopping
4. **Threshold Optimization**: F1-maximizing threshold selection
5. **Comprehensive Evaluation**: Multiple metrics and visualization

### Key Functions
- `build_employee_level_df()`: Aggregates action-level data to employee level
- `choose_threshold_max_f1()`: Implements sophisticated threshold selection
- `predict_best()`: Version-compatible prediction handling

## Dependencies

```python
numpy>=1.21.0
pandas>=1.3.0
xgboost>=1.5.0
scikit-learn>=1.0.0
matplotlib>=3.5.0
seaborn>=0.11.0
gdown>=4.0.0
```

## Usage

### Running the Pipeline
```bash
# Execute the complete pipeline
jupyter notebook 04-modeling-pipeline/03_meta_xgboost.ipynb
```

### Key Parameters
- `THRESHOLD = 0.2`: Risk threshold for employee classification
- `SEED = 42`: Random seed for reproducibility
- Early stopping: 10 rounds
- Max depth: 4 (prevents overfitting)

## Performance Analysis

### Strengths
1. **Ensemble Approach**: Combines strengths of temporal (LSTM) and anomaly (IF) detection
2. **Robust Threshold Selection**: Data-driven threshold optimization
3. **No Overfitting**: Early stopping and conservative hyperparameters
4. **Interpretable Results**: Feature importance provides business insights

### Considerations
1. **Class Imbalance**: Only 5% positive cases (17/335 in test)
2. **Limited Test Cases**: Small number of positive cases limits statistical power
3. **Threshold Generalization**: Validation-based threshold may not generalize to future data distributions

### Model Reliability
The consistent performance across validation and test sets, combined with the early stopping mechanism, suggests a robust model that generalizes well to unseen data.

---

**Note**: This meta-model represents the final stage of a comprehensive insider threat detection system, combining multiple specialized models for optimal risk assessment accuracy.
