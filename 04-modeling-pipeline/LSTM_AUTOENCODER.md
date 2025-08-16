# LSTM Autoencoder for Insider Threat Detection

## Overview
This notebook implements LSTM (Long Short-Term Memory) Autoencoder models for detecting insider threats in employee behavioral data. The project includes two versions: a baseline simple model (V1) and an improved model (V2) with enhanced evaluation metrics and hyperparameter optimization.

## Table of Contents
- [Objective](#objective)
- [Data Description](#data-description)
- [Methodology](#methodology)
- [Model Architecture](#model-architecture)
- [Implementation Details](#implementation-details)
- [Evaluation Metrics](#evaluation-metrics)
- [Results](#results)
- [File Structure](#file-structure)
- [Usage](#usage)
- [Dependencies](#dependencies)

## Objective
The primary goal is to develop an unsupervised anomaly detection system that can identify potentially malicious employees based on their behavioral patterns over time. The system uses temporal sequences of employee activities to learn normal behavior patterns and flag anomalies.

## Data Description
The model processes employee behavioral data with the following characteristics:
- **Time-series data**: Employee activities tracked over multiple days
- **Features**: Z-scored behavioral metrics (excluding static demographic features)
- **Target**: Binary classification (malicious vs. benign employees)
- **Splits**: Training, validation, and test sets
- **Minimum sequence length**: 30 days per employee
- **Feature filtering**: Excludes static features like department, position, background checks

### Key Data Processing Steps:
1. **Feature Selection**: Uses only `*_zscore` features, excluding static employee attributes
2. **Temporal Grouping**: Groups data by employee ID and sorts chronologically
3. **Sequence Creation**: Creates time-series sequences per employee
4. **Padding/Truncation**: Standardizes sequence lengths (V2 supports truncation to last N timesteps)

## Methodology

### Approach
The project implements an **unsupervised learning approach** using autoencoder neural networks:
1. **Training Phase**: Models learn to reconstruct normal (benign) employee behavior patterns
2. **Anomaly Detection**: High reconstruction errors indicate potential anomalies
3. **Threshold Selection**: Uses validation set to optimize detection thresholds

### Two-Version Implementation

#### Version 1 (V1) - Baseline Simple Model
- **Architecture**: Simple LSTM autoencoder without regularization
- **Latent Dimension**: 32
- **Evaluation**: Mean MSE with fixed threshold (97.5th percentile of training scores)
- **Purpose**: Baseline comparison and proof of concept

#### Version 2 (V2) - Improved Model
- **Architecture**: Enhanced with dropout regularization and smaller bottleneck
- **Latent Dimension**: 16 (more compressed representation)
- **Dropout Rate**: 0.1
- **Evaluation**: Top-K scoring with validation-tuned thresholds
- **Features**: Advanced evaluation metrics and CSV output generation

## Model Architecture

### V1 Architecture
```
Input Layer (timesteps, features)
    ↓
LSTM Encoder (64 units, tanh)
    ↓
Dense Bottleneck (32 units, relu)
    ↓
Repeat Vector (repeat bottleneck)
    ↓
LSTM Decoder (64 units, tanh)
    ↓
TimeDistributed Dense (output features)
```

### V2 Architecture (Improved)
```
Input Layer (timesteps, features)
    ↓
LSTM Encoder (64 units, tanh)
    ↓
Dropout (0.1)
    ↓
Dense Bottleneck (16 units, relu)
    ↓
Repeat Vector (repeat bottleneck)
    ↓
LSTM Decoder (64 units, tanh)
    ↓
Dropout (0.1)
    ↓
TimeDistributed Dense (output features)
```

### Key Architecture Features:
- **Encoder-Decoder Structure**: Compresses temporal patterns into latent representation
- **LSTM Layers**: Capture temporal dependencies in behavioral sequences
- **Bottleneck Layer**: Forces model to learn compact representations
- **Reconstruction Objective**: Minimizes Mean Squared Error (MSE) between input and output

## Implementation Details

### Data Preparation Functions
- `prepare_lstm_input()` (V1): Basic sequence preparation with padding
- `prepare_lstm_input_V2()` (V2): Enhanced with sequence truncation support

### Training Configuration
- **Optimizer**: Adam
- **Loss Function**: Mean Squared Error (MSE)
- **Batch Size**: 32
- **Maximum Epochs**: 50 (V2), 20 (V1)
- **Early Stopping**: Patience of 5 epochs
- **Validation Monitoring**: Best weights restored based on validation loss

### Reproducibility Measures
- **Fixed Random Seeds**: Ensures consistent results
- **Threading Control**: Single-threaded execution for reproducibility
- **Seed Reset**: Between model versions for fair comparison

## Evaluation Metrics

### V1 Evaluation (Simple Baseline)
- **Scoring Method**: Mean MSE across all timesteps and features
- **Threshold**: Fixed at 97.5th percentile of training scores
- **Metrics**: Precision, Recall, F1-score, Confusion Matrix
- **Datasets**: Applied to validation and test sets

### V2 Evaluation (Advanced)
- **Scoring Method**: Top-K mean (default K=3) of reconstruction errors
- **Threshold Optimization**: Grid search on validation set using:
  - Percentile-based thresholds (80-99th percentiles)
  - Statistical thresholds (Mean + k*STD, k=1.0,1.5,2.0,2.5)
- **Selection Criteria**: Best F1-score on validation set
- **Comprehensive Metrics**:
  - Classification Report (Precision, Recall, F1)
  - ROC Curve and AUC Score
  - Confusion Matrices
  - Score Distribution Histograms

### Advanced Features (V2)
- **Top-K Scoring**: More robust than simple averaging
- **Validation-Tuned Thresholds**: Optimizes detection performance
- **Cross-Split Analysis**: Consistent evaluation across train/val/test
- **CSV Output Generation**: Saves scores for downstream analysis

## Results

### V1 Results (Baseline)
- **Test Accuracy**: 94.3%
- **Precision (Malicious)**: 43.8%
- **Recall (Malicious)**: 41.2%
- **F1-Score (Malicious)**: 42.4%

### V2 Results (Improved)
- **Test Accuracy**: 98.0%
- **Precision (Malicious)**: 92.0%
- **Recall (Malicious)**: 65.0%
- **F1-Score (Malicious)**: 76.0%
- **ROC AUC**: Computed and visualized

### Performance Comparison
The V2 model shows significant improvements over V1:
- **Higher Precision**: Reduced false positive rate
- **Better Overall Accuracy**: More reliable predictions
- **Optimized Thresholds**: Better balance between precision and recall

## File Structure
```
├── 04-modeling-pipeline/
│   └── 01_lstm_autoencoder.ipynb
├── outputs/
│   └── lstm_v2/
│       ├── lstm_score_per_employee_train.csv
│       ├── lstm_score_per_employee_val.csv
│       ├── lstm_score_per_employee_test.csv
│       └── lstm_scores_all_splits.csv
├── best_lstm_v1.keras (V1 model checkpoint)
└── best_lstm_model.keras (V2 model checkpoint)
```

### Output Files Description
- **Individual Split Files**: Separate CSV files for train/validation/test scores
- **Unified File**: Combined scores across all data splits
- **Model Checkpoints**: Saved best models for inference

## Usage

### Running the Notebook
1. **Environment Setup**: Ensure all dependencies are installed
2. **Data Paths**: Update file paths to your processed data location
3. **Sequential Execution**: Run cells in order (V1 followed by V2)
4. **Output Review**: Check generated visualizations and CSV files

### Key Parameters to Modify
- `max_length`: Maximum sequence length (default: 60 for V2)
- `min_days`: Minimum sequence length per employee (default: 30)
- `TOP_K`: Number of top errors to average (default: 3)
- `latent_dim`: Bottleneck dimension (32 for V1, 16 for V2)
- `dropout_rate`: Regularization strength (V2 only, default: 0.1)

### Customization Options
- **Feature Selection**: Modify `exclude_keywords` to change feature sets
- **Threshold Tuning**: Adjust percentile ranges and statistical multipliers
- **Architecture**: Modify LSTM units, layers, or activation functions
- **Training**: Change epochs, batch size, or patience parameters

## Dependencies
```python
# Core Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Deep Learning
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, LSTM, RepeatVector, TimeDistributed, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Evaluation
from sklearn.metrics import (
    precision_score, recall_score, f1_score, classification_report,
    confusion_matrix, ConfusionMatrixDisplay, roc_curve, roc_auc_score
)

# System
import os
import random
from google.colab import drive  # For Colab environment
```

## Technical Considerations

### Memory and Performance
- **Sequence Padding**: May create large tensors; monitor memory usage
- **Batch Processing**: Uses batched predictions for efficiency
- **Model Checkpoints**: Automatically saves best models during training

### Limitations and Assumptions
- **Unsupervised Learning**: Relies on assumption that training data is predominantly benign
- **Temporal Dependencies**: Assumes behavioral patterns have temporal structure
- **Feature Engineering**: Performance depends on quality of input features
- **Threshold Sensitivity**: Detection performance varies with threshold selection

### Future Enhancements
- **Attention Mechanisms**: Could improve temporal pattern recognition
- **Multi-Scale Analysis**: Different time window analyses
- **Ensemble Methods**: Combining multiple autoencoder variants
- **Online Learning**: Adapting to evolving behavioral patterns

## Conclusion
This LSTM Autoencoder implementation provides a robust foundation for insider threat detection using temporal behavioral data. The two-version approach demonstrates clear performance improvements through architectural enhancements and evaluation methodology refinements. The comprehensive evaluation framework and output generation make it suitable for production deployment and further research.
