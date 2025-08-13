import numpy as np
from sklearn.feature_selection import VarianceThreshold


class VarianceCorrelationFilter:
    """מחלקה לפילטרינג פיצ'רים לפי וריאנס וקורלציה"""
    
    def __init__(self):
        self.variance_threshold = None
        self.correlation_threshold = 0.95
        self.variance_filtered_features_ = []
        self.correlation_filtered_features_ = []
        
    def _is_protected_column(self, col_name):
        """בדיקה האם העמודה מוגנת (מכילה zscore או quartile)"""
        return 'zscore' in col_name.lower() or 'quartile' in col_name.lower()
        
    def fit_variance_filtering(self, df, threshold=0.01):
        """פילטרינג פיצ'רים עם וריאנס נמוך"""
        
        # הפרדת פיצ'רים נומריים
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'target' in numeric_cols:
            numeric_cols.remove('target')
        
        if len(numeric_cols) == 0:
            self.variance_filtered_features_ = df.columns.tolist()
            return df
        
        # הפרדה בין עמודות מוגנות לרגילות
        protected_cols = [col for col in numeric_cols if self._is_protected_column(col)]
        regular_cols = [col for col in numeric_cols if not self._is_protected_column(col)]
        
        
        if len(regular_cols) == 0:
            self.variance_filtered_features_ = df.columns.tolist()
            return df
        
        # יצירת VarianceThreshold רק לעמודות הרגילות
        self.variance_threshold = VarianceThreshold(threshold=threshold)
        
        # אימון על הפיצ'רים הנומריים הרגילים
        self.variance_threshold.fit(df[regular_cols])
        
        # קבלת שמות הפיצ'רים הרגילים שנשארים
        selected_regular = [col for col, selected in 
                           zip(regular_cols, self.variance_threshold.get_support()) 
                           if selected]
        
        # שמירת רשימת הפיצ'רים שנשארים (רגילים + מוגנים + לא נומריים)
        non_numeric_cols = [col for col in df.columns if col not in numeric_cols]
        self.variance_filtered_features_ = selected_regular + protected_cols + non_numeric_cols
        
        removed_count = len(regular_cols) - len(selected_regular)
        
        return df[self.variance_filtered_features_]
    
    def transform_variance_filtering(self, df):
        """החלת פילטרינג וריאנס על דאטה חדש"""
        if self.variance_threshold is None:
            raise ValueError("Variance filtering not fitted yet")
        
        # Filter features to only include those that exist in the current dataframe
        available_features = [col for col in self.variance_filtered_features_ if col in df.columns]
        
        if len(available_features) != len(self.variance_filtered_features_):
            missing_features = set(self.variance_filtered_features_) - set(available_features)
        
        return df[available_features]
    
    def fit_correlation_filtering(self, df, threshold=0.95):
        """פילטרינג פיצ'רים עם קורלציה גבוהה"""
        
        self.correlation_threshold = threshold
        
        # הפרדת פיצ'רים נומריים
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'target' in numeric_cols:
            numeric_cols.remove('target')
        
        if len(numeric_cols) <= 1:
            self.correlation_filtered_features_ = df.columns.tolist()
            return df
        
        # הפרדה בין עמודות מוגנות לרגילות
        protected_cols = [col for col in numeric_cols if self._is_protected_column(col)]
        regular_cols = [col for col in numeric_cols if not self._is_protected_column(col)]
        
        
        if len(regular_cols) <= 1:
            self.correlation_filtered_features_ = df.columns.tolist()
            return df
        
        # חישוב מטריצת קורלציה רק לעמודות הרגילות
        corr_matrix = df[regular_cols].corr().abs()
        
        # מציאת זוגות פיצ'רים עם קורלציה גבוהה
        upper_tri = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        
        # פיצ'רים להסרה (רק מהעמודות הרגילות)
        to_drop = [column for column in upper_tri.columns 
                  if any(upper_tri[column] > threshold)]
        
        # שמירת רשימת הפיצ'רים שנשארים
        remaining_regular = [col for col in regular_cols if col not in to_drop]
        non_numeric_cols = [col for col in df.columns if col not in numeric_cols]
        self.correlation_filtered_features_ = remaining_regular + protected_cols + non_numeric_cols
                
        return df[self.correlation_filtered_features_]
    
    def transform_correlation_filtering(self, df):
        """החלת פילטרינג קורלציה על דאטה חדש"""
        if not hasattr(self, 'correlation_filtered_features_'):
            raise ValueError("Correlation filtering not fitted yet")
        
        # Filter features to only include those that exist in the current dataframe
        available_features = [col for col in self.correlation_filtered_features_ if col in df.columns]
        
        if len(available_features) != len(self.correlation_filtered_features_):
            missing_features = set(self.correlation_filtered_features_) - set(available_features)
        
        return df[available_features]