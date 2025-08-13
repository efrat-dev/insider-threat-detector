import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from pipeline.preprocessing_pipeline import PreprocessingPipeline

def split_data(X, y, employee_col='employee_id', date_col='date'):
    """חלוקה עם מיון לפי עובד ותאריך עבור """    
    # צור DataFrame מאוחד למיון
    combined_df = pd.concat([X, y], axis=1)
    
    # מיין לפי employee_id ואז לפי date
    if employee_col in combined_df.columns and date_col in combined_df.columns:
        combined_df = combined_df.sort_values(by=[employee_col, date_col])
        print(f"Data sorted by {employee_col} and {date_col}")
    elif employee_col in combined_df.columns:
        combined_df = combined_df.sort_values(by=employee_col)
        print(f"Data sorted by {employee_col} only (date column not found)")
    else:
        print(f"Warning: Employee column '{employee_col}' not found. Using original order.")
    
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
            
    df = pd.read_csv('insider_threat_dataset.csv')
    print(f"Original dataset size: {len(df)} records")
        
    # המרה לfloat32 כדי לחסוך זיכרון
    df = df.astype({col: 'float32' for col in df.select_dtypes(include=['float64']).columns})
        
    # הסר עמודות שלא רלוונטיות
    columns_to_drop = [col for col in ['is_emp_malicious', 'modification_details'] if col in df.columns]
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)
        print(f"Dropped columns: {columns_to_drop}")
    
    # הכן את הדאטה לעיבוד
    target_col = 'is_malicious'
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    print(f"\nPreparing X and y...")
    print(f"X shape: {X.shape}")
    print(f"y shape: {y.shape}")
        
    pipeline = PreprocessingPipeline()
    
    # אמן את הפייפליין על כל הדאטה (רק fit, לא transform עדיין)
    print("\n🔧 FITTING pipeline...")
    pipeline.fit(X, y)
    print("✅ Pipeline fit completed!")
        
    # החל את הפייפליין על כל הדאטה
    print("\n🔄 TRANSFORMING data...")
    X_processed = pipeline.transform(X)
    print("✅ Pipeline transform completed!")
                    
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X_processed, y)
    
    print(f"\nDataset split sizes after preprocessing and cleaning:")
    print(f"Train: {len(X_train)} samples ({len(X_train)/len(X_processed)*100:.1f}%)")
    print(f"Validation: {len(X_val)} samples ({len(X_val)/len(X_processed)*100:.1f}%)")
    print(f"Test: {len(X_test)} samples ({len(X_test)/len(X_processed)*100:.1f}%)")
    
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
    train_filename = 'train_processed.csv'
    val_filename = 'val_processed.csv'
    test_filename = 'test_processed.csv'
    
    train_df.to_csv(train_filename, index=False)
    val_df.to_csv(val_filename, index=False)
    test_df.to_csv(test_filename, index=False)
    
    print(f"\nFinal processed dataset shapes:")
    print(f"Train shape: {train_df.shape}")
    print(f"Validation shape: {val_df.shape}")
    print(f"Test shape: {test_df.shape}")
    
    # בדוק את התפלגות הטרגט בכל סט
    print(f"\nTarget distribution:")
    print(f"Train - Positive: {y_train.sum()}/{len(y_train)} ({y_train.mean()*100:.2f}%)")
    print(f"Val - Positive: {y_val.sum()}/{len(y_val)} ({y_val.mean()*100:.2f}%)")
    print(f"Test - Positive: {y_test.sum()}/{len(y_test)} ({y_test.mean()*100:.2f}%)")
    
    print(f"\nFiles saved:")
    print(f"- {train_filename}") 
    print(f"- {val_filename}")
    print(f"- {test_filename}")

if __name__ == '__main__':
    main()