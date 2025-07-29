import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from pipeline.preprocessing_pipeline import PreprocessingPipeline

def split_data_for_isolation_forest(X, y):
    """חלוקה רנדומלית עבור Isolation Forest"""
    print("Using random split for Isolation Forest...")
    
    # ראשית: חלק ל-Train (60%) ו-Temp (40%)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.4, random_state=42, stratify=y
    )
    
    # שנית: חלק את Temp ל-Validation (20%) ו-Test (20%)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def split_data_for_lstm(X, y, date_column='date'):
    """חלוקה זמנית עבור LSTM"""
    print("Using temporal split for LSTM...")
    
    # וודא שהדאטה ממויין לפי תאריך
    if date_column in X.columns:
        # צור DataFrame מאוחד לסורטינג
        combined_df = pd.concat([X, y], axis=1)
        combined_df = combined_df.sort_values(by=date_column)
        
        # פצל בחזרה
        X_sorted = combined_df.drop(columns=[y.name])
        y_sorted = combined_df[y.name]
    else:
        print(f"Warning: Date column '{date_column}' not found. Using index order.")
        X_sorted, y_sorted = X, y
    
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
    # בדוק אם צוין פרמטר עבור סוג המודל
    if len(sys.argv) < 2:
        print("Usage: python main.py <model_type>")
        print("Available model types: isolation-forest, lstm")
        sys.exit(1)
    
    model_type = sys.argv[1].lower()
    
    if model_type not in ['isolation-forest', 'lstm']:
        print("Error: Invalid model type. Use 'isolation-forest' or 'lstm'")
        sys.exit(1)
    
    print(f"Processing data for {model_type} model...")
    
    # טען את הדאטה
    df = pd.read_csv('insider_threat_dataset.csv')
    df = df.astype({col: 'float32' for col in df.select_dtypes(include=['float64']).columns})
    
    # אם אסור למחוק את העמודה הזו - צריך לראות האם להסיר אותה מהעיבוד כמו טרגט
    df = df.drop(columns=['is_emp_malicious'])
    
    # הכן את הדאטה לחלוקה
    target_col = 'is_malicious'
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # חלק את הדאטה לפי סוג המודל
    if model_type == 'isolation-forest':
        X_train, X_val, X_test, y_train, y_val, y_test = split_data_for_isolation_forest(X, y)
    elif model_type == 'lstm':
        X_train, X_val, X_test, y_train, y_val, y_test = split_data_for_lstm(X, y)
    
    print(f"\nDataset split sizes:")
    print(f"Train: {len(X_train)} samples ({len(X_train)/len(X)*100:.1f}%)")
    print(f"Validation: {len(X_val)} samples ({len(X_val)/len(X)*100:.1f}%)")
    print(f"Test: {len(X_test)} samples ({len(X_test)/len(X)*100:.1f}%)")
    
    # צור את הפייפליין עם סוג המודל
    pipeline = PreprocessingPipeline(model_type=model_type)
    
    # אמן את הפייפליין על הטריין בלבד
    pipeline.fit(X_train, y_train)
    
    # החל את הפייפליין על כל הסטים בנפרד
    X_train_processed = pipeline.transform(X_train)
    X_val_processed = pipeline.transform(X_val)
    X_test_processed = pipeline.transform(X_test)
    
    # הכן DataFrames עם הטרגט
    train_df = pd.concat([
        X_train_processed.reset_index(drop=True), 
        y_train.reset_index(drop=True)
    ], axis=1)

    val_df = pd.concat([
        X_val_processed.reset_index(drop=True), 
        y_val.reset_index(drop=True)
    ], axis=1)

    test_df = pd.concat([
        X_test_processed.reset_index(drop=True), 
        y_test.reset_index(drop=True)
    ], axis=1)

    # שמור את התוצאות עם סיומת המודל
    train_filename = f'train_processed_{model_type.replace("-", "_")}.csv'
    val_filename = f'val_processed_{model_type.replace("-", "_")}.csv'
    test_filename = f'test_processed_{model_type.replace("-", "_")}.csv'
    
    train_df.to_csv(train_filename, index=False)
    val_df.to_csv(val_filename, index=False)
    test_df.to_csv(test_filename, index=False)
    
    print(f"\nProcessed dataset shapes:")
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