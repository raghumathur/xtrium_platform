#==========================================================================================
# Import the Streamlit library through a custom helper function from the app's utilities module.
# This allows for centralized handling of the Streamlit import, making it easier to manage and mock for testing.
from app.utils.import_helpers import st, np, pd

# Import the function to extract dataframes from the database.
# This function likely provides a way to retrieve structured data (e.g., materials or applications) for use in the app.
from app.backends.database.dataframes import extract_dataframes

# Import utility functions for working with periodic table data and chemical formulas:
# - `load_periodic_table`: Loads data about chemical elements (e.g., atomic numbers, symbols, names).
# - `extract_symbols`: Extracts element symbols from a given input (e.g., chemical formula).
# - `parse_formula`: Parses a chemical formula into its component elements and their quantities.
from app.utils.periodic_table import load_periodic_table, extract_symbols, parse_formula

# Import the function to render material filters in the app.
# This is likely responsible for displaying filter UI components (e.g., dropdowns, checkboxes) that allow users to refine their search for materials.
from app.components.search_applications.material_filters import render_filters
from app.utils.property_filters import materials_property_filters

# Import the function to generate application suggestions.
# This function provides recommendations or matches for applications based on the user's input or selected criteria.
from app.components.search_applications.application_suggestions import get_recommendations
#==========================================================================================

def get_selected_materials(materials_df):
    """
    Handles the material selection functionality for the application.
    This function allows users to choose between building materials using
    periodic elements or searching from a predefined list of known materials.

    :param materials_df: Unified materials database DataFrame containing
                         information about various materials.
    :param applications_df: DataFrame containing application-specific details
                            for different materials.
    :param costs_df: DataFrame containing cost information for materials.
    :return: Selected materials based on the user's pathway choice.
    """

    # Define the two pathways for material selection
    pathways = ["Build with periodic elements", "Search materials database"]
    # 'pathways' is a list of options presented to the user to guide their
    # material selection process.

    # Create a radio button interface for the user to select their pathway
    selection_type = st.radio(
        "Select a pathway to define your material",  # Title for the input widget
        range(len(pathways)),  # Options are represented by their indices
        format_func=lambda x: pathways[x],  # Display the actual pathway text for each index
        key="material_selection_type"  # Unique key to store this input's state
    )
    # The 'st.radio' widget is used for single-option selection. The user selects
    # either "Build with periodic elements" or "Search known materials", and the
    # corresponding index (0 or 1) is stored in 'selection_type'.

    # Map the user's selection to the corresponding function for material selection
    selected_materials = {0: build_from_periodic_table, 
                          1: browse_materials_list}.get(selection_type, 
                                                        lambda _: None)(materials_df)
    # A dictionary maps the index of the selected pathway (0 or 1) to its corresponding
    # handler function: 'build_from_periodic_table' or 'browse_materials_list'.
    # If the user's choice doesn't match any predefined pathways, a default
    # function returning None is used.
    # The chosen function is then invoked with 'materials_df' as its argument.

    # Return the materials selected based on the user's pathway choice
    return selected_materials


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
    col_elements, col_button, col_shortlist = st.columns([5, 1, 5])
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
                if "name" in materials_df.columns:
                    # Filter materials that contain all selected element symbols in their formulas
                    shortlisted_names = list(
                        set(
                            materials_df[
                                materials_df["name"].apply(
                                    lambda x: all(symbol in parse_formula(x) for symbol in element_symbols)
                                )
                            ]["name"]
                        )
                    )
                    # Update session state with the shortlisted material names
                    st.session_state["shortlisted_names"] = shortlisted_names
                else:
                    # Display a warning if the 'name' column is missing
                    warning_placeholder.warning("There was an issue accessing the database")
                    print("'name' column not found in the materials database.")

    # Column for displaying shortlisted materials
    with col_shortlist:
        # Dropdown to select from the shortlisted materials
        if "shortlisted_names" in st.session_state:
            st.selectbox(
                "Shortlisted Materials",  # Widget label
                options=st.session_state["shortlisted_names"],  # List of shortlisted names
                key="shortlisted_materials",  # Unique key for the widget
            )
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
                                     Must include a column named 'name'.

    Returns:
        selected_materials (str or None): The name of the selected material, or None if no selection is made.
    """
    
    # Initialize the variable to store the user's selection.
    # Initially set to None in case no selection is made or there's an issue with the data.
    selected_materials = None

    # Check if the DataFrame contains a column named 'name' which is required for displaying material options.
    if "name" in materials_df.columns:
        
        # Display a dropdown (select box) for material selection using Streamlit.
        # The dropdown is populated with the list of material names from the 'name' column of the DataFrame.
        selected_materials = st.selectbox(
            "Select a Material",  # Label for the select box displayed in the UI.
            options=materials_df["name"].tolist(),  # List of options derived from the 'name' column.
            key="compound_selection"  # Key to identify the widget in Streamlit's session state.
        )
    else:
        # Display a warning message in the Streamlit app if the 'name' column is missing from the DataFrame.
        st.warning("There was an issue accessing the database")
        
        # Print an error message in the console for debugging purposes.
        print("'name' column not found in the materials database.")

    # Return the selected material name (or None if no selection is made).
    return selected_materials


def find_applications():
    """
    Processes input data to identify and recommend applications based on selected materials and dynamic filters.
    
    Args:
        databases (list): A list of databases containing materials, applications, and costs information.

    Steps:
        1. Extract dataframes from the provided databases.
        2. Determine the selected material based on user interaction or predefined criteria.
        3. Apply dynamic filters for recommendations.
        4. Provide application recommendations based on the selected material and filters.
    """

    # Initialize data structures to default values
    selected_materials = None
    selected_material_row = None 

    # Extract DataFrames
    # Extract relevant dataframes (e.g., materials, applications, and costs) from the input databases.
    materials_df, applications_df, costs_df, suppliers_df = extract_dataframes(st.session_state.databases)

    # Get the selected material
    # This step retrieves a user-selected material based on interactions or criteria defined within the `get_selected_materials` function.
    selected_materials = get_selected_materials(materials_df)
    # Uncomment the line below for debugging or visualization of selected materials.

    # selected_material_row = {col: None for col in materials_df.columns}
    if selected_materials:
        # Filter the materials dataframe to get the row corresponding to the selected material.
        # This assumes `name` is a column in materials_df that uniquely identifies each material.
        selected_material_row = materials_df[materials_df["name"] == selected_materials].iloc[0]
        # Uncomment the line below to inspect the selected material row during debugging.

    # Monitor selected_materials for changes and reset filters if needed
    if "selected_materials" not in st.session_state:
        st.session_state["selected_materials"] = None    

    # Check if the selected material has changed
    if st.session_state["selected_materials"] != selected_materials:
        st.session_state["filters"] = []  # Reset filters
        st.session_state["selected_materials"] = selected_materials
        #st.info("Filters reset due to material change.")

    # Step 3: Dynamic Filters
    # Render dynamic filters based on the materials dataframe and any additional criteria (e.g., user input).
    # Filters help refine recommendations based on user preferences or constraints.
    if selected_materials and selected_material_row is not None and not selected_material_row.empty:
        #dothisthing(0, materials_df, selected_material_row)
        #dothatthing(materials_df, selected_material_row)
        #selected_filters = render_filters(0, materials_df, selected_material_row)
        selected_filters = materials_property_filters(0, materials_df, selected_material_row)
        #st.write(selected_filters)
   
    # Step 4: Generate Recommendations
    # If a material is selected, and its corresponding row exists and is not empty, proceed to generate recommendations.
    if selected_materials and selected_material_row is not None and not selected_material_row.empty:
        # This function provides recommendations for applications based on the selected material, its properties, and the applied filters.
        get_recommendations(applications_df, selected_material_row, selected_filters, suppliers_df)
        # Alternatively, this line can be used to invoke another recommendation function (if implemented differently).
        # recommend_applications_for_material(selected_material_row, applications_df, selected_filters)