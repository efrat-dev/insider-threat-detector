#!/usr/bin/env python3
"""
מודול הוספת רעש לדאטה סינתטי - גרסה עם רעש נמוך כברירת מחדל
-------------------------------------------------
הוספת רעש סינתטי באופן ריאליסטי ומבוקר, לשדות נומריים, בינאריים וזמני כניסה
תוך שמירה על עקביות בין שדות תלוים
"""

import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging


class DataNoiseInjector:
    """מחלקה להוספת רעש לדאטה סינתטי"""
    
    def __init__(self, burn_noise_rate: float = 0.05,   # הוחזר ל-5%
                 print_noise_rate: float = 0.05,        # הוחזר ל-5%
                 entry_time_noise_rate: float = 0.10,   # הוחזר ל-10%
                 use_gaussian: bool = False,              # הוחזר ל-False
                 random_seed: Optional[int] = None):
        """
        אתחול מחלקת הוספת הרעש
        
        Args:
            burn_noise_rate: אחוז השורות שיושפעו מרעש צריבה (ברירת מחדל: 5%)
            print_noise_rate: אחוז השורות שיושפעו מרעש הדפסה (ברירת מחדל: 5%)
            entry_time_noise_rate: אחוז השורות שיושפעו מרעש זמן כניסה (ברירת מחדל: 10%)
            use_gaussian: האם להשתמש ברעש גאוסיאני לשדות מסוימים
            random_seed: זרע אקראי לשחזור תוצאות
        """
        self.burn_noise_rate = burn_noise_rate
        self.print_noise_rate = print_noise_rate
        self.entry_time_noise_rate = entry_time_noise_rate
        self.use_gaussian = use_gaussian
        
        if random_seed is not None:
            random.seed(random_seed)
            np.random.seed(random_seed)
        
        self.logger = logging.getLogger(__name__)
        self.statistics = {
            'total_rows': 0,
            'modified_rows': 0,
            'burn_modifications': 0,
            'print_modifications': 0,
            'entry_time_modifications': 0
        }
    
    def inject_burn_noise(self, row: pd.Series, changes: List[str]) -> pd.Series:
        """הוספת רעש לנתוני צריבה - גרסה נמוכה"""
        if random.random() < self.burn_noise_rate:
            self.statistics['burn_modifications'] += 1
            
            # סה"כ כמות בקשות - טווח נמוך
            if self.use_gaussian:
                delta_burns = max(1, int(np.random.normal(2, 1)))
            else:
                delta_burns = random.randint(1, 3)  # הוחזר לטווח נמוך
            row['num_burn_requests'] += delta_burns
            changes.append(f"num_burn_requests += {delta_burns}")
            
            # סה"כ קבצים - טווח נמוך
            if self.use_gaussian:
                delta_files = max(1, int(np.random.normal(6, 4)))
            else:
                delta_files = random.randint(2, 10)  # הוחזר לטווח נמוך
            row['total_files_burned'] += delta_files
            changes.append(f"total_files_burned += {delta_files}")
            
            # סה"כ נפח צריבה - טווח נמוך
            if self.use_gaussian:
                delta_mb = max(50, int(np.random.normal(175, 75)))
            else:
                delta_mb = random.randint(50, 300)  # הוחזר לטווח נמוך
            row['total_burn_volume_mb'] += delta_mb
            changes.append(f"total_burn_volume_mb += {delta_mb}")
            
            # בקשות במועד חריג - הסתברות נמוכה
            if random.random() < 0.3:  # הוחזר ל-30%
                additional_off_hours = 1
                row['num_burn_requests_off_hours'] += additional_off_hours
                changes.append(f"num_burn_requests_off_hours += {additional_off_hours}")
            
            # סיווג ממוצע של הבקשות - שינוי נמוך
            if self.use_gaussian:
                delta_avg = np.random.normal(0, 0.3)
            else:
                delta_avg = round(random.uniform(-0.4, 0.4), 2)  # הוחזר לטווח נמוך
            row['avg_request_classification'] = max(0, min(4, row['avg_request_classification'] + delta_avg))
            changes.append(f"avg_request_classification adjusted by {delta_avg}")
            
            # סיווג מקסימלי - הסתברות נמוכה
            if random.random() < 0.05 and row['max_request_classification'] < 4:  # הוחזר ל-5%
                increment = 1
                row['max_request_classification'] = min(4, row['max_request_classification'] + increment)
                changes.append(f"max_request_classification +{increment}")
            
            # מספר קמפוסים - הסתברות נמוכה
            if random.random() < 0.03:  # הוחזר ל-3%
                if row['burn_campuses'] < 2:  # הוחזר ל-2
                    old_campuses = row['burn_campuses']
                    row['burn_campuses'] += 1
                    changes.append(f"burn_campuses: {old_campuses} → {row['burn_campuses']}")
                
                if row['burn_campuses'] > 1:
                    row['burned_from_other'] = 1
                    changes.append("burned_from_other set to 1")
        
        return row
    
    def inject_print_noise(self, row: pd.Series, changes: List[str]) -> pd.Series:
        """הוספת רעש לנתוני הדפסות - גרסה נמוכה"""
        if row['num_print_commands'] > 0 and random.random() < self.print_noise_rate:
            self.statistics['print_modifications'] += 1
            
            # כמות פקודות הדפסה - שינוי נמוך
            if self.use_gaussian:
                noise_factor = max(0.05, np.random.normal(0.15, 0.05))
            else:
                noise_factor = random.uniform(0.05, 0.2)  # הוחזר לטווח נמוך
            delta_prints = max(1, int(row['num_print_commands'] * noise_factor))
            row['num_print_commands'] += delta_prints
            changes.append(f"num_print_commands += {delta_prints}")
            
            # התאמת כמות עמודים
            old_prints = max(row['num_print_commands'] - delta_prints, 1)
            pages_per_print = row['total_printed_pages'] / old_prints
            additional_pages = int(delta_prints * pages_per_print)
            row['total_printed_pages'] += additional_pages
            changes.append(f"total_printed_pages += {additional_pages}")
            
            # אחוז הדפסות בצבע - שינוי נמוך
            if self.use_gaussian:
                color_delta = np.random.normal(0, 0.03)
            else:
                color_delta = random.uniform(-0.05, 0.05)  # הוחזר לטווח נמוך
            row['ratio_color_prints'] = min(1.0, max(0.0, row['ratio_color_prints'] + color_delta))
            changes.append(f"ratio_color_prints adjusted by {color_delta:.3f}")
            
            # פקודות הדפסה במועד חריג - הסתברות נמוכה
            if random.random() < 0.3:  # הוחזר ל-30%
                additional_off_hours = 1
                row['num_print_commands_off_hours'] += additional_off_hours
                changes.append(f"num_print_commands_off_hours += {additional_off_hours}")
        
        return row
    
    def inject_entry_time_noise(self, row: pd.Series, changes: List[str]) -> pd.Series:
        """הוספת רעש לשעת הכניסה - גרסה נמוכה"""
        if pd.notna(row['first_entry_time']) and random.random() < self.entry_time_noise_rate:
            self.statistics['entry_time_modifications'] += 1
            
            try:
                # שינוי שעת הכניסה - טווח נמוך
                t = datetime.strptime(row['first_entry_time'], "%H:%M")
                if self.use_gaussian:
                    delta_minutes = int(np.random.normal(0, 7))
                else:
                    delta_minutes = random.randint(-10, 10)  # הוחזר לטווח נמוך
                
                new_time = (datetime.combine(datetime.today(), t.time()) + timedelta(minutes=delta_minutes)).time()
                row['first_entry_time'] = new_time.strftime("%H:%M")
                changes.append(f"first_entry_time shifted by {delta_minutes} mins")
                
                # עדכון שדות תלויים
                hour = new_time.hour
                row['entered_during_night_hours'] = 1 if hour < 6 or hour >= 22 else 0
                row['early_entry_flag'] = 1 if hour < 7 else 0
                changes.append("updated night and early entry flags")
                
            except Exception as e:
                self.logger.warning(f"Failed to parse entry time: {row['first_entry_time']}, error: {e}")
        
        return row
    
    def inject_full_noise(self, row: pd.Series) -> pd.Series:
        """הוספת רעש מלא לשורה"""
        changes = []
        
        # הוספת רעש לכל סוגי הנתונים
        row = self.inject_burn_noise(row, changes)
        row = self.inject_print_noise(row, changes)
        row = self.inject_entry_time_noise(row, changes)
        
        # תיעוד שינויים
        if changes:
            row['row_modified'] = True
            row['modification_details'] = "; ".join(changes)
            self.statistics['modified_rows'] += 1
        else:
            row['row_modified'] = False
            row['modification_details'] = ""
        
        return row
    
    def add_noise_to_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        הוספת רעש לדאטה פריים שלם
        
        Args:
            df: דאטה פריים מקורי
            
        Returns:
            דאטה פריים עם רעש
        """
        self.logger.info(f"Starting noise injection for {len(df)} rows")
        self.statistics['total_rows'] = len(df)
        
        # הוספת עמודות תיעוד אם הן לא קיימות
        if 'row_modified' not in df.columns:
            df['row_modified'] = False
        if 'modification_details' not in df.columns:
            df['modification_details'] = ""
        
        # הפעלת הפונקציה על כל שורה
        df_noised = df.apply(self.inject_full_noise, axis=1)
        
        self.logger.info(f"Noise injection completed. Modified {self.statistics['modified_rows']} out of {self.statistics['total_rows']} rows")
        return df_noised
    
    def get_statistics(self) -> Dict:
        """החזרת סטטיסטיקות על הרעש שנוסף"""
        return self.statistics.copy()