#==========================================================================================
# Import necessary modules and libraries for material filtering and property analysis
#==========================================================================================

# Import streamlit and pandas from the app's utility helpers
from app.utils.import_helpers import st, pd

# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np

# Import utility functions for working with periodic table data and chemical formulas
from app.utils.periodic_table import load_periodic_table, extract_symbols

# Import the material helper functions for filtering
from app.utils.material_helpers import extract_material_types, filter_by_elements, filter_by_material_types

# Initialize session state for filter application if it doesn't exist
def initialize_filter_state():
    """Initialize the session state for filters if it doesn't exist."""
    if "applied_filters" not in st.session_state:
        st.session_state.applied_filters = {
            "material_types": [],
            "periodic_elements": [],
            "property_filters": []
        }

# Ensure pandas numeric type functions are available
if not hasattr(pd.api.types, 'is_numeric_dtype'):
    # Fallback function if pandas version doesn't have this
    def is_numeric_dtype(obj):
        return pd.api.types.is_number(obj) or isinstance(obj, (int, float, np.number))
    pd.api.types.is_numeric_dtype = is_numeric_dtype

def material_type_filters(materials_df):
    """
    Renders material type filter UI and returns selected material types.
    
    Args:
        materials_df (pd.DataFrame): Materials database DataFrame
        
    Returns:
        list: Selected material types
    """
    #st.subheader("Filter by Material Type")
    material_types = extract_material_types(materials_df)
    
    # Retrieve material types from session state
    selected_types = st.multiselect(
        "Specify Material Type(s)",
        options=material_types,
        default=st.session_state.applied_filters["material_types"] if "applied_filters" in st.session_state else [],
        key="material_type_filter"
    )
    
    # Update session state
    if "applied_filters" in st.session_state:
        st.session_state.applied_filters["material_types"] = selected_types
    
    return selected_types

def periodic_element_filters(materials_df):
    """
    Renders periodic element filter UI and returns selected elements.
    
    Args:
        materials_df (pd.DataFrame): Materials database DataFrame
        
    Returns:
        list: Selected element symbols ready for filtering
    """
    #st.subheader("Filter by Elements")
    
    # Load the periodic table data
    periodic_table = load_periodic_table()
    
    # Element selector using periodic table elements
    selected_elements = st.multiselect(
        "Specify Constituent Element(s)",
        options=periodic_table,
        default=st.session_state.applied_filters["periodic_elements"] if "applied_filters" in st.session_state else [],
        key="element_filter"
    )
    
    # Update session state
    if "applied_filters" in st.session_state:
        st.session_state.applied_filters["periodic_elements"] = selected_elements
    
    # Extract element symbols for filtering
    element_symbols = extract_symbols(selected_elements) if selected_elements else []
    
    return element_symbols

def render_material_selection_filters(materials_df):
    """
    Renders a complete UI expander for all material selection filters including:
    - Material type filters
    - Periodic element filters
    - Property range filters
    
    This function is used for filtering materials BEFORE selection in the material discovery process.
    It is different from render_filters which is used for recommendation weighting AFTER material selection.
    
    Args:
        materials_df (pd.DataFrame): Materials database DataFrame containing all available materials
        
    Returns:
        pd.DataFrame: Filtered materials DataFrame after applying all selection filters
    """
    # Ensure we have properly initialized filter state
    initialize_filter_state()
    # Ensure we have a copy of the original dataset
    filtered_materials = materials_df.copy()
    original_count = len(filtered_materials)
    
    # Create a collapsible expander for all filters with Clear button in the header
    expander_label = "Filters"
    
    # Create the expander
    with st.expander(expander_label, expanded=False):
        # Place clear button at the top right of the filter section for better visibility
        # This follows the pattern used in many modern UIs where action buttons are placed
        # at the top of their relevant sections
        clear_clicked = st.button(
            "🗑️ Clear All Filters",
            help="Reset all filters to default values", 
            key="clear_filters_btn",
            use_container_width=True,
            type="secondary"
        )
        
        # Process clear button click
        if clear_clicked:
            # Reset all filter collections
            st.session_state.applied_filters = {
                "material_types": [],
                "periodic_elements": [],
                "property_filters": []
            }
            
            # Also reset property filters state
            if "property_filters" in st.session_state:
                st.session_state.property_filters = []
                
            st.experimental_rerun()
        
        # Create two columns for material filter (left) and element filter (right)
        material_filter_col, element_filter_col = st.columns(2)
        
        # === MATERIAL TYPE FILTER (LEFT COLUMN) ===
        with material_filter_col:
            # Use consolidated material type filter function
            selected_types = material_type_filters(materials_df)
            
            # Apply type filter if selected
            if selected_types:
                filtered_materials = filter_by_material_types(filtered_materials, selected_types)
        
        # === ELEMENT FILTER (RIGHT COLUMN) ===
        with element_filter_col:
            # Use consolidated element filter function
            selected_elements = periodic_element_filters(materials_df)
            
            # Apply element filter if selected
            if selected_elements:
                filtered_materials = filter_by_elements(filtered_materials, selected_elements)
        
        # === PROPERTY RANGE FILTERS ===
        # st.subheader("Filter by Properties")
        
        # Apply property range filters
        property_filters = property_range_filters(materials_df)
        
        # Filter materials by property ranges
        if property_filters:
            for filter_item in property_filters:
                parameter = filter_item["parameter"]
                filter_min = filter_item["filter_min"]
                filter_max = filter_item["filter_max"]
                
                if parameter and (filter_min is not None or filter_max is not None):
                    # Apply minimum filter if specified
                    if filter_min is not None:
                        filtered_materials = filtered_materials[filtered_materials[parameter] >= filter_min]
                    
                    # Apply maximum filter if specified
                    if filter_max is not None:
                        filtered_materials = filtered_materials[filtered_materials[parameter] <= filter_max]
        
        # Save property filters to session state
        st.session_state.applied_filters["property_filters"] = property_filters
        
        # No separator needed
    
    # Show filtering status
    filtered_count = len(filtered_materials)
    #percent = (filtered_count / original_count) * 100 if original_count > 0 else 0
    #st.write(f"Showing {filtered_count} of {original_count} materials ({percent:.1f}%)")
    
    # If no materials match filters, show warning
    if filtered_materials.empty:
        st.warning("No materials match your filter criteria. Try adjusting your filters.")
    
    return filtered_materials

def property_range_filters(materials_df):
    """
    Creates range-based property filters that work on the entire material database.
    Used for filtering materials before selection.
    
    Args:
        materials_df: DataFrame containing materials and their properties
        
    Returns:
        List of active property filters, each with parameter, filter_min, filter_max
    """
    # Get numerical columns that have sufficient data for filtering
    numerical_columns = []
    for col in materials_df.columns:
        # Skip non-numeric columns, special columns and ID columns
        if not pd.api.types.is_numeric_dtype(materials_df[col]) or col == "serial" or "id" in col.lower():
            continue
            
        # Check if column has sufficient numerical data
        valid_values = materials_df[col].dropna()
        if len(valid_values) >= 2 and len(valid_values.unique()) > 1:
            numerical_columns.append(col)
    
    # Sort the numerical columns alphabetically for better user experience
    numerical_columns.sort()
    
    # If no suitable numerical columns are available, show a warning and stop
    if not numerical_columns:
        st.warning("No suitable numerical columns available in the materials database for filtering.")
        return []
    
    # Initialize session state for property range filters
    if "property_filters" not in st.session_state:
        st.session_state.property_filters = []
    
    # Add Filter Button
    if st.button("➕ Add Property Filter"):
        st.session_state.property_filters.append({
            "parameter": numerical_columns[0] if numerical_columns else None,
            "filter_min": None,
            "filter_max": None
        })
    
    # Loop through existing filters
    for idx, filter_data in enumerate(st.session_state.property_filters):
        # Create columns for filter UI
        cols = st.columns([4, 6, 0.5])
        
        # Property selector
        with cols[0]:
            selected_param = st.selectbox(
                "Property",
                options=numerical_columns,
                key=f"property_param_{idx}"
            )
            filter_data["parameter"] = selected_param
        
        # Range slider
        with cols[1]:
            if selected_param:
                # Get non-NaN values for the selected parameter
                valid_values = materials_df[selected_param].dropna()
                
                try:
                    # Get database min/max values from non-NaN values
                    db_min_val = float(valid_values.min())
                    db_max_val = float(valid_values.max())
                    
                    # Handle edge case where min and max are the same
                    if db_min_val == db_max_val:
                        # Create a small range around the single value
                        db_min_val = db_min_val * 0.99 if db_min_val != 0 else -0.01
                        db_max_val = db_max_val * 1.01 if db_max_val != 0 else 0.01
                        
                    # Ensure we have valid values
                    if np.isnan(db_min_val) or np.isnan(db_max_val) or db_min_val >= db_max_val:
                        raise ValueError(f"Invalid range for {selected_param}: [{db_min_val}, {db_max_val}]")
                    
                    # Create range slider
                    filter_min_val, filter_max_val = st.slider(
                        f"{selected_param} Range",
                        min_value=db_min_val,
                        max_value=db_max_val,
                        value=(db_min_val, db_max_val),
                        key=f"property_range_{idx}"
                    )
                    
                    # Store values in filter
                    filter_data["filter_min"] = filter_min_val
                    filter_data["filter_max"] = filter_max_val
                except Exception as e:
                    st.warning(f"Could not create slider for {selected_param}: {str(e)}")
                    filter_data["filter_min"] = None
                    filter_data["filter_max"] = None
        
        # Remove button
        with cols[2]:
            if st.button("❌", key=f"remove_property_filter_{idx}"):
                st.session_state.property_filters.pop(idx)
                st.rerun()
    
    # Return active filters
    return st.session_state.property_filters


def render_filters(tab_index, materials_df, selected_material_row):
    """
    Render dynamic filters for a Streamlit app for recommendation weighting.
    This function is used after material selection to adjust property importance
    for application recommendations.

    Features:
    1. Adds and removes filters dynamically with proper indexing.
    2. Synchronizes a slider's min/max values with manual inputs.
    3. Stores all filter selections in Streamlit session state.
    4. Prepares filter data in an organized structure for downstream processes.

    :param tab_index: Unique tab index for scoping Streamlit component keys.
    :param materials_df: DataFrame containing materials data.
    :param selected_material_row: Selected material as a DataFrame row for property extraction.
    """

    # Extract relevant numerical columns from the selected material row
    relevant_columns = []
    
    # Safely extract numeric columns
    for col in selected_material_row.index:
        # Skip serial column and null values
        if col == "serial" or pd.isna(selected_material_row[col]):
            continue
            
        # Check if the column value is numeric
        try:
            # Try to convert to float to test if it's numeric
            float(selected_material_row[col])
            relevant_columns.append(col)
        except (ValueError, TypeError):
            # Skip if not convertible to float
            continue

    # If no relevant columns are available, show a warning and stop
    if not relevant_columns:
        st.warning("No numerical properties available for this material for weighting.")
        return []
    
    # 2. Initialize session state for filters if not already initialized
    if "filters" not in st.session_state:
        st.session_state["filters"] = []  # List to hold filter dictionaries

    # Validate and flush invalid filters
    # st.session_state["filters"] = [
    #     f for f in st.session_state["filters"] if f.get("parameter") in relevant_columns or f.get("parameter") is None
    #    ]

    # 3. Add Filter Button
    if st.button("➕ Add Filter", key=f"add_filter_button_{tab_index}"):
        # Append a new empty filter dictionary to the session state
        st.session_state["filters"].append({
            "parameter": None,
            "value": None,
            "weightage": 50
        })

    # 4. Loop through existing filters and render them
    for idx, filter_data in enumerate(st.session_state["filters"]):
        # Create layout for the current filter row with 6 columns
        cols = st.columns([4, 4, 2, 2, 1])


        # Column 0: Drop-down for selecting the filter parameter
        with cols[0]:
            dbparam = filter_data.get("parameter")
            # Default to first param if none selected yet
            if not dbparam and relevant_columns:
                dbparam = relevant_columns[0]
                
            # Create the parameter selection dropdown
            selected_param = st.selectbox(
                "Parameter",
                options=relevant_columns,  # Options for selection
                index=relevant_columns.index(dbparam) if dbparam in relevant_columns else 0,
                key=f"param_{tab_index}_{idx}"
            )
            # Update the selected parameter in session state
            st.session_state["filters"][idx]["parameter"] = selected_param

        # Column 1: Slider for selecting a single value
        with cols[1]:
            # Initialize default values
            column_min, column_max = 0.0, 1.0
            
            # Fetch the column's min and max values for slider initialization if parameter exists
            if selected_param and selected_param in materials_df.columns:
                try:
                    column_min = float(materials_df[selected_param].min())
                    column_max = float(materials_df[selected_param].max())
                    
                    # Ensure min and max aren't equal (Streamlit requirement)
                    if column_min == column_max:
                        column_max = column_min + 1.0
                except:
                    # Fallback if conversion fails
                    pass
            
            # If the parameter has just been selected or changed, initialize its value
            if ("value" not in st.session_state["filters"][idx] or 
                st.session_state["filters"][idx]["parameter"] != selected_param):
                # Default to midpoint of range
                st.session_state["filters"][idx]["value"] = (column_min + column_max) / 2
            
            # Create slider for selecting importance value 
            slider_value = st.slider(
                f"{selected_param} Importance",
                min_value=float(column_min),
                max_value=float(column_max),
                value=st.session_state["filters"][idx]["value"],  # Use current value
                key=f"slider_{tab_index}_{idx}"
            )
            
            # Update session state with the slider value
            st.session_state["filters"][idx]["value"] = slider_value

        # Column 2: Text Input for the value (fine-tuned control)
        with cols[2]:
            # Format the slider value as a default for the text box
            text_value = st.text_input(
                "Value",
                value=f"{slider_value:.2f}",
                key=f"text_value_{tab_index}_{idx}"
            )
            # Update session state with the entered value if valid
            try:
                parsed_value = float(text_value)
                st.session_state["filters"][idx]["value"] = parsed_value
            except ValueError:
                # If invalid input, retain the previous slider value
                pass
            
        # Column 3: Weightage slider
        with cols[3]:
            # Initialize default weightage if not already present
            if "weightage" not in st.session_state["filters"][idx]:
                st.session_state["filters"][idx]["weightage"] = 50  # Default to neutral
                
            # Slider for adjusting the filter's importance in recommendations
            weightage_value = st.slider(
                "Importance",
                min_value=0,
                max_value=100,
                value=st.session_state["filters"][idx]["weightage"],
                key=f"weightage_{tab_index}_{idx}"
            )
            # Update session state with the weightage value
            st.session_state["filters"][idx]["weightage"] = weightage_value

        # Column 4: Delete Button for the current filter
        with cols[4]:
            st.markdown("<div style='height:29px;'></div>", unsafe_allow_html=True)  # Spacing
            if st.button("❌", key=f"remove_filter_{tab_index}_{idx}"):
                st.session_state["filters"].pop(idx)  # Remove the filter at the current index
                st.rerun()  # Force the app to re-render and reflect changes
    
    # 5. Create the final organized structure of active filters
    # Only include filters that have valid parameters and values
    selected_filters = [
        {
            "parameter": f["parameter"],
            "value": f["value"],
            "weightage": f["weightage"]
        }
        for f in st.session_state["filters"]
        if f.get("parameter") and f.get("value") is not None  # Only include valid filters
    ]
    
    # Show active filter count for debugging if needed
    # st.write(f"Active recommendation weights: {len(selected_filters)}")

    # 6. Return the organized filters for downstream use
    return selected_filters


#==========================================================================================
# Application Matching Preferences System
# Modular UI components for post-selection application matching preferences
#==========================================================================================

def get_fallback_domains():
    """
    Returns fallback application domains when applications DataFrame is not available.
    These are based on the specialized semiconductor packaging applications in DEMO_APPLICATIONS.
    
    Returns:
        list: Default application domains
    """
    return [
        "Memory & Storage",
        "RF & Communications",
        "Photonics & Optical",
        "Advanced Packaging",
        "Sensors & MEMS",
        "Advanced 3D Packaging",
        "Power Electronics",
        "Heterogeneous Integration"
    ]


def extract_numerical_properties(selected_material_row):
    """
    Extract numerical properties from a material row for use in application matching.
    Reuses the existing code pattern for numeric property extraction.
    
    Args:
        selected_material_row: DataFrame row containing material properties
        
    Returns:
        dict: Dictionary of property names to numerical values
    """
    numerical_props = {}
    
    # Safely extract numeric columns
    for col in selected_material_row.index:
        # Skip serial column and null values
        if col == "serial" or pd.isna(selected_material_row[col]):
            continue
            
        # Check if the column value is numeric
        try:
            # Try to convert to float to test if it's numeric
            val = float(selected_material_row[col])
            numerical_props[col] = val
        except (ValueError, TypeError):
            # Skip if not convertible to float
            continue

    return numerical_props


def render_property_importance(tab_index, numerical_props, materials_df):
    """
    Renders selective property importance sliders for weighting properties.
    
    Args:
        tab_index: Unique tab index for scoping Streamlit component keys
        numerical_props: Dictionary of numerical properties and their values
        materials_df: DataFrame containing all materials data
        
    Returns:
        dict: Dictionary of properties and their importance values
    """
    # st.markdown("### Property Importance")
    # st.caption("Select and adjust importance of key material properties")
    
    # Initialize the property weights dictionary
    property_weights = {}
    
    # Get list of valid properties (excluding NaN values)
    valid_props = [prop for prop, value in numerical_props.items() if not pd.isna(value)]
    
    # Initialize session state for selected properties if not exists
    state_key = f"selected_props_{tab_index}"
    if state_key not in st.session_state:
        st.session_state[state_key] = []
        # Pre-select 2-3 of the most commonly important properties if available
        # common_important_props = ['Tensile_Strength', 'Elastic_Modulus', 'Thermal_Conductivity',
        #                        'CTE', 'Tg', 'Density']
        # pre_selected = [p for p in common_important_props if p in valid_props][:2]
        # st.session_state[state_key] = pre_selected if pre_selected else valid_props[:2] if len(valid_props) >= 2 else valid_props
    
    # Add property selector with multiselect
    selected_props = st.multiselect(
        "Select properties to adjust importance:",
        options=valid_props,
        default=st.session_state[state_key],
        key=f"prop_multiselect_{tab_index}",
        help="Choose which properties are relevant for your application"
    )
    
    # Update session state with selected properties
    st.session_state[state_key] = selected_props
    
    # Show compact table of selected properties with importance selectors
    if selected_props:
        # Use simple select boxes instead of sliders
        # Define importance levels with their corresponding numerical values
        importance_options = ["Low", "Medium", "High"]
        importance_values = {"Low": 25, "Medium": 50, "High": 90}
        
        for prop in selected_props:
            value = numerical_props[prop]
            
            # Use columns for compact layout
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.caption(f"**{prop}**")
                
            with col2:
                # Create a unique key for this selector
                selector_key = f"prop_importance_{tab_index}_{prop}"
                
                # Use select box for Low/Medium/High with default of Medium
                importance_label = st.select_slider(
                    "",
                    options=importance_options,
                    value=st.session_state.get(selector_key, "Medium"),
                    key=selector_key,
                    label_visibility="collapsed"
                )
                
                # Convert label to numerical value
                importance_value = importance_values.get(importance_label, 50)
            
            with col3:
                # Display just the property value in compact form
                st.caption(f"({value:.1f})")
            
            # Add the property importance to the return dictionary
            property_weights[prop] = {
                "value": value,
                "importance": importance_value,
                "level": importance_label  # Also store the text level for reference
            }
    else:
        st.info("Select property to indicate importance")
    
    # No need for percentile note anymore
    return property_weights


def render_application_domain_focus(tab_index, applications_df=None):
    """
    Renders UI for selecting application domains to focus on.
    Dynamically populates the domains from the applications DataFrame's 'industry' column.
    
    Args:
        tab_index: Unique tab index for scoping Streamlit component keys
        applications_df: DataFrame containing applications data with 'industry' column
        
    Returns:
        list: Selected application domains
    """
    # st.markdown("### Domain Focus")
    # st.caption("Select application areas")
    
    # Initialize session state for domain selection
    if "selected_domains" not in st.session_state:
        st.session_state.selected_domains = []
    
    # Dynamically retrieve domains from applications DataFrame if available
    if applications_df is not None and 'industry' in applications_df.columns:
        try:
            # Get unique industry values and sort them
            domains = sorted(applications_df['industry'].unique().tolist())
            if not domains:  # Fallback if no values found
                domains = get_fallback_domains()
        except Exception as e:
            domains = get_fallback_domains()
    else:
        # Fallback to default domains if applications_df not available
        domains = get_fallback_domains()
    
    selected_domains = st.multiselect(
        "Industry Focus",
        options=domains,
        default=st.session_state.selected_domains,
        key=f"domains_{tab_index}"
    )
    
    # Update session state
    st.session_state.selected_domains = selected_domains
    
    return selected_domains


def render_supply_chain_preferences(tab_index):
    """
    Renders UI for setting supply chain preferences.
    
    Args:
        tab_index: Unique tab index for scoping Streamlit component keys
        
    Returns:
        dict: Supply chain preferences
    """
    # st.markdown("### Supply Chain")
    # st.caption("Supply requirements")
    
    # Initialize preferences dictionary
    preferences = {}
        
    # Lead time and cost in columns for compactness
    # col1, col2 = st.columns(2)
    
    #with col1:
    # Maximum acceptable lead time - more important than the slider
    preferences["lead_time_max"] = st.number_input(
        "Max lead time (weeks)",
        min_value=1,
        max_value=52,
        value=8,
        key=f"lead_time_max_{tab_index}"
    )

    #with col2:
    # Cost importance - simple selection
    cost_options = {"Low": 25, "Medium": 50, "High": 75, "Critical": 100}
    cost_importance = st.selectbox(
        "Cost priority",
        options=list(cost_options.keys()),
        index=1,  # Medium by default
        key=f"cost_imp_sel_{tab_index}"
    )
    preferences["cost_importance"] = cost_options[cost_importance]
    
    # Domestic preference
    preferences["domestic_preferred"] = st.checkbox(
        "Domestic suppliers",
        value=False,
        key=f"domestic_pref_{tab_index}"
    )

    return preferences


def render_sustainability_preferences(tab_index):
    """
    Renders UI for setting sustainability preferences.
    Implements enhanced sustainability analysis from the material matching improvements.
    
    Args:
        tab_index: Unique tab index for scoping Streamlit component keys
        
    Returns:
        dict: Sustainability preferences
    """
    # st.markdown("### Sustainability")
    # st.caption("Environmental factors")
    
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
    
    # Carbon importance - simplified as radio
    #carbon_options = {"Low": 25, "Medium": 50, "High": 75}
    #selected_carbon = st.radio(
    #    "Carbon footprint priority",
    #    options=list(carbon_options.keys()),
    #    index=1,  # Medium by default
    #    key=f"carbon_radio_{tab_index}",
    #    horizontal=True
    #)
    #preferences["carbon_footprint_importance"] = carbon_options[selected_carbon]
    
    return preferences


def render_application_matching_preferences(tab_index, materials_df, selected_material_row, applications_df=None):
    """
    Master function that renders a comprehensive interface for setting application matching
    preferences after material selection. Uses modular components for different preference areas.
    
    This function replaces the redundant filtering approach with a more specialized
    interface for application matching based on material properties.
    
    Args:
        tab_index: Unique tab index for scoping Streamlit component keys
        materials_df: DataFrame containing all materials data
        selected_material_row: Selected material as a DataFrame row
        applications_df: DataFrame containing applications data (optional)
    
    Returns:
        dict: Comprehensive matching preferences to guide application recommendations
    """
    # st.subheader("Application Matching Preferences")
    
    # Extract numerical properties
    numerical_props = extract_numerical_properties(selected_material_row)
    
    # Check if we have properties to work with
    if not numerical_props:
        st.warning("No numerical properties available for this material for application matching.")
        return {}
    
    matching_preferences = {}
    
    with st.expander("Application Matching Preferences", expanded=False):
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])  # Adjust column widths as needed
        
        # Column 1: Property importance matrix (wider column for sliders)
        with col1:
            property_weights = render_property_importance(tab_index, numerical_props, materials_df)
            matching_preferences["property_weights"] = property_weights
        
        # Column 2: Application domain focus
        with col2:
            selected_domains = render_application_domain_focus(tab_index, applications_df)
            matching_preferences["application_domains"] = selected_domains
        
        # Column 3: Supply chain preferences
        with col3:
            supply_chain_prefs = render_supply_chain_preferences(tab_index)
            matching_preferences["supply_chain"] = supply_chain_prefs
        
        # Column 4: Sustainability criteria
        with col4:
            sustainability_prefs = render_sustainability_preferences(tab_index)
            matching_preferences["sustainability"] = sustainability_prefs
    
    return matching_preferences