# Insider Threat Detection System

A comprehensive machine learning pipeline for detecting insider threats using multiple complementary approaches including temporal pattern analysis, anomaly detection, and ensemble methods.

## 🎯 Project Overview

This project implements an advanced insider threat detection system that combines three specialized machine learning models to identify potentially malicious employees based on their behavioral patterns and background characteristics. The system processes employee activity data to detect anomalous behavior that may indicate security risks.

### Key Features

- **Multi-Model Ensemble**: Combines temporal analysis, anomaly detection, and meta-learning
- **Peer-Relative Analysis**: Compares employee behavior against departmental and positional peers
- **Temporal Pattern Recognition**: Analyzes behavioral sequences over time
- **Automated Hyperparameter Optimization**: Systematic parameter tuning across all models
- **Production-Ready Pipeline**: Comprehensive evaluation and deployment-ready outputs

## 🏗️ System Architecture

The system employs a three-stage modeling approach:

```
Raw Employee Data
        ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   LSTM          │   Isolation     │   Static        │
│   Autoencoder   │   Forest        │   Features      │
│   (Temporal)    │   (Anomaly)     │   (Background)  │
└─────────────────┴─────────────────┴─────────────────┘
        ↓               ↓               ↓
        └───────────────┼───────────────┘
                        ↓
                ┌─────────────────┐
                │   XGBoost       │
                │   Meta-Model    │
                │   (Final Risk)  │
                └─────────────────┘
                        ↓
                Employee Risk Scores
```

## 🤖 Models Overview

### 1. LSTM Autoencoder - Temporal Pattern Analysis

**Purpose**: Detects anomalies in temporal behavioral sequences using unsupervised learning.

**Key Features**:
- Encoder-decoder architecture for temporal pattern compression
- Dropout regularization and bottleneck layers
- Top-K reconstruction error scoring
- Validation-tuned threshold optimization

**Performance**:
- Test Accuracy: 98.0%
- Precision: 92.0%
- Recall: 65.0%
- F1-Score: 76.0%

**📖 Detailed Documentation**: [LSTM Autoencoder README](./docs/LSTM_AUTOENCODER.md)  
**💻 Implementation**: [01_lstm_autoencoder.ipynb](./01_lstm_autoencoder.ipynb)

---

### 2. Isolation Forest - Peer-Relative Anomaly Detection

**Purpose**: Identifies employees with anomalous behavior patterns relative to their organizational peers.

**Key Features**:
- Peer-relative feature engineering (department/position-based)
- Multiple score aggregation strategies
- Automated hyperparameter sweeping
- Department-specific threshold optimization

**Performance**:
- Validation F1-Score: 80.0%
- Test F1-Score: 72.7%
- Precision: 75.0% (with precision floor enforcement)

**📖 Detailed Documentation**: [Isolation Forest README](./docs/ISOLATION_FOREST.md)  
**💻 Implementation**: [02_isolation_forest.ipynb](./02_isolation_forest.ipynb)

---

### 3. XGBoost Meta-Model - Final Risk Assessment

**Purpose**: Combines outputs from specialized models with static employee features for final risk classification.

**Key Features**:
- Ensemble approach combining LSTM and Isolation Forest scores
- Integration of 14 static employee features
- F1-optimized threshold selection
- Feature importance analysis

**Performance**:
- Test Accuracy: 99%
- Precision: 89%
- Recall: 100%
- F1-Score: 94%
- ROC AUC: 0.98

**📖 Detailed Documentation**: [XGBoost Meta-Model README](./docs/XGBOOST.md)  
**💻 Implementation**: [03_meta_xgboost.ipynb](./03_xgboost.ipynb)

## 🚀 Quick Start

### Prerequisites

```bash
pip install numpy pandas matplotlib scikit-learn tensorflow xgboost gdown
```

### Running the Complete Pipeline

1. **Temporal Analysis**:
   ```bash
   jupyter notebook 04-modeling-pipeline/01_lstm_autoencoder.ipynb
   ```

2. **Anomaly Detection**:
   ```bash
   jupyter notebook 04-modeling-pipeline/02_isolation_forest.ipynb
   ```

3. **Meta-Model Training**:
   ```bash
   jupyter notebook 04-modeling-pipeline/03_meta_xgboost.ipynb
   ```

### Expected Outputs

- **LSTM Scores**: `outputs/lstm_v2/lstm_scores_all_splits.csv`
- **Isolation Forest Scores**: `IF_peer_relative_top3_output/if_score_per_employee.csv`
- **Final Risk Assessments**: Employee-level risk classifications
- **Model Artifacts**: Trained model checkpoints and evaluation plots

## 📊 Data Requirements

### Input Data Structure

- **Action-Level Data**: Employee daily activities with behavioral features
- **Employee Mapping**: Department and position information
- **Static Features**: Background characteristics (seniority, citizenship, etc.)
- **Temporal Requirements**: Minimum 30 days of activity per employee

### Key Data Splits

- **Training Set**: Model development and feature learning
- **Validation Set**: Hyperparameter optimization and threshold tuning
- **Test Set**: Final performance evaluation

## 🔍 Key Technical Innovations

### 1. Peer-Relative Feature Engineering
- Computes behavioral anomalies relative to departmental and positional peers
- Handles organizational hierarchy and role-specific normal behavior
- Provides robust baseline for comparison across different employee groups

### 2. Multi-Scale Temporal Analysis
- LSTM captures long-term behavioral patterns and dependencies
- Top-K scoring focuses on most anomalous activities rather than average behavior
- Sequence truncation and padding handle variable-length employee histories

### 3. Ensemble Meta-Learning
- Combines complementary strengths of temporal and anomaly detection approaches
- Integrates behavioral patterns with static risk factors
- Uses validation-based threshold optimization for optimal precision-recall balance

## 📈 Performance Summary

| Model | Precision | Recall | F1-Score | Strengths |
|-------|-----------|--------|----------|-----------|
| **LSTM Autoencoder** | 92.0% | 65.0% | 76.0% | Temporal patterns, low false positives |
| **Isolation Forest** | 75.0% | 70.6% | 72.7% | Peer-relative analysis, robust to outliers |
| **XGBoost Meta-Model** | 89.0% | 100% | 94.0% | Ensemble approach, perfect recall |

### Business Impact

- **Risk Detection**: 100% recall on test set - no high-risk employees missed
- **False Positive Control**: High precision minimizes unnecessary investigations
- **Interpretability**: Feature importance provides actionable insights
- **Scalability**: Handles large organizational datasets efficiently

## 🛠️ Advanced Configuration

### Hyperparameter Optimization

Each model includes comprehensive hyperparameter sweeping:

- **LSTM**: Architecture depth, dropout rates, bottleneck dimensions
- **Isolation Forest**: Peer grouping strategies, aggregation methods, contamination levels
- **XGBoost**: Tree depth, learning rates, regularization parameters

### Threshold Selection Strategies

- **Validation-Based**: F1-score maximization with precision floors
- **Statistical**: Percentile-based and standard deviation multipliers
- **Business-Driven**: Configurable precision-recall trade-offs

## 📝 Documentation Deep Dive

For comprehensive technical details, algorithm explanations, and implementation notes:

- **[Isolation Forest Documentation](./docs/ISOLATION_FOREST.md)**: Peer-relative anomaly detection methodology
- **[LSTM Autoencoder Documentation](./docs/LSTM_AUTOENCODER.md)**: Temporal pattern analysis and architecture details  
- **[XGBoost Meta-Model Documentation](./docs/XGBOOST.md)**: Ensemble approach and feature integration

## 🔧 Customization and Extension

### Adding New Features

1. **Static Features**: Add employee background variables to XGBoost model
2. **Behavioral Features**: Include additional activity metrics in LSTM input
3. **Peer Groups**: Extend peer-relative analysis to new organizational dimensions

### Model Enhancements

- **Attention Mechanisms**: Improve temporal pattern recognition in LSTM
- **Ensemble Methods**: Add additional specialized models to meta-learning stage
- **Online Learning**: Implement adaptive thresholds for evolving threats

## 🚨 Production Considerations

### Deployment Requirements

- **Model Artifacts**: Trained model checkpoints and preprocessing pipelines
- **Threshold Configuration**: Environment-specific threshold settings
- **Monitoring**: Performance drift detection and retraining triggers

### Security and Privacy

- **Data Protection**: Employee behavioral data requires secure handling
- **Model Interpretability**: Feature importance supports audit and compliance
- **Bias Detection**: Regular evaluation across demographic groups

---

**Note**: This system processes sensitive employee data and should be deployed with appropriate security, privacy, and ethical considerations.