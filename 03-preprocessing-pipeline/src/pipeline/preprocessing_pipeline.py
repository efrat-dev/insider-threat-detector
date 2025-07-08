from pipeline.base_preprocessor import InsiderThreatPreprocessor
from pipeline.data_cleaning import DataCleaner
from pipeline.feature_engineering import FeatureEngineer
from pipeline.data_transformation import DataTransformer
from pipeline.advanced_feature_engineering import AdvancedFeatureEngineer

class PreprocessingPipeline:
    """Pipeline מלא לעיבוד מקדים"""
    
    def __init__(self):
        self.base_preprocessor = InsiderThreatPreprocessor()
        self.data_cleaner = DataCleaner()
        self.feature_engineer = FeatureEngineer()
        self.data_transformer = DataTransformer()
    
    def create_full_pipeline(self):
        """יצירת pipeline מלא לעיבוד מקדים"""
        def full_preprocessing(df):
            print("Starting full preprocessing pipeline...")
            
            # 1. טיפול בערכים חסרים
            df = self.data_cleaner.handle_missing_values(df)
            
            # 2. המרת טיפוסי נתונים
            df = self.data_cleaner.convert_data_types(df)
            
            # 3. חילוץ תכונות זמן
            df = self.feature_engineer.extract_time_features(df)
            
            # 4. יצירת תכונות אינטראקציה
            df = self.feature_engineer.create_interaction_features(df)
            
            # 5. החלת טרנספורמציה לוגריתמית
            df = self.feature_engineer.apply_log_transform(df)
            
            # 6. טיפול בחריגים
            df = self.data_cleaner.handle_outliers(df, method='cap')
            
            # 7. קידוד משתנים קטגוריים
            df = self.feature_engineer.encode_categorical_variables(df, encoding_method='label')
            
            # 8. סינון תכונות
            df = self.data_transformer.feature_filtering(df, method='correlation', threshold=0.95)
            
            # 9. נורמליזציה
            df = self.data_transformer.normalize_features(df, method='standard')
            
            # 10. בדיקות עקביות
            self.data_cleaner.consistency_checks(df)
                        
            print("Full preprocessing pipeline completed successfully!")
            return df
        
        return full_preprocessing 