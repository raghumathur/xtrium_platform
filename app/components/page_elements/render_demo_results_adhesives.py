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
MATERIALS_DB_PATH = os.path.join(CURRENT_DIR, 'assets', 'databases', 'materials_database_adhesives_medical.csv')
APPLICATIONS_DB_PATH = os.path.join(CURRENT_DIR, 'assets', 'databases', 'applications_database_adhesives_medical.csv')

# Read databases
def load_database():
    """Load materials and applications databases"""
    try:
        materials_df = pd.read_csv(MATERIALS_DB_PATH)
        applications_df = pd.read_csv(APPLICATIONS_DB_PATH)
        return materials_df, applications_df
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return None, None

# Load data
materials_df, applications_df = load_database()

# Demo data structures
DEMO_PARSED_ENTITIES = {
    'material_type': 'adhesive formulation',
    'context_filters': ['biocompatible', 'skin-safe', 'moisture-resistant', 'circular'],
    'application_focus': ['medical wearables', 'flexible electronics'],
    'regulatory_requirements': ['FDA', 'EU MDR'],
    'material_insights': {
        'title': 'Material Insights',
        'subtitle': 'Properties analyzed in context of medical wearables and skin contact applications',
        'key_factors': [
            {
                'category': 'Biocompatibility',
                'properties': [
                    {'name': 'Cytotoxicity', 'value': 'ISO 10993-5 compliant'},
                    {'name': 'Skin Sensitization', 'value': 'Non-sensitizing'},
                    {'name': 'Dermal Irritation', 'value': 'Non-irritating'}
                ]
            },
            {
                'category': 'Physical Properties',
                'properties': [
                    {'name': 'Adhesion Strength', 'value': '2.5-3.5 N/inch'},
                    {'name': 'MVTR', 'value': '800-1200 g/m²/24hr'},
                    {'name': 'Wear Time', 'value': '7-14 days'}
                ]
            },
            {
                'category': 'Sustainability',
                'properties': [
                    {'name': 'Recyclability', 'value': 'Class 2 recyclable'},
                    {'name': 'Bio-based Content', 'value': '45-55%'},
                    {'name': 'Carbon Footprint', 'value': '< 2.5 kg CO2e/kg'}
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
            'value': 'adhesive formulation',
            'confidence': 0.99
        },
        {
            'node': 'CONTEXT',
            'children': [
                {
                    'node': 'REQUIREMENT',
                    'value': 'high-performance',
                    'confidence': 0.98
                },
                {
                    'node': 'REQUIREMENT',
                    'value': 'sustainable',
                    'confidence': 0.98
                }
            ]
        },
        {
            'node': 'REQUIREMENTS',
            'children': [
                {
                    'node': 'PROPERTY',
                    'value': 'biocompatible',
                    'confidence': 0.99
                },
                {
                    'node': 'PROPERTY',
                    'value': 'moisture-resistant',
                    'confidence': 0.97
                },
                {
                    'node': 'PROPERTY',
                    'value': 'sustainable',
                    'confidence': 0.95
                },
                {
                    'node': 'PROPERTY',
                    'value': 'skin-safe',
                    'confidence': 0.98
                }
            ]
        },
        {
            'node': 'DOMAINS',
            'children': [
                {
                    'node': 'INDUSTRY',
                    'value': 'medical devices',
                    'confidence': 0.99
                },
                {
                    'node': 'APPLICATION',
                    'value': 'wearable devices',
                    'confidence': 0.98
                }
            ]
        },
        {
            'node': 'COMPLIANCE',
            'children': [
                {
                    'node': 'REGULATION',
                    'value': 'FDA',
                    'confidence': 0.99
                },
                {
                    'node': 'REGULATION',
                    'value': 'EU MDR',
                    'confidence': 0.98
                }
            ]
        }
    ]
}

DEMO_APPLICATIONS = [
    # 1. Advanced Wound Care
    {
        'component': 'Diabetic Ulcer Monitoring Patch',
        'use_case': 'Smart pH and exudate monitoring for chronic diabetic foot ulcers',
        'sector': 'Critical Wound Management',
        'rationale': 'Hydrogel-based smart adhesive with embedded silver nanoparticles and pH-sensitive microsensors. Provides real-time infection monitoring and moisture management for diabetic foot ulcers, with proven 72% faster healing rates.',
        'source_url': 'https://www.smith-nephew.com/professional/products/advanced-wound-management/',
        'requirements': {
            'biocompatibility': {'standard': 'ISO 10993-10', 'level': 'non-sensitizing'},
            'antimicrobial': {'effectiveness': '99.9%', 'test_method': 'JIS Z 2801'},
            'moisture_management': {'mvtr': '1000-1200', 'unit': 'g/m²/24hr'},
            'wear_time': {'duration': '7', 'unit': 'days'}
        },
        'sustainability_data': {
            'recyclability': 0.82,
            'energy_efficiency': 0.90,
            'waste_reduction': 0.85,
            'carbon_footprint': {'value': 2.8, 'unit': 'kgCO2/kg'},
            'circular_materials': {'percentage': 70, 'recyclable_components': ['electronics housing', 'adhesive backing']}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Avery Dennison Medical', 'location': 'Ireland', 'lead_time': '2-3 weeks', 'certifications': ['ISO 13485', 'EU MDR']},
                {'name': 'Scapa Healthcare', 'location': 'UK', 'lead_time': '3-4 weeks', 'certifications': ['ISO 13485', 'FDA GMP']}
            ],
            'processing_capabilities': ['clean room manufacturing', 'precision coating', 'die cutting'],
            'regional_availability': ['North America', 'Europe', 'Asia Pacific'],
            'typical_lead_time': '2-4 weeks'
        },
        'consumers': [
            {
                'name': 'iRhythm Technologies',
                'location': 'USA',
                'annual_volume': '300,000 units',
                'rating': 4.8,
                'certifications': ['ISO 13485', 'FDA Class II', 'EU MDR'],
                'quality_score': 96
            },
            {
                'name': 'Preventice Solutions',
                'location': 'USA',
                'annual_volume': '250,000 units',
                'rating': 4.7,
                'certifications': ['ISO 13485', 'FDA Class II'],
                'quality_score': 94
            }
        ]
    },

    # 2. Smart Insulin Pump Adhesive
    {
        'component': 'Closed-Loop Insulin Pump Fixation',
        'use_case': '14-day waterproof attachment for artificial pancreas systems',
        'sector': 'Critical Drug Delivery',
        'rationale': 'Micropatterned silicone adhesive with moisture-wicking channels and skin-strain distribution matrix. Enables 14-day continuous wear for closed-loop insulin systems with 99.7% device retention rate and zero skin reactions in clinical trials.', 
        'source_url': 'https://www.insulet.com/omnipod',
        'requirements': {
            'biocompatibility': {'standard': 'ISO 10993-10', 'level': 'hypoallergenic'},
            'wear_duration': {'min': 3, 'unit': 'days'},
            'moisture_resistance': {'rating': 'excellent', 'test_method': 'ASTM D3330'},
            'skin_adhesion': {'strength': '3.0-3.5', 'unit': 'N/25mm'}
        },
        'sustainability_data': {
            'recyclability': 0.88,
            'energy_efficiency': 0.93,
            'waste_reduction': 0.87,
            'carbon_footprint': {'value': 2.5, 'unit': 'kgCO2/kg'},
            'circular_materials': {'percentage': 75, 'recyclable_components': ['pump housing', 'adhesive liner']}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Henkel Healthcare', 'location': 'Germany', 'lead_time': '2-3 weeks', 'certifications': ['ISO 13485', 'EU MDR']},
                {'name': 'H.B. Fuller', 'location': 'USA', 'lead_time': '3-4 weeks', 'certifications': ['ISO 13485', 'FDA GMP']}
            ],
            'processing_capabilities': ['clean room manufacturing', 'precision coating', 'die cutting'],
            'regional_availability': ['North America', 'Europe', 'Asia Pacific'],
            'typical_lead_time': '2-4 weeks'
        },
        'consumers': [
            {
                'name': 'Insulet Corporation',
                'location': 'USA',
                'annual_volume': '400,000 units',
                'rating': 4.9,
                'certifications': ['ISO 13485', 'FDA Class III', 'EU MDR'],
                'quality_score': 98
            },
            {
                'name': 'Medtronic Diabetes',
                'location': 'USA',
                'annual_volume': '350,000 units',
                'rating': 4.8,
                'certifications': ['ISO 13485', 'FDA Class III', 'EU MDR'],
                'quality_score': 97
            }
        ]
    },

    # 3. ECG Monitoring Patch
    {
        'component': 'Multi-Lead ECG Monitoring Array',
        'use_case': '12-lead ECG monitoring with motion artifact compensation',
        'sector': 'Cardiac Diagnostics',
        'rationale': 'Stretchable conductive adhesive with pressure-sensitive microchannels and ionic conductivity. Maintains signal quality during movement with 98% accuracy compared to hospital ECGs, while reducing motion artifacts by 86%.',
        'source_url': 'https://www.smith-nephew.com/professional/products/advanced-wound-management/',
        'requirements': {
            'biocompatibility': {'standard': 'ISO 10993-6', 'level': 'bioactive'},
            'wear_duration': {'min': 7, 'unit': 'days'},
            'moisture_resistance': {'rating': 'moderate', 'test_method': 'ASTM F2258'},
            'antimicrobial': {'type': 'silver ions', 'efficacy': '99.9%'}
        },
        'sustainability_data': {
            'recyclability': 0.80,
            'energy_efficiency': 0.88,
            'waste_reduction': 0.85,
            'carbon_footprint': {'value': 3.0, 'unit': 'kgCO2/kg'},
            'circular_materials': {'percentage': 60, 'recyclable_components': ['outer packaging', 'protective films']}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Smith & Nephew', 'location': 'UK', 'lead_time': '2-3 weeks', 'certifications': ['ISO 13485', 'EU MDR']},
                {'name': 'Mölnlycke Health Care', 'location': 'Sweden', 'lead_time': '2-4 weeks', 'certifications': ['ISO 13485', 'FDA GMP']}
            ],
            'processing_capabilities': ['clean room manufacturing', 'antimicrobial coating', 'sterilization'],
            'regional_availability': ['North America', 'Europe', 'Asia Pacific'],
            'typical_lead_time': '2-3 weeks'
        },
        'consumers': [
            {
                'name': 'Mayo Clinic',
                'location': 'USA',
                'annual_volume': '200,000 units',
                'rating': 4.9,
                'certifications': ['JCI Accredited'],
                'quality_score': 98
            },
            {
                'name': 'Cleveland Clinic',
                'location': 'USA',
                'annual_volume': '180,000 units',
                'rating': 4.8,
                'certifications': ['JCI Accredited'],
                'quality_score': 97
            }
        ]
    },

    # 4. Transdermal Drug Delivery Patch
    {
        'component': 'Nanoporous Drug-Eluting Matrix',
        'use_case': 'Precision-controlled CNS medication delivery through skin barrier',
        'sector': 'Advanced Therapeutics',
        'rationale': 'Nanostructured polymer matrix with programmable drug-release kinetics and crystallization inhibition. Achieves 94% bioavailability for CNS therapeutics with plasma concentration variance under 8%, enabling precise dosing for Parkinsons and epilepsy medications.',
        'source_url': 'https://www.3m.com/3M/en_US/drug-delivery-systems-us/',
        'requirements': {
            'biocompatibility': {'standard': 'ISO 10993-5,10', 'level': 'non-irritating'},
            'wear_duration': {'min': 7, 'unit': 'days'},
            'drug_compatibility': {'test_method': 'USP <87>', 'stability': '24 months'},
            'permeation_rate': {'range': '2-5', 'unit': 'µg/cm²/hr'}
        },
        'sustainability_data': {
            'recyclability': 0.75,
            'energy_efficiency': 0.89,
            'waste_reduction': 0.82,
            'carbon_footprint': {'value': 3.5, 'unit': 'kgCO2/kg'},
            'circular_materials': {'percentage': 55, 'recyclable_components': ['backing', 'pouch']}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': '3M Drug Delivery Systems', 'location': 'USA', 'lead_time': '3-4 weeks', 'certifications': ['ISO 13485', 'FDA GMP']},
                {'name': 'Mylan Technologies', 'location': 'USA', 'lead_time': '3-5 weeks', 'certifications': ['ISO 13485', 'FDA GMP']}
            ],
            'processing_capabilities': ['clean room manufacturing', 'drug incorporation', 'sterilization'],
            'regional_availability': ['North America', 'Europe'],
            'typical_lead_time': '3-5 weeks'
        },
        'consumers': [
            {
                'name': 'Novartis Pharmaceuticals',
                'location': 'Switzerland',
                'annual_volume': '1,000,000 units',
                'rating': 4.9,
                'certifications': ['ISO 13485', 'FDA GMP', 'EMA GMP'],
                'quality_score': 98
            },
            {
                'name': 'GSK',
                'location': 'UK',
                'annual_volume': '800,000 units',
                'rating': 4.8,
                'certifications': ['ISO 13485', 'FDA GMP', 'EMA GMP'],
                'quality_score': 97
            }
        ]
    },

    # 5. Biosensor Array
    {
        'component': 'Biosensor Adhesive Matrix',
        'use_case': 'Multi-parameter physiological monitoring',
        'sector': 'Medical Diagnostics',
        'rationale': 'Conductive adhesive matrix enabling multiple sensor integration while maintaining skin comfort.',
        'source_url': 'https://www.parker.com/portal/site/PARKER/medical-solutions/',
        'requirements': {
            'biocompatibility': {'standard': 'ISO 10993-5', 'level': 'non-cytotoxic'},
            'electrical_conductivity': {'range': '1-10', 'unit': 'S/cm'},
            'wear_duration': {'min': 5, 'unit': 'days'},
            'sensor_compatibility': {'types': ['electrochemical', 'impedance', 'optical']}
        },
        'sustainability_data': {
            'recyclability': 0.78,
            'energy_efficiency': 0.91,
            'waste_reduction': 0.84,
            'carbon_footprint': {'value': 3.1, 'unit': 'kgCO2/kg'},
            'circular_materials': {'percentage': 62, 'recyclable_components': ['electronics', 'adhesive matrix']}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Parker Medical', 'location': 'USA', 'lead_time': '3-4 weeks', 'certifications': ['ISO 13485', 'FDA GMP']},
                {'name': 'Heraeus Medical', 'location': 'Germany', 'lead_time': '3-5 weeks', 'certifications': ['ISO 13485', 'EU MDR']}
            ],
            'processing_capabilities': ['clean room manufacturing', 'sensor integration', 'sterilization'],
            'regional_availability': ['North America', 'Europe', 'Asia Pacific'],
            'typical_lead_time': '3-4 weeks'
        },
        'consumers': [
            {
                'name': 'Philips Healthcare',
                'location': 'Netherlands',
                'annual_volume': '150,000 units',
                'rating': 4.8,
                'certifications': ['ISO 13485', 'FDA Class II', 'EU MDR'],
                'quality_score': 96
            },
            {
                'name': 'GE Healthcare',
                'location': 'USA',
                'annual_volume': '120,000 units',
                'rating': 4.7,
                'certifications': ['ISO 13485', 'FDA Class II', 'EU MDR'],
                'quality_score': 95
            }
        ]
    },

    # 6. Smart Bandage
    {
        'component': 'Smart Bandage Adhesive',
        'use_case': 'Interactive wound healing monitoring',
        'sector': 'Medical Devices',
        'rationale': 'pH-sensitive adhesive with integrated sensors for wound healing monitoring.',
        'source_url': 'https://www.molnlycke.com/products-solutions/smart-wound-care/',
        'requirements': {
            'biocompatibility': {'standard': 'ISO 10993-10', 'level': 'non-sensitizing'},
            'pH_sensitivity': {'range': '5-9', 'accuracy': '±0.2'},
            'wear_duration': {'min': 4, 'unit': 'days'},
            'moisture_handling': {'MVTR': '800-1200', 'unit': 'g/m²/24hr'}
        },
        'sustainability_data': {
            'recyclability': 0.83,
            'energy_efficiency': 0.90,
            'waste_reduction': 0.86,
            'carbon_footprint': {'value': 2.9, 'unit': 'kgCO2/kg'},
            'circular_materials': {'percentage': 68, 'recyclable_components': ['sensors', 'backing material']}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Mölnlycke Health Care', 'location': 'Sweden', 'lead_time': '2-3 weeks', 'certifications': ['ISO 13485', 'EU MDR']},
                {'name': 'ConvaTec', 'location': 'UK', 'lead_time': '2-4 weeks', 'certifications': ['ISO 13485', 'FDA GMP']}
            ],
            'processing_capabilities': ['clean room manufacturing', 'sensor integration', 'sterilization'],
            'regional_availability': ['North America', 'Europe'],
            'typical_lead_time': '2-4 weeks'
        },
        'consumers': [
            {
                'name': 'Wound Care Centers of America',
                'location': 'USA',
                'annual_volume': '100,000 units',
                'rating': 4.7,
                'certifications': ['JCI Accredited'],
                'quality_score': 94
            },
            {
                'name': 'European Wound Management Association',
                'location': 'Europe',
                'annual_volume': '90,000 units',
                'rating': 4.8,
                'certifications': ['EU Healthcare Provider'],
                'quality_score': 95
            }
        ]
    },

    # 7. Neurostimulation Electrode
    {
        'component': 'Neuro Electrode Adhesive',
        'use_case': 'Long-term neural monitoring and stimulation',
        'sector': 'Medical Devices',
        'rationale': 'Conductive adhesive for secure electrode placement with minimal impedance.',
        'source_url': 'https://www.natus.com/products-services/neuro/',
        'requirements': {
            'biocompatibility': {'standard': 'ISO 10993-5,10', 'level': 'non-irritating'},
            'electrical_resistance': {'max': '100', 'unit': 'Ω'},
            'wear_duration': {'min': 2, 'unit': 'weeks'},
            'signal_quality': {'SNR': '>40', 'unit': 'dB'}
        },
        'sustainability_data': {
            'recyclability': 0.76,
            'energy_efficiency': 0.88,
            'waste_reduction': 0.83,
            'carbon_footprint': {'value': 3.3, 'unit': 'kgCO2/kg'},
            'circular_materials': {'percentage': 58, 'recyclable_components': ['electrode base', 'conductive elements']}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Natus Medical', 'location': 'USA', 'lead_time': '2-3 weeks', 'certifications': ['ISO 13485', 'FDA GMP']},
                {'name': 'Nihon Kohden', 'location': 'Japan', 'lead_time': '3-4 weeks', 'certifications': ['ISO 13485', 'PMDA']}
            ],
            'processing_capabilities': ['clean room manufacturing', 'electrode coating', 'sterilization'],
            'regional_availability': ['North America', 'Europe', 'Asia Pacific'],
            'typical_lead_time': '2-4 weeks'
        },
        'consumers': [
            {
                'name': 'Medtronic Neuromodulation',
                'location': 'USA',
                'annual_volume': '200,000 units',
                'rating': 4.9,
                'certifications': ['ISO 13485', 'FDA Class III', 'EU MDR'],
                'quality_score': 98
            },
            {
                'name': 'Boston Scientific Neuromodulation',
                'location': 'USA',
                'annual_volume': '180,000 units',
                'rating': 4.8,
                'certifications': ['ISO 13485', 'FDA Class III', 'EU MDR'],
                'quality_score': 97
            }
        ]
    },

    # 8. Ostomy Seal
    {
        'component': 'Ostomy Barrier Adhesive',
        'use_case': 'Skin protection and leak prevention',
        'sector': 'Medical Devices',
        'rationale': 'Protective adhesive barrier with enhanced skin protection and leakage prevention.',
        'source_url': 'https://www.coloplast.com/ostomy-care/',
        'requirements': {
            'biocompatibility': {'standard': 'ISO 10993-10', 'level': 'skin protective'},
            'wear_duration': {'min': 3, 'unit': 'days'},
            'erosion_resistance': {'rating': 'excellent', 'test_method': 'ASTM F2258'},
            'barrier_properties': {'WVTR': '<4', 'unit': 'g/m²/24hr'}
        },
        'sustainability_data': {
            'recyclability': 0.81,
            'energy_efficiency': 0.89,
            'waste_reduction': 0.85,
            'carbon_footprint': {'value': 2.7, 'unit': 'kgCO2/kg'},
            'circular_materials': {'percentage': 64, 'recyclable_components': ['barrier film', 'protective layer']}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'Coloplast', 'location': 'Denmark', 'lead_time': '2-3 weeks', 'certifications': ['ISO 13485', 'EU MDR']},
                {'name': 'ConvaTec', 'location': 'UK', 'lead_time': '2-4 weeks', 'certifications': ['ISO 13485', 'FDA GMP']}
            ],
            'processing_capabilities': ['clean room manufacturing', 'barrier coating', 'die cutting'],
            'regional_availability': ['North America', 'Europe', 'Asia Pacific'],
            'typical_lead_time': '2-3 weeks'
        },
        'consumers': [
            {
                'name': 'UOAA Affiliated Centers',
                'location': 'USA',
                'annual_volume': '300,000 units',
                'rating': 4.8,
                'certifications': ['Healthcare Provider Certified'],
                'quality_score': 96
            },
            {
                'name': 'European Ostomy Association',
                'location': 'Europe',
                'annual_volume': '250,000 units',
                'rating': 4.7,
                'certifications': ['EU Healthcare Provider'],
                'quality_score': 95
            }
        ]
    },

    # 9. Surgical Drape
    {
        'component': 'Surgical Adhesive Drape',
        'use_case': 'Sterile field maintenance during surgery',
        'sector': 'Medical Devices',
        'rationale': 'Antimicrobial adhesive drape for maintaining sterile surgical field.',
        'source_url': 'https://www.3m.com/3M/en_US/medical-us/medical-solutions/',
        'requirements': {
            'biocompatibility': {'standard': 'ISO 10993-5', 'level': 'non-cytotoxic'},
            'antimicrobial': {'efficacy': '99.99%', 'duration': '24 hours'},
            'tensile_strength': {'min': '15', 'unit': 'N/25mm'},
            'sterilization': {'method': 'EtO', 'validation': 'ISO 11135'}
        },
        'sustainability_data': {
            'recyclability': 0.79,
            'energy_efficiency': 0.91,
            'waste_reduction': 0.87,
            'carbon_footprint': {'value': 2.6, 'unit': 'kgCO2/kg'},
            'circular_materials': {'percentage': 66, 'recyclable_components': ['drape material', 'packaging']}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': '3M Medical Solutions', 'location': 'USA', 'lead_time': '2-3 weeks', 'certifications': ['ISO 13485', 'FDA GMP']},
                {'name': 'Paul Hartmann AG', 'location': 'Germany', 'lead_time': '2-4 weeks', 'certifications': ['ISO 13485', 'EU MDR']}
            ],
            'processing_capabilities': ['clean room manufacturing', 'antimicrobial coating', 'sterilization'],
            'regional_availability': ['North America', 'Europe', 'Asia Pacific'],
            'typical_lead_time': '2-3 weeks'
        },
        'consumers': [
            {
                'name': 'HCA Healthcare',
                'location': 'USA',
                'annual_volume': '1,000,000 units',
                'rating': 4.8,
                'certifications': ['JCI Accredited'],
                'quality_score': 96
            },
            {
                'name': 'Asklepios Kliniken',
                'location': 'Germany',
                'annual_volume': '800,000 units',
                'rating': 4.7,
                'certifications': ['EU Healthcare Provider'],
                'quality_score': 95
            }
        ]
    },

    # 10. Continuous Glucose Monitoring Patch
    {
        'component': 'CGM Adhesive Patch',
        'use_case': 'Long-term wear glucose monitoring sensor attachment',
        'sector': 'Medical Wearables',
        'rationale': 'Biocompatible adhesive formulation optimized for extended skin contact while maintaining sensor accuracy. Meets FDA Class III and EU MDR requirements.',
        'source_url': 'https://www.medisiltech.com/wearable-adhesives/cgm-patch',
        'requirements': {
            'biocompatibility': {'standard': 'ISO 10993-10', 'level': 'non-sensitizing'},
            'wear_duration': {'min': 14, 'unit': 'days'},
            'moisture_resistance': {'rating': 'excellent', 'test_method': 'ASTM D3330'},
            'skin_adhesion': {'strength': '2.5-3.0', 'unit': 'N/25mm'}
        },
        'sustainability_data': {
            'recyclability': 0.85,
            'energy_efficiency': 0.92,
            'waste_reduction': 0.88,
            'carbon_footprint': {'value': 3.2, 'unit': 'kgCO2/kg'},
            'circular_materials': {'percentage': 65, 'recyclable_components': ['backing film', 'release liner']}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'MediSil Technologies', 'location': 'USA', 'lead_time': '2-3 weeks', 'certifications': ['ISO 13485', 'FDA GMP']},
                {'name': 'BioTech Adhesives', 'location': 'Germany', 'lead_time': '3-4 weeks', 'certifications': ['ISO 13485', 'EU MDR']}
            ],
            'processing_capabilities': ['clean room manufacturing', 'precision coating', 'die cutting'],
            'regional_availability': ['North America', 'Europe', 'Asia Pacific'],
            'typical_lead_time': '2-4 weeks'
        },
        'consumers': [
            {
                'name': 'Dexcom',
                'location': 'USA',
                'annual_volume': '500,000 units',
                'rating': 4.9,
                'certifications': ['ISO 13485', 'FDA Class III', 'EU MDR'],
                'quality_score': 98
            },
            {
                'name': 'Abbott Diabetes Care',
                'location': 'USA',
                'annual_volume': '450,000 units',
                'rating': 4.8,
                'certifications': ['ISO 13485', 'FDA Class III', 'EU MDR'],
                'quality_score': 97
            },
            {
                'name': 'Medtronic',
                'location': 'Ireland',
                'annual_volume': '300,000 units',
                'rating': 4.9,
                'certifications': ['ISO 13485', 'FDA Class III', 'EU MDR', 'MDSAP'],
                'quality_score': 99
            }
        ]
    },
    # 2. Smart Wound Dressing
    {
        'component': 'Smart Wound Care Patch',
        'use_case': 'Advanced wound monitoring with integrated sensors',
        'sector': 'Medical Wearables',
        'rationale': 'Biocompatible adhesive system that maintains wound moisture while allowing sensor functionality. Compliant with wound care device regulations.',
        'source_url': 'https://www.medisiltech.com/wearable-adhesives/wound-care',
        'requirements': {
            'biocompatibility': {'standard': 'ISO 10993-10', 'level': 'non-sensitizing'},
            'moisture_vapor_transmission': {'rate': '2000-2500', 'unit': 'g/m²/24h'},
            'bacterial_barrier': {'standard': 'ASTM F1608', 'rating': 'excellent'},
            'wear_duration': {'min': 7, 'unit': 'days'}
        },
        'sustainability_data': {
            'recyclability': 0.80,
            'energy_efficiency': 0.90,
            'waste_reduction': 0.85,
            'carbon_footprint': {'value': 2.8, 'unit': 'kgCO2/kg'},
            'circular_materials': {'percentage': 60, 'recyclable_components': ['outer packaging', 'sensor module']}
        },
        'supply_chain_data': {
            'manufacturers': [
                {'name': 'WoundTech Solutions', 'location': 'USA', 'lead_time': '2-3 weeks', 'certifications': ['ISO 13485', 'FDA GMP']},
                {'name': 'MediPatch Innovations', 'location': 'Switzerland', 'lead_time': '3-4 weeks', 'certifications': ['ISO 13485', 'EU MDR']}
            ],
            'processing_capabilities': ['clean room manufacturing', 'sensor integration', 'sterile packaging'],
            'regional_availability': ['North America', 'Europe', 'Asia Pacific'],
            'typical_lead_time': '2-4 weeks'
        },
        'consumers': [
            {
                'name': 'Smith & Nephew',
                'location': 'UK',
                'annual_volume': '300,000 units',
                'rating': 4.8,
                'certifications': ['ISO 13485', 'FDA Class II', 'EU MDR'],
                'quality_score': 97
            },
            {
                'name': 'Mölnlycke Health Care',
                'location': 'Sweden',
                'annual_volume': '250,000 units',
                'rating': 4.9,
                'certifications': ['ISO 13485', 'FDA Class II', 'EU MDR'],
                'quality_score': 98
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
    
    # Applications header
    st.markdown(f"""
        <div style='{STYLE_SECTION_HEADER}'>
            <h2>📊 Medical Applications & Use Cases</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Use CSV data if available, otherwise fall back to demo data
    if applications_df is not None and not applications_df.empty:
        # Convert each row to our application data structure
        for idx, row in applications_df.iterrows():
            # Create application data structure from CSV row
            app_data = {
                'component': row['Use-case'],
                'use_case': row['Commercial name'],
                'sector': row['Industry'],
                'required_properties': {
                    'Adhesion Strength': f"{row['Adhesion Strength (N/inch)']} N/inch" if 'Adhesion Strength (N/inch)' in row else 'N/A',
                    'MVTR': f"{row['MVTR (g/m²/24hr)']} g/m²/24hr" if 'MVTR (g/m²/24hr)' in row else 'N/A',
                    'Wear Time': f"{row['Wear Time (days)']} days" if 'Wear Time (days)' in row else 'N/A'
                },
                'sustainability': {
                    'bio_based_content': row['Bio-based Content (%)'] if 'Bio-based Content (%)' in row else 0,
                    'carbon_footprint': {'value': row['Carbon Footprint (kg CO2e/kg)'] if 'Carbon Footprint (kg CO2e/kg)' in row else 0, 'unit': 'kgCO2/kg'},
                    'circular_materials': {'percentage': row['Bio-based Content (%)'] if 'Bio-based Content (%)' in row else 0, 
                                        'recyclable_components': ['outer packaging', 'protective liners']}
                },
                'supply_chain_data': {
                    'manufacturers': [
                        {'name': f"Medical Adhesives Corp - {row['Type']}", 'location': 'USA', 'lead_time': '2-3 weeks', 'certifications': ['ISO 13485', 'FDA GMP']}
                    ],
                    'processing_capabilities': ['clean room manufacturing', 'precision coating', 'die cutting'],
                    'regional_availability': ['North America', 'Europe', 'Asia Pacific'],
                    'typical_lead_time': '2-4 weeks'
                },
                'consumers': [
                    {'name': row['Industry'] + ' Leaders', 'location': 'Global', 'annual_volume': '500,000 units', 
                    'rating': 4.9, 'certifications': ['ISO 13485', 'FDA Class II'], 'quality_score': 96}
                ]
            }
            # Add delay for all but the first item
            if idx > 0:
                time.sleep(0.25)
                
            with st.expander(app_data['component'], expanded=(idx == 0)):
                render_application_details(app_data)
    else:
        # Fall back to demo data
        for idx, app in enumerate(DEMO_APPLICATIONS):
            # Add delay for all but the first item
            if idx > 0:
                time.sleep(0.5)
                
            with st.expander(app['component'], expanded=(idx == 0)):
                render_application_details(app)

def render_report_adhesives(query: Optional[str] = None) -> None:
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
        material_type = DEMO_PARSED_ENTITIES['material_type']
        st.error("Unable to load material database. Using demo data instead.")
    else:
        # Use actual material data
        material_type = "medical adhesive formulation"
    
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
            material_type
        ), unsafe_allow_html=True)
        
        # Create two rows of three columns each
        st.markdown("#### Biocompatibility & Safety")
        col1, col2, col3 = st.columns(3)
        
        # Row 1: Biocompatibility and Safety
        # If we have materials data from CSV, use it
        if materials_df is not None and not materials_df.empty:
            # Use first row for demonstration purposes
            material_row = materials_df.iloc[0]
            
            cytotoxicity = material_row['Cytotoxicity'] if 'Cytotoxicity' in material_row else 'ISO 10993-5 Compliant'
            skin_irritation = material_row['Skin irritation'] if 'Skin irritation' in material_row else 'Non-irritating'
            biocompatibility = material_row['Biocompatibility'] if 'Biocompatibility' in material_row else 'Class 100K Clean Room'
            
            adhesion_strength = f"{material_row['Adhesion Strength (N/inch)']} N/inch" if 'Adhesion Strength (N/inch)' in material_row else '2.5-3.5 N/inch'
            mvtr = f"{material_row['MVTR (g/m²/24hr)']} g/m²/24hr" if 'MVTR (g/m²/24hr)' in material_row else '800-1200 g/m²/24hr'
            wear_time = f"{material_row['Wear Time (days)']} days" if 'Wear Time (days)' in material_row else '7-14 Days'
            
            bio_based = f"{material_row['Bio-based Content (%)']}%" if 'Bio-based Content (%)' in material_row else '45-55%'
            recyclability = material_row['Recyclability'] if 'Recyclability' in material_row else 'Class 2 Recyclable'
            carbon_footprint = f"< {material_row['Carbon Footprint (kg CO2e/kg)']} kg CO2e/kg" if 'Carbon Footprint (kg CO2e/kg)' in material_row else '< 2.5 kg CO2e/kg'
        else:
            # Fallback to demo data
            cytotoxicity = "ISO 10993-5 Compliant"
            skin_irritation = "Non-irritating"
            biocompatibility = "Class 100K Clean Room"
            
            adhesion_strength = "2.5-3.5 N/inch"
            mvtr = "800-1200 g/m²/24hr"
            wear_time = "7-14 Days"
            
            bio_based = "45-55%"
            recyclability = "Class 2 Recyclable"
            carbon_footprint = "< 2.5 kg CO2e/kg"
        
        with col1:
            render_key_property_card(
                "Cytotoxicity",
                cytotoxicity,
                "Meets medical device standards for cell compatibility and safety.",
                0.98,
                "https://www.iso.org/standard/36406.html"
            )
        
        with col2:
            render_key_property_card(
                "Skin Contact",
                skin_irritation,
                "Extended wear testing shows no adverse skin reactions.",
                0.96,
                "https://www.fda.gov/medical-devices/biocompatibility-testing-medical-devices/use-international-standard-iso-10993-1"
            )
        
        with col3:
            render_key_property_card(
                "Bioburden Control",
                biocompatibility,
                "Manufactured in controlled environment for medical safety.",
                0.95
            )
        
        # Row 2: Performance Properties
        st.markdown("#### Performance & Durability")
        col4, col5, col6 = st.columns(3)
        
        with col4:
            render_key_property_card(
                "Adhesion Strength",
                adhesion_strength,
                "Optimal balance of secure attachment and gentle removal.",
                0.97,
                "https://www.astm.org/f2258-05r15.html"
            )
        
        with col5:
            render_key_property_card(
                "Moisture Management",
                mvtr,
                "Allows skin breathability while maintaining adhesion.",
                0.94,
                "https://www.astm.org/e96_e96m-16.html"
            )
        
        with col6:
            render_key_property_card(
                "Wear Duration",
                wear_time,
                "Extended wear capability for continuous monitoring.",
                0.96
            )
            
        # Row 3: Sustainability
        st.markdown("#### Sustainability & Circular Economy")
        col7, col8, col9 = st.columns(3)
        
        with col7:
            render_key_property_card(
                "Bio-based Content",
                bio_based,
                "Significant renewable material content reducing fossil fuel dependency.",
                0.93,
                "https://www.biopreferred.gov/BioPreferred/faces/pages/ProductCategories.xhtml"
            )
        
        with col8:
            render_key_property_card(
                "Recyclability",
                recyclability,
                "End-of-life material recovery supporting circular economy.",
                0.92
            )
        
        with col9:
            render_key_property_card(
                "Carbon Footprint",
                carbon_footprint,
                "Lower environmental impact compared to traditional adhesives.",
                0.94,
                "https://www.epa.gov/climateleadership/scope-3-inventory-guidance"
            )
