"""
Behavioral Feature Engineering for Insider Threat Detection
יצירת תכונות התנהגותיות לזיהוי איומים פנימיים
"""

import pandas as pd
import numpy as np
from typing import Dict, List


class BehavioralFeatureEngineer:
    """מהנדס תכונות התנהגותיות מתקדם"""
    
    def __init__(self):
        self.behavioral_features = []
    
    def create_behavioral_risk_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """יצירת תכונות סיכון התנהגותי מתקדמות"""
        df = df.copy()
        
        # מדד פעילות חשודה משוקלל
        df['weighted_suspicious_activity'] = (
            df.get('entered_during_night_hours', 0) * 3 +
            df.get('early_entry_flag', 0) * 1.5 +
            df.get('late_exit_flag', 0) * 1.5 +
            df.get('entry_during_weekend', 0) * 2.5 +
            df.get('off_hours_print_ratio', 0) * 2 +
            df.get('off_hours_burn_ratio', 0) * 3
        )
        
        # דפוס עבודה חריג
        df['unusual_work_pattern'] = (
            (df.get('is_weekend', 0) & (df.get('total_presence_minutes', 0) > 240)) |  # עבודה ארוכה בסוף השבוע
            (df.get('work_duration_hours', 0) > 14) |  # עבודה מעל 14 שעות
            (df.get('work_duration_hours', 0) < 2)     # עבודה מתחת לשעתיים
        ).astype(int)
        
        # מדד פעילות דיגיטלית חשודה
        df['digital_footprint_risk'] = (
            df.get('is_heavy_printer', 0) * 2 +
            df.get('is_high_volume_printer', 0) * 2 +
            df.get('is_heavy_burner', 0) * 3 +
            df.get('is_high_volume_burner', 0) * 3 +
            df.get('prints_from_other_campus', 0) * 2 +
            df.get('burns_from_other_campus', 0) * 3
        )
        
        # מדד יעילות חשודה (פעילות גבוהה בזמן קצר)
        df['efficiency_anomaly'] = (
            df.get('print_efficiency', 0) * df.get('burn_efficiency', 0)
        ) / np.maximum(df.get('work_duration_hours', 1), 1)
        
        # מדד סיכון התנהגותי מתקדם
        df['behavioral_risk_advanced'] = (
            df.get('has_suspicious_access', 0) * 3 +
            df.get('unusual_work_pattern', 0) * 2 +
            df.get('digital_footprint_risk', 0) * 0.5 +
            df.get('night_shift_pattern', 0) * 2
        )
        
        self.behavioral_features.extend([
            'weighted_suspicious_activity', 'unusual_work_pattern',
            'digital_footprint_risk', 'efficiency_anomaly',
            'behavioral_risk_advanced'
        ])
        
        return df
    
    def get_behavioral_feature_summary(self, df: pd.DataFrame) -> Dict:
        """סיכום תכונות התנהגותיות"""
        behavioral_cols = [col for col in df.columns if any(x in col for x in 
                          ['weighted_suspicious', 'unusual_work', 'digital_footprint', 
                           'efficiency_anomaly', 'behavioral_risk_advanced'])]
        
        summary = {}
        for col in behavioral_cols:
            if col in df.columns:
                summary[col] = {
                    'mean': df[col].mean(),
                    'std': df[col].std(),
                    'max': df[col].max(),
                    'min': df[col].min()
                }
        
        return summary