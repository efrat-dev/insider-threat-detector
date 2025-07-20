#!/usr/bin/env python3
"""
מודול הוספת רעש לדאטה סינתטי - גרסה עם רעש קיצוני כברירת מחדל
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
    
    def __init__(self, burn_noise_rate: float = 0.85,   # הועלה ל-85%
                 print_noise_rate: float = 0.80,        # הועלה ל-80%
                 entry_time_noise_rate: float = 0.90,   # הועלה ל-90%
                 use_gaussian: bool = True,              # ברירת מחדל: True
                 random_seed: Optional[int] = None):
        """
        אתחול מחלקת הוספת הרעש
        
        Args:
            burn_noise_rate: אחוז השורות שיושפעו מרעש צריבה (ברירת מחדל: 85%)
            print_noise_rate: אחוז השורות שיושפעו מרעש הדפסה (ברירת מחדל: 80%)
            entry_time_noise_rate: אחוז השורות שיושפעו מרעש זמן כניסה (ברירת מחדל: 90%)
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
        """הוספת רעש לנתוני צריבה - גרסה קיצונית"""
        if random.random() < self.burn_noise_rate:
            self.statistics['burn_modifications'] += 1
            
            # סה"כ כמות בקשות - טווח קיצוני
            if self.use_gaussian:
                delta_burns = max(1, int(np.random.normal(8, 5)))
            else:
                delta_burns = random.randint(3, 20)  # הועלה ל-20
            row['num_burn_requests'] += delta_burns
            changes.append(f"num_burn_requests += {delta_burns}")
            
            # סה"כ קבצים - טווח קיצוני
            if self.use_gaussian:
                delta_files = max(1, int(np.random.normal(20, 15)))
            else:
                delta_files = random.randint(5, 60)  # הועלה ל-60
            row['total_files_burned'] += delta_files
            changes.append(f"total_files_burned += {delta_files}")
            
            # סה"כ נפח צריבה - טווח קיצוני
            if self.use_gaussian:
                delta_mb = max(100, int(np.random.normal(500, 300)))
            else:
                delta_mb = random.randint(100, 2000)  # הועלה ל-2000
            row['total_burn_volume_mb'] += delta_mb
            changes.append(f"total_burn_volume_mb += {delta_mb}")
            
            # בקשות במועד חריג - הסתברות קיצונית
            if random.random() < 0.85:  # הועלה ל-85%
                additional_off_hours = random.randint(2, 8)
                row['num_burn_requests_off_hours'] += additional_off_hours
                changes.append(f"num_burn_requests_off_hours += {additional_off_hours}")
            
            # סיווג ממוצע של הבקשות - שינוי קיצוני
            if self.use_gaussian:
                delta_avg = np.random.normal(0, 1.0)
            else:
                delta_avg = round(random.uniform(-1.5, 1.5), 2)  # הועלה ל-1.5
            row['avg_request_classification'] = max(0, min(4, row['avg_request_classification'] + delta_avg))
            changes.append(f"avg_request_classification adjusted by {delta_avg}")
            
            # סיווג מקסימלי - הסתברות קיצונית
            if random.random() < 0.40 and row['max_request_classification'] < 4:  # הועלה ל-40%
                increment = random.randint(1, 3)
                row['max_request_classification'] = min(4, row['max_request_classification'] + increment)
                changes.append(f"max_request_classification +{increment}")
            
            # מספר קמפוסים - הסתברות קיצונית
            if random.random() < 0.35:  # הועלה ל-35%
                if row['burn_campuses'] < 5:  # הועלה ל-5
                    old_campuses = row['burn_campuses']
                    row['burn_campuses'] += random.randint(1, 2)
                    changes.append(f"burn_campuses: {old_campuses} → {row['burn_campuses']}")
                
                if row['burn_campuses'] > 1:
                    row['burned_from_other'] = 1
                    changes.append("burned_from_other set to 1")
        
        return row
    
    def inject_print_noise(self, row: pd.Series, changes: List[str]) -> pd.Series:
        """הוספת רעש לנתוני הדפסות - גרסה קיצונית"""
        if row['num_print_commands'] > 0 and random.random() < self.print_noise_rate:
            self.statistics['print_modifications'] += 1
            
            # כמות פקודות הדפסה - שינוי קיצוני
            if self.use_gaussian:
                noise_factor = max(0.1, np.random.normal(0.5, 0.3))
            else:
                noise_factor = random.uniform(0.3, 0.8)  # הועלה ל-0.8
            delta_prints = max(1, int(row['num_print_commands'] * noise_factor))
            row['num_print_commands'] += delta_prints
            changes.append(f"num_print_commands += {delta_prints}")
            
            # התאמת כמות עמודים
            old_prints = max(row['num_print_commands'] - delta_prints, 1)
            pages_per_print = row['total_printed_pages'] / old_prints
            additional_pages = int(delta_prints * pages_per_print * random.uniform(0.5, 1.8))
            row['total_printed_pages'] += additional_pages
            changes.append(f"total_printed_pages += {additional_pages}")
            
            # אחוז הדפסות בצבע - שינוי קיצוני
            if self.use_gaussian:
                color_delta = np.random.normal(0, 0.20)
            else:
                color_delta = random.uniform(-0.30, 0.30)  # הועלה ל-0.30
            row['ratio_color_prints'] = min(1.0, max(0.0, row['ratio_color_prints'] + color_delta))
            changes.append(f"ratio_color_prints adjusted by {color_delta:.3f}")
            
            # פקודות הדפסה במועד חריג - הסתברות קיצונית
            if random.random() < 0.75:  # הועלה ל-75%
                additional_off_hours = random.randint(2, 6)
                row['num_print_commands_off_hours'] += additional_off_hours
                changes.append(f"num_print_commands_off_hours += {additional_off_hours}")
        
        return row
    
    def inject_entry_time_noise(self, row: pd.Series, changes: List[str]) -> pd.Series:
        """הוספת רעש לשעת הכניסה - גרסה קיצונית"""
        if pd.notna(row['first_entry_time']) and random.random() < self.entry_time_noise_rate:
            self.statistics['entry_time_modifications'] += 1
            
            try:
                # שינוי שעת הכניסה - טווח קיצוני
                t = datetime.strptime(row['first_entry_time'], "%H:%M")
                if self.use_gaussian:
                    delta_minutes = int(np.random.normal(0, 45))
                else:
                    delta_minutes = random.randint(-90, 90)  # הועלה ל-90
                
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
    
    def save_noised_data(self, df: pd.DataFrame, output_path: str) -> None:
        """שמירת הדאטה עם הרעש לקובץ (CSV או Excel)"""
        if output_path.lower().endswith('.csv'):
            df.to_csv(output_path, index=False, encoding='utf-8')
            self.logger.info(f"Noised data saved to CSV: {output_path}")
        elif output_path.lower().endswith(('.xlsx', '.xls')):
            df.to_excel(output_path, index=False)
            self.logger.info(f"Noised data saved to Excel: {output_path}")
        else:
            raise ValueError(f"Unsupported output format: {output_path}. Supported formats: .csv, .xlsx, .xls")


def add_noise_to_file(input_file: str, output_file: str, 
                     burn_noise_rate: float = 0.85,      # הועלה ל-85%
                     print_noise_rate: float = 0.80,     # הועלה ל-80%
                     entry_time_noise_rate: float = 0.90, # הועלה ל-90%
                     use_gaussian: bool = True,           # ברירת מחדל: True
                     random_seed: Optional[int] = None) -> Dict:
    """
    פונקציה נוחה להוספת רעש לקובץ (Excel או CSV)
    
    Args:
        input_file: נתיב קובץ הקלט (.xlsx או .csv)
        output_file: נתיב קובץ הפלט (.xlsx או .csv)
        burn_noise_rate: אחוז רעש צריבה (ברירת מחדל: 85%)
        print_noise_rate: אחוז רעש הדפסה (ברירת מחדל: 80%)
        entry_time_noise_rate: אחוז רעש זמן כניסה (ברירת מחדל: 90%)
        use_gaussian: האם להשתמש ברעש גאוסיאני (ברירת מחדל: True)
        random_seed: זרע אקראי
        
    Returns:
        סטטיסטיקות על הרעש שנוסף
    """
    # זיהוי סוג הקובץ וקריאה
    if input_file.lower().endswith('.csv'):
        df = pd.read_csv(input_file)
    elif input_file.lower().endswith(('.xlsx', '.xls')):
        df = pd.read_excel(input_file)
    else:
        raise ValueError(f"Unsupported file format: {input_file}. Supported formats: .csv, .xlsx, .xls")
    
    # יצירת מזריק הרעש
    noise_injector = DataNoiseInjector(
        burn_noise_rate=burn_noise_rate,
        print_noise_rate=print_noise_rate,
        entry_time_noise_rate=entry_time_noise_rate,
        use_gaussian=use_gaussian,
        random_seed=random_seed
    )
    
    # הוספת הרעש
    df_noised = noise_injector.add_noise_to_dataframe(df)
    
    # שמירת התוצאה
    noise_injector.save_noised_data(df_noised, output_file)
    
    return noise_injector.get_statistics()


# פונקציות נוחות עם רמות רעש שונות
def add_light_noise(input_file: str, output_file: str, random_seed: Optional[int] = None) -> Dict:
    """רעש קל (הגדרות מקוריות)"""
    return add_noise_to_file(input_file, output_file, 
                           burn_noise_rate=0.05, 
                           print_noise_rate=0.05, 
                           entry_time_noise_rate=0.10,
                           use_gaussian=False,
                           random_seed=random_seed)

def add_moderate_noise(input_file: str, output_file: str, random_seed: Optional[int] = None) -> Dict:
    """רעש בינוני"""
    return add_noise_to_file(input_file, output_file, 
                           burn_noise_rate=0.25, 
                           print_noise_rate=0.20, 
                           entry_time_noise_rate=0.30,
                           use_gaussian=True,
                           random_seed=random_seed)

def add_heavy_noise(input_file: str, output_file: str, random_seed: Optional[int] = None) -> Dict:
    """רעש כבד"""
    return add_noise_to_file(input_file, output_file, 
                           burn_noise_rate=0.45, 
                           print_noise_rate=0.40, 
                           entry_time_noise_rate=0.50,
                           use_gaussian=True,
                           random_seed=random_seed)

def add_extreme_noise(input_file: str, output_file: str, random_seed: Optional[int] = None) -> Dict:
    """רעש קיצוני (זה עכשיו ברירת המחדל)"""
    return add_noise_to_file(input_file, output_file, 
                           burn_noise_rate=0.85, 
                           print_noise_rate=0.80, 
                           entry_time_noise_rate=0.90,
                           use_gaussian=True,
                           random_seed=random_seed)

def add_maximum_noise(input_file: str, output_file: str, random_seed: Optional[int] = None) -> Dict:
    """רעש מקסימלי - הרמה הגבוהה ביותר"""
    return add_noise_to_file(input_file, output_file, 
                           burn_noise_rate=0.95, 
                           print_noise_rate=0.90, 
                           entry_time_noise_rate=0.95,
                           use_gaussian=True,
                           random_seed=random_seed)


def add_noise_to_excel_file(input_file: str, output_file: str, 
                           burn_noise_rate: float = 0.85,      # עודכן ל-85%
                           print_noise_rate: float = 0.80,     # עודכן ל-80%
                           entry_time_noise_rate: float = 0.90, # עודכן ל-90%
                           use_gaussian: bool = True,           # עודכן
                           random_seed: Optional[int] = None) -> Dict:
    """
    פונקציה נוחה להוספת רעש לקובץ אקסל (backwards compatibility)
    """
    return add_noise_to_file(input_file, output_file, burn_noise_rate, 
                            print_noise_rate, entry_time_noise_rate, 
                            use_gaussian, random_seed)