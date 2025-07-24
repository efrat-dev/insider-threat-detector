from pipeline.data_cleaning import DataCleaner
from pipeline.data_transformation import DataTransformer
# from pipeline.feature_engineering.feature_engineer_manager.complete_feature_engineer import CompleteFeatureEngineer
from .feature_pipeline import FeatureEngineer
class PreprocessingPipeline:
    """Pipeline מלא לעיבוד מקדים"""
    
    def __init__(self):
        self.data_cleaner = DataCleaner()
        # self.complete_feature_engineer = CompleteFeatureEngineer()  # שימוש במהנדס התכונות המלא
        self.data_transformer = DataTransformer()
        self.feature_engineer = FeatureEngineer()

    def create_full_pipeline(self, target_col='is_malicious'):
        """יצירת pipeline מלא לעיבוד מקדים"""
        def full_preprocessing(df):
            print("Starting full preprocessing pipeline...")
            
            # 1. טיפול בערכים חסרים
            df = self.data_cleaner.handle_missing_values(df)
            
            # 2. המרת טיפוסי נתונים
            df = self.data_cleaner.convert_data_types(df)
            
            # 3. יצירת כל התכונות הבסיסיות (מחליף את השלבים 3-7 הקודמים)

            # # 3.1. יצירת תכונות בסיסיות
            # df = self.feature_engineer.create_all_basic_features(df)
            
            # # 3.2. יצירת תכונות מתקדמות  
            # df = self.feature_engineer.create_all_advanced_features(df)
            
            # 3.3. הסרת עמודות מקוריות
            df = self.feature_engineer.remove_original_columns(df)
            
            # 3.4. קידוד משתנים קטגוריאליים
            df = self.feature_engineer.categorical_encoder.encode_categorical_variables(df, target_col)
            
            # 3.5. טרנספורמציות סטטיסטיות
            df = self.feature_engineer.statistical_transformer.apply_statistical_transforms(df)
            
            # # 3.6. יצירת אנומליות סטטיסטיות (מוערך)
            # try:
            #     df = self.feature_engineer.factory.safe_engineer_call('anomaly', 'create_statistical_anomalies', df)
            # except Exception as e:
            #     print(f"Error in statistical anomalies: {e}")
            
            # 3.7. סטנדרטיזציה של טיפוסי נתונים
            df = self.feature_engineer.standardize_data_types(df, target_col)

            # 4. טיפול בחריגים
            df = self.data_cleaner.handle_outliers(df, method='cap')
            
            # 5. סינון תכונות
            # שלב 1: הסרת correlation גבוה
            df = self.data_transformer.feature_filtering(df, method='correlation', threshold=0.95)
            
            # שלב 2: הסרת variance נמוך - סף מתון יותר
            df = self.data_transformer.feature_filtering(df, method='variance', threshold=0.0001)  # במקום 0.95!
            
            # 6. נורמליזציה
            df = self.data_transformer.normalize_features(df, method='standard')
                        
            print("Full preprocessing pipeline completed successfully!")
            print(f"Final DataFrame shape: {df.shape}")
            return df
        

        return full_preprocessing