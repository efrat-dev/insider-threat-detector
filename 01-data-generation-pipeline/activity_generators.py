"""
activity_generators.py - יצירת פעילויות (הדפסה, שריפה, נסיעות, גישה)
מכיל את כל הלוגיקה ליצירת פעילויות יומיומיות של עובדים
"""

import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional
from config.config import Config


class PrintActivityGenerator:
    """מחלקה ליצירת פעילויות הדפסה"""
    
    def __init__(self, behavioral_patterns: Dict[str, Any]):
        self.patterns = behavioral_patterns
    
    def generate_print_activity(self, employee: Dict[str, Any], date: datetime.date, 
                              is_malicious: bool, is_abroad: bool) -> Dict[str, Any]:
        """יוצר פעילות הדפסה יומית לעובד"""
        
        # אם עובד בחו"ל - הסתברות נמוכה להדפסה
        if is_abroad and not is_malicious and np.random.random() < 0.98:
            return self._empty_print_activity()
        
        if is_abroad and is_malicious and np.random.random() < 0.85:
            return self._empty_print_activity()
        
        # קבלת דפוס התנהגות לפי קבוצה
        group = employee['behavioral_group']
        pattern = self.patterns[group]  # שימוש ב-dictionary access במקום מתודה
        
        # בדיקה אם העובד מדפיס היום
        if np.random.random() > pattern['print_likelihood']:
            return self._empty_print_activity()
        
        # יצירת פעילות הדפסה
        multiplier = self._get_malicious_multiplier(is_malicious)
        
        num_commands = max(1, int(np.random.poisson(
            pattern['print_volume']['commands_mean']) * multiplier))
        
        total_pages = max(1, int(np.random.poisson(
            pattern['print_volume']['pages_mean'] * num_commands) * multiplier))
        
        color_ratio = self._calculate_color_ratio(pattern['print_volume']['color_ratio'])
        
        # חישוב הדפסות מחוץ לשעות עבודה
        off_hours_commands, off_hours_pages = self._calculate_off_hours_printing(
            num_commands, total_pages, pattern, is_malicious)
        
        # הדפסה מקמפוסים מרובים
        print_campuses, printed_from_other = self._calculate_multi_campus_printing(
            employee, is_malicious)
        
        # חישוב הדפסות צבע ושחור-לבן
        num_color = int(total_pages * color_ratio)
        num_bw = total_pages - num_color
        
        return {
            'num_print_commands': num_commands,
            'total_printed_pages': total_pages,
            'num_print_commands_off_hours': off_hours_commands,
            'num_printed_pages_off_hours': off_hours_pages,
            'num_color_prints': num_color,
            'num_bw_prints': num_bw,
            'ratio_color_prints': color_ratio if total_pages > 0 else 0,
            'printed_from_other': printed_from_other,
            'print_campuses': print_campuses
        }
    
    def _get_malicious_multiplier(self, is_malicious: bool) -> float:
        """מחזיר מכפיל לעובדים זדוניים"""
        if is_malicious:
            return np.random.uniform(1.5, 3.0)
        return np.random.uniform(0.8, 1.2)
    
    def _calculate_color_ratio(self, base_ratio: float) -> float:
        """מחשב יחס הדפסות צבע עם רעש"""
        return max(0, min(1, np.random.normal(base_ratio, 0.1)))
    
    def _calculate_off_hours_printing(self, num_commands: int, total_pages: int,
                                    pattern: Dict[str, Any], is_malicious: bool) -> Tuple[int, int]:
        """מחשב הדפסות מחוץ לשעות עבודה"""
        off_hours_tendency = pattern.get('off_hours_tendency', 0.1)
        if is_malicious:
            off_hours_tendency *= 2
        
        if np.random.random() < off_hours_tendency:
            off_hours_commands = max(0, int(num_commands * np.random.uniform(0.2, 0.8)))
            off_hours_pages = max(0, int(total_pages * np.random.uniform(0.2, 0.8)))
            return off_hours_commands, off_hours_pages
        
        return 0, 0
    
    def _calculate_multi_campus_printing(self, employee: Dict[str, Any], 
                                       is_malicious: bool) -> Tuple[int, int]:
        """מחשב הדפסה מקמפוסים מרובים"""
        print_campuses = 1
        printed_from_other = 0
        
        if is_malicious and np.random.random() < 0.25:
            print_campuses = np.random.choice([2, 3])
            printed_from_other = 1
        elif np.random.random() < 0.05:
            print_campuses = 2
            printed_from_other = 1
        
        return print_campuses, printed_from_other
    
    def _empty_print_activity(self) -> Dict[str, Any]:
        """מחזיר פעילות הדפסה ריקה"""
        return {
            'num_print_commands': 0,
            'total_printed_pages': 0,
            'num_print_commands_off_hours': 0,
            'num_printed_pages_off_hours': 0,
            'num_color_prints': 0,
            'num_bw_prints': 0,
            'ratio_color_prints': 0,
            'printed_from_other': 0,
            'print_campuses': 0
        }


class BurnActivityGenerator:
    """מחלקה ליצירת פעילויות שריפה"""
    
    def __init__(self, behavioral_patterns: Dict[str, Any]):
        self.patterns = behavioral_patterns
    
    def generate_burn_activity(self, employee: Dict[str, Any], date: datetime.date,
                             is_malicious: bool, is_abroad: bool) -> Dict[str, Any]:
        """יוצר פעילות שריפה יומית לעובד"""
        
        # אם עובד בחו"ל - הסתברות נמוכה מאוד לשריפה
        if is_abroad and not is_malicious and np.random.random() < 0.99:
            return self._empty_burn_activity()
        
        if is_abroad and is_malicious and np.random.random() < 0.90:
            return self._empty_burn_activity()
        
        # קבלת דפוס התנהגות
        group = employee['behavioral_group']
        pattern = self.patterns[group]  # שימוש ב-dictionary access במקום מתודה
        
        # הסתברות שריפה - גבוהה יותר לעובדים זדוניים
        base_likelihood = pattern['burn_likelihood']
        if is_malicious:
            base_likelihood *= 3
        
        if np.random.random() > base_likelihood:
            return self._empty_burn_activity()
        
        # יצירת פעילות שריפה
        burn_params = pattern['burn_params']
        
        if is_malicious:
            num_requests = max(1, int(np.random.poisson(burn_params['requests_mean']) * 
                                    np.random.uniform(1.5, 2.5)))
            volume_mb = np.random.lognormal(burn_params['volume_mean'], 1.5)
            num_files = max(1, int(np.random.poisson(burn_params['files_mean']) * 
                                 np.random.uniform(1.8, 3.0)))
        else:
            num_requests = max(1, np.random.poisson(burn_params['requests_mean']))
            volume_mb = np.random.lognormal(burn_params['volume_mean'], 1.0)
            num_files = max(1, np.random.poisson(burn_params['files_mean']))
        
        # רמות סיווג
        classifications = self._generate_classifications(
            employee, num_requests, burn_params, is_malicious)
        
        # שריפה מחוץ לשעות עבודה
        off_hours_requests = self._calculate_off_hours_burning(
            num_requests, pattern, is_malicious)
        
        # שריפה מקמפוסים מרובים
        burn_campuses, burned_from_other = self._calculate_multi_campus_burning(
            is_malicious)
        
        return {
            'num_burn_requests': num_requests,
            'max_request_classification': max(classifications),
            'avg_request_classification': np.mean(classifications),
            'num_burn_requests_off_hours': off_hours_requests,
            'total_burn_volume_mb': int(volume_mb),
            'total_files_burned': num_files,
            'burned_from_other': burned_from_other,
            'burn_campuses': burn_campuses
        }
    
    def _generate_classifications(self, employee: Dict[str, Any], num_requests: int,
                                burn_params: Dict[str, Any], is_malicious: bool) -> list:
        """יוצר רמות סיווג לבקשות שריפה"""
        employee_classification = employee['classification']
        
        if burn_params['high_classification'] or is_malicious:
            max_classification = min(4, employee_classification + 
                                   np.random.choice([0, 1, 2], p=[0.3, 0.4, 0.3]))
        else:
            max_classification = min(employee_classification, 
                                   np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1]))
        
        return [np.random.randint(1, max_classification + 1) for _ in range(num_requests)]
    
    def _calculate_off_hours_burning(self, num_requests: int, 
                                   pattern: Dict[str, Any], is_malicious: bool) -> int:
        """מחשב שריפות מחוץ לשעות עבודה"""
        off_hours_tendency = pattern.get('off_hours_tendency', 0.1)
        
        if is_malicious and np.random.random() < off_hours_tendency:
            return max(0, int(num_requests * np.random.uniform(0.3, 0.8)))
        
        return 0
    
    def _calculate_multi_campus_burning(self, is_malicious: bool) -> Tuple[int, int]:
        """מחשב שריפה מקמפוסים מרובים"""
        burn_campuses = 1
        burned_from_other = 0
        
        if is_malicious and np.random.random() < 0.2:
            burn_campuses = np.random.choice([2, 3])
            burned_from_other = 1
        
        return burn_campuses, burned_from_other
    
    def _empty_burn_activity(self) -> Dict[str, Any]:
        """מחזיר פעילות שריפה ריקה"""
        return {
            'num_burn_requests': 0,
            'max_request_classification': 0,
            'avg_request_classification': 0,
            'num_burn_requests_off_hours': 0,
            'total_burn_volume_mb': 0,
            'total_files_burned': 0,
            'burned_from_other': 0,
            'burn_campuses': 0
        }


class TravelActivityGenerator:
    """מחלקה ליצירת פעילויות נסיעות"""
    
    def __init__(self, behavioral_patterns: Dict[str, Any]):
        self.patterns = behavioral_patterns
        self.employee_trips = {}  # מעקב אחר נסיעות פעילות
    
    def generate_travel_activity(self, employee: Dict[str, Any], date: datetime.date,
                               is_malicious: bool) -> Dict[str, Any]:
        """יוצר פעילות נסיעות יומית לעובד"""
        emp_id = employee['emp_id']
        
        # בדיקה אם עובד בנסיעה פעילה
        if emp_id in self.employee_trips:
            return self._handle_existing_trip(emp_id, date)
        
        # בדיקה אם מתחיל נסיעה חדשה
        if self._should_start_new_trip(employee, is_malicious):
            return self._start_new_trip(employee, date, is_malicious)
        
        return self._no_travel_activity()
    
    def _handle_existing_trip(self, emp_id: str, date: datetime.date) -> Dict[str, Any]:
        """מטפל בנסיעה קיימת"""
        trip = self.employee_trips[emp_id]
        days_since_start = (date - trip['start_date']).days
        
        if days_since_start < trip['duration']:
            return {
                'is_abroad': 1,
                'trip_day_number': days_since_start + 1,
                'country_name': trip['country'],
                'is_hostile_country_trip': 1 if trip['country'] in Config.HOSTILE_COUNTRIES else 0,
                'is_official_trip': trip['is_official'],
                'is_origin_country_trip': 1 if trip['country'] == trip['origin_country'] else 0
            }
        else:
            # סיום הנסיעה
            del self.employee_trips[emp_id]
            return self._no_travel_activity()
    
    def _should_start_new_trip(self, employee: Dict[str, Any], is_malicious: bool) -> bool:
        """בודק אם צריך להתחיל נסיעה חדשה"""
        group = employee['behavioral_group']
        pattern = self.patterns[group]  # שימוש ב-dictionary access במקום מתודה
        
        travel_likelihood = pattern['travel_likelihood']
        if is_malicious:
            travel_likelihood *= 1.5
        
        return np.random.random() < travel_likelihood
    
    def _start_new_trip(self, employee: Dict[str, Any], date: datetime.date,
                       is_malicious: bool) -> Dict[str, Any]:
        """מתחיל נסיעה חדשה"""
        emp_id = employee['emp_id']  # שימוש ב-emp_id במקום id
        origin_country = employee['origin_country']
        
        # בחירת יעד
        if is_malicious and np.random.random() < 0.3:
            country = np.random.choice(Config.HOSTILE_COUNTRIES)
        else:
            country = np.random.choice(Config.TRAVEL_COUNTRIES)
        
        # קביעה אם נסיעה רשמית
        is_official = np.random.choice([0, 1], p=[0.3, 0.7])
        
        # בדיקה אם נסיעה לארץ מוצא
        is_origin_trip = 1 if country == origin_country else 0
        
        if is_origin_trip and np.random.random() < 0.6:
            is_official = 0  # נסיעות לארץ מוצא פחות רשמיות
        
        # משך הנסיעה - הוספת משתני Config חסרים
        min_duration = getattr(Config, 'MIN_TRIP_DURATION', 1)
        max_duration = getattr(Config, 'MAX_TRIP_DURATION', 14)
        duration = np.random.randint(min_duration, max_duration + 1)
        
        # שמירת הנסיעה
        self.employee_trips[emp_id] = {
            'country': country,
            'start_date': date,
            'duration': duration,
            'is_official': is_official,
            'origin_country': origin_country
        }
        
        return {
            'is_abroad': 1,
            'trip_day_number': 1,
            'country_name': country,
            'is_hostile_country_trip': 1 if country in Config.HOSTILE_COUNTRIES else 0,
            'is_official_trip': is_official,
            'is_origin_country_trip': is_origin_trip
        }
    
    def _no_travel_activity(self) -> Dict[str, Any]:
        """מחזיר פעילות נסיעות ריקה"""
        return {
            'is_abroad': 0,
            'trip_day_number': None,
            'country_name': None,
            'is_hostile_country_trip': 0,
            'is_official_trip': 0,
            'is_origin_country_trip': 0
        }


class AccessActivityGenerator:
    """מחלקה ליצירת פעילויות גישה לבניין"""
    
    def __init__(self, behavioral_patterns: Dict[str, Any]):
        self.patterns = behavioral_patterns
    
    def generate_access_activity(self, employee: Dict[str, Any], date: datetime.date,
                               is_malicious: bool, is_abroad: bool) -> Dict[str, Any]:
        """יוצר פעילות גישה יומית לעובד"""
        
        # טיפול בעובד שבחו"ל
        if is_abroad:
            if is_malicious and np.random.random() < 0.05:
                pass  # גישה חשודה מחו"ל
            elif not is_malicious and np.random.random() < 0.001:
                pass  # גישה לגיטימית נדירה
            else:
                return self._empty_access_activity()
        
        # בדיקת היעדרות
        if np.random.random() < 0.05:
            return self._empty_access_activity()
        
        # קבלת שעות עבודה
        start_hour, end_hour = self._get_work_hours(employee, date, is_malicious)
        
        # בדיקת עבודה בסוף השבוע
        if not self._should_work_weekend(employee, date, is_malicious):
            return self._empty_access_activity()
        
        # יצירת פעילות גישה
        return self._generate_access_data(employee, date, start_hour, end_hour, is_malicious)
    
    def _get_work_hours(self, employee: Dict[str, Any], date: datetime.date,
                       is_malicious: bool) -> Tuple[float, float]:
        """מחשב שעות עבודה לפי דפוס התנהגות"""
        group = employee['behavioral_group']
        pattern = self.patterns[group]  # שימוש ב-dictionary access במקום מתודה
        
        # שעות עבודה בסיסיות
        start_hour = np.random.normal(
            pattern['work_hours']['start_mean'],
            pattern['work_hours']['start_std']
        )
        end_hour = np.random.normal(
            pattern['work_hours']['end_mean'],
            pattern['work_hours']['end_std']
        )
        
        # הגבלת גבולות - הוספת משתני Config חסרים
        min_work_hour = getattr(Config, 'MIN_WORK_HOUR', 6)
        max_work_hour = getattr(Config, 'MAX_WORK_HOUR', 22)
        min_work_duration = getattr(Config, 'MIN_WORK_DURATION', 4)
        
        start_hour = max(min_work_hour, min(12, start_hour))
        end_hour = max(start_hour + min_work_duration, 
                      min(max_work_hour, end_hour))
        
        # עובדים זדוניים - שעות יותר חריגות
        if is_malicious and np.random.random() < 0.3:
            if np.random.random() < 0.5:
                start_hour = np.random.uniform(5, 7)  # מוקדם מאוד
            else:
                end_hour = np.random.uniform(20, 23)  # מאוחר מאוד
        
        return start_hour, end_hour
    
    def _should_work_weekend(self, employee: Dict[str, Any], date: datetime.date,
                           is_malicious: bool) -> bool:
        """בודק אם עובד צריך לעבוד בסוף השבוע"""
        if date.weekday() < 4:  # ימי חול
            return True
        
        group = employee['behavioral_group']
        pattern = self.patterns[group]  # שימוש ב-dictionary access במקום מתודה
        
        # אבטחה עובדת תמיד
        if group == 'E':
            return np.random.random() < pattern.get('weekend_work', 0.6)
        
        # עובדים זדוניים - יותר עבודה בסופ"ש
        if is_malicious and np.random.random() < 0.3:
            return True
        
        # עובדים רגילים - עבודה נדירה בסופ"ש
        return np.random.random() < 0.05
    
    def _generate_access_data(self, employee: Dict[str, Any], date: datetime.date,
                            start_hour: float, end_hour: float, is_malicious: bool) -> Dict[str, Any]:
        """יוצר נתוני גישה מפורטים"""
        base_date = datetime.combine(date, datetime.min.time())
        first_entry = base_date + timedelta(hours=start_hour)
        last_exit = base_date + timedelta(hours=end_hour)
        
        # מספר כניסות/יציאות
        if is_malicious and np.random.random() < 0.2:
            num_entries = np.random.choice([2, 3, 4], p=[0.5, 0.3, 0.2])
        else:
            num_entries = np.random.choice([1, 2], p=[0.8, 0.2])
        
        num_exits = num_entries
        
        # זמן נוכחות
        total_minutes = int((last_exit - first_entry).total_seconds() / 60)
        
        # דגלים
        early_entry = 1 if first_entry.hour < 6 else 0
        late_exit = 1 if last_exit.hour > 22 else 0
        night_entry = 1 if first_entry.hour <= 5 or first_entry.hour >= 22 else 0
        weekend_entry = 1 if date.weekday() >= 4 else 0
        
        # גישה לקמפוסים מרובים
        num_unique_campus = 1
        if is_malicious and np.random.random() < 0.15:
            num_unique_campus = np.random.choice([2, 3])
        
        return {
            'num_entries': num_entries,
            'num_exits': num_exits,
            'first_entry_time': first_entry.strftime('%H:%M'),
            'last_exit_time': last_exit.strftime('%H:%M'),
            'total_presence_minutes': total_minutes,
            'entered_during_night_hours': night_entry,
            'num_unique_campus': num_unique_campus,
            'early_entry_flag': early_entry,
            'late_exit_flag': late_exit,
            'entry_during_weekend': weekend_entry
        }
    
    def _empty_access_activity(self) -> Dict[str, Any]:
        """מחזיר פעילות גישה ריקה"""
        return {
            'num_entries': 0,
            'num_exits': 0,
            'first_entry_time': None,
            'last_exit_time': None,
            'total_presence_minutes': 0,
            'entered_during_night_hours': 0,
            'num_unique_campus': 0,
            'early_entry_flag': 0,
            'late_exit_flag': 0,
            'entry_during_weekend': 0
        }


class RiskIndicatorGenerator:
    """מחלקה ליצירת מדדי סיכון"""
    
    @staticmethod
    def calculate_risk_travel_indicator(travel_data: Dict[str, Any], 
                                      print_data: Dict[str, Any],
                                      burn_data: Dict[str, Any]) -> int:
        """מחשב מדד סיכון נסיעות"""
        if (travel_data['is_abroad'] == 1 and 
            travel_data['is_official_trip'] == 0 and 
            travel_data['is_hostile_country_trip'] == 1 and
            (burn_data['total_files_burned'] > 0 or 
             print_data['total_printed_pages'] > 0)):
            return 1
        return 0
    
    @staticmethod
    def calculate_additional_risk_indicators(employee: Dict[str, Any],
                                           all_activities: Dict[str, Any]) -> Dict[str, Any]:
        """מחשב מדדי סיכון נוספים"""
        
        # מדד פעילות חריגה
        unusual_activity_score = 0
        
        # פעילות מחוץ לשעות
        if (all_activities['num_print_commands_off_hours'] > 0 or
            all_activities['num_burn_requests_off_hours'] > 0):
            unusual_activity_score += 1
        
        # פעילות מקמפוסים מרובים
        if (all_activities['printed_from_other'] == 1 or
            all_activities['burned_from_other'] == 1):
            unusual_activity_score += 1
        
        # גישה חריגה
        if (all_activities['entered_during_night_hours'] == 1 or
            all_activities['entry_during_weekend'] == 1):
            unusual_activity_score += 1
        
        return {
            'unusual_activity_score': unusual_activity_score,
            'high_volume_print_flag': 1 if all_activities['total_printed_pages'] > 50 else 0,
            'high_classification_burn_flag': 1 if all_activities['max_request_classification'] >= 4 else 0,
            'multi_campus_activity_flag': 1 if all_activities['num_unique_campus'] > 1 else 0
        }