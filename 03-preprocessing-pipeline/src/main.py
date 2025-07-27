import pandas as pd
from sklearn.model_selection import train_test_split
from pipeline.preprocessing_pipeline import PreprocessingPipeline

def main():
    # טען את הדאטה
    df = pd.read_csv('insider_threat_dataset.csv')
    df = df.astype({col: 'float32' for col in df.select_dtypes(include=['float64']).columns})

    ###אם אסור למחוק את העמודה הזו - צריך לראות האם להסיר אותה מהעיבוד כמו טרגט
    df.drop(columns=['is_emp_malicious'])

    # חלק לטריין וטסט לפני כל עיבוד
    target_col = 'is_malicious'
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # צור את הפייפליין
    pipeline = PreprocessingPipeline()
    
    # אמן את הפייפליין על הטריין בלבד
    pipeline.fit(X_train, y_train)
    
    # החל את הפייפליין על הטריין והטסט בנפרד
    X_train_processed = pipeline.transform(X_train)
    X_test_processed = pipeline.transform(X_test)
    
    # שמור את התוצאות
    train_df = pd.concat([X_train_processed, y_train.reset_index(drop=True)], axis=1)
    test_df = pd.concat([X_test_processed, y_test.reset_index(drop=True)], axis=1)
    
    train_df.to_csv('train_processed.csv', index=False)
    test_df.to_csv('test_processed.csv', index=False)
    
    print(f"Train shape: {train_df.shape}")
    print(f"Test shape: {test_df.shape}")

if __name__ == '__main__':
    main()