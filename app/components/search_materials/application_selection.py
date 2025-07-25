#==========================================================================================
# Import the Streamlit library through a custom helper function from the app's utilities module.
# This allows for centralized handling of the Streamlit import, making it easier to manage and mock for testing.
from app.utils.import_helpers import st, np, pd

# Import the function to extract dataframes from the database.
# This function likely provides a way to retrieve structured data (e.g., materials or applications) for use in the app.
from app.backends.database.dataframes import extract_dataframes

# Import the functions to render application filters in the app.
# These are responsible for displaying filter UI components for application properties and recommendations.
from app.components.search_materials.application_filters import (
    render_application_selection_filters, property_range_filters, material_type_filters,
    industry_filters, render_material_matching_preferences
)

# Import the function to generate material suggestions.
# This function provides recommendations or matches for materials based on the user's input or selected criteria.
from app.components.search_materials.material_suggestions import get_recommendations
#==========================================================================================

def unified_application_selection(applications_df):
    """
    Unified application selection with progressive filtering.
    
    Combines industry selection and database browsing with
    advanced filtering capabilities. All filter UI rendering is delegated
    to the render_application_selection_filters function.
    
    Args:
        applications_df (pd.DataFrame): Applications database DataFrame
        
    Returns:
        str or None: Selected application name or None if no selection
    """
    # Use the consolidated application filter rendering function
    # This will render all filter UI and return the filtered applications dataframe
    filtered_applications = render_application_selection_filters(applications_df)
    
    # If no applications match filters, return None
    if filtered_applications.empty:
        return None
        
    # Create formatted application name options for selection
    def format_application_name(row):
        # Handle potential missing values in any column
        use_case = str(row.get('Use-case', '')) if pd.notna(row.get('Use-case')) else 'Unknown'
        industry = str(row.get('Industry', '')) if pd.notna(row.get('Industry')) else 'Unknown'
        
        return f"{use_case} ({industry})"
    
    formatted_applications = filtered_applications.apply(format_application_name, axis=1).tolist()
    
    # Create a mapping for display names to actual application names
    display_to_name_map = {}
    for idx, row in filtered_applications.iterrows():
        display_name = format_application_name(row)
        application_name = row.get('Use-case', '')
        display_to_name_map[display_name] = application_name
    
    # Add the mapping to session state for later use
    st.session_state["application_display_map"] = display_to_name_map
    
    # Add divider before application selection
    st.divider()
    
    # Select an application from the filtered list
    st.markdown("### Select Application")
    selected_application_display = st.selectbox(
        "Select an application from the filtered list:",
        options=formatted_applications,
        key="selected_application_display"
    )
    
    # Get the actual application name from the display name
    if selected_application_display and selected_application_display in display_to_name_map:
        selected_application = display_to_name_map[selected_application_display]
        st.session_state["selected_application_name"] = selected_application
        return selected_application
    
    return None

def get_selected_application(applications_df):
    """
    Handles the application selection functionality for the material search.
    This function now uses the unified application selection approach.

    Args:
        applications_df (pd.DataFrame): Unified applications database DataFrame
        
    Returns:
        str: The name of the selected application, or None if no selection is made
    """
    # Use the unified application selection interface
    selected_application = unified_application_selection(applications_df)
    
    return selected_application

def find_materials():
    """
    Processes input data to identify and recommend materials based on selected applications and dynamic filters.
    
    Uses the unified application selection interface to allow users to filter and select applications,
    then applies importance weights to properties for recommendation tuning.
    
    Steps:
        1. Extract dataframes from the databases.
        2. Present unified application selection UI with progressive filtering.
        3. Apply property importance weights for the selected application.
        4. Provide material recommendations based on the selected application and weights.
    """

    # Initialize data structures to default values
    selected_application = None
    selected_application_row = None 

    # Extract DataFrames from session state databases
    materials_df, applications_df, costs_df, suppliers_df = extract_dataframes(st.session_state.databases)

    # Use the unified application selection interface
    # This combines material type, industry, and property filtering before application selection
    selected_application = get_selected_application(applications_df)

    if selected_application:
        # Get the actual application name and find its properties
        selected_application_name = st.session_state.get("selected_application_name", selected_application)
        
        # Get the matching applications - ensure consistent string type for comparison
        matching_applications = applications_df[applications_df["Use-case"].astype(str) == str(selected_application_name)]
        
        # Check if we found any matches
        if matching_applications.empty:
            st.error(f"No application found with name: {selected_application_name}")
            return
            
        selected_application_row = matching_applications.iloc[0]

    # Monitor selected application for changes and reset recommendation weights if needed
    if "previous_selected_application" not in st.session_state:
        st.session_state["previous_selected_application"] = None    

    # Check if the selected application has changed
    if st.session_state.get("previous_selected_application") != selected_application:
        # Reset property weights when application changes
        st.session_state["filters"] = []  
        st.session_state["previous_selected_application"] = selected_application

    # Apply material matching preferences if an application is selected
    matching_preferences = {}
    if selected_application and selected_application_row is not None and not selected_application_row.empty:
        # Use the new modular material matching preferences system
        # This provides a comprehensive UI for property importance weighting,
        # constituent elements focus, supply chain and sustainability preferences
        matching_preferences = render_material_matching_preferences(
            tab_index=0,
            applications_df=applications_df,
            selected_application_row=selected_application_row,
            materials_df=materials_df
        )
   
    # Generate recommendations if an application is selected
    if selected_application and selected_application_row is not None and not selected_application_row.empty:
        #st.markdown("### Material Recommendations")
        
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
        
        # Get recommendations based on application properties and matching preferences
        get_recommendations(
            materials_df,
            selected_application_row,
            property_weights,
            suppliers_df,
            # Pass additional preferences that may be used in enhanced recommendation logic
            elements=matching_preferences.get("constituent_elements", []),
            supply_chain=matching_preferences.get("supply_chain", {}),
            sustainability=matching_preferences.get("sustainability", {})
        )