# geographic_data.py
"""
Geographic data including campuses, origin countries, and travel destinations.
"""

class GeographicData:
    # Campus locations
    CAMPUSES = ['Campus A', 'Campus B', 'Campus C']
    
    # Origin countries and their distribution weights
    ORIGIN_COUNTRIES = [
        'Israel', 'Russia', 'Ukraine', 'USA', 'France', 'Ethiopia', 'Morocco',
        'Argentina', 'Germany', 'UK', 'India', 'China', 'South Africa',
        'Brazil', 'Canada', 'Romania', 'Hungary', 'Poland', 'Turkey', 'Georgia'
    ]

    ORIGIN_COUNTRY_WEIGHTS = [
        0.475, 0.08, 0.07, 0.05, 0.05, 0.04, 0.03,
        0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
        0.015, 0.015, 0.015, 0.01, 0.01, 0.01, 0.01
    ]
        
    # Travel destinations
    TRAVEL_COUNTRIES = [
    'USA', 'UK', 'France', 'Germany', 'Italy', 'Spain', 'Netherlands',
    'Cyprus', 'Greece', 'Turkey', 'UAE', 'Thailand', 'India',
    'China', 'Japan', 'Georgia', 'Austria', 'Switzerland',
    'Romania', 'Ukraine', 'South Korea', 'Belgium', 'Czech Republic'
    ]   

    # Countries considered hostile for security purposes
    HOSTILE_COUNTRIES = {
        1: [ 
            'Iran', 'Syria', 'Lebanon', 'Iraq', 'Yemen'
        ],
        2: [  
            'Libya', 'Afghanistan', 'Pakistan', 'Sudan', 'Qatar',
            'Russia', 'North Korea'
        ],
        3: [  
            'Algeria', 'Malaysia', 'Kuwait', 'Tunisia'
        ]
    }
