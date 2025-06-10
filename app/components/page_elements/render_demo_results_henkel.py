import streamlit as st
import pandas as pd
import time
from typing import Dict, List, Optional, Tuple, Union

# Styling constants
STYLE_CHIP = """
    display:inline-block;
    padding:4px 12px;
    margin:2px;
    background-color:rgba(38, 39, 48, 0.8);
    border-radius:15px;
    font-size:0.9em;
    border:1px solid rgba(128, 128, 128, 0.4);
    color:#ffffff
"""

STYLE_SECTION_HEADER = """
    color:#666666;
    text-transform:uppercase;
    letter-spacing:1px;
    font-size:0.85em;
    margin-bottom:1em
"""

STYLE_CONFIDENCE_BAR = """
    background-color:rgba(38, 39, 48, 0.8);
    padding:8px 12px;
    margin:4px 0;
    border-radius:4px;
    font-size:0.9em
"""

STYLE_TABLE = """
    table {
        font-size: 0.9em;
        width: 100%;
        color: rgb(49, 51, 63) !important;
    }
    thead tr th {
        background-color: #f0f2f6 !important;
        color: rgb(49, 51, 63) !important;
        font-weight: bold !important;
    }
    tbody tr:first-child td {
        background-color: white !important;
        color: rgb(49, 51, 63) !important;
    }
    tbody td:first-child {
        color: rgb(49, 51, 63) !important;
    }
    td {
        padding: 8px;
        background-color: white !important;
    }
"""

# Demo data structures
DEMO_PARSED_ENTITIES = {
    'material_type': 'semiconductor packaging adhesive',
    'context_filters': ['halogen-free', 'low-VOC', 'thermally-conductive', 'high-reliability'],
    'application_focus': ['advanced packaging', 'high-performance computing'],
    'regulatory_requirements': ['RoHS', 'REACH', 'JEDEC'],
    'material_insights': {
        'title': 'Material Insights',
        'subtitle': 'Properties analyzed for high-performance semiconductor packaging applications',
        'key_factors': [
            {
                'category': 'Thermal Performance',
                'properties': [
                    {'name': 'Thermal Conductivity', 'value': '2.3-2.8 W/m·K'},
                    {'name': 'Thermal Resistance', 'value': '0.12-0.15 °C/W'},
                    {'name': 'Operating Temperature', 'value': '-55 to 150°C'}
                ]
            },
            {
                'category': 'Reliability',
                'properties': [
                    {'name': 'JEDEC MSL', 'value': 'Level 1'},
                    {'name': 'Reflow Cycles', 'value': '3x 260°C'},
                    {'name': 'Adhesion Strength', 'value': '20-25 MPa'}
                ]
            },
            {
                'category': 'Sustainability',
                'properties': [
                    {'name': 'Halogen Content', 'value': '<850 ppm'},
                    {'name': 'VOC Content', 'value': '<100 g/L'},
                    {'name': 'Carbon Footprint', 'value': '3.0-3.2 kg CO2e/kg'}
                ]
            }
        ]
    }
}

# Demo data structure for parse tree
DEMO_PARSE_TREE = {
    'node': 'QUERY',
    'children': [
        {
            'node': 'MATERIAL',
            'value': 'semiconductor packaging adhesive',
            'confidence': 0.96
        },
        {
            'node': 'CONTEXT',
            'children': [
                {
                    'node': 'REQUIREMENT',
                    'value': 'high-performance',
                    'confidence': 0.89
                },
                {
                    'node': 'REQUIREMENT',
                    'value': 'sustainable',
                    'confidence': 0.85
                }
            ]
        },
        {
            'node': 'REQUIREMENTS',
            'children': [
                {
                    'node': 'PROPERTY',
                    'value': 'thermally-conductive',
                    'confidence': 0.94
                },
                {
                    'node': 'PROPERTY',
                    'value': 'halogen-free',
                    'confidence': 0.98
                },
                {
                    'node': 'PROPERTY',
                    'value': 'high-reliability',
                    'confidence': 0.91
                },
                {
                    'node': 'PROPERTY',
                    'value': 'low-warpage',
                    'confidence': 0.86
                }
            ]
        },
        {
            'node': 'DOMAINS',
            'children': [
                {
                    'node': 'INDUSTRY',
                    'value': 'semiconductor',
                    'confidence': 0.93
                },
                {
                    'node': 'APPLICATION',
                    'value': 'advanced packaging',
                    'confidence': 0.89
                }
            ]
        },
        {
            'node': 'COMPLIANCE',
            'children': [
                {
                    'node': 'REGULATION',
                    'value': 'JEDEC',
                    'confidence': 0.97
                },
                {
                    'node': 'REGULATION',
                    'value': 'RoHS',
                    'confidence': 0.96
                },
                {
                    'node': 'REGULATION',
                    'value': 'REACH',
                    'confidence': 0.95
                }
            ]
        }
    ]
}

DEMO_APPLICATIONS = [
    # 1. High-Performance Computing
    {
        'component': 'Cryogenic Die Attach System',
        'use_case': 'Ultra-low temperature quantum computing chip assembly',
        'sector': 'Quantum Computing',
        'rationale': 'Novel hybrid adhesive system with graphene-enhanced thermal interface. Maintains bond integrity from room temperature down to -270°C with minimal CTE mismatch stress. Enables direct integration with superconducting qubit circuits.',
        'source_url': 'https://www.henkel-adhesives.com/us/en/industries/emerging-technologies.html',
        'requirements': {
            'thermal_conductivity': {'min': 3.5, 'unit': 'W/m·K'},
            'cte': {'max': 12, 'unit': 'ppm/°C'},
            'operating_temp': {'min': -270, 'max': 25, 'unit': '°C'},
            'adhesion_strength': {'min': 18, 'unit': 'MPa'},
            'cure_profile': {'temp': 150, 'time': 45, 'unit': 'min'},
            'outgassing': {'max': 0.05, 'unit': '%'},
            'shelf_life': {'duration': 6, 'unit': 'months', 'temp': '-40°C'}
        },
        'sustainability_metrics': {
            'halogen_content': {'value': '<500', 'unit': 'ppm'},
            'voc_emissions': {'value': '<50', 'unit': 'g/L'},
            'carbon_footprint': {'value': 4.2, 'unit': 'kgCO2/kg'},
            'recyclability': {'rating': 'EU Class 3', 'separable': False},
            'rare_materials': {'present': True, 'recycled_content': '15%'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Henkel Research Lab', 'location': 'Germany', 'lead_time': '4-6 weeks', 'certifications': ['ISO 9001', 'ISO 14001', 'Clean Room Class 1000']},
                {'name': 'Henkel Quantum Materials', 'location': 'USA', 'lead_time': '5-7 weeks', 'certifications': ['ISO 9001', 'Clean Room Class 1000']}
            ],
            'key_suppliers': [
                {'name': 'Graphene Manufacturing Group', 'material': 'graphene sheets', 'location': 'Canada'},
                {'name': 'Quantum Materials Corp', 'material': 'quantum dots', 'location': 'USA'},
                {'name': 'DIC Corporation', 'material': 'epoxy resins', 'location': 'Japan'}
            ],
            'manufacturing_sites': [
                {
                    'location': 'Germany',
                    'capacity': '500 kg/month',
                    'certifications': ['ISO 9001', 'ISO 14001', 'Clean Room Class 1000'],
                    'lead_time': '4-6 weeks'
                },
                {
                    'location': 'USA',
                    'annual_volume': '4,800 kg',
                    'rating': 4.7,
                    'certifications': ['ISO 9001', 'Clean Room Class 1000'],
                    'quality_score': 94
                }
            ]
        },
        'consumers': [
            {
                'name': 'IBM Quantum',
                'location': 'USA',
                'annual_volume': '800 kg',
                'rating': 4.8,
                'certifications': ['ISO 9001', 'Clean Room Class 100'],
                'quality_score': 96
            },
            {
                'name': 'Google Quantum AI',
                'location': 'USA',
                'annual_volume': '600 kg',
                'rating': 4.7,
                'certifications': ['ISO 9001', 'Clean Room Class 100'],
                'quality_score': 95
            },
            {
                'name': 'IQM Quantum Computers',
                'location': 'Finland',
                'annual_volume': '400 kg',
                'rating': 4.6,
                'certifications': ['ISO 9001', 'Clean Room Class 1000'],
                'quality_score': 93
            }
        ]
    },

    # 2. Mobile & Edge Computing
    {
        'component': 'Low-Warpage Underfill',
        'use_case': 'Mobile processor flip-chip packaging with ultra-low warpage',
        'sector': 'Mobile Computing',
        'rationale': 'Advanced capillary underfill with nano-silica reinforcement and stress-absorbing chemistry. Achieves <20µm warpage at 260°C with 2.3 W/m·K thermal conductivity and halogen-free formulation.',
        'source_url': 'https://www.henkel-adhesives.com/us/en/industries/electronics.html',
        'requirements': {
            'warpage': {'max': 25, 'unit': 'µm', 'temp': 260},
            'thermal_conductivity': {'min': 2.0, 'max': 2.3, 'unit': 'W/m·K'},
            'cte': {'min': 30, 'max': 40, 'unit': 'ppm/°C'},
            'fillet_height': {'min': 75, 'target': 85, 'unit': '%'},
            'cure_profile': {'temp': 165, 'time': 45, 'unit': 'min'},
            'shelf_life': {'duration': 6, 'unit': 'months', 'temp': '-40°C'},
            'moisture_sensitivity': {'level': 'MSL-3'}
        },
        'sustainability_metrics': {
            'halogen_content': {'value': '<850', 'unit': 'ppm'},
            'voc_emissions': {'value': '<80', 'unit': 'g/L'},
            'carbon_footprint': {'value': 2.9, 'unit': 'kgCO2/kg'},
            'recyclability': {'rating': 'EU Class 2', 'separable': True}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Henkel Electronics', 'location': 'Korea', 'lead_time': '1-2 weeks', 'certifications': ['ISO 9001', 'IATF 16949', 'ISO 14001']},
                {'name': 'Henkel China', 'location': 'China', 'lead_time': '1-2 weeks', 'certifications': ['ISO 9001', 'IATF 16949']},
                {'name': 'Henkel Americas', 'location': 'USA', 'lead_time': '2-3 weeks', 'certifications': ['ISO 9001']}
            ],
            'key_suppliers': [
                {'name': 'Momentive', 'material': 'silica fillers', 'location': 'USA'},
                {'name': 'Nagase', 'material': 'epoxy resins', 'location': 'Japan'},
                {'name': 'Evonik', 'material': 'specialty additives', 'location': 'Germany'}
            ],
            'manufacturing_sites': [
                {
                    'location': 'Korea',
                    'capacity': '45,000 kg/month',
                    'certifications': ['ISO 9001', 'IATF 16949', 'ISO 14001'],
                    'lead_time': '2-3 weeks'
                },
                {
                    'location': 'China',
                    'annual_volume': '380,000 kg',
                    'rating': 4.2,
                    'certifications': ['ISO 9001', 'IATF 16949'],
                    'quality_score': 88
                }
            ]
        },
        'consumers': [
            {
                'name': 'Qualcomm',
                'location': 'USA',
                'annual_volume': '12,000 kg',
                'rating': 4.5,
                'certifications': ['ISO 9001', 'ISO 14001'],
                'quality_score': 92
            },
            {
                'name': 'MediaTek',
                'location': 'Taiwan',
                'annual_volume': '14,000 kg',
                'rating': 4.3,
                'certifications': ['ISO 9001', 'IATF 16949'],
                'quality_score': 89
            },
            {
                'name': 'Samsung Electronics',
                'location': 'Korea',
                'annual_volume': '17,000 kg',
                'rating': 4.7,
                'certifications': ['ISO 9001', 'ISO 14001', 'IATF 16949'],
                'quality_score': 94
            }
        ]
    },

    # 3. Automotive & Industrial
    {
        'component': 'High-Reliability Die Attach Film',
        'use_case': 'Power semiconductor assembly for electric vehicle inverters',
        'sector': 'Automotive Electronics',
        'rationale': 'Advanced die attach film with silver-sintering technology and stress-relief additives. Delivers 3.2 W/m·K thermal conductivity and passes 3000 thermal cycles (-40°C to 150°C) with zero delamination.',
        'source_url': 'https://www.henkel-adhesives.com/us/en/industries/automotive.html',
        'requirements': {
            'thermal_conductivity': {'min': 2.8, 'target': 3.2, 'unit': 'W/m·K'},
            'thermal_cycling': {'cycles': 2000, 'range': '-40 to 150°C', 'criteria': 'No delamination'},
            'die_shear_strength': {'min': 25, 'target': 30, 'unit': 'MPa'},
            'operating_temp': {'min': -40, 'max': 175, 'unit': '°C'},
            'cure_profile': {'temp': 200, 'time': 60, 'pressure': 5, 'unit': {'temp': '°C', 'time': 'min', 'pressure': 'MPa'}},
            'shelf_life': {'duration': 12, 'unit': 'months', 'temp': '-40°C'},
            'qualification': {'standards': ['AEC-Q100 Grade 0', 'JEDEC JESD22-A104']}
        },
        'sustainability_metrics': {
            'halogen_content': {'value': '<800', 'unit': 'ppm'},
            'voc_emissions': {'value': '<50', 'unit': 'g/L'},
            'carbon_footprint': {'value': 3.5, 'unit': 'kgCO2/kg'},
            'recyclability': {'rating': 'EU Class 2', 'separable': True}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Henkel Electronics', 'location': 'Japan', 'lead_time': '1-2 weeks', 'certifications': ['ISO 9001', 'IATF 16949', 'ISO 14001']},
                {'name': 'Henkel Europe', 'location': 'Germany', 'lead_time': '1-2 weeks', 'certifications': ['ISO 9001', 'IATF 16949']},
                {'name': 'Henkel Americas', 'location': 'USA', 'lead_time': '2-3 weeks', 'certifications': ['ISO 9001']}
            ],
            'key_suppliers': [
                {'name': 'Heraeus', 'material': 'silver powders', 'location': 'Germany'},
                {'name': 'Toray', 'material': 'specialty polymers', 'location': 'Japan'},
                {'name': 'DuPont', 'material': 'electronic materials', 'location': 'USA'}
            ],
            'manufacturing_sites': [
                {
                    'location': 'Japan',
                    'capacity': '40,000 kg/month',
                    'certifications': ['ISO 9001', 'IATF 16949', 'ISO 14001'],
                    'lead_time': '1-2 weeks'
                },
                {
                    'location': 'Germany',
                    'annual_volume': '320,000 kg',
                    'rating': 4.5,
                    'certifications': ['ISO 9001', 'IATF 16949', 'ISO 14001'],
                    'quality_score': 92
                }
            ]
        },
        'consumers': [
            {
                'name': 'Infineon Technologies',
                'location': 'Germany',
                'annual_volume': '28,000 kg',
                'rating': 4.6,
                'certifications': ['ISO 9001', 'IATF 16949', 'ISO 14001'],
                'quality_score': 93
            },
            {
                'name': 'STMicroelectronics',
                'location': 'France',
                'annual_volume': '22,000 kg',
                'rating': 4.4,
                'certifications': ['ISO 9001', 'IATF 16949'],
                'quality_score': 90
            },
            {
                'name': 'ON Semiconductor',
                'location': 'USA',
                'annual_volume': '25,000 kg',
                'rating': 4.2,
                'certifications': ['ISO 9001', 'IATF 16949'],
                'quality_score': 88
            }
        ]
    },

    # 4. Advanced Memory Packaging
    {
        'component': 'Ultra-Thin Die Attach Film',
        'use_case': 'HBM (High Bandwidth Memory) stacking for AI accelerators',
        'sector': 'Memory & Storage',
        'rationale': 'Ultra-thin (5-15µm) die attach film enabling reliable HBM2E/3 stacking. Features controlled bond line thickness and void-free lamination for critical thermal management.',
        'requirements': {
            'thickness': {'min': 5, 'max': 15, 'unit': 'µm'},
            'thermal_conductivity': {'min': 2.5, 'target': 3.0, 'unit': 'W/m·K'},
            'warpage': {'max': 15, 'unit': 'µm'},
            'void_content': {'max': 0.1, 'unit': '%'},
            'adhesion_strength': {'min': 15, 'unit': 'MPa'},
            'cure_profile': {'temp': 180, 'time': 30, 'pressure': 3, 'unit': {'temp': '°C', 'time': 'min', 'pressure': 'MPa'}},
            'moisture_sensitivity': {'level': 'MSL-2'}
        },
        'sustainability_metrics': {
            'halogen_content': {'value': '<500', 'unit': 'ppm'},
            'voc_emissions': {'value': '<30', 'unit': 'g/L'},
            'carbon_footprint': {'value': 2.8, 'unit': 'kgCO2/kg'},
            'recyclability': {'rating': 'EU Class 2', 'separable': True}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Henkel Advanced Memory', 'location': 'South Korea', 'lead_time': '3-4 weeks', 'certifications': ['ISO 9001', 'ISO 14001', 'Clean Room Class 1000']}
            ],
            'manufacturing_sites': [
                {
                    'location': 'South Korea',
                    'capacity': '8,000 kg/month',
                    'rating': 4.6,
                    'certifications': ['ISO 9001', 'Clean Room Class 1000'],
                    'quality_score': 93
                }
            ]
        },
        'consumers': [
            {'name': 'SK hynix', 'location': 'Korea', 'annual_volume': '45,000 kg', 'rating': 4.7, 'quality_score': 94, 'certifications': ['ISO 9001', 'IATF 16949']},
            {'name': 'Samsung Memory', 'location': 'Korea', 'annual_volume': '52,000 kg', 'rating': 4.8, 'quality_score': 95, 'certifications': ['ISO 9001', 'IATF 16949', 'ISO 14001']}
        ]
    },

    # 5. Advanced Packaging for RF
    {
        'component': 'Low-K Compatible Underfill',
        'use_case': '5G mmWave RF module assembly',
        'sector': 'RF & Communications',
        'rationale': 'Low dielectric constant underfill optimized for 5G mmWave applications. Provides excellent protection while maintaining signal integrity up to 80 GHz.',
        'requirements': {
            'dielectric_constant': {'max': 2.8, 'freq': '40 GHz', 'unit': 'Dk'},
            'loss_tangent': {'max': 0.002, 'freq': '40 GHz'},
            'cte': {'min': 25, 'max': 35, 'unit': 'ppm/°C'},
            'glass_transition': {'min': 150, 'unit': '°C'},
            'flow_rate': {'min': 8, 'max': 12, 'unit': 'mm/s'},
            'moisture_sensitivity': {'level': 'MSL-3'},
            'qualification': {'standards': ['JEDEC JESD22-A112']}
        },
        'sustainability_metrics': {
            'halogen_content': {'value': '<750', 'unit': 'ppm'},
            'voc_emissions': {'value': '<60', 'unit': 'g/L'},
            'carbon_footprint': {'value': 3.1, 'unit': 'kgCO2/kg'},
            'recyclability': {'rating': 'EU Class 2', 'separable': True}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Henkel RF Solutions', 'location': 'USA', 'lead_time': '2-3 weeks', 'certifications': ['ISO 9001', 'ISO 14001']}
            ],
            'manufacturing_sites': [
                {
                    'location': 'USA',
                    'capacity': '12,000 kg/month',
                    'rating': 4.5,
                    'certifications': ['ISO 9001', 'Clean Room Class 10000'],
                    'quality_score': 91
                }
            ]
        },
        'consumers': [
            {'name': 'Qualcomm RF', 'location': 'USA', 'annual_volume': '35,000 kg', 'rating': 4.6, 'quality_score': 92, 'certifications': ['ISO 9001', 'ISO 14001']},
            {'name': 'Qorvo', 'location': 'USA', 'annual_volume': '28,000 kg', 'rating': 4.5, 'quality_score': 91, 'certifications': ['ISO 9001', 'IATF 16949']}
        ]
    },

    # 6. Photonic Integration
    {
        'component': 'Optically-Clear Die Attach',
        'use_case': 'Silicon photonics chip packaging',
        'sector': 'Photonics & Optical',
        'rationale': 'Optically transparent die attach adhesive for silicon photonics integration. Features >98% transmission in 1310-1550nm range and ultra-low outgassing.',
        'requirements': {
            'optical_transmission': {'min': 98, 'wavelength': '1310-1550', 'unit': {'transmission': '%', 'wavelength': 'nm'}},
            'refractive_index': {'value': 1.45, 'tolerance': 0.02},
            'outgassing': {'max': 0.02, 'unit': '%'},
            'thermal_conductivity': {'min': 0.5, 'unit': 'W/m·K'},
            'cte': {'value': 45, 'tolerance': 5, 'unit': 'ppm/°C'},
            'cure_profile': {'temp': 150, 'time': 60, 'unit': {'temp': '°C', 'time': 'min'}},
            'storage': {'temp': -40, 'humidity': 5, 'unit': {'temp': '°C', 'humidity': '%RH'}}
        },
        'sustainability_metrics': {
            'halogen_content': {'value': '<100', 'unit': 'ppm'},
            'voc_emissions': {'value': '<20', 'unit': 'g/L'},
            'carbon_footprint': {'value': 2.5, 'unit': 'kgCO2/kg'},
            'recyclability': {'rating': 'EU Class 3', 'separable': False}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Henkel Photonics', 'location': 'Switzerland', 'lead_time': '4-5 weeks', 'certifications': ['ISO 9001', 'Clean Room Class 100']}
            ],
            'manufacturing_sites': [
                {
                    'location': 'Switzerland',
                    'capacity': '2,000 kg/month',
                    'rating': 4.7,
                    'certifications': ['ISO 9001', 'Clean Room Class 100'],
                    'quality_score': 94
                }
            ]
        },
        'consumers': [
            {'name': 'Intel Silicon Photonics', 'location': 'USA', 'annual_volume': '8,000 kg', 'rating': 4.8, 'quality_score': 95, 'certifications': ['ISO 9001', 'ISO 14001', 'Clean Room Class 100']},
            {'name': 'Cisco Optics', 'location': 'USA', 'annual_volume': '6,000 kg', 'rating': 4.6, 'quality_score': 92, 'certifications': ['ISO 9001', 'TL 9000']}
        ]
    },

    # 7. Chiplet Integration
    {
        'component': 'Hybrid Bond Enhancement Film',
        'use_case': 'Advanced chiplet integration using hybrid bonding',
        'sector': 'Advanced Packaging',
        'rationale': 'Ultra-clean surface preparation film for Cu-Cu hybrid bonding. Enables <10nm surface roughness and oxide-free Cu surfaces for direct bonding.',
        'requirements': {
            'surface_roughness': {'max': 10, 'unit': 'nm'},
            'particle_size': {'max': 0.1, 'unit': 'µm'},
            'contact_angle': {'max': 5, 'unit': 'degrees'},
            'ionic_contamination': {'max': 0.02, 'unit': 'µg/cm²'},
            'shelf_life': {'duration': 3, 'unit': 'months', 'temp': '-40°C'},
            'process_window': {'temp': {'min': 20, 'max': 30}, 'humidity': {'min': 35, 'max': 55}, 'unit': {'temp': '°C', 'humidity': '%RH'}},
            'bond_strength': {'min': 20, 'unit': 'MPa'}
        },
        'sustainability_metrics': {
            'halogen_content': {'value': '<50', 'unit': 'ppm'},
            'voc_emissions': {'value': '<10', 'unit': 'g/L'},
            'carbon_footprint': {'value': 2.2, 'unit': 'kgCO2/kg'},
            'recyclability': {'rating': 'EU Class 3', 'separable': False},
            'water_usage': {'value': 1.5, 'unit': 'L/kg'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Henkel Advanced Tech', 'location': 'Taiwan', 'lead_time': '5-6 weeks', 'certifications': ['ISO 9001', 'Clean Room Class 10']}
            ],
            'manufacturing_sites': [
                {
                    'location': 'Taiwan',
                    'capacity': '1,500 kg/month',
                    'rating': 4.8,
                    'certifications': ['ISO 9001', 'Clean Room Class 10'],
                    'quality_score': 96
                }
            ]
        },
        'consumers': [
            {'name': 'TSMC', 'location': 'Taiwan', 'annual_volume': '12,000 kg', 'rating': 4.9, 'quality_score': 97, 'certifications': ['ISO 9001', 'ISO 14001', 'IATF 16949', 'Clean Room Class 10']},
            {'name': 'Intel Foundry', 'location': 'USA', 'annual_volume': '8,000 kg', 'rating': 4.7, 'quality_score': 94, 'certifications': ['ISO 9001', 'ISO 14001', 'Clean Room Class 100']}
        ]
    },

    # 8. MEMS & Sensors
    {
        'component': 'Low Stress Encapsulant',
        'use_case': 'MEMS microphone and pressure sensor packaging',
        'sector': 'Sensors & MEMS',
        'rationale': 'Ultra-low modulus encapsulant designed for sensitive MEMS devices. Provides environmental protection while maintaining acoustic/pressure membrane movement.',
        'requirements': {
            'youngs_modulus': {'max': 0.5, 'unit': 'GPa'},
            'viscosity': {'min': 3000, 'max': 5000, 'unit': 'cP'},
            'thixotropic_index': {'min': 2.5, 'unit': None},
            'gel_time': {'value': 4, 'tolerance': 1, 'unit': 'hours'},
            'acoustic_transmission': {'min': 95, 'freq': '20Hz-20kHz', 'unit': '%'},
            'hermeticity': {'max': 1e-8, 'unit': 'atm·cc/s'},
            'operation_temp': {'min': -40, 'max': 125, 'unit': '°C'}
        },
        'sustainability_metrics': {
            'halogen_content': {'value': '<100', 'unit': 'ppm'},
            'voc_emissions': {'value': '<15', 'unit': 'g/L'},
            'carbon_footprint': {'value': 2.1, 'unit': 'kgCO2/kg'},
            'recyclability': {'rating': 'EU Class 3', 'separable': False}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Henkel MEMS', 'location': 'Netherlands', 'lead_time': '3-4 weeks', 'certifications': ['ISO 9001', 'Clean Room Class 1000']}
            ],
            'manufacturing_sites': [
                {
                    'location': 'Netherlands',
                    'capacity': '5,000 kg/month',
                    'rating': 4.5,
                    'certifications': ['ISO 9001', 'Clean Room Class 1000'],
                    'quality_score': 92
                }
            ]
        },
        'consumers': [
            {'name': 'Knowles', 'location': 'USA', 'annual_volume': '25,000 kg', 'rating': 4.6, 'quality_score': 93, 'certifications': ['ISO 9001', 'IATF 16949', 'Clean Room Class 1000']},
            {'name': 'Bosch Sensortec', 'location': 'Germany', 'annual_volume': '18,000 kg', 'rating': 4.7, 'quality_score': 94, 'certifications': ['ISO 9001', 'IATF 16949', 'ISO 14001']}
        ]
    },

    # 9. Advanced 3D Packaging
    {
        'component': 'Temporary Bonding Adhesive',
        'use_case': 'Wafer thinning for 3D-IC stacking',
        'sector': 'Advanced Packaging',
        'rationale': 'Thermally debondable adhesive for temporary wafer bonding during ultra-thin wafer processing. Enables <50µm wafer thickness with laser release.',
        'requirements': {
            'bond_strength': {'min': 10, 'temp': 25, 'unit': {'strength': 'MPa', 'temp': '°C'}},
            'thickness_uniformity': {'max': 3, 'unit': '%'},
            'thermal_stability': {'min': 300, 'unit': '°C'},
            'laser_release': {'wavelength': 308, 'power': 150, 'unit': {'wavelength': 'nm', 'power': 'mJ/cm²'}},
            'residue': {'max': 0.1, 'unit': '%'},
            'chemical_resistance': {'media': ['TMAH', 'HF', 'IPA'], 'time': 120, 'unit': 'min'}
        },
        'sustainability_metrics': {
            'halogen_content': {'value': '<200', 'unit': 'ppm'},
            'voc_emissions': {'value': '<40', 'unit': 'g/L'},
            'carbon_footprint': {'value': 2.9, 'unit': 'kgCO2/kg'},
            'recyclability': {'rating': 'EU Class 2', 'separable': True},
            'solvent_recovery': {'value': 85, 'unit': '%'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Henkel 3D-IC', 'location': 'Japan', 'lead_time': '3-4 weeks', 'certifications': ['ISO 9001', 'Clean Room Class 100']}
            ],
            'manufacturing_sites': [
                {
                    'location': 'Japan',
                    'capacity': '3,500 kg/month',
                    'rating': 4.7,
                    'certifications': ['ISO 9001', 'Clean Room Class 100'],
                    'quality_score': 94
                }
            ]
        },
        'consumers': [
            {'name': 'TSMC Advanced Packaging', 'location': 'Taiwan', 'annual_volume': '15,000 kg', 'rating': 4.8, 'quality_score': 96, 'certifications': ['ISO 9001', 'ISO 14001', 'Clean Room Class 100']},
            {'name': 'Samsung Foundry', 'location': 'Korea', 'annual_volume': '12,000 kg', 'rating': 4.7, 'quality_score': 95, 'certifications': ['ISO 9001', 'IATF 16949', 'Clean Room Class 100']}
        ]
    },

    # 10. Power Electronics
    {
        'component': 'Silver Sinter Paste',
        'use_case': 'Wide bandgap power semiconductor assembly',
        'sector': 'Power Electronics',
        'rationale': 'Pressure-less silver sintering paste for SiC/GaN power devices. Enables >250°C continuous operation with 100+ thermal cycles reliability.',
        'requirements': {
            'thermal_conductivity': {'min': 150, 'typical': 200, 'unit': 'W/m·K'},
            'electrical_conductivity': {'min': 1e5, 'unit': 'S/m'},
            'die_shear_strength': {'min': 30, 'temp': 250, 'unit': {'strength': 'MPa', 'temp': '°C'}},
            'porosity': {'max': 15, 'unit': '%'},
            'sintering_profile': {'temp': 250, 'time': 30, 'atmosphere': 'N2', 'unit': {'temp': '°C', 'time': 'min'}},
            'particle_size': {'d50': 0.1, 'unit': 'µm'}
        },
        'sustainability_metrics': {
            'halogen_content': {'value': '<50', 'unit': 'ppm'},
            'voc_emissions': {'value': '<25', 'unit': 'g/L'},
            'carbon_footprint': {'value': 3.8, 'unit': 'kgCO2/kg'},
            'silver_recycling': {'recovery': 90, 'unit': '%'},
            'water_usage': {'value': 2.1, 'unit': 'L/kg'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Henkel Power Electronics', 'location': 'Germany', 'lead_time': '4-5 weeks', 'certifications': ['ISO 9001', 'IATF 16949', 'Clean Room Class 1000']}
            ],
            'manufacturing_sites': [
                {
                    'location': 'Germany',
                    'capacity': '2,000 kg/month',
                    'rating': 4.8,
                    'certifications': ['ISO 9001', 'IATF 16949', 'Clean Room Class 1000'],
                    'quality_score': 95
                }
            ]
        },
        'consumers': [
            {'name': 'Infineon', 'location': 'Germany', 'annual_volume': '10,000 kg', 'rating': 4.8, 'quality_score': 96, 'certifications': ['ISO 9001', 'IATF 16949', 'ISO 14001', 'Clean Room Class 1000']},
            {'name': 'Wolfspeed', 'location': 'USA', 'annual_volume': '8,000 kg', 'rating': 4.7, 'quality_score': 94, 'certifications': ['ISO 9001', 'IATF 16949', 'Clean Room Class 1000']}
        ]
    },

    # 11. Heterogeneous Integration
    {
        'component': 'Reworkable Edge Seal',
        'use_case': 'Chiplet-to-substrate sealing in heterogeneous packages',
        'sector': 'Advanced Packaging',
        'rationale': 'Precision dispensable edge seal with rework capability. Provides hermetic protection while allowing chiplet replacement in high-value compute packages.',
        'requirements': {
            'dispensing_width': {'min': 50, 'max': 200, 'unit': 'µm'},
            'cure_shrinkage': {'max': 0.5, 'unit': '%'},
            'moisture_permeability': {'max': 0.02, 'unit': 'g/m²·24h'},
            'adhesion_strength': {'min': 12, 'unit': 'MPa'},
            'rework_temp': {'value': 200, 'tolerance': 10, 'unit': '°C'},
            'gap_filling': {'max': 75, 'unit': 'µm'},
            'ionic_content': {'max': 10, 'unit': 'ppm'}
        },
        'sustainability_metrics': {
            'halogen_content': {'value': '<100', 'unit': 'ppm'},
            'voc_emissions': {'value': '<30', 'unit': 'g/L'},
            'carbon_footprint': {'value': 2.4, 'unit': 'kgCO2/kg'},
            'recyclability': {'rating': 'EU Class 2', 'separable': True},
            'material_recovery': {'value': 80, 'unit': '%'}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Henkel Advanced Integration', 'location': 'USA', 'lead_time': '3-4 weeks', 'certifications': ['ISO 9001', 'Clean Room Class 100']}
            ],
            'manufacturing_sites': [
                {
                    'location': 'USA',
                    'capacity': '1,000 kg/month',
                    'rating': 4.6,
                    'certifications': ['ISO 9001', 'Clean Room Class 100'],
                    'quality_score': 93
                }
            ]
        },
        'consumers': [
            {'name': 'AMD', 'location': 'USA', 'annual_volume': '5,000 kg', 'rating': 4.7, 'quality_score': 94, 'certifications': ['ISO 9001', 'ISO 14001', 'Clean Room Class 100']},
            {'name': 'Intel', 'location': 'USA', 'annual_volume': '6,000 kg', 'rating': 4.8, 'quality_score': 95, 'certifications': ['ISO 9001', 'IATF 16949', 'ISO 14001', 'Clean Room Class 100']}
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
            material_type = DEMO_PARSED_ENTITIES['material_type']
            material_html = render_chip(material_type)
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
        
        # Regulatory requirements
        with col2:
            st.markdown("<p style='margin-bottom:0.5em'><strong>Regulatory Requirements</strong></p>", unsafe_allow_html=True)
            reg_html = ''.join(render_chip(reg) for reg in DEMO_PARSED_ENTITIES['regulatory_requirements'])
            st.markdown(f"<div style='line-height:2.2'>{reg_html}</div>", unsafe_allow_html=True)
        
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
        'Medical Devices & Wearables': [
            '3M Healthcare', 'Medtronic', 'Johnson & Johnson Medical',
            'Abbott Laboratories', 'Dexcom', 'Insulet Corporation',
            'iRhythm Technologies', 'Masimo Corporation', 'BD Medical', 'Smith & Nephew'
        ],
        'Medical Adhesives Manufacturing': [
            'Henkel Healthcare', 'H.B. Fuller', 'Avery Dennison Medical',
            'Scapa Healthcare', 'Berry Global', 'Polymer Science Inc',
            'Adhezion Biomedical', 'Vancive Medical Technologies', 'Tesa Medical', 'Mactac Medical'
        ],
        'Medical Materials & Components': [
            'DuPont Healthcare', 'BASF Medical Solutions', 'Eastman Medical',
            'Covestro Medical', 'DSM Biomedical', 'Celanese Medical',
            'Lubrizol Life Science', 'Evonik Health Care', 'Arkema Medical', 'Solvay Healthcare'
        ],
        'Medical Contract Manufacturing': [
            'Flex Medical', 'Jabil Healthcare', 'Integer Holdings',
            'West Pharmaceutical', 'Phillips-Medisize', 'Gerresheimer Medical',
            'Nemera', 'Celestica Health', 'Plexus Medical', 'Sanmina Medical'
        ],
        'Medical Testing & Certification': [
            'TÜV SÜD Medical', 'SGS Life Sciences', 'Eurofins Medical',
            'UL Healthcare', 'BSI Medical', 'DEKRA Medical',
            'Intertek Medical', 'DNV GL Healthcare', 'LNE/G-MED', 'NSAI Medical'
        ],
        'Medical Research & Innovation': [
            'Mayo Clinic Labs', 'Cleveland Clinic Innovations', 'Johns Hopkins MedTech',
            'Stanford Biodesign', 'MIT Medical', 'Harvard Medical Innovation',
            'Fraunhofer Medical', 'Imperial College Healthcare', 'CSIRO Health', 'Karolinska Institutet'
        ],
        'Medical Regulatory Bodies': [
            'FDA CDRH', 'EMA Medical Devices', 'MHRA Devices',
            'Health Canada Medical Devices', 'TGA Medical Devices', 'PMDA Japan',
            'BfArM', 'ANVISA Medical', 'NMPA Medical', 'Saudi FDA Medical'
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
    st.markdown("### Here's what Xtrium found...")
    
    # Render each application with a delay
    for i, app in enumerate(DEMO_APPLICATIONS):
        # Add delay for all but the first item
        if i > 0:
            time.sleep(0.5)
            
        with st.expander(app['component']):
            render_application_details(app)

def render_report_adhesives2(query: Optional[str] = None) -> None:
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
    
    with st.expander("⁂ Key Factors Report"):
        # Material header with query context
        st.markdown("""
            <div style='{}'>
                <p style='color:#666666; text-transform:uppercase; letter-spacing:1px; font-size:0.8em; margin:0;'>Material Analysis</p>
                <h3 style='margin:0.2em 0; font-size:1.2em;'>{}</h3>
                <p style='color:#666666; font-size:0.9em; margin:0.2em 0;'>Properties analyzed for medical wearable applications</p>
            </div>
        """.format(
            STYLE_MATERIAL_HEADER,
            DEMO_PARSED_ENTITIES['material_type']
        ), unsafe_allow_html=True)
        
        # Create two rows of three columns each
        st.markdown("#### Biocompatibility & Safety")
        col1, col2, col3 = st.columns(3)
        
        # Row 1: Biocompatibility and Safety
        with col1:
            render_key_property_card(
                "Cytotoxicity",
                "ISO 10993-5 Compliant",
                "Meets medical device standards for cell compatibility and safety.",
                0.98,
                "https://www.iso.org/standard/36406.html"
            )
        
        with col2:
            render_key_property_card(
                "Skin Contact",
                "Non-irritating",
                "Extended wear testing shows no adverse skin reactions.",
                0.96,
                "https://www.fda.gov/medical-devices/biocompatibility-testing-medical-devices/use-international-standard-iso-10993-1"
            )
        
        with col3:
            render_key_property_card(
                "Bioburden Control",
                "Class 100K Clean Room",
                "Manufactured in controlled environment for medical safety.",
                0.95
            )
        
        # Row 2: Performance Properties
        st.markdown("#### Performance & Durability")
        col4, col5, col6 = st.columns(3)
        
        with col4:
            render_key_property_card(
                "Adhesion Strength",
                "2.5-3.5 N/inch",
                "Optimal balance of secure attachment and gentle removal.",
                0.97,
                "https://www.astm.org/f2258-05r15.html"
            )
        
        with col5:
            render_key_property_card(
                "Moisture Management",
                "800-1200 g/m²/24hr MVTR",
                "Allows skin breathability while maintaining adhesion.",
                0.94,
                "https://www.astm.org/e96_e96m-16.html"
            )
        
        with col6:
            render_key_property_card(
                "Wear Duration",
                "7-14 Days",
                "Extended wear capability for continuous monitoring.",
                0.96
            )
            
        # Row 3: Sustainability
        st.markdown("#### Sustainability & Circular Economy")
        col7, col8, col9 = st.columns(3)
        
        with col7:
            render_key_property_card(
                "Bio-based Content",
                "45-55%",
                "Significant renewable material content reducing fossil fuel dependency.",
                0.93,
                "https://www.biopreferred.gov/BioPreferred/faces/pages/ProductCategories.xhtml"
            )
        
        with col8:
            render_key_property_card(
                "Recyclability",
                "Class 2 Recyclable",
                "End-of-life material recovery supporting circular economy.",
                0.92
            )
        
        with col9:
            render_key_property_card(
                "Carbon Footprint",
                "< 2.5 kg CO2e/kg",
                "Lower environmental impact compared to traditional adhesives.",
                0.94,
                "https://www.epa.gov/climateleadership/scope-3-inventory-guidance"
            )
