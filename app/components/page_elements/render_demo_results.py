import streamlit as st
import pandas as pd
import time
import os
from typing import Dict, List, Optional, Tuple, Union
from app.ui.styles import get_chip_styles, get_section_header_styles, get_confidence_bar_styles, get_table_styles

# Use centralized styling
STYLE_CHIP = get_chip_styles()
STYLE_SECTION_HEADER = get_section_header_styles()
STYLE_CONFIDENCE_BAR = get_confidence_bar_styles()
STYLE_TABLE = get_table_styles()

# Define database paths
CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
MATERIALS_DB_PATH = []
APPLICATIONS_DB_PATH = []
#MATERIALS_DB_PATH = os.path.join(CURRENT_DIR, 'assets', 'databases', 'materials_database_steel.csv')
#APPLICATIONS_DB_PATH = os.path.join(CURRENT_DIR, 'assets', 'databases', 'applications_database_steel.csv')

# Read databases
def load_database():
    """Load materials and applications databases"""
    try:
        # Since the paths are now empty lists, return empty DataFrames
        # to avoid file not found errors
        materials_df = pd.DataFrame()
        applications_df = pd.DataFrame()
        return materials_df, applications_df
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return None, None

# Load data
materials_df, applications_df = load_database()

# Demo data structures
DEMO_PARSED_ENTITIES = {
    'material': 'Inconel 625',
    'context_filters': ['sustainable', 'high-performance', 'emerging energy', 'aerospace'],
    'application_focus': ['energy systems', 'aerospace systems']
}

# Demo data structure for parse tree
DEMO_PARSE_TREE = {
    'node': 'QUERY',
    'children': [
        {
            'node': 'MATERIAL',
            'value': 'Inconel 625',
            'confidence': 0.98
        },
        {
            'node': 'REQUIREMENTS',
            'children': [
                {
                    'node': 'PERFORMANCE',
                    'value': 'high-performance',
                    'confidence': 0.95
                },
                {
                    'node': 'SUSTAINABILITY',
                    'value': 'sustainable',
                    'confidence': 0.92
                }
            ]
        },
        {
            'node': 'DOMAINS',
            'children': [
                {
                    'node': 'INDUSTRY',
                    'value': 'aerospace',
                    'confidence': 0.96
                },
                {
                    'node': 'INDUSTRY',
                    'value': 'energy',
                    'confidence': 0.94
                }
            ]
        }
    ]
}

DEMO_APPLICATIONS = [
    # 1. Most established aerospace application
    {
        'component': 'Turbine Blade Ring Assembly',
        'use_case': 'High-temperature combustion chambers and first-stage turbine blades',
        'sector': 'Commercial Aviation',
        'rationale': 'Exceptional high-temperature strength and oxidation resistance perfectly match turbine operating conditions. Proven reliability in critical aerospace applications.',
        'source_url': 'https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-625.pdf',
        'requirements': {
            'temperature_resistance': {'min': 980, 'unit': 'C'},
            'oxidation_resistance': {'level': 'excellent'},
            'fatigue_resistance': {'cycles': 1e8},
            'creep_resistance': {'level': 'high'}
        },
        'sustainability_data': {
            'recyclability': 0.95,
            'energy_efficiency': 0.88,
            'waste_reduction': 0.92,
            'carbon_footprint': {'value': 12.5, 'unit': 'kgCO2/kg'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Special Metals', 'location': 'USA', 'lead_time': '4-6 weeks'},
                {'name': 'VDM Metals', 'location': 'Germany', 'lead_time': '6-8 weeks'}
            ],
            'processing_capabilities': ['investment casting', 'forging', 'machining'],
            'regional_availability': ['North America', 'Europe', 'Asia'],
            'typical_lead_time': '4-8 weeks'
        },
        'consumers': [
            {
                'name': 'GE Aerospace',
                'location': 'USA',
                'annual_volume': '50,000 units',
                'rating': 4.8,
                'certifications': ['AS9100D', 'ISO 9001:2015', 'NADCAP'],
                'quality_score': 98
            },
            {
                'name': 'Pratt & Whitney',
                'location': 'USA',
                'annual_volume': '45,000 units',
                'rating': 4.7,
                'certifications': ['AS9100D', 'ISO 9001:2015', 'NADCAP'],
                'quality_score': 96
            },
            {
                'name': 'Rolls-Royce',
                'location': 'UK',
                'annual_volume': '40,000 units',
                'rating': 4.9,
                'certifications': ['AS9100D', 'ISO 9001:2015', 'NADCAP', 'EN 9100'],
                'quality_score': 99
            }
        ]
    },
    # 2. Critical nuclear application
    {
        'component': 'Advanced Passive 1000 Control Rod Guide Assembly',
        'use_case': 'Precision guide tubes for control rod clusters in Pressurized Water Reactors',
        'sector': 'Nuclear Power Generation',
        'rationale': 'Outstanding radiation resistance, excellent corrosion resistance in high-temperature water, and proven long-term stability.',
        'source_url': 'https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-625.pdf',
        'requirements': {
            'radiation_resistance': {'level': 'excellent'},
            'temperature_resistance': {'min': 650, 'unit': 'C'},
            'corrosion_resistance': {'level': 'superior'},
            'design_life': {'years': 40}
        },
        'sustainability_data': {
            'recyclability': 0.90,
            'energy_efficiency': 0.95,
            'waste_reduction': 0.88,
            'carbon_footprint': {'value': 14.2, 'unit': 'kgCO2/kg'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'ATI Metals', 'location': 'USA', 'lead_time': '8-12 weeks'},
                {'name': 'Carpenter Technology', 'location': 'USA', 'lead_time': '10-14 weeks'}
            ],
            'processing_capabilities': ['forging', 'machining', 'heat treatment'],
            'regional_availability': ['North America', 'Europe'],
            'typical_lead_time': '10-14 weeks'
        },
        'consumers': [
            {
                'name': 'Westinghouse',
                'location': 'USA',
                'annual_volume': '15,000 units',
                'rating': 4.7,
                'certifications': ['ASME N-Stamp', 'ISO 9001:2015', 'NUPIC'],
                'quality_score': 97
            },
            {
                'name': 'GE Nuclear',
                'location': 'USA',
                'annual_volume': '12,000 units',
                'rating': 4.8,
                'certifications': ['ASME N-Stamp', 'ISO 9001:2015', 'NUPIC'],
                'quality_score': 98
            },
            {
                'name': 'Framatome',
                'location': 'France',
                'annual_volume': '10,000 units',
                'rating': 4.9,
                'certifications': ['ASME N-Stamp', 'ISO 9001:2015', 'NUPIC', 'RCC-M'],
                'quality_score': 99
            }
        ]
    },
    # 3. Emerging clean energy application
    {
        'component': 'Proton Exchange Membrane Electrolyzer Stack Components',
        'use_case': 'Bipolar plates and cell frames in high-pressure water splitting systems',
        'sector': 'Green Hydrogen Production',
        'rationale': 'Superior corrosion resistance in aggressive electrolyte environments. High durability ensures long-term reliability in green hydrogen production.',
        'source_url': 'https://www.sciencedirect.com/science/article/pii/S2238785420319007',
        'requirements': {
            'corrosion_resistance': {'level': 'superior'},
            'temperature_resistance': {'min': 80, 'unit': 'C'},
            'pressure_rating': {'max': 30, 'unit': 'bar'},
            'fatigue_resistance': {'cycles': 1e6}
        },
        'sustainability_data': {
            'recyclability': 0.98,
            'energy_efficiency': 0.94,
            'waste_reduction': 0.95,
            'carbon_footprint': {'value': 10.2, 'unit': 'kgCO2/kg'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'ThyssenKrupp', 'location': 'Germany', 'lead_time': '6-8 weeks'},
                {'name': 'Sandvik', 'location': 'Sweden', 'lead_time': '5-7 weeks'}
            ],
            'processing_capabilities': ['plate forming', 'welding', 'surface treatment'],
            'regional_availability': ['Europe', 'North America', 'Asia'],
            'typical_lead_time': '5-8 weeks'
        },
        'consumers': [
            {
                'name': 'Nel Hydrogen',
                'location': 'Norway',
                'annual_volume': '25,000 units',
                'rating': 4.6,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'PED 2014/68/EU'],
                'quality_score': 94
            },
            {
                'name': 'Siemens Energy',
                'location': 'Germany',
                'annual_volume': '30,000 units',
                'rating': 4.8,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'PED 2014/68/EU'],
                'quality_score': 97
            },
            {
                'name': 'Plug Power',
                'location': 'USA',
                'annual_volume': '22,000 units',
                'rating': 4.7,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'ASME BPVC'],
                'quality_score': 95
            }
        ]
    },
    # 4. Advanced aerospace application
    {
        'component': 'Rocket Engine Components',
        'use_case': 'Thrust chambers and propulsion system components',
        'sector': 'Space & Defense',
        'rationale': 'Exceptional strength at extreme temperatures and excellent resistance to combustion environments. Critical for next-generation space propulsion.',
        'source_url': 'https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-625.pdf',
        'requirements': {
            'temperature_resistance': {'min': 1200, 'unit': 'C'},
            'strength_retention': {'temp': 800, 'unit': 'C', 'retention': 0.85},
            'thermal_fatigue': {'cycles': 1e4},
            'oxidation_resistance': {'level': 'superior'}
        },
        'sustainability_data': {
            'recyclability': 0.92,
            'energy_efficiency': 0.90,
            'waste_reduction': 0.88,
            'carbon_footprint': {'value': 13.8, 'unit': 'kgCO2/kg'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Precision Castparts', 'location': 'USA', 'lead_time': '12-16 weeks'},
                {'name': 'Arconic', 'location': 'USA', 'lead_time': '10-14 weeks'}
            ],
            'processing_capabilities': ['precision casting', 'additive manufacturing', 'machining'],
            'regional_availability': ['North America'],
            'typical_lead_time': '12-16 weeks'
        },
        'consumers': [
            {
                'name': 'SpaceX',
                'location': 'USA',
                'annual_volume': '5,000 units',
                'rating': 4.9,
                'certifications': ['AS9100D', 'ITAR', 'NASA-STD-6016'],
                'quality_score': 99
            },
            {
                'name': 'Blue Origin',
                'location': 'USA',
                'annual_volume': '3,000 units',
                'rating': 4.8,
                'certifications': ['AS9100D', 'ITAR', 'NASA-STD-6016'],
                'quality_score': 97
            },
            {
                'name': 'Rocket Lab',
                'location': 'USA',
                'annual_volume': '2,000 units',
                'rating': 4.7,
                'certifications': ['AS9100D', 'ITAR', 'NASA-STD-6016'],
                'quality_score': 96
            }
        ]
    },
    # 5. Advanced nuclear application
    {
        'component': 'Small Modular Reactor Components',
        'use_case': 'Primary loop piping and heat exchangers',
        'sector': 'Nuclear Energy',
        'rationale': 'Excellent resistance to high-temperature water corrosion and radiation damage. Critical for next-generation nuclear systems.',
        'source_url': 'https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-625.pdf',
        'requirements': {
            'radiation_resistance': {'level': 'excellent'},
            'temperature_resistance': {'min': 550, 'unit': 'C'},
            'pressure_rating': {'max': 150, 'unit': 'bar'},
            'design_life': {'years': 60}
        },
        'sustainability_data': {
            'recyclability': 0.94,
            'energy_efficiency': 0.96,
            'waste_reduction': 0.90,
            'carbon_footprint': {'value': 11.5, 'unit': 'kgCO2/kg'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'BWX Technologies', 'location': 'USA', 'lead_time': '16-20 weeks'},
                {'name': 'Haynes International', 'location': 'USA', 'lead_time': '14-18 weeks'}
            ],
            'processing_capabilities': ['tube drawing', 'welding', 'heat treatment'],
            'regional_availability': ['North America', 'Europe'],
            'typical_lead_time': '16-20 weeks'
        },
        'consumers': [
            {
                'name': 'NuScale Power',
                'location': 'USA',
                'annual_volume': '8,000 units',
                'rating': 4.8,
                'certifications': ['ASME N-Stamp', 'ISO 9001:2015', 'NQA-1'],
                'quality_score': 98
            },
            {
                'name': 'TerraPower',
                'location': 'USA',
                'annual_volume': '6,000 units',
                'rating': 4.7,
                'certifications': ['ASME N-Stamp', 'ISO 9001:2015', 'NQA-1'],
                'quality_score': 97
            },
            {
                'name': 'X-energy',
                'location': 'USA',
                'annual_volume': '4,000 units',
                'rating': 4.6,
                'certifications': ['ASME N-Stamp', 'ISO 9001:2015', 'NQA-1'],
                'quality_score': 95
            }
        ]
    }
    ,
    # 6. Chemical processing application
    {
        'component': 'Chemical Processing Equipment',
        'use_case': 'Pressure vessels and heat exchangers in aggressive environments',
        'sector': 'Chemical & Process',
        'rationale': 'Superior corrosion resistance in acidic and high-chloride environments. Proven long-term reliability in critical process equipment.',
        'source_url': 'https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-625.pdf',
        'requirements': {
            'corrosion_resistance': {'level': 'exceptional'},
            'temperature_resistance': {'min': 450, 'unit': 'C'},
            'pressure_rating': {'max': 200, 'unit': 'bar'},
            'design_life': {'years': 25}
        },
        'sustainability_data': {
            'recyclability': 0.96,
            'energy_efficiency': 0.92,
            'waste_reduction': 0.94,
            'carbon_footprint': {'value': 11.8, 'unit': 'kgCO2/kg'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Allegheny Technologies', 'location': 'USA', 'lead_time': '10-12 weeks'},
                {'name': 'Outokumpu', 'location': 'Finland', 'lead_time': '12-14 weeks'}
            ],
            'processing_capabilities': ['plate forming', 'welding', 'heat treatment'],
            'regional_availability': ['North America', 'Europe', 'Asia'],
            'typical_lead_time': '10-14 weeks'
        },
        'consumers': [
            {
                'name': 'DuPont',
                'location': 'USA',
                'annual_volume': '20,000 units',
                'rating': 4.8,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'ASME BPVC', 'PED 2014/68/EU'],
                'quality_score': 97
            },
            {
                'name': 'BASF',
                'location': 'Germany',
                'annual_volume': '18,000 units',
                'rating': 4.9,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'PED 2014/68/EU', 'AD 2000-Merkblatt'],
                'quality_score': 98
            },
            {
                'name': 'Dow Chemical',
                'location': 'USA',
                'annual_volume': '15,000 units',
                'rating': 4.7,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'ASME BPVC'],
                'quality_score': 96
            }
        ]
    },
    # 7. Marine energy application
    {
        'component': 'Offshore Wind Turbine Components',
        'use_case': 'Critical fasteners and structural components in marine environments',
        'sector': 'Renewable Energy',
        'rationale': 'Exceptional resistance to marine corrosion and high fatigue strength. Essential for long-term reliability in offshore installations.',
        'source_url': 'https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-625.pdf',
        'requirements': {
            'corrosion_resistance': {'level': 'superior'},
            'fatigue_strength': {'cycles': 1e7},
            'tensile_strength': {'min': 800, 'unit': 'MPa'},
            'design_life': {'years': 30}
        },
        'sustainability_data': {
            'recyclability': 0.97,
            'energy_efficiency': 0.93,
            'waste_reduction': 0.95,
            'carbon_footprint': {'value': 10.8, 'unit': 'kgCO2/kg'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Carpenter Technology', 'location': 'USA', 'lead_time': '8-10 weeks'},
                {'name': 'ThyssenKrupp', 'location': 'Germany', 'lead_time': '10-12 weeks'}
            ],
            'processing_capabilities': ['forging', 'machining', 'coating'],
            'regional_availability': ['North America', 'Europe'],
            'typical_lead_time': '8-12 weeks'
        },
        'consumers': [
            {
                'name': 'Siemens Gamesa',
                'location': 'Germany',
                'annual_volume': '35,000 units',
                'rating': 4.8,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'DNV-GL', 'IEC 61400'],
                'quality_score': 97
            },
            {
                'name': 'Vestas Wind',
                'location': 'Denmark',
                'annual_volume': '30,000 units',
                'rating': 4.9,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'DNV-GL', 'IEC 61400'],
                'quality_score': 98
            },
            {
                'name': 'GE Renewable Energy',
                'location': 'USA',
                'annual_volume': '28,000 units',
                'rating': 4.7,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'DNV-GL', 'IEC 61400'],
                'quality_score': 96
            }
        ]
    },
    # 8. Advanced energy storage
    {
        'component': 'Molten Salt Energy Storage Systems',
        'use_case': 'Heat exchangers and storage tanks for concentrated solar power',
        'sector': 'Renewable Energy',
        'rationale': 'Excellent resistance to molten salt corrosion at high temperatures. Critical for next-generation energy storage.',
        'source_url': 'https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-625.pdf',
        'requirements': {
            'temperature_resistance': {'min': 700, 'unit': 'C'},
            'corrosion_resistance': {'level': 'excellent'},
            'thermal_cycling': {'cycles': 1e4},
            'design_life': {'years': 30}
        },
        'sustainability_data': {
            'recyclability': 0.95,
            'energy_efficiency': 0.94,
            'waste_reduction': 0.93,
            'carbon_footprint': {'value': 11.2, 'unit': 'kgCO2/kg'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Special Metals', 'location': 'USA', 'lead_time': '12-14 weeks'},
                {'name': 'VDM Metals', 'location': 'Germany', 'lead_time': '14-16 weeks'}
            ],
            'processing_capabilities': ['plate forming', 'welding', 'heat treatment'],
            'regional_availability': ['North America', 'Europe'],
            'typical_lead_time': '12-16 weeks'
        },
        'consumers': [
            {
                'name': 'Abengoa Solar',
                'location': 'Spain',
                'annual_volume': '12,000 units',
                'rating': 4.8,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'ASME BPVC', 'IEC 62734'],
                'quality_score': 97
            },
            {
                'name': 'SolarReserve',
                'location': 'USA',
                'annual_volume': '10,000 units',
                'rating': 4.7,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'ASME BPVC', 'IEC 62734'],
                'quality_score': 96
            },
            {
                'name': 'ACWA Power',
                'location': 'Saudi Arabia',
                'annual_volume': '8,000 units',
                'rating': 4.6,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'ASME BPVC'],
                'quality_score': 95
            }
        ]
    },
    # 9. Advanced aerospace application
    {
        'component': 'Hypersonic Aircraft Components',
        'use_case': 'Leading edges and thermal protection systems',
        'sector': 'Aerospace & Defense',
        'rationale': 'Exceptional high-temperature strength and oxidation resistance at hypersonic speeds. Critical for next-generation aerospace.',
        'source_url': 'https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-625.pdf',
        'requirements': {
            'temperature_resistance': {'min': 1100, 'unit': 'C'},
            'oxidation_resistance': {'level': 'superior'},
            'thermal_shock': {'cycles': 1e3},
            'strength_retention': {'temp': 1000, 'unit': 'C', 'retention': 0.80}
        },
        'sustainability_data': {
            'recyclability': 0.93,
            'energy_efficiency': 0.89,
            'waste_reduction': 0.91,
            'carbon_footprint': {'value': 13.5, 'unit': 'kgCO2/kg'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'ATI Metals', 'location': 'USA', 'lead_time': '16-20 weeks'},
                {'name': 'Carpenter Technology', 'location': 'USA', 'lead_time': '18-22 weeks'}
            ],
            'processing_capabilities': ['forging', 'additive manufacturing', 'heat treatment'],
            'regional_availability': ['North America'],
            'typical_lead_time': '16-22 weeks'
        },
        'consumers': [
            {
                'name': 'Lockheed Martin',
                'location': 'USA',
                'annual_volume': '4,000 units',
                'rating': 4.9,
                'certifications': ['AS9100D', 'ITAR', 'NADCAP', 'ISO 9001:2015'],
                'quality_score': 99
            },
            {
                'name': 'Boeing Defense',
                'location': 'USA',
                'annual_volume': '3,500 units',
                'rating': 4.8,
                'certifications': ['AS9100D', 'ITAR', 'NADCAP', 'ISO 9001:2015'],
                'quality_score': 98
            },
            {
                'name': 'Northrop Grumman',
                'location': 'USA',
                'annual_volume': '3,000 units',
                'rating': 4.8,
                'certifications': ['AS9100D', 'ITAR', 'NADCAP', 'ISO 9001:2015'],
                'quality_score': 97
            }
        ]
    },
    # 10. Advanced nuclear fusion
    {
        'component': 'Fusion Reactor Components',
        'use_case': 'Plasma-facing components and structural elements',
        'sector': 'Nuclear Fusion',
        'rationale': 'Superior radiation resistance and excellent thermal properties. Essential for next-generation fusion reactors.',
        'source_url': 'https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-625.pdf',
        'requirements': {
            'radiation_resistance': {'level': 'exceptional'},
            'temperature_resistance': {'min': 800, 'unit': 'C'},
            'thermal_conductivity': {'value': 9.8, 'unit': 'W/mK'},
            'neutron_tolerance': {'level': 'high'}
        },
        'sustainability_data': {
            'recyclability': 0.92,
            'energy_efficiency': 0.97,
            'waste_reduction': 0.96,
            'carbon_footprint': {'value': 12.0, 'unit': 'kgCO2/kg'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Special Metals', 'location': 'USA', 'lead_time': '20-24 weeks'},
                {'name': 'Haynes International', 'location': 'USA', 'lead_time': '22-26 weeks'}
            ],
            'processing_capabilities': ['precision machining', 'advanced welding', 'specialized coating'],
            'regional_availability': ['North America', 'Europe'],
            'typical_lead_time': '20-26 weeks'
        },
        'consumers': [
            {
                'name': 'ITER Organization',
                'location': 'France',
                'annual_volume': '2,000 units',
                'rating': 4.9,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'ASME N-Stamp', 'RCC-MR'],
                'quality_score': 99
            },
            {
                'name': 'Commonwealth Fusion',
                'location': 'USA',
                'annual_volume': '1,500 units',
                'rating': 4.8,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'ASME N-Stamp'],
                'quality_score': 97
            },
            {
                'name': 'General Fusion',
                'location': 'Canada',
                'annual_volume': '1,000 units',
                'rating': 4.7,
                'certifications': ['ISO 9001:2015', 'ISO 14001', 'ASME N-Stamp'],
                'quality_score': 96
            }
        ]
    }
]

def render_chip(content: str) -> str:
    """Render a chip with consistent styling."""
    return f"<div style='{STYLE_CHIP}'>{content}</div>"

def render_confidence_bar(value: str, confidence: float) -> str:
    """Render a confidence bar with consistent styling."""
    bar_color = '#00cc96' if confidence >= 0.9 else '#ffd43b' if confidence >= 0.7 else '#ff6b6b'
    bar_width = f"{confidence * 100}%"
    
    return f"""
        <div style='{STYLE_CONFIDENCE_BAR}'>
            <div style='margin-bottom:6px'>{value}</div>
            <div style='background-color:rgba(28, 28, 36, 0.8); height:4px; border-radius:2px; overflow:hidden;'>
                <div style='background-color:{bar_color}; width:{bar_width}; height:100%;'></div>
            </div>
            <div style='color:#666666; font-size:0.8em; margin-top:4px; text-align:right'>{confidence*100:.0f}%</div>
        </div>
    """

def render_section_header(title: str) -> None:
    """Render a section header with consistent styling."""
    st.markdown(f"<p style='{STYLE_SECTION_HEADER}'>{title}</p>", unsafe_allow_html=True)

def render_query_analysis() -> None:
    """Render the query analysis section including parsed entities and parse tree."""
    with st.expander("🗐  View Query Analysis"):
        render_section_header("Query Elements")
        
        # Create two columns for primary focus areas
        focus_col1, focus_col2 = st.columns(2)
        
        # Material focus
        with focus_col1:
            st.markdown("<p style='margin-bottom:0.5em'><strong>Material Focus</strong></p>", unsafe_allow_html=True)
            material_html = render_chip(DEMO_PARSED_ENTITIES['material'])
            st.markdown(f"<div style='line-height:2.2'>{material_html}</div>", unsafe_allow_html=True)
        
        # Application focus
        with focus_col2:
            st.markdown("<p style='margin-bottom:0.5em'><strong>Application Focus</strong></p>", unsafe_allow_html=True)
            domain_html = ''.join(render_chip(domain) for domain in DEMO_PARSED_ENTITIES['application_focus'])
            st.markdown(f"<div style='line-height:2.2'>{domain_html}</div>", unsafe_allow_html=True)
        
        # Create two columns for additional context
        col1, col2 = st.columns(2)
        
        # Context filters as chips in a container
        with col1:
            st.markdown("<p style='margin-bottom:0.5em'><strong>Context Filters</strong></p>", unsafe_allow_html=True)
            filter_html = ''.join(render_chip(filter) for filter in DEMO_PARSED_ENTITIES['context_filters'])
            st.markdown(f"<div style='line-height:2.2'>{filter_html}</div>", unsafe_allow_html=True)
        
        # Key requirements with consistent chip style
        with col2:
            st.markdown("<p style='margin-bottom:0.5em'><strong>Key Requirements</strong></p>", unsafe_allow_html=True)
            requirements = ["High Performance", "Sustainability", "Emerging Tech"]
            req_html = ''.join(render_chip(req) for req in requirements)
            st.markdown(f"<div style='line-height:2.2'>{req_html}</div>", unsafe_allow_html=True)
        
        # Add a divider before the parse tree
        st.markdown("---")
        
        # Render parse tree with confidence scores
        st.markdown("<p style='color:#666666; text-transform:uppercase; letter-spacing:1px; font-size:0.85em; margin:1.5em 0 1em 0'>Semantic Structure</p>", unsafe_allow_html=True)
        
        # Create a grid for semantic elements
        semantic_cols = st.columns(3)
        
        # Group parse tree elements by type
        semantic_groups = {
            'Material': [],
            'Requirements': [],
            'Domains': []
        }
        
        # Organize elements into groups
        for child in DEMO_PARSE_TREE['children']:
            if child['node'] == 'MATERIAL':
                semantic_groups['Material'].append((child['value'], child.get('confidence', 1.0)))
            elif child['node'] == 'REQUIREMENTS' and 'children' in child:
                for subchild in child['children']:
                    semantic_groups['Requirements'].append((subchild['value'], subchild.get('confidence', 1.0)))
            elif child['node'] == 'DOMAINS' and 'children' in child:
                for subchild in child['children']:
                    semantic_groups['Domains'].append((subchild['value'], subchild.get('confidence', 1.0)))
        
        # Display groups in columns
        for col, (group_name, items) in zip(semantic_cols, semantic_groups.items()):
            with col:
                st.markdown(f"<strong>{group_name}</strong>", unsafe_allow_html=True)
                for value, confidence in items:
                    # Calculate colors based on confidence
                    bar_color = '#00cc96' if confidence >= 0.9 else '#ffd43b' if confidence >= 0.7 else '#ff6b6b'
                    bar_width = f"{confidence * 100}%"
                    
                    st.markdown(
                        f"<div style='background-color:rgba(38, 39, 48, 0.8); padding:8px 12px; margin:4px 0; border-radius:4px; font-size:0.9em;'>"
                        f"<div style='margin-bottom:6px'>{value}</div>"
                        f"<div style='background-color:rgba(28, 28, 36, 0.8); height:4px; border-radius:2px; overflow:hidden;'>"
                        f"<div style='background-color:{bar_color}; width:{bar_width}; height:100%;'></div>"
                        f"</div>"
                        f"<div style='color:#666666; font-size:0.8em; margin-top:4px; text-align:right'>{confidence*100:.0f}%</div>"
                        f"</div>", 
                        unsafe_allow_html=True
                    )


def render_application_details(app: Dict[str, any]) -> None:
    """Render details for a single application"""
    # Create two columns
    left_col, right_col = st.columns([3, 2])

    # Left Column: Component, Use Case, Sector, and Performance Analysis
    with left_col:
        # Component Section
        st.markdown(f"##### {app['component']}")
        st.markdown(f"""<div style='margin-bottom:1em;'>
            <span style='color:#666666;'>Use Case:</span> {app['use_case']}<br>
            <span style='color:#666666;'>Sector:</span> {app['sector']}
        </div>""", unsafe_allow_html=True)

        # Material Capabilities Section
        st.markdown("""
            <div style='margin: 1em 0;'>
                <p style='color:#666666; margin-bottom:0.5em;'><strong>Rationale for Match</strong></p>
                <div style='display:flex; flex-wrap:wrap; gap:8px;'>
                    <span style='display:inline-block; padding:6px 12px; background-color:rgba(0, 204, 150, 0.1); 
                          color:#00cc96; border-radius:16px; font-size:0.9em;'>
                        High Temperature Resilient
                    </span>
                    <span style='display:inline-block; padding:6px 12px; background-color:rgba(0, 204, 150, 0.1); 
                          color:#00cc96; border-radius:16px; font-size:0.9em;'>
                        Fatigue Resistant
                    </span>
                    <span style='display:inline-block; padding:6px 12px; background-color:rgba(0, 204, 150, 0.1); 
                          color:#00cc96; border-radius:16px; font-size:0.9em;'>
                        Corrosion Resistant
                    </span>
                    <span style='display:inline-block; padding:6px 12px; background-color:rgba(0, 204, 150, 0.1); 
                          color:#00cc96; border-radius:16px; font-size:0.9em;'>
                        High Strength
                    </span>
                    <span style='display:inline-block; padding:6px 12px; background-color:rgba(0, 204, 150, 0.1); 
                          color:#00cc96; border-radius:16px; font-size:0.9em;'>
                        Oxidation Resistant
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Get validation metrics based on application
        validation_metrics = {
            'Gas Turbine Hot Section Components': {
                'data_points': '1000+',  # Based on extensive ASTM/ASME testing data
                'standards': '8',  # ASTM B443, B444, B446, ASME SB-443/444/446, AMS 5666, AWS ERNiCrMo-3
                'use_cases': '25+',  # Major aerospace OEMs and power generation applications
                'property_match': 96,  # High match for temperature, corrosion, and fatigue resistance
                'sustainability': 85,  # Good recyclability but energy-intensive production
                'supply_chain': 94,  # Well-established supply chain with major manufacturers
                'confidence': 95  # Extensive historical data and proven track record
            },
            'Hydrogen Production Systems': {
                'data_points': '300+',  # Newer application, focused testing for H2 environments
                'standards': '4',  # ASTM B444, ASME B31.12, NACE MR0175, ISO 15156-3
                'use_cases': '10',  # Emerging applications in electrolysis and H2 processing
                'property_match': 92,  # Excellent for corrosion and H2 embrittlement resistance
                'sustainability': 94,  # Critical role in green hydrogen production
                'supply_chain': 88,  # Growing but still developing supply chain
                'confidence': 90  # Strong data but less historical evidence than aerospace
            }
        }.get(app['component'], {
            'data_points': '500+',
            'standards': '3',
            'use_cases': '10',
            'property_match': 90,
            'sustainability': 88,
            'supply_chain': 88,
            'confidence': 90
        })

        # Validation Indicator
        st.markdown(
            f"""<div style='margin: 1em 0; display: flex; align-items: center; gap: 16px;'>
                <div style='display: flex; align-items: center; gap: 8px;'>
                    <span style='color: #4dabf7; font-weight: 500; font-size: 1.1em;'>✓</span>
                    <span style='color: #666666; font-size: 1em;'>Xtrium Validated</span>
                </div>
                <div style='display: flex; align-items: center; gap: 16px; color: #888888; font-size: 0.95em;'>
                    <span><span style='color: #4dabf7'>📊</span> {validation_metrics['data_points']} data points</span>
                    <span><span style='color: #4dabf7'>🏢</span> {validation_metrics['standards']} standards</span>
                    <span><span style='color: #4dabf7'>⚙️</span> {validation_metrics['use_cases']} use cases</span>
                </div>
            </div>""",
            unsafe_allow_html=True
        )

    # Right Column: Scores
    with right_col:
        st.markdown('<div style="background-color:rgba(38, 39, 48, 0.03); padding:1.5em; border-radius:8px;">', unsafe_allow_html=True)
        
        # Property Match Score
        st.markdown(f'<div style="margin-bottom:1.5em"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em"><span style="color:#888888;font-size:1em;font-weight:500">Property Match Score</span><span style="color:#00cc96;font-weight:500">{validation_metrics["property_match"]}%</span></div><div style="background-color:rgba(38, 39, 48, 0.1);height:6px;border-radius:3px"><div style="width:{validation_metrics["property_match"]}%;height:100%;background-color:#00cc96"></div></div></div>', unsafe_allow_html=True)
        
        # Sustainability Score
        st.markdown(f'<div style="margin-bottom:1.5em"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em"><span style="color:#888888;font-size:1em;font-weight:500">Sustainability Score</span><span style="color:#00cc96;font-weight:500">{validation_metrics["sustainability"]}%</span></div><div style="background-color:rgba(38, 39, 48, 0.1);height:6px;border-radius:3px"><div style="width:{validation_metrics["sustainability"]}%;height:100%;background-color:#00cc96"></div></div></div>', unsafe_allow_html=True)
        
        # Supply Chain Score
        st.markdown(f'<div style="margin-bottom:1.5em"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em"><span style="color:#888888;font-size:1em;font-weight:500">Supply Chain Score</span><span style="color:#00cc96;font-weight:500">{validation_metrics["supply_chain"]}%</span></div><div style="background-color:rgba(38, 39, 48, 0.1);height:6px;border-radius:3px"><div style="width:{validation_metrics["supply_chain"]}%;height:100%;background-color:#00cc96"></div></div></div>', unsafe_allow_html=True)
        
        # Xtrium Confidence Score
        st.markdown(f'<div style="margin-top:0.75em;padding-top:0.75em;border-top:1px solid rgba(38, 39, 48, 0.1)"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em"><span style="color:#888888;font-size:1.1em;font-weight:600">Xtrium Confidence Score</span><span style="color:#4dabf7;font-weight:600">{validation_metrics["confidence"]}%</span></div><div style="background-color:rgba(77, 171, 247, 0.2);height:8px;border-radius:4px"><div style="width:{validation_metrics["confidence"]}%;height:100%;background-color:#4dabf7"></div></div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Organizations Section
    st.markdown("##### Key Organizations")
    org_cols = st.columns(3)
    
    for idx, org in enumerate(app['consumers']):
        with org_cols[idx % 3]:
            st.markdown(f"""
                <div style='background-color:rgba(38, 39, 48, 0.1); padding:12px; border-radius:4px; margin-bottom:8px;'>
                    <a href='#' onclick='return false;' style='text-decoration:none; cursor:pointer;'>
                        <div style='font-weight:500; margin-bottom:4px; color:#4dabf7; transition:color 0.2s ease;' 
                             onmouseover='this.style.color="#74c0fc"' 
                             onmouseout='this.style.color="#4dabf7"'>
                            {org['name']}
                        </div>
                    </a>
                    <div style='display:flex; align-items:center; margin:4px 0;'>
                        <div style='color:#ffd43b; font-size:0.9em;'>{'★' * int(org['rating'])}{'☆' * (5 - int(org['rating']))}</div>
                        <div style='color:#666666; font-size:0.8em; margin-left:6px;'>{org['rating']}/5.0</div>
                    </div>
                    <div style='color:#666666; font-size:0.9em;'>{org['location']}</div>
                    <div style='color:#666666; font-size:0.8em; margin-top:4px;'>Annual Volume: {org['annual_volume']}</div>
                    <div style='display:flex; flex-wrap:wrap; gap:4px; margin-top:8px;'>
                        {' '.join(f"<span style='background-color:rgba(77, 171, 247, 0.1); color:#4dabf7; font-size:0.7em; padding:2px 6px; border-radius:3px;'>{cert}</span>" for cert in org['certifications'])}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Handle click events
            if st.button(f"Contact {org['name']}", key=f"btn_{app['component']}_{org['name']}", type="secondary"):
                st.session_state[f"selected_org_{app['component']}"] = org['name']
                with st.expander("Organization Details", expanded=True):
                    st.markdown(f"### {org['name']}")
    
    # Additional Organizations Section
    st.markdown("""<div style='margin-top:1.5em;'>
        <p style='color:#666666; font-size:0.9em; margin-bottom:0.5em;'>More Organizations in This Sector</p>
    </div>""", unsafe_allow_html=True)
    
    # Dictionary mapping sectors to their relevant organizations
    sector_organizations = {
        'Commercial Aviation': [
            'MTU Aero Engines', 'Safran Aircraft Engines', 'IHI Corporation',
            'Kawasaki Heavy Industries', 'COMAC', 'Embraer', 'Bombardier Aerospace',
            'Spirit AeroSystems', 'Leonardo', 'Honeywell Aerospace'
        ],
        'Nuclear Power Generation': [
            'EDF Energy', 'Rosatom', 'KEPCO', 'CNNC', 'Bruce Power',
            'Exelon Generation', 'NPCIL', 'KHNP', 'CEZ Group', 'OPG'
        ],
        'Green Hydrogen Production': [
            'Air Liquide', 'Linde', 'Air Products', 'Engie', 'Shell Hydrogen',
            'Iberdrola', 'ThyssenKrupp Uhde', 'McPhy Energy', 'ITM Power', 'Hydrogenics'
        ],
        'Space & Defense': [
            'Aerojet Rocketdyne', 'United Launch Alliance', 'Arianespace', 'ISRO',
            'JAXA', 'Firefly Aerospace', 'Virgin Orbit', 'Relativity Space', 'CASC', 'AVIO'
        ],
        'Nuclear Energy': [
            'AREVA', 'Hitachi-GE Nuclear', 'Mitsubishi Nuclear', 'SNPTC',
            'KAERI', 'BARC', 'CNEA', 'INVAP', 'ENEC', 'NECSA'
        ],
        'Chemical & Process': [
            'Evonik', 'LyondellBasell', 'Solvay', 'Air Products', 'Eastman Chemical',
            'Covestro', 'Huntsman', 'Celanese', 'Arkema', 'Lanxess'
        ],
        'Renewable Energy': [
            'Ørsted', 'EDP Renewables', 'Enel Green Power', 'NextEra Energy',
            'RWE Renewables', 'Acciona Energía', 'Brookfield Renewable', 'SSE Renewables',
            'Vattenfall', 'E.ON Climate & Renewables'
        ],
        'Nuclear Fusion': [
            'TAE Technologies', 'Tokamak Energy', 'First Light Fusion', 'Helion Energy',
            'Renaissance Fusion', 'Marvel Fusion', 'Zap Energy', 'Type One Energy',
            'Princeton Fusion Systems', 'CTFusion'
        ]
    }
    
    # Get organizations from both the application data and sector list
    key_orgs = [org['name'] for org in app.get('consumers', [])]
    additional_orgs = sector_organizations.get(app['sector'], [])
    all_orgs = list(set(key_orgs + additional_orgs))  # Remove duplicates
    
    if all_orgs:
        selected_org = st.selectbox(
            "",
            options=all_orgs,
            key=f"select_{app['component']}",
            format_func=lambda x: f"{x} - {app['sector']}"
        )
        if selected_org:
            # Main organization header with key metrics
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center; 
                padding:8px 16px;'>
                <div>
                    <div style='font-size:1.2em; font-weight:500;'>{selected_org}</div>
                    <div style='display:flex; gap:12px; color:#666; font-size:0.9em;'>
                        <span>Headquarters</span>
                        <span>{app['sector']}</span>
                    </div>
                </div>
                <div style='text-align:right;'>
                    <div style='font-size:1.2em;'>{'★' * 4}{'☆' * 1}</div>
                    <div style='font-size:0.9em; color:#666;'>Quality Score: 95%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Key details in a compact 3-column layout
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.markdown("##### Annual Volume")
                st.markdown("<div style='font-size:1.1em;'>50,000 units/year</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("##### Certifications")
                certs = ['AS9100D', 'ISO 9001:2015', 'NADCAP'] if 'Aviation' in app['sector'] or 'Space' in app['sector'] \
                    else ['ASME N-Stamp', 'ISO 9001:2015', 'NQA-1'] if 'Nuclear' in app['sector'] \
                    else ['ISO 9001:2015', 'ISO 14001']
                cert_html = ' '.join([f"<span style='{STYLE_CHIP}'>{cert}</span>" for cert in certs])
                st.markdown(f"<div style='display:flex; flex-wrap:wrap; gap:4px;'>{cert_html}</div>", unsafe_allow_html=True)

            with col3:
                st.markdown("##### Review Score")
                st.progress(0.92)
                st.markdown("<div style='text-align:center; font-size:0.8em;'>95%</div>", unsafe_allow_html=True)

            # Contact form with collapsible section using HTML/CSS
            st.markdown("""<div style='margin-top:1em;'>
                <details style='border-radius:4px; padding:8px;'>
                    <summary style='cursor:pointer; padding:4px; user-select:none;'>
                        📧 Contact Organization
                    </summary>
                    <div style='padding:12px 8px 4px 8px;'>
            """, unsafe_allow_html=True)
            
            with st.form(key=f"contact_{app['component']}_{selected_org}"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Your Name")
                with col2:
                    email = st.text_input("Your Email")
                message = st.text_area("Message", placeholder=f"Enter your message for {selected_org}...")
                if st.form_submit_button("Send Inquiry"):
                    st.success("Thank you! Your inquiry has been sent.")
            
            st.markdown("</div></details></div>", unsafe_allow_html=True)

def render_application_suggestions() -> None:
    """Render AI-matched application suggestions."""
    
    # Applications header
    st.markdown(f"""
        <div style='{STYLE_SECTION_HEADER}'>
            <h2>📊 Steel Applications & Use Cases</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Use CSV data if available, otherwise fall back to demo data
    if applications_df is not None and not applications_df.empty:
        # Convert each row to our application data structure
        for idx, row in applications_df.iterrows():
            # Limit to a reasonable number of applications
            if idx >= 5:
                break
                
            # Create application data structure from CSV row
            app_data = {
                'component': row['Use-case'],
                'use_case': row['Commercial name'],
                'sector': row['Industry'],
                'required_properties': {
                    'Tensile Strength': f"{row['Tensile Strength (MPa)']} MPa" if 'Tensile Strength (MPa)' in row else 'N/A',
                    'Yield Strength': f"{row['Yield Strength (MPa)']} MPa" if 'Yield Strength (MPa)' in row else 'N/A',
                    'Density': f"{row['Density (g/cm³)']} g/cm³" if 'Density (g/cm³)' in row else 'N/A',
                    'Thermal Conductivity': f"{row['Thermal Conductivity (W/m·K)']} W/m·K" if 'Thermal Conductivity (W/m·K)' in row else 'N/A'
                },
                'sustainability': {
                    'recycled_content': row['Recyclability (%)'] if 'Recyclability (%)' in row else 75,
                    'carbon_footprint': {'value': row['Carbon Footprint (kg CO2e/kg)'] if 'Carbon Footprint (kg CO2e/kg)' in row else 2.8, 'unit': 'kgCO2/kg'},
                    'energy_reduction': row['Energy Efficiency (%)'] if 'Energy Efficiency (%)' in row else 60,
                    'waste_reduction': 0.85,
                    'circular_materials': {'percentage': row['Recyclability (%)'] if 'Recyclability (%)' in row else 75, 'recyclable_components': ['structural elements', 'fasteners']}
                },
                'supply_chain_data': {
                    'manufacturers': [
                        {'name': f"Steel Solutions Inc. - {row['Type'] if 'Type' in row else 'Specialty'}", 'location': 'USA', 'lead_time': '6-8 weeks', 'certifications': ['ISO 9001:2015', 'ISO 14001']}
                    ],
                    'processing_capabilities': ['forging', 'machining', 'heat treatment'],
                    'regional_availability': ['North America', 'Europe', 'Asia'],
                    'typical_lead_time': '6-8 weeks'
                },
                'consumers': [
                    {'name': row['Industry'] + ' Leaders', 'location': 'Global', 'annual_volume': '50,000 units', 
                    'rating': 4.8, 'certifications': ['ISO 9001:2015'], 'quality_score': 95}
                ]
            }
            # Add delay for all but the first item
            if idx > 0:
                time.sleep(0.25)
                
            with st.expander(app_data['component'], expanded=(idx == 0)):
                render_application_details(app_data)
    else:
        # Fall back to demo data
        st.warning("Could not load steel applications data. Using demo data instead.")
        for idx, app in enumerate(DEMO_APPLICATIONS):
            # Limit to 5 applications for brevity
            if idx >= 5:
                break
                
            # Add delay for all but the first item
            if idx > 0:
                time.sleep(0.5)
                
            with st.expander(app['component'], expanded=(idx == 0)):
                render_application_details(app)

def render_report(query: Optional[str] = None) -> None:
    """Render a comprehensive report based on the user's query.
    
    Args:
        query: The user's query string. If None, no report will be rendered.
    """
    if not query:
        return
        
    # Add a slight pause for better UX
    time.sleep(1)
    
    # Display the query in a subtle, compact format
    st.markdown(f"""<div style='display:flex; align-items:center; gap:0.5em; margin:0.5em 0; 
                font-size:0.9em;'>
                <span style='color:#666666;'>Query:</span>
                <span style='color:#cccccc;'>{query}</span>
                </div>""", unsafe_allow_html=True)
    
    # Show query analysis in an expander
    render_query_analysis()
    
    # Material properties summary"
    render_material_properties_table()
    
    # Application suggestions
    render_application_suggestions()

    # Here you would typically process the query and generate actual results
    # For now, we'll return a simple demonstration report
    #report = {
    #    'query': query,
    #    'relevant_materials': ['Inconel 718', 'Ti-6Al-4V', 'Al 7075'],
    #    'properties': ['High temperature resistance', 'Corrosion resistance', 'High strength'],
    #    'applications': ['Aerospace components', 'Gas turbines', 'High-stress environments']
    #}
    #return report

def render_key_property_card(title: str, value: str, impact: str, confidence: float, source_url: Optional[str] = None) -> None:
    """Render a card showing a key material property and its impact.
    
    Args:
        title: Name of the property
        value: Measured or qualitative value
        impact: Relevance to user's requirements
        confidence: Confidence score for this property's impact
        source_url: Optional URL to source documentation
    """
    confidence_color = '#00cc96' if confidence >= 0.9 else '#ffd43b' if confidence >= 0.7 else '#ff6b6b'
    confidence_width = f"{confidence * 100}%"
    
    source_html = f"""<div style='margin-top:0.5em; text-align:right;'>
        <a href='{source_url}' target='_blank' style='color:#4dabf7; font-size:0.8em;
        text-decoration:none; opacity:0.8; transition:opacity 0.2s;' 
        onmouseover='this.style.opacity=1' onmouseout='this.style.opacity=0.8'>View Source</a>
    </div>""" if source_url else ""
    
    st.markdown(f"""
    <div style='background-color:rgba(38, 39, 48, 0.03); padding:1em; border-radius:4px; margin-bottom:1em;'>
        <div style='margin-bottom:0.5em;'>
            <div style='color:#666666; font-size:0.85em; margin-bottom:0.2em;'>{title}</div>
            <div style='font-size:1.1em; font-weight:500;'>{value}</div>
        </div>
        <div style='color:#666666; font-size:0.9em; margin-bottom:0.5em;'>{impact}</div>
        <div style='background-color:rgba(38, 39, 48, 0.1); height:4px; border-radius:2px; overflow:hidden;'>
            <div style='background-color:{confidence_color}; width:{confidence_width}; height:100%; 
                border-radius:2px; transition:width 0.3s ease-in-out;'></div>
        </div>
        {source_html}
    </div>
    """, unsafe_allow_html=True)

# Add new style constant at the top of the file
STYLE_MATERIAL_HEADER = """
    padding: 0.5em 1em;
    border-radius: 8px;
    background: linear-gradient(90deg, rgba(38, 39, 48, 0.1) 0%, rgba(38, 39, 48, 0) 100%);
    border-left: 3px solid #00cc96;
    margin-bottom: 1em;
"""

def render_material_properties_table() -> None:
    """Render key material properties relevant to the user's requirements."""
    
    if materials_df is None or materials_df.empty:
        material_name = DEMO_PARSED_ENTITIES['material']
        st.error("Unable to load material database. Using demo data instead.")
    else:
        # Use actual material data from first row for demonstration
        material_name = materials_df.iloc[0]['Commercial name'] if 'Commercial name' in materials_df.columns else DEMO_PARSED_ENTITIES['material']
    
    with st.expander("⁂ Key Material Properties"):
        # Material header with query context
        st.markdown("""
            <div style='{}'>
                <p style='color:#666666; text-transform:uppercase; letter-spacing:1px; font-size:0.8em; margin:0;'>Material Analysis</p>
                <h3 style='margin:0.2em 0; font-size:1.2em;'>{}</h3>
                <p style='color:#666666; font-size:0.9em; margin:0.2em 0;'>Properties analyzed in context of high-temperature, corrosion-resistant applications</p>
            </div>
        """.format(
            STYLE_MATERIAL_HEADER,
            material_name
        ), unsafe_allow_html=True)
        
        # Separator before first section
        st.markdown("""<hr style='border:none; height:1px; background-color:rgba(38, 39, 48, 0.1); 
                  margin:1.5em 0 1em 0;'>""", unsafe_allow_html=True)
        
        # First Row: Performance and Sustainability Properties
        st.markdown("#### Performance & Sustainability")
        col1, col2, col3 = st.columns(3)
        
        # Column 1: High-Temperature Properties
        with col1:
            render_key_property_card(
                "Tensile Strength", 
                tensile_strength, 
                "Excellent high-temperature strength retention",
                0.98,
                "https://www.specialmetals.com/assets/smc/documents/alloys/inconel/inconel-alloy-625.pdf"
            )
            
        with col2:
            render_key_property_card(
                "Yield Strength", 
                yield_strength, 
                "Superior load-bearing capacity in extreme environments",
                0.97,
                "https://www.specialmetals.com/assets/smc/documents/alloys/inconel/inconel-alloy-625.pdf"
            )
            
        with col3:
            render_key_property_card(
                "Density", 
                density, 
                "Weight-efficient high-performance material",
                0.96
            )
            
        # Create three columns for the thermal properties
        st.markdown("#### Thermal & Chemical Properties")
        col4, col5, col6 = st.columns(3)
        
        with col4:
            render_key_property_card(
                "Melting Point", 
                melting_point, 
                "Suitable for high-temperature applications",
                0.96,
                "https://www.specialmetals.com/assets/smc/documents/alloys/inconel/inconel-alloy-625.pdf"
            )
            
        with col5:
            render_key_property_card(
                "Thermal Conductivity", 
                thermal_conductivity, 
                "Low thermal conductivity ideal for thermal barriers",
                0.95
            )
            
        with col6:
            render_key_property_card(
                "Corrosion Resistance", 
                corrosion_resistance, 
                "Superior resistance to oxidation and corrosion",
                0.99,
                "https://www.specialmetals.com/assets/smc/documents/alloys/inconel/inconel-alloy-625.pdf"
            )
        
        # Create three columns for the sustainability metrics
        st.markdown("#### Sustainability & Circularity")
        col7, col8, col9 = st.columns(3)
        
        with col7:
            render_key_property_card(
                "Recycled Content", 
                recycled_content, 
                "Industry-standard recycled content for specialty steel alloys",
                0.92
            )
            
        with col8:
            render_key_property_card(
                "Recyclability", 
                recyclability, 
                "Highly valuable for recycling and reprocessing",
                0.94
            )
            
        with col9:
            render_key_property_card(
                "Carbon Footprint", 
                carbon_footprint, 
                "Lifetime carbon savings outweigh production footprint",
                0.93,
                "https://nickelinstitute.org/media/4202/lifecycledata2020.pdf"
            )
        
        # Separator between sections
        st.markdown("""<hr style='border:none; height:1px; background-color:rgba(38, 39, 48, 0.1); 
                  margin:2em 0 1em 0;'>""", unsafe_allow_html=True)
        
        # Second Row: Lifecycle and Circular Economy
        st.markdown("#### Lifecycle & Circular Economy")
        col4, col5, col6 = st.columns(3)
        
        # Separator after last section
        st.markdown("""<hr style='border:none; height:1px; background-color:rgba(38, 39, 48, 0.1); 
                  margin:2em 0 0.5em 0;'>""", unsafe_allow_html=True)
        
        # Column 4: Lifecycle Properties
        with col4:
            render_key_property_card(
                "Service Life",
                "25+ years with maintenance",
                "Extended durability reduces material consumption and replacement frequency.",
                0.96
            )
            render_key_property_card(
                "Maintenance Interval",
                "5-7 years typical",
                "Reduced maintenance requirements lower lifecycle resource usage.",
                0.93
            )
        
        # Column 5: Resource Efficiency
        with col5:
            render_key_property_card(
                "Material Efficiency",
                "High strength-to-weight",
                "Optimizes material usage while maintaining performance requirements.",
                0.95
            )
            render_key_property_card(
                "Energy Efficiency",
                "High thermal performance",
                "Reduces operational energy consumption in high-temperature applications.",
                0.94
            )
        
        # Column 6: Circular Economy
        with col6:
            render_key_property_card(
                "Recyclability",
                ">90% recoverable",
                "High-value material recovery at end-of-life, supporting circular economy.",
                0.94
            )
            render_key_property_card(
                "Manufacturing Impact",
                "Minimal waste in processing",
                "Efficient processing with high material utilization and recyclable scrap.",
                0.92
            )
