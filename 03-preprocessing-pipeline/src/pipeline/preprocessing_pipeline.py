from pipeline.base_preprocessor import InsiderThreatPreprocessor
from pipeline.data_cleaning import DataCleaner
from pipeline.data_transformation import DataTransformer
from pipeline.feature_engineering.feature_engineer_manager.complete_feature_engineer import CompleteFeatureEngineer

class PreprocessingPipeline:
    """Pipeline מלא לעיבוד מקדים"""
    
    def __init__(self):
        self.base_preprocessor = InsiderThreatPreprocessor()
        self.data_cleaner = DataCleaner()
        self.complete_feature_engineer = CompleteFeatureEngineer()  # שימוש במהנדס התכונות המלא
        self.data_transformer = DataTransformer()
    
    def create_full_pipeline(self):
        """יצירת pipeline מלא לעיבוד מקדים"""
        def full_preprocessing(df):
            print("Starting full preprocessing pipeline...")
            
            # 1. טיפול בערכים חסרים
            df = self.data_cleaner.handle_missing_values(df)
            
            # 2. המרת טיפוסי נתונים
            df = self.data_cleaner.convert_data_types(df)
            
            # 3. יצירת כל התכונות הבסיסיות (מחליף את השלבים 3-7 הקודמים)
            df = self.complete_feature_engineer.apply_complete_feature_engineering(df)

            # 4. טיפול בחריגים
            df = self.data_cleaner.handle_outliers(df, method='cap')
            
            # 5. סינון תכונות
            # שלב 1: הסרת correlation גבוה
            df = self.data_transformer.feature_filtering(df, method='correlation', threshold=0.95)
            
            # שלב 2: הסרת variance נמוך - סף מתון יותר
            df = self.data_transformer.feature_filtering(df, method='variance', threshold=0.0001)  # במקום 0.95!
            
            # 6. נורמליזציה
            df = self.data_transformer.normalize_features(df, method='standard')
            
            # 7. בדיקות עקביות
            self.data_cleaner.consistency_checks(df)
            
            print("Full preprocessing pipeline completed successfully!")
            print(f"Final DataFrame shape: {df.shape}")
            return df
        
        return full_preprocessing