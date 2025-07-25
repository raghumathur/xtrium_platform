#==========================================================================================
# Import necessary modules and libraries for application filtering and property analysis
#==========================================================================================

# Import streamlit and pandas from the app's utility helpers
from app.utils.import_helpers import st, pd

# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np

# Initialize session state for filter application if it doesn't exist
def initialize_filter_state():
    """Initialize the session state for filters if it doesn't exist."""
    if "applied_filters" not in st.session_state:
        st.session_state.applied_filters = {
            "material_types": [],
            "industry": [],
            "property_filters": []
        }

# Ensure pandas numeric type functions are available
if not hasattr(pd.api.types, 'is_numeric_dtype'):
    # Fallback function if pandas version doesn't have this
    def is_numeric_dtype(obj):
        return pd.api.types.is_number(obj) or isinstance(obj, (int, float, np.number))
    pd.api.types.is_numeric_dtype = is_numeric_dtype

def material_type_filters(applications_df):
    """
    Renders material type filter UI and returns selected material types.
    
    Args:
        applications_df (pd.DataFrame): Applications database DataFrame
        
    Returns:
        list: Selected material types
    """
    # Extract unique material types from the applications database
    if 'Commercial name' in applications_df.columns:
        material_types = sorted(applications_df['Commercial name'].dropna().unique().tolist())
    else:
        material_types = []
        st.warning("Material type information not found in the applications database.")
    
    # Retrieve material types from session state
    selected_types = st.multiselect(
        "Material Type",
        options=material_types,
        default=st.session_state.applied_filters["material_types"] if "applied_filters" in st.session_state else [],
        key="material_type_filter"
    )
    
    # Update session state
    if "applied_filters" in st.session_state:
        st.session_state.applied_filters["material_types"] = selected_types
    
    return selected_types

def industry_filters(applications_df):
    """
    Renders industry filter UI and returns selected industries.
    
    Args:
        applications_df (pd.DataFrame): Applications database DataFrame
        
    Returns:
        list: Selected industries ready for filtering
    """
    
    # Extract unique industries from the applications database
    if 'Industry' in applications_df.columns:
        industries = sorted(applications_df['Industry'].dropna().unique().tolist())
    else:
        industries = []
        st.warning("Industry information not found in the applications database.")
    
    # Industry selector
    selected_industries = st.multiselect(
        "Industry",
        options=industries,
        default=st.session_state.applied_filters["industry"] if "applied_filters" in st.session_state else [],
        key="industry_filter"
    )
    
    # Update session state
    if "applied_filters" in st.session_state:
        st.session_state.applied_filters["industry"] = selected_industries
    
    return selected_industries

def render_application_selection_filters(applications_df):
    """
    Renders a complete UI expander for all application selection filters including:
    - Material type filters
    - Industry filters
    - Property range filters
    
    This function is used for filtering applications BEFORE selection in the application discovery process.
    
    Args:
        applications_df (pd.DataFrame): Applications database DataFrame containing all available applications
        
    Returns:
        pd.DataFrame: Filtered applications DataFrame after applying all selection filters
    """
    # Initialize filter state if needed
    initialize_filter_state()
    
    # Create a copy of the applications DataFrame to avoid modifying the original
    filtered_applications = applications_df.copy()
    
    # Create an expander for all filters
    with st.expander("Application Filters", expanded=False):
        col1, col2 = st.columns(2)
        
        # Material Type filter in column 1
        with col1:
            selected_material_types = material_type_filters(applications_df)
            
            # Apply material type filter if any types are selected
            if selected_material_types and not filtered_applications.empty:
                if 'Commercial name' in filtered_applications.columns:
                    filtered_applications = filtered_applications[
                        filtered_applications['Commercial name'].isin(selected_material_types)
                    ]
                    
        # Industry filter in column 2
        with col2:
            selected_industries = industry_filters(applications_df)
            
            # Apply industry filter if any industries are selected
            if selected_industries and not filtered_applications.empty:
                if 'Industry' in filtered_applications.columns:
                    filtered_applications = filtered_applications[
                        filtered_applications['Industry'].isin(selected_industries)
                    ]
        
        # Property range filters
        property_filters = property_range_filters(applications_df)
        
        # Apply property filters
        if property_filters and not filtered_applications.empty:
            for filter_item in property_filters:
                param = filter_item["parameter"]
                min_val = filter_item["filter_min"]
                max_val = filter_item["filter_max"]
                
                if param in filtered_applications.columns:
                    # Apply the filter to numeric columns
                    if pd.api.types.is_numeric_dtype(filtered_applications[param]):
                        filtered_applications = filtered_applications[
                            (filtered_applications[param] >= min_val) & 
                            (filtered_applications[param] <= max_val)
                        ]
    
    # Display count of filtered applications
    if not filtered_applications.empty:
        st.caption(f"Showing {len(filtered_applications)} applications")
    else:
        st.warning("No applications match the selected filters. Try adjusting your criteria.")
    
    return filtered_applications

def property_range_filters(applications_df):
    """
    Creates range-based property filters that work on the entire application database.
    Used for filtering applications before selection.
    
    Args:
        applications_df: DataFrame containing applications and their properties
        
    Returns:
        List of active property filters, each with parameter, filter_min, filter_max
    """
    # Find numeric columns for property filtering
    numeric_columns = []
    for col in applications_df.columns:
        if col not in ['Use-case', 'Industry', 'Commercial name', 'Chemical Name', 'Chemical Formula', 'Property Overlap'] and pd.api.types.is_numeric_dtype(applications_df[col]):
            numeric_columns.append(col)
    
    if not numeric_columns:
        return []
    
    # Initialize property filters in session state if they don't exist
    if "property_filters" not in st.session_state:
        st.session_state.property_filters = []
    
    # Add Property Filter button
    if st.button("➕ Add Property Filter"):
        # Add a new empty filter to the session state
        st.session_state.property_filters.append({
            "parameter": numeric_columns[0] if numeric_columns else None,
            "filter_min": None,
            "filter_max": None
        })
    
    # Display and manage existing property filters
    active_filters = []
    for idx, filter_item in enumerate(st.session_state.property_filters):
        cols = st.columns([3, 2, 2, 1])
        
        # Property selection dropdown
        with cols[0]:
            selected_param = st.selectbox(
                "Property",
                options=numeric_columns,
                index=numeric_columns.index(filter_item["parameter"]) if filter_item["parameter"] in numeric_columns else 0,
                key=f"property_param_{idx}"
            )
            st.session_state.property_filters[idx]["parameter"] = selected_param
        
        # If we have a valid parameter, show min/max range sliders
        if selected_param in numeric_columns:
            # Get min and max values for the selected property
            min_val = float(applications_df[selected_param].min())
            max_val = float(applications_df[selected_param].max())
            
            # Set default filter values if not already set
            if filter_item["filter_min"] is None or filter_item["filter_max"] is None:
                filter_item["filter_min"] = min_val
                filter_item["filter_max"] = max_val
            
            # Min value slider
            with cols[1]:
                filter_min = st.slider(
                    "Min",
                    min_value=min_val,
                    max_value=max_val,
                    value=filter_item["filter_min"],
                    key=f"property_min_{idx}"
                )
                st.session_state.property_filters[idx]["filter_min"] = filter_min
            
            # Max value slider
            with cols[2]:
                filter_max = st.slider(
                    "Max",
                    min_value=min_val,
                    max_value=max_val,
                    value=filter_item["filter_max"],
                    key=f"property_max_{idx}"
                )
                st.session_state.property_filters[idx]["filter_max"] = filter_max
        
        # Remove filter button
        with cols[3]:
            if st.button("❌", key=f"remove_property_{idx}"):
                st.session_state.property_filters.pop(idx)
                st.rerun()
        
        # Add to active filters if valid
        if selected_param in numeric_columns:
            active_filters.append({
                "parameter": selected_param,
                "filter_min": filter_item["filter_min"],
                "filter_max": filter_item["filter_max"]
            })
    
    return active_filters

#==========================================================================================
# Material Matching Preferences System
# Modular UI components for post-selection material matching preferences
#==========================================================================================

def extract_numerical_properties(selected_application_row):
    """
    Extract numerical properties from an application row for use in material matching.
    
    Args:
        selected_application_row: DataFrame row containing application properties
        
    Returns:
        dict: Dictionary of property names to numerical values
    """
    numerical_props = {}
    
    # Process each column in the application row
    for col, value in selected_application_row.items():
        # Skip non-numeric columns and common metadata fields
        if col in ['Use-case', 'Industry', 'Commercial name', 'Chemical Name', 'Chemical Formula', 'Property Overlap']:
            continue
            
        # Handle range values (e.g., "10-20")
        if isinstance(value, str) and '-' in value:
            try:
                # Extract min and max from range, then use average
                min_val, max_val = map(float, value.split('-'))
                numerical_props[col] = (min_val + max_val) / 2
            except (ValueError, TypeError):
                pass
        # Handle direct numeric values
        elif isinstance(value, (int, float)) and not pd.isna(value):
            numerical_props[col] = value
            
    return numerical_props

def render_property_importance(tab_index, numerical_props, applications_df):
    """
    Renders selective property importance sliders for weighting properties.
    
    Args:
        tab_index: Unique tab index for scoping Streamlit component keys
        numerical_props: Dictionary of numerical properties and their values
        applications_df: DataFrame containing all applications data
        
    Returns:
        dict: Dictionary of properties and their importance values
    """
    # st.markdown("### Property Importance")
    # st.caption("Adjust the importance of each property for material matching")
    
    # Initialize property weights dictionary
    property_weights = {}
    
    # Create sliders for each numerical property
    for prop, value in numerical_props.items():
        # Create a unique key for this property slider
        slider_key = f"prop_importance_{tab_index}_{prop.replace(' ', '_')}"
        
        # Create a slider for this property's importance
        importance = st.slider(
            f"{prop} Importance",
            min_value=0,
            max_value=100,
            value=50,  # Default to medium importance
            step=5,
            key=slider_key
        )
        
        # Store the property value and importance
        property_weights[prop] = {
            "value": value,
            "importance": importance
        }
    
    return property_weights

def render_constituent_elements_focus(tab_index, materials_df=None):
    """
    Renders UI for selecting constituent elements to focus on.
    Dynamically populates the elements from the periodic table.
    
    Args:
        tab_index: Unique tab index for scoping Streamlit component keys
        materials_df: DataFrame containing materials data with element information
        
    Returns:
        list: Selected constituent elements
    """
    from app.utils.periodic_table import load_periodic_table
    
    # Load the periodic table data
    periodic_table = load_periodic_table()
    
    # Element selector using periodic table elements
    selected_elements = st.multiselect(
        "Constituent Elements",
        options=periodic_table,
        key=f"constituent_elements_{tab_index}"
    )
    
    return selected_elements

def render_supply_chain_preferences(tab_index):
    """
    Renders UI for setting supply chain preferences.
    
    Args:
        tab_index: Unique tab index for scoping Streamlit component keys
        
    Returns:
        dict: Supply chain preferences
    """
    # Initialize preferences dictionary
    preferences = {}
    
    # Lead time preference
    lead_time_options = ["Not important", "Somewhat important", "Very important"]
    preferences["lead_time"] = st.selectbox(
        "Lead time priority",
        options=lead_time_options,
        index=1,  # Default to somewhat important
        key=f"lead_time_{tab_index}"
    )
    
    # Cost preference
    cost_options = ["Not important", "Somewhat important", "Very important"]
    preferences["cost"] = st.selectbox(
        "Cost priority",
        options=cost_options,
        index=1,  # Default to somewhat important
        key=f"cost_{tab_index}"
    )
    
    # Domestic suppliers preference
    preferences["domestic_suppliers"] = st.checkbox(
        "Domestic suppliers",
        value=False,
        key=f"domestic_pref_{tab_index}"
    )
    
    return preferences

def render_sustainability_preferences(tab_index):
    """
    Renders UI for setting sustainability preferences.
    
    Args:
        tab_index: Unique tab index for scoping Streamlit component keys
        
    Returns:
        dict: Sustainability preferences
    """
    # Initialize preferences dictionary
    preferences = {}
    
    # Regulatory compliance - critical for semiconductor industry
    compliance_options = ["Not required", "Preferred", "Required"]
    preferences["regulatory_compliance"] = st.selectbox(
        "Regulatory compliance",
        options=compliance_options,
        index=1,
        key=f"compliance_{tab_index}"
    )
    
    # Recyclability - most important sustainability factor
    preferences["recycling_required"] = st.checkbox(
        "Recyclable required",
        value=False,
        key=f"recycling_{tab_index}"
    )
    
    return preferences

def render_material_matching_preferences(tab_index, applications_df, selected_application_row, materials_df=None):
    """
    Master function that renders a comprehensive interface for setting material matching
    preferences after application selection. Uses modular components for different preference areas.
    
    Args:
        tab_index: Unique tab index for scoping Streamlit component keys
        applications_df: DataFrame containing all applications data
        selected_application_row: Selected application as a DataFrame row
        materials_df: DataFrame containing materials data (optional)
    
    Returns:
        dict: Comprehensive matching preferences to guide material recommendations
    """
    # Extract numerical properties
    numerical_props = extract_numerical_properties(selected_application_row)
    
    # Check if we have properties to work with
    if not numerical_props:
        st.warning("No numerical properties available for this application for material matching.")
        return {}
    
    matching_preferences = {}
    
    with st.expander("Material Matching Preferences", expanded=False):
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])  # Adjust column widths as needed
        
        # Column 1: Property importance matrix (wider column for sliders)
        with col1:
            property_weights = render_property_importance(tab_index, numerical_props, applications_df)
            matching_preferences["property_weights"] = property_weights
        
        # Column 2: Constituent elements focus
        with col2:
            selected_elements = render_constituent_elements_focus(tab_index, materials_df)
            matching_preferences["constituent_elements"] = selected_elements
        
        # Column 3: Supply chain preferences
        with col3:
            supply_chain_prefs = render_supply_chain_preferences(tab_index)
            matching_preferences["supply_chain"] = supply_chain_prefs
        
        # Column 4: Sustainability criteria
        with col4:
            sustainability_prefs = render_sustainability_preferences(tab_index)
            matching_preferences["sustainability"] = sustainability_prefs
    
    return matching_preferences