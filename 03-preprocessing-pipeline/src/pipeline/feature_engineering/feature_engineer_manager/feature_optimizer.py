    # File 4: feature_optimizer.py (Optimization and analysis - 43 lines)
import numpy as np
import pandas as pd
from typing import List, Dict

class FeatureOptimizer:
    """אופטימיזציה של סט תכונות"""
    
    def __init__(self, factory):
        self.factory = factory
        
    def remove_high_correlation_features(self, df: pd.DataFrame, threshold: float = 0.95) -> pd.DataFrame:
        """הסרת תכונות עם קורלציה גבוהה"""
        try:
            numeric_df = df.select_dtypes(include=['number'])
            correlation_matrix = numeric_df.corr().abs()
            
            # מציאת זוגות עם קורלציה גבוהה
            upper_triangle = correlation_matrix.where(
                np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool)
            )
            
            # תכונות להסרה
            to_remove = [column for column in upper_triangle.columns 
                        if any(upper_triangle[column] > threshold)]
            
            if to_remove:
                df = df.drop(columns=to_remove)
                print(f"Removed {len(to_remove)} highly correlated features")
            
            return df
        except Exception as e:
            print(f"Error removing correlated features: {e}")
            return df
        