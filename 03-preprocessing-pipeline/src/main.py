import pandas as pd
import logging
from sklearn.model_selection import train_test_split
from pipeline.preprocessing_pipeline import PreprocessingPipeline

# הגדרת לוגר פרודקשן
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def split_data(X, y, employee_col='employee_id', date_col='date'):
    """חלוקה עם מיון לפי עובד ותאריך עבור """    
    # צור DataFrame מאוחד למיון
    combined_df = pd.concat([X, y], axis=1)
    
    # מיין לפי employee_id ואז לפי date
    if employee_col in combined_df.columns and date_col in combined_df.columns:
        combined_df = combined_df.sort_values(by=[employee_col, date_col])
    elif employee_col in combined_df.columns:
        combined_df = combined_df.sort_values(by=employee_col)
    else:
        logger.warning(f"Employee column '{employee_col}' not found")
    
    # פצל בחזרה ל-X ו-y
    X_sorted = combined_df.drop(columns=[y.name])
    y_sorted = combined_df[y.name]
    
    n_samples = len(X_sorted)
    
    # חלוקה זמנית: 60% טריין, 20% ולידיישן, 20% טסט
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
    try:
        logger.info("Starting data processing pipeline")
        
        # טעינת דאטה
        df = pd.read_csv('insider_threat_dataset.csv')
        logger.info(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # המרה לfloat32 כדי לחסוך זיכרון
        df = df.astype({col: 'float32' for col in df.select_dtypes(include=['float64']).columns})
            
        # הסר עמודות שלא רלוונטיות
        columns_to_drop = [col for col in ['is_emp_malicious', 'modification_details'] if col in df.columns]
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)
        
        # הכן את הדאטה לעיבוד
        target_col = 'is_malicious'
        X = df.drop(columns=[target_col])
        y = df[target_col]
                
        pipeline = PreprocessingPipeline()
        
        # אמן את הפייפליין על כל הדאטה (רק fit, לא transform עדיין)
        pipeline.fit(X, y)
            
        # החל את הפייפליין על כל הדאטה
        X_processed = pipeline.transform(X)
        logger.info(f"Data processed: {X_processed.shape}")
                        
        X_train, X_val, X_test, y_train, y_val, y_test = split_data(X_processed, y)
        logger.info(f"Data split - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
            
        # הכן DataFrames עם הטרגט
        train_df = pd.concat([
            X_train.reset_index(drop=True), 
            y_train.reset_index(drop=True)
        ], axis=1)

        val_df = pd.concat([
            X_val.reset_index(drop=True), 
            y_val.reset_index(drop=True)
        ], axis=1)

        test_df = pd.concat([
            X_test.reset_index(drop=True), 
            y_test.reset_index(drop=True)
        ], axis=1)
        
        # שמור קבצי CSV
        train_df.to_csv('train_processed.csv', index=False)
        val_df.to_csv('val_processed.csv', index=False)
        test_df.to_csv('test_processed.csv', index=False)
        
        logger.info("Pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == '__main__':
    main()