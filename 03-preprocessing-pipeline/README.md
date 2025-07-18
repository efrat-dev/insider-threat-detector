# Insider Threat Detection Data Processing Pipeline

A comprehensive data preprocessing and feature engineering pipeline for insider threat detection in organizational security systems.

## Overview

This project provides a complete data processing pipeline specifically designed for insider threat detection datasets. It includes advanced data cleaning, feature engineering, transformation, and quality validation capabilities to prepare security data for machine learning models.

## Project Structure

```
src/
├── pipeline/
│   ├── preprocessing_pipeline.py          # Main pipeline orchestrator
│   ├── base_preprocessor.py               # Base preprocessing utilities
│   ├── data_cleaning.py                   # Data cleaning and validation
│   ├── data_transformation.py             # Data transformation utilities
│   ├── feature_engineering/
│   │   ├── basic/                         # Basic feature engineering
│   │   ├── advanced/                      # Advanced feature engineering
│   │   └── feature_engineer_manager/
│   │       └── complete_feature_engineer.py   # Complete feature engineering manager
│   └── main.py                            # Main execution script
```

## Features

### 🔧 Data Processing Pipeline
- **Automated Data Cleaning**: Handles missing values, outliers, and data type conversions
- **Data Quality Validation**: Comprehensive validation including completeness, consistency, and data type checks
- **Feature Engineering**: Both basic and advanced feature creation from raw security data
- **Data Transformation**: Normalization, standardization, and dimensionality reduction

### 📊 Data Quality Validation
- **Completeness Analysis**: Identifies and reports missing values
- **Consistency Checks**: Validates logical relationships between data fields
- **Data Type Validation**: Ensures proper data types for all columns
- **Range Validation**: Detects outliers and invalid value ranges
- **Duplicate Detection**: Identifies duplicate records and inconsistencies

### 🚀 Feature Engineering
- **Basic Features**: Time-based, printing behavior, access patterns, employee characteristics
- **Advanced Features**: Behavioral risk profiles, temporal patterns, anomaly detection
- **Interaction Features**: Complex feature interactions and polynomial transformations
- **Statistical Features**: Z-scores, ratios, and derived statistical measures

### 🔍 Data Transformation
- **Feature Filtering**: Correlation-based and variance-based feature selection
- **Normalization**: Standard, MinMax, and Robust scaling methods
- **Dimensionality Reduction**: PCA and other reduction techniques
- **Outlier Handling**: Capping and removal methods

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd insider-threat-detection
```

2. Install required dependencies:
```bash
pip install pandas numpy scikit-learn scipy
```

## Usage

### Basic Usage

```python
import pandas as pd
from pipeline.preprocessing_pipeline import PreprocessingPipeline

# Load your data
df = pd.read_csv('insider_threat_dataset.csv')

# Create and run the pipeline
pipeline = PreprocessingPipeline()
full_pipeline = pipeline.create_full_pipeline()
df_processed = full_pipeline(df)

# Save processed data
df_processed.to_csv('processed_data.csv', index=False)
```

### Advanced Usage

#### Data Quality Validation
```python
from pipeline.data_cleaning import DataQualityValidator

validator = DataQualityValidator()
quality_results = validator.run_full_validation(df)
print(f"Data Quality Score: {quality_results['quality_score']['overall_quality_score']}")
```

#### Custom Feature Engineering
```python
from pipeline.feature_engineering.feature_engineer_manager.complete_feature_engineer import CompleteFeatureEngineer

engineer = CompleteFeatureEngineer()

# Create basic features
df = engineer.create_all_basic_features(df)

# Create advanced features
df = engineer.create_all_advanced_features(df)

# Apply complete feature engineering
df = engineer.apply_complete_feature_engineering(df)
```

#### Data Transformation
```python
from pipeline.data_transformation import DataTransformer

transformer = DataTransformer()

# Feature filtering
df = transformer.feature_filtering(df, method='correlation', threshold=0.95)

# Normalization
df = transformer.normalize_features(df, method='standard')

# Dimensionality reduction
df = transformer.dimensionality_reduction(df, method='pca', n_components=0.95)
```

## Data Requirements

The pipeline expects a CSV file with the following key columns:
- `employee_id`: Unique identifier for employees
- `date`: Date of the recorded activity
- `is_malicious`: Binary target variable (0/1)
- Employee characteristics: `employee_seniority_years`, `is_contractor`, etc.
- Activity data: printing, burning, access patterns, etc.

## Pipeline Components

### 1. Data Cleaning (`DataCleaner`)
- Handles missing values using appropriate imputation strategies
- Converts data types to proper formats
- Detects and handles outliers
- Performs consistency checks

### 2. Data Quality Validation (`DataQualityValidator`)
- Comprehensive data quality assessment
- Generates quality scores and recommendations
- Identifies critical issues and warnings

### 3. Feature Engineering (`CompleteFeatureEngineer`)
- **Basic Features**: Time patterns, printing behavior, access patterns
- **Advanced Features**: Behavioral risk assessment, anomaly detection
- **Interaction Features**: Complex feature combinations
- **Statistical Features**: Derived statistical measures

### 4. Data Transformation (`DataTransformer`)
- Feature selection and filtering
- Multiple normalization methods
- Dimensionality reduction techniques

## Output

The pipeline generates:
- **Processed Dataset**: Clean, transformed data ready for ML models
- **Quality Reports**: Comprehensive data quality assessment
- **Feature Summary**: Details about created features
- **Processing Logs**: Step-by-step pipeline execution information

## Key Features

- **Modular Design**: Each component can be used independently
- **Comprehensive Validation**: Multi-level data quality checks
- **Advanced Feature Engineering**: State-of-the-art feature creation methods
- **Scalable Architecture**: Designed for large-scale security datasets
- **Error Handling**: Robust error handling and logging
- **Customizable**: Easy to modify and extend for specific use cases

## Error Handling

The pipeline includes comprehensive error handling:
- Graceful fallbacks for missing components
- Detailed error logging and reporting
- Safe execution with try-catch blocks
- Validation of input data and parameters

## Performance Considerations

- Memory-efficient processing for large datasets
- Optimized feature engineering algorithms
- Parallel processing capabilities where applicable
- Progress tracking and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or contributions, please open an issue in the repository or contact the development team.

---

**Note**: This pipeline is specifically designed for insider threat detection use cases but can be adapted for other security and behavioral analysis scenarios.
