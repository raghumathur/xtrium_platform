"""
Sustainability Scoring Module

This module provides functionality to calculate sustainability scores for materials and
applications based on their certifications, life cycle assessment (LCA) data, material
composition, and supply chain transparency.

The scoring is data-driven, with certification tiers extracted dynamically from the data
rather than being hardcoded.
"""

import pandas as pd
import numpy as np


def extract_certification_tiers(df):
    """
    Extract certification tiers from the applications DataFrame.
    
    Args:
        df (pd.DataFrame): Applications DataFrame potentially containing certification tier columns
        
    Returns:
        dict: Dictionary of certification tiers and their associated weights
    """
    # Default certification tiers in case they're not defined in the DataFrame
    default_tiers = {
        'tier1': ['Cradle to Cradle', 'FSC', 'GreenGuard Gold'],
        'tier2': ['ISO 14001', 'LEED', 'GreenGuard', 'ENERGY STAR', 'AS9100D', 'ASME'],
        'tier3': ['EPD', 'HPD', 'REACH', 'RoHS']
    }
    
    # Check if certification tier columns exist in the DataFrame
    cert_columns_exist = all(col in df.columns for col in ['cert_tier1', 'cert_tier2', 'cert_tier3'])
    
    if cert_columns_exist:
        # Use the first row with non-null certification tiers
        tiers = {}
        
        # Find first non-null value for each tier column
        for tier_col in ['cert_tier1', 'cert_tier2', 'cert_tier3']:
            tier_values = df[df[tier_col].notna()][tier_col].iloc[0] if any(df[tier_col].notna()) else ''
            tier_name = tier_col.replace('cert_', '')
            
            if isinstance(tier_values, str):
                # Split by comma and strip whitespace
                cert_list = [cert.strip() for cert in tier_values.split(',') if cert.strip()]
                tiers[tier_name] = cert_list
            else:
                # Use default tier if no valid data found
                tier_idx = int(tier_name[-1]) - 1
                tiers[tier_name] = default_tiers[f'tier{tier_idx + 1}']
    else:
        # Use default tiers if certification tier columns don't exist
        tiers = default_tiers
    
    return tiers


def parse_certifications(cert_str):
    """
    Parse certification string into a list of certifications.
    
    Args:
        cert_str: String of comma-separated certifications or list
        
    Returns:
        list: List of certification names
    """
    if pd.isna(cert_str) or cert_str == '':
        return []
        
    if isinstance(cert_str, str):
        # Split by comma and strip whitespace
        return [cert.strip() for cert in cert_str.split(',') if cert.strip()]
    elif isinstance(cert_str, list):
        return cert_str
    else:
        return []


def calculate_certification_score(row, cert_tiers):
    """
    Calculate sustainability score based on certifications.
    
    Args:
        row (pd.Series): Row from applications DataFrame
        cert_tiers (dict): Dictionary of certification tiers
        
    Returns:
        float: Certification score (0-40)
    """
    max_score = 40  # Maximum score for certifications component
    
    # Set weights for each tier
    tier_weights = {
        'tier1': 20,  # Tier 1 certifications are worth 20 points each
        'tier2': 10,  # Tier 2 certifications are worth 10 points each
        'tier3': 5    # Tier 3 certifications are worth 5 points each
    }
    
    # Get certifications from the row
    if 'certifications' not in row or pd.isna(row['certifications']):
        return 0
        
    # Parse certifications
    certs = parse_certifications(row['certifications'])
    if not certs:
        return 0
    
    # Calculate score based on which tier each certification belongs to
    total_points = 0
    for cert in certs:
        for tier, weight in tier_weights.items():
            if cert in cert_tiers.get(tier, []):
                total_points += weight
                break
    
    # Cap the score at the maximum
    final_score = min(total_points, max_score)
    
    # Return normalized score (0-40 range)
    return final_score


def calculate_lca_score(row):
    """
    Calculate sustainability score based on Life Cycle Assessment (LCA) data.
    
    Args:
        row (pd.Series): Row from applications DataFrame
        
    Returns:
        float: LCA score (0-30)
    """
    max_score = 30  # Maximum score for LCA component
    
    # Define LCA metrics and their weights
    lca_metrics = {
        'lca_carbon_footprint': 12,  # Carbon footprint has highest weight
        'lca_water_usage': 9,        # Water usage has medium weight
        'lca_energy': 9              # Energy consumption has medium weight
    }
    
    total_points = 0
    available_metrics = 0
    
    # For each LCA metric
    for metric, weight in lca_metrics.items():
        if metric in row and not pd.isna(row[metric]):
            try:
                # Get the value and handle range formats
                value_str = str(row[metric])
                
                # Handle ranges like "40.5–45.0" or "40.5-45.0"
                if '–' in value_str or '-' in value_str:
                    # Normalize the dash character
                    value_str = value_str.replace('–', '-')
                    # Split and get min/max values
                    parts = value_str.split('-')
                    if len(parts) == 2:
                        min_val = float(parts[0].strip())
                        max_val = float(parts[1].strip())
                        # Use the better (lower) value for environmental metrics
                        value = min_val
                    else:
                        # Invalid format, use default
                        continue
                else:
                    # Try to convert to float
                    value = float(value_str)
                
                # Lower values are better for LCA metrics (environmental impact)
                # Normalize to 0-100 scale where 0 is best (no impact)
                # Assume 0-100 scale where lower is better
                normalized_value = min(value, 100)  # Cap at 100
                
                # Apply a more favorable scoring curve for good LCA values
                # This uses a quadratic curve that rewards lower values more generously
                # For example: a value of 50 now gets 75% of the points instead of 50%
                metric_score = (1 - (normalized_value / 100)**2) * weight
                total_points += metric_score
                available_metrics += weight
                
            except (ValueError, TypeError) as e:
                # Skip metrics with non-numeric values
                continue
    
    # If no metrics are available, return 0
    if available_metrics == 0:
        return 0
    
    # Scale the score relative to available metrics and cap at max_score
    scaled_score = (total_points / available_metrics) * max_score
    return min(scaled_score, max_score)


def calculate_composition_score(row):
    """
    Calculate sustainability score based on material composition.
    
    Args:
        row (pd.Series): Row from applications DataFrame
        
    Returns:
        float: Composition score (0-20)
    """
    max_score = 20  # Maximum score for composition component
    
    # Define composition metrics and their weights
    composition_metrics = {
        'recycled_content': 12,    # Recycled content has higher weight
        'renewable_content': 8      # Renewable content has slightly lower weight
    }
    
    total_points = 0
    available_metrics = 0
    
    # For each composition metric
    for metric, weight in composition_metrics.items():
        if metric in row and not pd.isna(row[metric]):
            try:
                # Get the value and handle range formats
                value_str = str(row[metric])
                
                # Handle ranges like "50–55" or "50-55"
                if '–' in value_str or '-' in value_str:
                    # Normalize the dash character
                    value_str = value_str.replace('–', '-')
                    # Split and get min/max values
                    parts = value_str.split('-')
                    if len(parts) == 2:
                        min_val = float(parts[0].strip())
                        max_val = float(parts[1].strip())
                        # Use the better (higher) value for composition metrics
                        value = max_val
                    else:
                        # Invalid format, use default
                        continue
                else:
                    # Try to convert to float
                    value = float(value_str)
                
                # Higher values are better for composition metrics (recycled/renewable content)
                # Normalize to 0-100 scale
                normalized_value = min(value, 100)  # Cap at 100
                
                # Apply a more favorable scoring curve for composition metrics
                # This uses a square root curve that rewards moderate values more generously
                # For example: a value of 25 now gets 50% of the points instead of 25%
                metric_score = (normalized_value / 100)**0.5 * weight
                total_points += metric_score
                available_metrics += weight
                
            except (ValueError, TypeError) as e:
                # Skip metrics with non-numeric values
                continue
    
    # If no metrics are available, return 0
    if available_metrics == 0:
        return 0
    
    # Scale the score relative to available metrics and cap at max_score
    scaled_score = (total_points / available_metrics) * max_score
    return min(scaled_score, max_score)


def calculate_supply_chain_score(row):
    """
    Calculate sustainability score based on supply chain transparency.
    
    Args:
        row (pd.Series): Row from applications DataFrame
        
    Returns:
        float: Supply chain score (0-10)
    """
    max_score = 10  # Maximum score for supply chain component
    
    # Define supply chain metrics and their weights
    supply_chain_metrics = {
        'supply_chain_transparency': 10  # Supply chain transparency has full weight
    }
    
    total_points = 0
    available_metrics = 0
    
    # For the supply chain transparency metric
    for metric, weight in supply_chain_metrics.items():
        if metric in row and not pd.isna(row[metric]):
            # Higher values are better for supply chain metrics
            # (assuming they represent percentages of supply chain transparency)
            try:
                # Convert to float first to handle string values
                value = float(row[metric])
                if 0 <= value <= 100:
                    metric_score = value / 100 * weight
                    total_points += metric_score
                    available_metrics += weight
                else:
                    # Skip metrics with out-of-range values
                    continue
            except (ValueError, TypeError):
                # Skip metrics with non-numeric values
                continue
    
    # If no metrics are available, return 0
    if available_metrics == 0:
        return 0
    
    # Scale the score relative to available metrics and cap at max_score
    scaled_score = (total_points / available_metrics) * max_score
    return min(scaled_score, max_score)


def calculate_sustainability_score(app_row, cert_tiers=None):
    """
    Calculate a sustainability score (0-100) based on certification, LCA, material composition, and supply chain transparency.
    
    Args:
        app_row (pd.Series): Application data row from DataFrame
        cert_tiers (Dict[str, int], optional): Dictionary mapping certifications to their tier levels
        
    Returns:
        float: Sustainability score (0-100)
    """
    # Handle missing cert_tiers
    if cert_tiers is None:
        cert_tiers = {
            'tier1': ['Cradle to Cradle', 'FSC', 'GreenGuard Gold'],
            'tier2': ['ISO 14001', 'LEED', 'GreenGuard', 'ENERGY STAR'],
            'tier3': ['EPD', 'HPD', 'REACH', 'RoHS']
        }
    
    # Calculate each component score
    cert_score = calculate_certification_score(app_row, cert_tiers)
    lca_score = calculate_lca_score(app_row)
    composition_score = calculate_composition_score(app_row)
    supply_chain_score = calculate_supply_chain_score(app_row)
    
    # Sum up all component scores
    total_score = cert_score + lca_score + composition_score + supply_chain_score
    
    # Round to one decimal place
    return round(total_score, 1)


def get_sustainability_level(score):
    """
    Map sustainability score to a descriptive level and color.
    
    Args:
        score (float): Sustainability score (0-100)
        
    Returns:
        tuple: (level, color) where level is a string description and color is a hex color code
    """
    if score >= 80:
        return "Excellent", "#00cc96"  # Green
    elif score >= 60:
        return "Good", "#5DB85C"       # Light green
    elif score >= 40:
        return "Moderate", "#F0AD4E"   # Orange/Amber
    elif score >= 20:
        return "Fair", "#FF7F0E"       # Dark orange
    else:
        return "Poor", "#D9534F"       # Red
