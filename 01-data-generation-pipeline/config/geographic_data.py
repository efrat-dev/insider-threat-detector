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
        'Brazil', 'Canada', 'Romania', 'Hungary', 'Poland', 'Turkey', 'Georgia',
        'Iran', 'Syria', 'Lebanon', 'Iraq', 'Yemen',             # hostile level 1
        'Libya', 'Afghanistan', 'Pakistan', 'Sudan', 'Qatar',    # hostile level 2
        'North Korea', 'Algeria', 'Malaysia', 'Kuwait', 'Tunisia' # hostile level 2–3
    ]


    ORIGIN_COUNTRY_WEIGHTS = [
        0.432, 0.08, 0.07, 0.05, 0.05, 0.04, 0.03,
        0.02, 0.02, 0.02, 0.02, 0.02, 0.02,
        0.015, 0.015, 0.015, 0.01, 0.01, 0.01, 0.01,
        #hostile countries
        0.004,  # Iran
        0.004,  # Syria
        0.004,  # Lebanon
        0.003,  # Iraq
        0.003,  # Yemen
        0.003,  # Libya
        0.003,  # Afghanistan
        0.003,  # Pakistan
        0.003,  # Sudan
        0.003,  # Qatar
        0.002,  # North Korea
        0.002,  # Algeria
        0.002,  # Malaysia
        0.002,  # Kuwait
        0.002   # Tunisia
    ]
        
    # Travel destinations
    TRAVEL_COUNTRIES = [
        'Turkey', 'Greece', 'Cyprus', 'Italy', 'USA', 'UK', 'France', 'Germany',
        'UAE', 'Thailand', 'Spain', 'Netherlands', 'India',
        'China', 'Japan', 'Georgia', 'Austria', 'Switzerland',
        'Romania', 'Ukraine', 'South Korea', 'Belgium', 'Czech Republic'
    ]

    TRAVEL_COUNTRY_WEIGHTS = [
        0.12, 0.11, 0.1, 0.08, 0.1, 0.07, 0.06, 0.06,
        0.05, 0.04, 0.04, 0.03, 0.02,
        0.02, 0.02, 0.02, 0.01, 0.01,
        0.01, 0.01, 0.01, 0.005, 0.005
    ]

    # Countries considered hostile for security purposes
    HOSTILE_COUNTRIES = {
        3: [ 
            'Iran', 'Syria', 'Lebanon', 'Iraq', 'Yemen'
        ],
        2: [  
            'Libya', 'Afghanistan', 'Pakistan', 'Sudan', 'Qatar',
            'Russia', 'North Korea'
        ],
        1: [  
            'Algeria', 'Malaysia', 'Kuwait', 'Tunisia'
        ]
    }
