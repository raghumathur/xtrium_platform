#==========================================================================================
# Import the Streamlit library through a custom helper function from the app's utilities module.
# This allows for centralized handling of the Streamlit import, making it easier to manage and mock for testing.
from app.utils.import_helpers import st, np, pd

# Import the function to extract dataframes from the database.
# This function likely provides a way to retrieve structured data (e.g., materials or applications) for use in the app.
from app.backends.database.dataframes import extract_dataframes

# Import utility functions for working with periodic table data and chemical formulas:
# - `parse_formula`: Parses a chemical formula into its component elements and their quantities.
from app.utils.periodic_table import load_periodic_table, parse_formula

# Import the material helper functions for unified material selection
from app.utils.material_helpers import filter_by_elements, filter_by_material_types, create_display_to_name_map

# Import the functions to render material filters in the app.
# These are responsible for displaying filter UI components for material properties and recommendations.
from app.components.search_applications.material_filters import (
    render_filters, render_material_selection_filters, property_range_filters, material_type_filters,
    periodic_element_filters, render_application_matching_preferences
)
from app.utils.property_filters import materials_property_filters

# Import the function to generate application suggestions.
# This function provides recommendations or matches for applications based on the user's input or selected criteria.
from app.components.search_applications.application_suggestions import get_recommendations
#==========================================================================================

def unified_material_selection(materials_df):
    """
    Unified material selection with progressive filtering.
    
    Combines periodic table element selection and database browsing with
    advanced filtering capabilities. All filter UI rendering is delegated
    to the render_material_selection_filters function.
    
    Args:
        materials_df (pd.DataFrame): Materials database DataFrame
        
    Returns:
        str or None: Selected material name or None if no selection
    """
    # Use the consolidated material filter rendering function
    # This will render all filter UI and return the filtered materials dataframe
    filtered_materials = render_material_selection_filters(materials_df)
    
    # If no materials match filters, return None
    if filtered_materials.empty:
        return None
        
    # Create formatted material name options for selection with improved NaN handling
    def format_material_name(row):
        # Handle potential missing values in any column
        chemical_formula = str(row['chemical_formula']) if pd.notna(row.get('chemical_formula')) else 'Unknown'
        
        # Use commercial_name if available, otherwise use canonical_name if available
        if pd.notna(row.get('commercial_name')):
            return f"{row['commercial_name']} ({chemical_formula})"
        elif pd.notna(row.get('canonical_name')):
            return f"{row['canonical_name']} ({chemical_formula})"
        else:
            return chemical_formula
    
    formatted_materials = filtered_materials.apply(format_material_name, axis=1).tolist()
    
    # Create a mapping for display names to actual material names
    display_to_name_map = create_display_to_name_map(filtered_materials)
    
    # If no mapping was created, return None
    if not display_to_name_map:
        st.error("Could not create material name mappings.")
        return None
        
    # Add the mapping to session state for later use
    st.session_state["material_display_map"] = display_to_name_map
    
    # Add divider before material selection
    st.divider()
    
    # Select a material from the filtered list
    # Convert all chemical_formula values to strings before sorting to avoid type comparison errors
    filtered_material_names = sorted(filtered_materials["chemical_formula"].astype(str).unique().tolist())
    selected_material = st.selectbox(
        "Select Material",
        options=formatted_materials,
        index=0 if formatted_materials else None,
        key="unified_material_selector"
    )
    
    # Add divider after material selection
    st.divider()
    
    # Get the actual material name from the mapping
    if selected_material:
        selected_material_name = display_to_name_map.get(selected_material)
        st.session_state["selected_material_name"] = selected_material_name
        
        # Show selected material details
        # Check if there are any materials matching the selected name before accessing the first row
        # Ensure consistent string type comparison to prevent type mismatches
        matched_materials = filtered_materials[filtered_materials["chemical_formula"].astype(str) == str(selected_material_name)]
        if matched_materials.empty:
            st.warning(f"No material found with the formula: {selected_material_name}")
            return None
        
        selected_row = matched_materials.iloc[0]
    
        # Store numerical properties for use in application suggestions
        numerical_properties = {}
        for col in selected_row.index:
            # Skip null values
            if pd.isna(selected_row[col]):
                continue
                
            # Check if the value is numeric
            try:
                # Convert to float to test if it's numeric
                val = float(selected_row[col])
                numerical_properties[col] = val
            except (ValueError, TypeError):
                # Skip non-numeric values
                continue
                
        # Store the numerical properties in session state for later use
        st.session_state["material_numerical_properties"] = numerical_properties
        
        with st.expander("Selected Material Details", expanded=True):
            # Dynamically populate properties from the selected material row
            # Skip internal or metadata fields that aren't meaningful to display
            skip_columns = ['index', 'serial', '_id', 'id', 'timestamp', 'source', 'batch', 'property_overlap']
            
            # Collect all valid properties
            details = {}
            for col in selected_row.index:
                # Skip null values and specified columns
                if pd.isna(selected_row[col]) or col.lower() in skip_columns:
                    continue
                    
                # Add to details dictionary
                details[col] = selected_row[col]
            
            # Determine number of columns for display based on number of properties
            num_properties = len(details)
            if num_properties <= 4:
                num_cols = 2
            elif num_properties <= 9:
                num_cols = 3
            else:
                num_cols = 4
                
            # Create the appropriate number of columns
            cols = st.columns(num_cols)
            
            # Calculate properties per column (rounded up)
            props_per_col = (num_properties + num_cols - 1) // num_cols
            
            # Display properties in columns
            for i, (k, v) in enumerate(details.items()):
                col_idx = i // props_per_col
                # Ensure we don't exceed the number of columns
                col_idx = min(col_idx, num_cols - 1)
                with cols[col_idx]:
                    # Format the property name and value
                    property_name = k.replace('_', ' ').title()
                    
                    # Handle different value types
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        # Format numbers with appropriate precision
                        if float(v).is_integer():
                            formatted_value = f"{int(v)}"
                        else:
                            formatted_value = f"{v:.4g}"
                    else:
                        # Convert to string for display
                        formatted_value = str(v)
                        
                    st.write(f"**{property_name}:** {formatted_value}")
        
        return selected_material_name
        
    return None


def get_selected_materials(materials_df):
    """
    Handles the material selection functionality for the application.
    This function now uses the unified material selection approach.

    Args:
        materials_df (pd.DataFrame): Unified materials database DataFrame
        
    Returns:
        str: The name of the selected material, or None if no selection is made
    """
    # Use the unified material selection interface
    selected_material = unified_material_selection(materials_df)
    return selected_material


def build_from_periodic_table(materials_df):
    """
    Function to filter and shortlist materials based on selected elements from the periodic table.
    This function uses Streamlit widgets to provide an interactive interface for selecting elements,
    filtering materials, and displaying the shortlisted materials.

    Parameters:
        materials_df (pd.DataFrame): A DataFrame containing materials data with at least a 'name' column.

    Returns:
        selected_materials (list): The list of selected materials from the shortlisted options.
    """

    # Ensure session state variables are initialized
    # These variables store user selections and data persistence across Streamlit reruns
    if "selected_pt_elements" not in st.session_state:
        st.session_state["selected_pt_elements"] = []  # Stores selected periodic table elements
    if "shortlisted_names" not in st.session_state:
        st.session_state["shortlisted_names"] = []  # Stores names of shortlisted materials
    if "shortlisted_materials" not in st.session_state:
        st.session_state["shortlisted_materials"] = []  # Stores the final selected materials

    # Variable to hold the final selected materials; initialized to None
    selected_materials = None

    # Load the full periodic table for element selection
    # `load_periodic_table` is assumed to return a list of element names
    periodic_table = load_periodic_table()

    # Divide the layout into three columns: element selection, action button, and shortlisted materials
    col_elements, col_button, col_shortlist = st.columns([10, 1, 10])
    # Create a placeholder for displaying warning messages outside the columns
    warning_placeholder = st.empty()

    # Column for selecting elements from the periodic table
    with col_elements:
        # Multiselect widget for users to choose elements; updates session state
        selected_pt_elements = st.multiselect(
            "Select Elements",  # Widget label
            options=periodic_table,  # List of all elements
            # default=st.session_state["selected_pt_elements"],  # Pre-fill with existing session state
            key="selected_pt_elements",  # Unique key for the widget
        )

    # Clear shortlisted materials if no elements are selected
    if not st.session_state["selected_pt_elements"]:
        st.session_state["shortlisted_names"] = []

    # Column for the action button to filter materials
    with col_button:
        # Add some vertical spacing to align the button with the other columns
        st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
        # Button to trigger the shortlisting process
        if st.button("🢂", key="pt_shortlist_button"):
            if not st.session_state["selected_pt_elements"]:
                # Display a warning if no elements are selected
                warning_placeholder.warning("Please select at least one element to create compounds.")
            else:
                # Extract the chemical symbols of selected elements
                element_symbols = extract_symbols(st.session_state["selected_pt_elements"])

                # Check if the 'name' column exists in the materials DataFrame
                if "chemical_formula" in materials_df.columns:
                    # Filter materials that contain all selected element symbols in their formulas
                    # Get shortlisted materials based on selected elements
                    shortlisted_df = materials_df[
                        materials_df["chemical_formula"].apply(
                            lambda x: all(symbol in parse_formula(x) for symbol in element_symbols)
                        )
                    ]
                    # Create formatted list of "remarks (name)" for each material
                    formatted_names = shortlisted_df.apply(
                        lambda row: f"{row['commercial_name']} ({row['chemical_formula']})" if pd.notna(row['commercial_name']) else row['chemical_formula'],
                        axis=1
                    )
                    # Convert to a set to remove duplicates, then back to sorted list
                    shortlisted_names = sorted(set(formatted_names))
                    
                    # Update session state with the unique shortlisted material names
                    st.session_state["shortlisted_names"] = shortlisted_names
                    
                    # Create a mapping from display names to chemical formulas
                    # For each display name, find its corresponding row in shortlisted_df
                    mapping = {}
                    for display_name in shortlisted_names:
                        # If display name is just the formula (no remarks)
                        if '(' not in display_name:
                            mapping[display_name] = display_name
                        else:
                            # Extract the formula from the display name (it's in parentheses)
                            formula = display_name[display_name.rfind('(') + 1:display_name.rfind(')')]
                            mapping[display_name] = formula
                    
                    st.session_state["shortlisted_mapping"] = mapping
                else:
                    # Display a warning if the 'chemical_formula' column is missing
                    warning_placeholder.warning("There was an issue accessing the database")
                    print("'chemical_formula' column not found in the materials database.")

    # Column for displaying shortlisted materials
    with col_shortlist:
        # Dropdown to select from the shortlisted materials
        if "shortlisted_names" in st.session_state:
            selected = st.selectbox(
                "Shortlisted Materials",  # Widget label
                options=st.session_state["shortlisted_names"],  # List of formatted names
                key="shortlisted_materials",  # Unique key for the widget
            )
            # Store the actual chemical formula in session state if a selection is made
            if selected:
                st.session_state["selected_material_name"] = st.session_state["shortlisted_mapping"][selected]
        else:
            # Display an empty dropdown if no materials are shortlisted
            st.selectbox(
                "Shortlisted Materials",
                options=[],
                key="shortlisted_materials",
            )

        # Retrieve the final selected materials from the session state
        if st.session_state["shortlisted_materials"]:
            selected_materials = st.session_state["shortlisted_materials"]

    # Return the final list of selected materials
    return selected_materials


def browse_materials_list(materials_df):
    """
    Function to display a list of materials from a DataFrame using Streamlit
    and allow the user to select one material from the list.

    Args:
        materials_df (pd.DataFrame): A pandas DataFrame containing material data.
                                     Must include columns named 'name' and 'remarks'.

    Returns:
        selected_materials (str or None): The name of the selected material, or None if no selection is made.
    """
    
    # Initialize the variable to store the user's selection.
    # Initially set to None in case no selection is made or there's an issue with the data.
    selected_materials = None

    # Check if the DataFrame contains a column named 'name' which is required for displaying material options.
    if "chemical_formula" in materials_df.columns:
        # Create formatted display options with "remarks (name)" format similar to build_from_periodic_table
        formatted_options = materials_df.apply(
            lambda row: f"{row['commercial_name']} ({row['chemical_formula']})" if pd.notna(row['commercial_name']) else row['chemical_formula'],
            axis=1
        ).tolist()
        
        # Create a mapping from formatted display names to actual material names
        name_mapping = {}
        for i, display_name in enumerate(formatted_options):
            name_mapping[display_name] = materials_df['name'].iloc[i]
        
        # Store the mapping in session state for later reference
        if "material_name_mapping" not in st.session_state:
            st.session_state["material_name_mapping"] = {}
        st.session_state["material_name_mapping"] = name_mapping
        
        # Display the dropdown with formatted options
        selected_option = st.selectbox(
            "Select a Material",  # Label for the select box displayed in the UI.
            options=formatted_options,  # List of formatted options
            key="compound_selection"  # Key to identify the widget in Streamlit's session state.
        )
        
        # Map the selected formatted option back to the actual material name
        if selected_option:
            selected_materials = name_mapping[selected_option]
            # Store the material name in session state for consistency with build_from_periodic_table
            st.session_state["selected_material_name"] = selected_materials
    else:
        # Display a warning message in the Streamlit app if the 'name' column is missing from the DataFrame.
        st.warning("There was an issue accessing the database")
        
        # Print an error message in the console for debugging purposes.
        print("'chemical_formula' column not found in the materials database.")

    # Return the selected material name (or None if no selection is made).
    return selected_materials


def find_applications():
    """
    Processes input data to identify and recommend applications based on selected materials and dynamic filters.
    
    Uses the unified material selection interface to allow users to filter and select materials,
    then applies importance weights to properties for recommendation tuning.
    
    Steps:
        1. Extract dataframes from the databases.
        2. Present unified material selection UI with progressive filtering.
        3. Apply property importance weights for the selected material.
        4. Provide application recommendations based on the selected material and weights.
    """

    # Initialize data structures to default values
    selected_material = None
    selected_material_row = None 

    # Extract DataFrames from session state databases
    materials_df, applications_df, costs_df, suppliers_df = extract_dataframes(st.session_state.databases)

    # Use the unified material selection interface
    # This combines material type, element, and property filtering before material selection
    selected_material = get_selected_materials(materials_df)

    if selected_material:
        # Get the actual material name and find its properties
        selected_material_name = st.session_state.get("selected_material_name", selected_material)
        
        # Get the matching materials - ensure consistent string type for comparison
        matching_materials = materials_df[materials_df["chemical_formula"].astype(str) == str(selected_material_name)]
        
        # Check if we found any matches
        if matching_materials.empty:
            st.error(f"No material found with name: {selected_material_name}")
            return
            
        selected_material_row = matching_materials.iloc[0]

    # Monitor selected material for changes and reset recommendation weights if needed
    if "previous_selected_material" not in st.session_state:
        st.session_state["previous_selected_material"] = None    

    # Check if the selected material has changed
    if st.session_state.get("previous_selected_material") != selected_material:
        # Reset property weights when material changes
        st.session_state["filters"] = []  
        st.session_state["previous_selected_material"] = selected_material

    # Apply application matching preferences if a material is selected
    matching_preferences = {}
    if selected_material and selected_material_row is not None and not selected_material_row.empty:
        # Use the new modular application matching preferences system
        # This provides a comprehensive UI for property importance weighting,
        # application domain focus, supply chain and sustainability preferences
        matching_preferences = render_application_matching_preferences(
            tab_index=0,
            materials_df=materials_df,
            selected_material_row=selected_material_row,
            applications_df=applications_df
        )
   
    # Generate recommendations if a material is selected
    if selected_material and selected_material_row is not None and not selected_material_row.empty:
        #st.markdown("### Application Recommendations")
        
        # Extract property weights for compatibility with current recommendation engine
        property_weights = []
        if "property_weights" in matching_preferences:
            # Convert the new property weight format to the format expected by get_recommendations
            property_weights = [
                {
                    "parameter": prop,
                    "value": data["value"],
                    "weightage": data["importance"]
                } for prop, data in matching_preferences["property_weights"].items()
            ]
        
        # Get recommendations based on material properties and matching preferences
        get_recommendations(
            applications_df,
            selected_material_row,
            property_weights,
            suppliers_df,
            # Pass additional preferences that may be used in enhanced recommendation logic
            domains=matching_preferences.get("application_domains", []),
            supply_chain=matching_preferences.get("supply_chain", {}),
            sustainability=matching_preferences.get("sustainability", {})
        )