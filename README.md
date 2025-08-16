# Insider Threat Detection System

An ensemble machine learning approach for detecting insider threats using LSTM, Isolation Forest, and XGBoost models.

## Project Overview

This project implements a comprehensive insider threat detection system that analyzes employee behavior patterns to identify potential malicious activities. The system uses an ensemble approach combining deep learning (LSTM) and classical machine learning models (Isolation Forest and XGBoost) to achieve robust threat detection.

## Architecture

The project follows a sequential pipeline architecture:

```
project_root/
│
├─ 01-data-generation-pipeline/     # Synthetic data generation
├─ 02-exploratory-data-analysis/                 # Exploratory Data Analysis
├─ 03-preprocessing-pipeline/       # Data preprocessing & feature engineering
├─ 04-modeling-pipeline/            # Machine learning models
│   ├─ 01_lstm.ipynb              # LSTM neural network
│   ├─ 02_isolation_forest.ipynb  # Anomaly detection model
│   └─ 03_xgboost.ipynb           # Ensemble classifier
│
└─ outputs/                         # All pipeline outputs
    ├─ 01-data-generation-pipeline/             # Raw data backup
    ├─ 02-preprocessing/               # Processed data for LSTM & Isolation Forest
    └─ 03-modeling-pipeline/                    # Scores and model artifacts
```

## Data Flow

### 1. Data Generation
- **Pipeline**: `01_data_generation_pipeline/`
- **Output**: `data/raw/`
- **Purpose**: Generates synthetic employee and action data for training

### 2. Exploratory Data Analysis
- **Notebook**: `02_eda.ipynb`
- **Input**: `data/raw/`
- **Purpose**: Data exploration, visualization, and initial insights

### 3. Data Preprocessing
- **Pipeline**: `03_preprocessing_pipeline/`
- **Input**: `data/raw/`
- **Output**: `outputs/preprocessing/`
- **Purpose**: Feature engineering and creation of train/validation/test splits for LSTM and Isolation Forest models

### 4. Model Training & Predictions

#### LSTM Model (04a_lstm.ipynb)
- **Input**: `outputs/preprocessing/`
- **Output**: `outputs/lstm/`
- **Purpose**: Sequential pattern analysis and risk scoring at employee level
- **Key Features**: Time series analysis of user behavior patterns

#### Isolation Forest Model (04b_isolation_forest.ipynb)
- **Input**: `outputs/preprocessing/`
- **Output**: `outputs/isolation_forest/`
- **Purpose**: Anomaly detection for identifying outlier behavior
- **Key Features**: Unsupervised detection of unusual employee activities

#### XGBoost Ensemble Model (04c_xgboost.ipynb)
- **Input**: 
  - `outputs/preprocessing/` (original processed data)
  - `outputs/lstm/` (LSTM employee scores)
  - `outputs/isolation_forest/` (Isolation Forest anomaly scores)
- **Output**: `outputs/xgboost/`
- **Purpose**: Final ensemble classification using scores from previous models
- **Key Process**:
  1. Aggregates employee-level data with risk ratios
  2. Integrates LSTM and Isolation Forest scores as features
  3. Creates enriched train/validation/test datasets
  4. Produces final threat predictions

## Key Features

### Employee-Level Analysis
- Aggregation of actions to employee level using a malicious threshold (20%)
- Static employee features (seniority, department, position, etc.)
- Dynamic risk scoring based on historical behavior

### Ensemble Approach
- **LSTM**: Captures temporal patterns in user behavior
- **Isolation Forest**: Identifies statistical anomalies
- **XGBoost**: Combines insights from both models for final classification

### Comprehensive Output Management
- All intermediate results preserved in structured `outputs/` directory
- Clear separation between input data and generated outputs
- Modular pipeline allowing independent model execution

## Getting Started

1. **Data Generation**: Run the data generation pipeline to create synthetic datasets
2. **EDA**: Explore the data using the provided Jupyter notebook
3. **Preprocessing**: Execute preprocessing pipeline to prepare data for modeling
4. **Model Training**: Run models in sequence:
   - First: LSTM and Isolation Forest (can run in parallel)
   - Then: XGBoost (requires outputs from previous models)

## Model Dependencies

- **LSTM** and **Isolation Forest**: Independent models that can run in parallel
- **XGBoost**: Depends on outputs from both LSTM and Isolation Forest models

## Output Structure

Each model produces organized outputs including:
- **Model artifacts**: Trained models and parameters
- **Predictions**: Risk scores and classifications
- **Metrics**: Performance evaluation results
- **Data**: Processed datasets (especially for XGBoost enriched data)

## Technology Stack

- **Python**: Primary programming language
- **Jupyter Notebooks**: Interactive development and analysis
- **TensorFlow/Keras**: LSTM neural network implementation
- **Scikit-learn**: Isolation Forest and preprocessing utilities
- **XGBoost**: Gradient boosting ensemble model
- **Pandas/NumPy**: Data manipulation and numerical computing
