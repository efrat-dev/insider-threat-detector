"""
Temporal Feature Engineering for Insider Threat Detection
יצירת תכונות זמן מתקדמות לזיהוי איומים פנימיים
"""

import pandas as pd
import numpy as np
from typing import Dict, List


class TemporalFeatureEngineer:
    """מהנדס תכונות זמן מתקדם"""
    
    def __init__(self):
        self.temporal_features = []
    
    def create_advanced_temporal_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת דפוסי זמן מתקדמים"""
        df = df.copy()
        
        # דפוסי זמן מתקדמים
        df['time_consistency_score'] = np.abs(
            df.get('entry_hour', 9) - df.get('entry_hour', 9).mean()
        ) + np.abs(
            df.get('exit_hour', 17) - df.get('exit_hour', 17).mean()
        )
        
        # מדד יציבות זמנים
        df['schedule_stability'] = (
            (df.get('entry_hour', 9).between(7, 10)) &
            (df.get('exit_hour', 17).between(16, 19))
        ).astype(int)
        
        # פעילות בחגים/תקופות מיוחדות
        df['holiday_activity'] = (
            df.get('is_quarter_end', 0) * df.get('suspicious_access_score', 0)
        )
        
        # דפוס עבודה לילי
        df['night_shift_pattern'] = (
            (df.get('entry_hour', 9) >= 22) | (df.get('entry_hour', 9) <= 5)
        ).astype(int)
        
        # דפוס עבודה בסוף השבוע
        df['weekend_work_intensity'] = (
            df.get('is_weekend', 0) * df.get('total_presence_minutes', 0)
        )
        
        # מדד חריגות זמנים
        df['time_anomaly'] = (
            df['time_consistency_score'] > df['time_consistency_score'].quantile(0.9)
        ).astype(int)
        
        self.temporal_features.extend([
            'time_consistency_score', 'schedule_stability',
            'holiday_activity', 'night_shift_pattern',
            'weekend_work_intensity', 'time_anomaly'
        ])
        
        return df