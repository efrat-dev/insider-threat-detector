import pandas as pd
from pipeline.preprocessing_pipeline import PreprocessingPipeline  # ודאי שזה הנתיב הנכון

def main():
    # טען את הדאטה
    df = pd.read_csv('insider_threat_dataset.csv')  # שנה לנתיב הקובץ שלך

    # צור את הפייפליין
    pipeline = PreprocessingPipeline()
    full_pipeline = pipeline.create_full_pipeline()

    # הרץ את הפייפליין
    df_processed = full_pipeline(df)

    # שמור את התוצאה אם צריך
    df_processed.to_csv('processed_data.csv', index=False)

if __name__ == '__main__':
    main()