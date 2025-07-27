import pandas as pd
from sklearn.model_selection import train_test_split
from pipeline.preprocessing_pipeline import PreprocessingPipeline

def main():
    # טען את הדאטה
    df = pd.read_csv('insider_threat_dataset.csv')
    df = df.astype({col: 'float32' for col in df.select_dtypes(include=['float64']).columns})
    
    # אם אסור למחוק את העמודה הזו - צריך לראות האם להסיר אותה מהעיבוד כמו טרגט
    df = df.drop(columns=['is_emp_malicious'])
    
    # חלק לטריין/ולידיישן/טסט לפני כל עיבוד
    target_col = 'is_malicious'
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # ראשית: חלק ל-Train (60%) ו-Temp (40%)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.4, random_state=42, stratify=y
    )
    
    # שנית: חלק את Temp ל-Validation (20%) ו-Test (20%)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    
    print(f"Dataset split sizes:")
    print(f"Train: {len(X_train)} samples ({len(X_train)/len(X)*100:.1f}%)")
    print(f"Validation: {len(X_val)} samples ({len(X_val)/len(X)*100:.1f}%)")
    print(f"Test: {len(X_test)} samples ({len(X_test)/len(X)*100:.1f}%)")
    
    # צור את הפייפליין
    pipeline = PreprocessingPipeline()
    
    # אמן את הפייפליין על הטריין בלבד
    pipeline.fit(X_train, y_train)
    
    # החל את הפייפליין על כל הסטים בנפרד
    X_train_processed = pipeline.transform(X_train)
    X_val_processed = pipeline.transform(X_val)
    X_test_processed = pipeline.transform(X_test)
    
    # הכן DataFrames עם הטרגט
    train_df = pd.concat([X_train_processed, y_train.reset_index(drop=True)], axis=1)
    val_df = pd.concat([X_val_processed, y_val.reset_index(drop=True)], axis=1)
    test_df = pd.concat([X_test_processed, y_test.reset_index(drop=True)], axis=1)
    
    # שמור את התוצאות
    train_df.to_csv('train_processed.csv', index=False)
    val_df.to_csv('val_processed.csv', index=False)
    test_df.to_csv('test_processed.csv', index=False)
    
    print(f"\nProcessed dataset shapes:")
    print(f"Train shape: {train_df.shape}")
    print(f"Validation shape: {val_df.shape}")
    print(f"Test shape: {test_df.shape}")
    
    # בדוק את התפלגות הטרגט בכל סט
    print(f"\nTarget distribution:")
    print(f"Train - Positive: {y_train.sum()}/{len(y_train)} ({y_train.mean()*100:.2f}%)")
    print(f"Val - Positive: {y_val.sum()}/{len(y_val)} ({y_val.mean()*100:.2f}%)")
    print(f"Test - Positive: {y_test.sum()}/{len(y_test)} ({y_test.mean()*100:.2f}%)")

if __name__ == '__main__':
    main()