"""
Feature Analysis and Importance for Insider Threat Detection
ניתוח וחשיבות תכונות לזיהוי איומים פנימיים
"""

import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class FeatureAnalyzer:
    """מנתח תכונות מתקדם"""
    
    def __init__(self):
        self.feature_importance = {}
        self.feature_correlations = {}
    
    def get_feature_importance_analysis(self, df: pd.DataFrame, 
                                      target_col: str = 'is_malicious') -> Dict:
        """ניתוח חשיבות תכונות"""
        if target_col not in df.columns:
            print(f"Target column '{target_col}' not found")
            return {}
        
        # בחירת תכונות מספריות
        numerical_features = df.select_dtypes(include=[np.number]).columns
        numerical_features = [col for col in numerical_features if col != target_col]
        
        if len(numerical_features) == 0:
            print("No numerical features found for importance analysis")
            return {}
        
        X = df[numerical_features].fillna(0)
        y = df[target_col]
        
        try:
            # חישוב חשיבות עם mutual information
            mi_scores = mutual_info_classif(X, y, random_state=42)
            
            # חישוב חשיבות עם F-test
            f_scores, p_values = f_classif(X, y)
            
            # יצירת DataFrame עם הציונים
            importance_df = pd.DataFrame({
                'feature': numerical_features,
                'mutual_info_score': mi_scores,
                'f_score': f_scores,
                'p_value': p_values
            }).sort_values('mutual_info_score', ascending=False)
            
            # חישוב קורלציה עם המטרה
            correlations = []
            for feature in numerical_features:
                corr = df[feature].corr(df[target_col])
                correlations.append(corr)
            
            importance_df['correlation'] = correlations
            
            self.feature_importance = importance_df
            
            return {
                'importance_analysis': importance_df,
                'top_features_mi': importance_df.head(20)['feature'].tolist(),
                'top_features_f': importance_df.nlargest(20, 'f_score')['feature'].tolist(),
                'top_features_corr': importance_df.nlargest(20, 'correlation')['feature'].tolist()
            }
            
        except Exception as e:
            print(f"Error in feature importance analysis: {e}")
            return {}
    
    def analyze_feature_correlations(self, df: pd.DataFrame, 
                                   threshold: float = 0.8) -> Dict:
        """ניתוח קורלציות בין תכונות"""
        numerical_features = df.select_dtypes(include=[np.number]).columns
        
        if len(numerical_features) < 2:
            return {}
        
        # חישוב מטריצת קורלציה
        correlation_matrix = df[numerical_features].corr()
        
        # מציאת קורלציות גבוהות
        high_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i + 1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > threshold:
                    high_correlations.append({
                        'feature1': correlation_matrix.columns[i],
                        'feature2': correlation_matrix.columns[j],
                        'correlation': corr_value
                    })
        
        high_corr_df = pd.DataFrame(high_correlations)
        high_corr_df = high_corr_df.sort_values('correlation', key=abs, ascending=False)
        
        self.feature_correlations = correlation_matrix
        
        return {
            'correlation_matrix': correlation_matrix,
            'high_correlations': high_corr_df,
            'multicollinear_features': high_corr_df['feature1'].tolist() + high_corr_df['feature2'].tolist()
        }
    
    def get_feature_statistics(self, df: pd.DataFrame) -> Dict:
        """סטטיסטיקות תכונות"""
        numerical_features = df.select_dtypes(include=[np.number]).columns
        
        stats_dict = {}
        for col in numerical_features:
            stats_dict[col] = {
                'mean': df[col].mean(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'median': df[col].median(),
                'skewness': df[col].skew(),
                'kurtosis': df[col].kurtosis(),
                'null_count': df[col].isnull().sum(),
                'unique_count': df[col].nunique()
            }
        
        return stats_dict
    
    def identify_redundant_features(self, df: pd.DataFrame, 
                                  correlation_threshold: float = 0.95) -> List[str]:
        """זיהוי תכונות מיותרות"""
        numerical_features = df.select_dtypes(include=[np.number]).columns
        correlation_matrix = df[numerical_features].corr()
        
        # מציאת תכונות עם קורלציה גבוהה מאוד
        redundant_features = set()
        
        for i in range(len(correlation_matrix.columns)):
            for j in range(i + 1, len(correlation_matrix.columns)):
                if abs(correlation_matrix.iloc[i, j]) > correlation_threshold:
                    # השאר את התכונה עם השם הקצר יותר
                    col1 = correlation_matrix.columns[i]
                    col2 = correlation_matrix.columns[j]
                    
                    if len(col1) > len(col2):
                        redundant_features.add(col1)
                    else:
                        redundant_features.add(col2)
        
        return list(redundant_features)
    
    def get_feature_distribution_analysis(self, df: pd.DataFrame, 
                                        target_col: str = 'is_malicious') -> Dict:
        """ניתוח התפלגות תכונות"""
        if target_col not in df.columns:
            return {}
        
        numerical_features = df.select_dtypes(include=[np.number]).columns
        numerical_features = [col for col in numerical_features if col != target_col]
        
        distribution_analysis = {}
        
        for feature in numerical_features:
            # התפלגות עבור כל קבוצה
            malicious_dist = df[df[target_col] == 1][feature].describe()
            benign_dist = df[df[target_col] == 0][feature].describe()
            
            # בדיקת הבדלים מובהקים
            from scipy.stats import mannwhitneyu
            try:
                stat, p_value = mannwhitneyu(
                    df[df[target_col] == 1][feature].dropna(),
                    df[df[target_col] == 0][feature].dropna(),
                    alternative='two-sided'
                )
                
                distribution_analysis[feature] = {
                    'malicious_stats': malicious_dist.to_dict(),
                    'benign_stats': benign_dist.to_dict(),
                    'mann_whitney_p_value': p_value,
                    'is_significant': p_value < 0.05
                }
            except Exception as e:
                distribution_analysis[feature] = {
                    'malicious_stats': malicious_dist.to_dict(),
                    'benign_stats': benign_dist.to_dict(),
                    'error': str(e)
                }
        
        return distribution_analysis