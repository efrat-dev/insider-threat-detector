# Insider Threat Detection Data Preprocessing Pipeline

## Overview

This project provides a comprehensive data preprocessing pipeline for insider threat detection datasets. The pipeline handles various data quality issues, creates meaningful features, and prepares data for machine learning models through a series of modular, reusable components.

## 🚀 Quick Start

```bash
python src/main.py
```

This will process your `insider_threat_dataset.csv` and generate three output files:
- `train_processed.csv` (60% of data)
- `val_processed.csv` (20% of data) 
- `test_processed.csv` (20% of data)

## 📁 Project Structure

```
src/
├── main.py                          # Main execution script
└── pipeline/
    ├── preprocessing_pipeline.py    # Main pipeline orchestrator
    ├── data_cleaning.py            # Missing values and outlier handling
    ├── categorical_encoder.py      # Advanced categorical encoding
    ├── feature_creator.py          # Domain-specific feature engineering
    ├── statistical_transformer.py  # Statistical transformations
    ├── variance_correlation_filter.py # Feature selection
    ├── feature_normalizer.py       # Data normalization
    └── data_type_converter.py      # Data type optimization
```

## 📚 Documentation

- **[Pipeline Architecture](./docs/PIPELINE_ARCHITECTURE.md)** - Detailed overview of the preprocessing pipeline structure and workflow
- **[Feature Engineering Guide](./docs/FEATURE_ENGINEERING.md)** - Comprehensive guide to feature creation and transformation strategies  
- **[Data Processing Components](./docs/DATA_PROCESSING.md)** - Deep dive into individual pipeline components and their functionality
- **[API Reference](./docs/API_REFERENCE.md)** - Complete API documentation for all classes and methods

## 🔧 Key Features

### Advanced Data Cleaning
- **Missing Value Handling**: Intelligent imputation strategies based on data types and domain knowledge
- **Outlier Detection**: IQR-based outlier detection with configurable handling methods
- **Data Type Optimization**: Automatic conversion to appropriate data types for memory efficiency

### Smart Categorical Encoding
- **Adaptive Strategy Selection**: Different encoding methods based on cardinality
- **Rare Category Grouping**: Automatic grouping of infrequent categories to reduce dimensionality
- **Target Encoding**: Mean target encoding for high-cardinality categorical variables

### Domain-Specific Feature Engineering
- **Temporal Features**: Time-based features including entry/exit patterns, weekday/weekend indicators
- **Media/Security Features**: Burn request analysis, classification patterns, off-hours activity
- **Employee Behavior Features**: Seniority patterns, location analysis, travel behavior

### Statistical Transformations
- **Z-score Normalization**: Standardization of numerical features
- **Robust Scaling**: Outlier-resistant normalization methods
- **Feature Selection**: Variance and correlation-based feature filtering

## 🎯 Pipeline Workflow

1. **Data Loading** ([`src/main.py`](src/main.py))
   - Load dataset and perform initial memory optimization
   - Handle irrelevant columns

2. **Data Cleaning** ([`src/pipeline/data_cleaning.py`](src/pipeline/data_cleaning.py))
   - Missing value imputation
   - Outlier detection and handling

3. **Data Type Conversion** ([`src/pipeline/data_type_converter.py`](src/pipeline/data_type_converter.py))
   - Optimize data types for memory efficiency
   - Convert datetime and categorical columns

4. **Feature Engineering** ([`src/pipeline/feature_creator.py`](src/pipeline/feature_creator.py))
   - Create temporal, media, and employee-specific features
   - Generate domain-relevant derived features

5. **Categorical Encoding** ([`src/pipeline/categorical_encoder.py`](src/pipeline/categorical_encoder.py))
   - Apply adaptive encoding strategies
   - Handle high-cardinality categorical variables

6. **Statistical Transformations** ([`src/pipeline/statistical_transformer.py`](src/pipeline/statistical_transformer.py))
   - Apply z-score transformations
   - Generate statistical features

7. **Feature Selection** ([`src/pipeline/variance_correlation_filter.py`](src/pipeline/variance_correlation_filter.py))
   - Remove low-variance features
   - Handle highly correlated features

8. **Normalization** ([`src/pipeline/feature_normalizer.py`](src/pipeline/feature_normalizer.py))
   - Apply final scaling transformations
   - Ensure features are on similar scales

## 🔬 Core Components

### PreprocessingPipeline ([`src/pipeline/preprocessing_pipeline.py`](src/pipeline/preprocessing_pipeline.py))
The main orchestrator that coordinates all preprocessing steps. Supports fit/transform paradigm for proper train/test separation.

### CategoricalEncoder ([`src/pipeline/categorical_encoder.py`](src/pipeline/categorical_encoder.py))
Advanced categorical encoding with automatic strategy selection:
- Binary encoding for 2-category variables
- One-hot encoding for low-cardinality (≤3 categories)
- Target + frequency encoding for medium cardinality (4-10 categories)
- Minimal encoding for high-cardinality variables

### FeatureCreator ([`src/pipeline/feature_creator.py`](src/pipeline/feature_creator.py))
Domain-specific feature engineering for insider threat detection:
- **Temporal features**: Entry/exit patterns, time-based indicators
- **Media features**: Burn request analysis, printing behavior
- **Employee features**: Seniority analysis, location patterns

## 📊 Input Data Requirements

The pipeline expects a CSV file with insider threat data containing columns such as:
- Employee information (ID, department, seniority, etc.)
- Temporal data (dates, entry/exit times)
- Behavioral data (burn requests, print commands, etc.)
- Target variable (`is_malicious`)

## 📈 Output

The pipeline generates three processed datasets:
- **Training set** (60%): For model training
- **Validation set** (20%): For hyperparameter tuning
- **Test set** (20%): For final model evaluation

Data is sorted by employee ID and date to ensure temporal consistency within the splits.

## 🛠️ Configuration

The pipeline uses sensible defaults but can be customized:

```python
from pipeline.preprocessing_pipeline import PreprocessingPipeline

# Create and configure pipeline
pipeline = PreprocessingPipeline()

# Fit on training data
pipeline.fit(X_train, y_train)

# Transform new data
X_processed = pipeline.transform(X_test)
```

## 🔍 Monitoring and Logging

The pipeline includes comprehensive logging to track:
- Data shape changes at each step
- Feature creation and selection
- Encoding strategy decisions
- Error handling and warnings

## 🚨 Error Handling

Robust error handling ensures the pipeline continues processing even when individual components encounter issues:
- Graceful handling of missing columns
- Fallback strategies for encoding failures
- Detailed error logging for debugging

## 📋 Requirements

- pandas >= 1.3.0
- numpy >= 1.21.0
- scikit-learn >= 1.0.0

## 📄 License

This project is licensed under the MIT License.
