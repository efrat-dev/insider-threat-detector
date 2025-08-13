import pandas as pd
import logging
from pipeline.preprocessing_pipeline import PreprocessingPipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def split_data(X, y, employee_col='employee_id', date_col='date'):
    """Sorts the dataset by employee and date, then splits it into training, validation, and test sets."""
    # Combine X and y to maintain alignment during sorting
    combined_df = pd.concat([X, y], axis=1)
    
    if employee_col in combined_df.columns and date_col in combined_df.columns:
        combined_df = combined_df.sort_values(by=[employee_col, date_col])
    elif employee_col in combined_df.columns:
        combined_df = combined_df.sort_values(by=employee_col)
    else:
        logger.warning(f"Employee column '{employee_col}' not found. Skipping sorting.")
    
    X_sorted = combined_df.drop(columns=[y.name])
    y_sorted = combined_df[y.name]
    
    n_samples = len(X_sorted)
    # The following calculates indices for 60/20/20 train/val/test split
    train_end = int(0.6 * n_samples)
    val_end = int(0.8 * n_samples)
    
    X_train = X_sorted.iloc[:train_end]
    X_val = X_sorted.iloc[train_end:val_end]
    X_test = X_sorted.iloc[val_end:]
    
    y_train = y_sorted.iloc[:train_end]
    y_val = y_sorted.iloc[train_end:val_end]
    y_test = y_sorted.iloc[val_end:]
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def main():
    """Main function to execute the production data processing pipeline."""
    try:
        logger.info("Starting data processing pipeline")
        
        df = pd.read_csv('insider_threat_dataset.csv')
        logger.info(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Convert float64 columns to float32 to reduce memory usage
        float_cols = df.select_dtypes(include=['float64']).columns
        df = df.astype({col: 'float32' for col in float_cols})
        
        # Drop irrelevant columns if they exist
        columns_to_drop = [col for col in ['is_emp_malicious', 'modification_details'] if col in df.columns]
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)
            logger.info(f"Dropped columns: {columns_to_drop}")
        
        target_col = 'is_malicious'
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        pipeline = PreprocessingPipeline()
        pipeline.fit(X, y)
        X_processed = pipeline.transform(X)
        logger.info(f"Data processed: {X_processed.shape}")
        
        X_train, X_val, X_test, y_train, y_val, y_test = split_data(X_processed, y)
        logger.info(f"Data split - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
        
        # Reset index to avoid misalignment when concatenating features and target
        train_df = pd.concat([X_train.reset_index(drop=True), y_train.reset_index(drop=True)], axis=1)
        val_df = pd.concat([X_val.reset_index(drop=True), y_val.reset_index(drop=True)], axis=1)
        test_df = pd.concat([X_test.reset_index(drop=True), y_test.reset_index(drop=True)], axis=1)
        
        train_df.to_csv('train_processed.csv', index=False)
        val_df.to_csv('val_processed.csv', index=False)
        test_df.to_csv('test_processed.csv', index=False)
        
        logger.info("Pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == '__main__':
    main()