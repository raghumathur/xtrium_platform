import pandas as pd
import json
import os
from typing import Dict, List, Any
import csv

# Import the DEMO_APPLICATIONS from render_results.py
from render_results import DEMO_APPLICATIONS

# Directory to save the CSV files
csv_dir = os.path.dirname(os.path.abspath(__file__))

# Add application_id to each application
for i, app in enumerate(DEMO_APPLICATIONS):
    app['application_id'] = i + 1  # 1-indexed IDs

# 1. Create applications.csv
applications_data = []
for app in DEMO_APPLICATIONS:
    applications_data.append({
        'application_id': app['application_id'],
        'component': app['component'],
        'use_case': app['use_case'],
        'sector': app['sector'],
        'rationale': app['rationale'],
        'source_url': app.get('source_url', '')  # Some entries might not have a source_url
    })

applications_df = pd.DataFrame(applications_data)
applications_df.to_csv(os.path.join(csv_dir, 'applications.csv'), index=False)

# 2. Create applications_requirements.csv
requirements_data = []
for app in DEMO_APPLICATIONS:
    app_id = app['application_id']
    requirements = app.get('requirements', {})
    
    # Flatten nested dictionaries in requirements
    flat_requirements = {'application_id': app_id}
    for key, value in requirements.items():
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                flat_requirements[f"{key}_{subkey}"] = subvalue
        else:
            flat_requirements[key] = value
    
    requirements_data.append(flat_requirements)

requirements_df = pd.DataFrame(requirements_data)
requirements_df.to_csv(os.path.join(csv_dir, 'applications_requirements.csv'), index=False)

# 3. Create sustainability.csv
sustainability_data = []
for app in DEMO_APPLICATIONS:
    app_id = app['application_id']
    sustainability = app.get('sustainability_data', {})
    
    # Flatten nested dictionaries in sustainability data
    flat_sustainability = {'application_id': app_id}
    for key, value in sustainability.items():
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                flat_sustainability[f"{key}_{subkey}"] = subvalue
        else:
            flat_sustainability[key] = value
    
    sustainability_data.append(flat_sustainability)

sustainability_df = pd.DataFrame(sustainability_data)
sustainability_df.to_csv(os.path.join(csv_dir, 'sustainability.csv'), index=False)

# 4. Create consumers.csv (merging consumers and supply chain data)
consumers_data = []

for app in DEMO_APPLICATIONS:
    app_id = app['application_id']
    
    # Process consumers
    for consumer in app.get('consumers', []):
        consumer_data = {
            'application_id': app_id,
            'entity_type': 'consumer',
            'name': consumer.get('name', ''),
            'location': consumer.get('location', ''),
            'volume': consumer.get('annual_volume', ''),
            'rating': consumer.get('rating', ''),
            'quality_score': consumer.get('quality_score', ''),
            'certifications': ','.join(consumer.get('certifications', [])),
            'lead_time': '',
            'typical_lead_time': ''
        }
        consumers_data.append(consumer_data)
    
    # Process manufacturers from supply chain data
    supply_chain = app.get('supply_chain_data', {})
    for manufacturer in supply_chain.get('manufacturers', []):
        manufacturer_data = {
            'application_id': app_id,
            'entity_type': 'manufacturer',
            'name': manufacturer.get('name', ''),
            'location': manufacturer.get('location', ''),
            'volume': '',  # Manufacturers don't have volume in the original data
            'rating': '',  # Manufacturers don't have ratings in the original data
            'quality_score': '',  # Manufacturers don't have quality scores in the original data
            'certifications': '',  # Manufacturers don't have certifications in the original data
            'lead_time': manufacturer.get('lead_time', ''),
            'typical_lead_time': supply_chain.get('typical_lead_time', '')
        }
        consumers_data.append(manufacturer_data)

consumers_df = pd.DataFrame(consumers_data)
consumers_df.to_csv(os.path.join(csv_dir, 'consumers.csv'), index=False)

# Add additional information to a README file to explain the structure
readme_content = """# CSV Data Files for Xtrium Platform

This directory contains CSV files extracted from the DEMO_APPLICATIONS data structure:

1. **applications.csv**: Basic information about each application including component, use case, sector, rationale, and source URL.
2. **applications_requirements.csv**: Requirements for each application, with flattened nested structures.
3. **sustainability.csv**: Sustainability data for each application, with flattened nested structures.
4. **consumers.csv**: Combined data on consumers and manufacturers (from supply chain data), with entity_type distinguishing between them.

## Additional Supply Chain Information

The following information from the supply_chain_data structure is not included in the CSV files but might be useful for future reference:

- processing_capabilities: List of manufacturing processes for each application
- regional_availability: List of regions where the application components are available

These could be added as additional CSV files if needed.
"""

with open(os.path.join(csv_dir, 'csv_data_readme.md'), 'w') as f:
    f.write(readme_content)

print(f"CSV files successfully created in: {csv_dir}")
print("- applications.csv")
print("- applications_requirements.csv")
print("- sustainability.csv")
print("- consumers.csv")
print("- csv_data_readme.md")
