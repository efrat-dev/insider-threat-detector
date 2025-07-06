# geographic_data.py
"""
Geographic data including campuses, origin countries, and travel destinations.
"""

class GeographicData:
    # Campus locations
    CAMPUSES = ['Campus A', 'Campus B', 'Campus C']
    
    # Origin countries and their distribution weights
    ORIGIN_COUNTRIES = [
        'Israel', 'USA', 'Russia', 'China', 'India', 
        'Germany', 'France', 'UK', 'Canada', 'Australia', 'Other'
    ]
    
    ORIGIN_COUNTRY_WEIGHTS = [0.05, 0.03, 0.02, 0.05, 0.05, 0.2, 0.15, 0.1, 0.1, 0.1, 0.15]
    
    # Travel destinations
    TRAVEL_COUNTRIES = [
        'USA', 'Germany', 'France', 'UK', 'Canada', 'Australia', 
        'Japan', 'South Korea', 'Singapore', 'India', 'China', 
        'Russia', 'Turkey', 'UAE', 'Other'
    ]
    
    # Countries considered hostile for security purposes
    HOSTILE_COUNTRIES = ['Iran', 'Russia', 'China', 'North Korea', 'Syria']