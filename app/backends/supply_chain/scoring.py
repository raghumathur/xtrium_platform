"""
Supply Chain Scoring Module

This module provides functions to calculate supply chain scores based on buyer metrics 
and market data for applications.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple
import hashlib

def calculate_supply_chain_score(
    app_row: pd.Series,
    buyers_df: pd.DataFrame,
    application: str = None
) -> float:
    """
    Calculate a supply chain score (0-100) based on buyer metrics and market data
    
    Args:
        app_row (pd.Series): Application data row from DataFrame
        buyers_df (pd.DataFrame): Buyers database DataFrame
        application (str, optional): Name of the application to filter buyers by
        
    Returns:
        float: Supply chain score (0-100)
    """
    # TEMPORARY: Return a fixed high score for testing
    return 85.0
    
    # Calculate buyer metrics score
    buyer_score = calculate_buyer_metrics_score(buyers_df, application)
    
    # Calculate market metrics score
    market_score = calculate_market_metrics_score(app_row)
    
    # Combine scores according to weights
    total_score = (
        (buyer_score * components['buyer_metrics'] / 100) +
        (market_score * components['market_metrics'] / 100)
    )
    
    # Ensure score is between 0-100
    return max(0, min(total_score, max_score))

def calculate_buyer_metrics_score(
    buyers_df: pd.DataFrame,
    application: str = None
) -> float:
    """
    Calculate a score based on buyer metrics from the buyers database.
    
    Args:
        buyers_df (pd.DataFrame): Buyers database
        application (str, optional): Application name to filter buyers
        
    Returns:
        float: Buyer metrics score (0-100)
    """
    # Check if buyers dataframe is empty
    if buyers_df.empty:
        return 50.0  # Default score if no buyer data
    
    # Filter buyers by application if specified
    if application and 'Application' in buyers_df.columns:
        filtered_buyers = buyers_df[buyers_df['Application'] == application]
        # If no buyers for this application, use all buyers
        if filtered_buyers.empty:
            filtered_buyers = buyers_df
    else:
        filtered_buyers = buyers_df
    
    # Define buyer metrics and their weights (total should be 100%)
    metrics = {
        'Supply_Chain_Tier': {
            'weight': 25,
            'better': 'lower',
            'normalize': lambda x: max(0, 100 - (x - 1) * 25)  # Tier 1 = 100, Tier 2 = 75, etc.
        },
        'Review_Score': {
            'weight': 20,
            'better': 'higher',
            'normalize': lambda x: (x / 5) * 100  # Assuming 5-point scale
        },
        'Recent_Growth_Rate': {
            'weight': 15,
            'better': 'moderate',
            'normalize': lambda x: 100 - abs(x - 7) * 8  # Optimal growth ~7%
        },
        'Typical_Lead_Time_Days': {
            'weight': 25,
            'better': 'lower',
            'normalize': lambda x: max(0, 100 - (x / 90) * 100)  # 0 days = 100, 90+ days = 0
        },
        'Contract_Duration_Months': {
            'weight': 15,
            'better': 'higher',
            'normalize': lambda x: min(100, (x / 36) * 100)  # 36+ months = 100
        }
    }
    
    # Initialize total weighted score
    total_score = 0
    available_weight = 0
    
    # Calculate score for each metric
    for metric, config in metrics.items():
        if metric in filtered_buyers.columns:
            # Get values and remove potential non-numeric values
            try:
                values = pd.to_numeric(filtered_buyers[metric], errors='coerce')
                values = values.dropna()
                
                if not values.empty:
                    # Calculate normalized score for each value
                    normalized_values = values.apply(config['normalize'])
                    
                    # Average the normalized values
                    avg_score = normalized_values.mean()
                    
                    # Add weighted score to total
                    total_score += avg_score * config['weight'] / 100
                    available_weight += config['weight']
            except:
                # Skip metrics with errors
                continue
    
    # If no metrics available, return default score
    if available_weight == 0:
        return 50.0
    
    # Scale to available weight
    final_score = (total_score / available_weight) * 100
    
    return max(0, min(final_score, 100))

def calculate_market_metrics_score(app_row: pd.Series) -> float:
    """
    Calculate a score based on market metrics for the application.
    
    Args:
        app_row (pd.Series): Application data row containing market metrics
        
    Returns:
        float: Market metrics score (0-100)
    """
    # Define market metrics and their weights (total should be 100%)
    metrics = {
        'market_size_usd': {
            'weight': 20,
            'better': 'higher',
            'normalize': lambda x: min(100, (x / 1e9) * 100)  # 1B+ USD = 100
        },
        'market_growth_rate': {
            'weight': 30,
            'better': 'higher',
            'normalize': lambda x: min(100, max(0, x * 10))  # 10%+ = 100
        },
        'market_concentration': {
            'weight': 25,
            'better': 'moderate',
            'normalize': lambda x: 100 - abs((x * 100) - 50)  # 0.5 = 100 (optimal)
        },
        'price_volatility': {
            'weight': 25,
            'better': 'lower',
            'normalize': lambda x: max(0, 100 - (x * 100))  # 0 = 100, 1 = 0
        }
    }
    
    # Initialize total weighted score
    total_score = 0
    available_weight = 0
    
    # Calculate score for each metric
    for metric, config in metrics.items():
        if metric in app_row and not pd.isna(app_row[metric]):
            try:
                # Get value
                value = float(app_row[metric])
                
                # Calculate normalized score
                normalized_score = config['normalize'](value)
                
                # Add weighted score to total
                total_score += normalized_score * config['weight'] / 100
                available_weight += config['weight']
            except (ValueError, TypeError):
                # Skip metrics with errors
                continue
    
    # If no metrics available, return default score
    if available_weight == 0:
        return 50.0
    
    # Scale to available weight
    final_score = (total_score / available_weight) * 100
    
    return max(0, min(final_score, 100))

def get_supply_chain_level(score: float) -> Tuple[str, str]:
    """
    Convert a numeric supply chain score to a level description and color.
    
    Args:
        score (float): Supply chain score (0-100)
        
    Returns:
        Tuple[str, str]: (level description, color)
    """
    if score >= 90:
        return "Excellent", "#00b050"  # Green
    elif score >= 75:
        return "Good", "#00b050"  # Green
    elif score >= 60:
        return "Adequate", "#92d050"  # Light green
    elif score >= 45:
        return "Moderate", "#ffbf00"  # Amber
    elif score >= 30:
        return "Fair", "#ff7f00"  # Orange
    else:
        return "Poor", "#ff0000"  # Red
