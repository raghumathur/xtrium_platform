#==========================================================================================
# Import necessary modules and libraries from the application's utility helpers.

# Import the Streamlit library using a custom helper from the app's utilities.
# This ensures that the Streamlit library is accessed consistently throughout the application.

# Import the pandas library as 'pd' for working with structured data such as DataFrames.
# Pandas is commonly used for data manipulation and analysis.

from app.utils.import_helpers import st, pd
#==========================================================================================

def render_filters(tab_index, materials_df, selected_material_row):
    """
    Render dynamic filters for a Streamlit app.

    Features:
    1. Adds and removes filters dynamically with proper indexing.
    2. Synchronizes a slider's min/max values with manual inputs.
    3. Stores all filter selections in Streamlit session state.
    4. Prepares filter data in an organized structure for downstream processes.

    :param tab_index: Unique tab index for scoping Streamlit component keys.
    :param materials_df: DataFrame containing numerical columns for filtering.
    """

    # 1. Extract non-empty numerical columns from the provided DataFrame row, excluding "serial"
    """
    numerical_columns = [col for col in materials_df.select_dtypes(include='number').columns if col != "serial"]

    # If no numerical columns are available, show a warning and stop
    if not numerical_columns:
        st.warning("No numerical columns available in the materials database for filtering.")
        return
    """
    # Initialize relevant columns
    #relevant_columns = []
    #selected_filters = []
    #selected_param = None
    #st.write(relevant_columns)
    # st.write(selected_param)
    # Extract relevant columns
    # relevant_columns = [
    #    col for col in selected_material_row.index
    #    if pd.api.types.is_number(selected_material_row[col]) and col != "serial" and not pd.isna(selected_material_row[col])
    #]
    """
    # If no relevant columns are available, show a warning and stop
    if not relevant_columns:
        st.warning("No relevant columns available in the materials database for filtering.")
        return
    """
    #st.write(relevant_columns)
    
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
            # if not selected_param:
            #     st.session_state["filters"] = []
            #if dbparam
            selected_param = st.selectbox(
                "Parameter",
                options=relevant_columns,  # Options for selection
                index=relevant_columns.index(dbparam) if dbparam else 0,
                key=f"param_{tab_index}_{idx}"
            )
            # Update the selected parameter in session state
            st.session_state["filters"][idx]["parameter"] = selected_param

        # Column 1: Slider for selecting a single value
        with cols[1]:
            # Initializing column_min, column_max
            column_min, column_max = 0.0, 1.0
            # Fetch the column's min and max values for slider initialization
            if selected_param:
                column_min = materials_df[selected_param].min()
                column_max = materials_df[selected_param].max()

            # If the parameter has just been selected, initialize its value in session state
            if "value" not in st.session_state["filters"][idx] or st.session_state["filters"][idx]["parameter"] != selected_param:
                st.session_state["filters"][idx]["value"] = (column_min + column_max) / 2  # Default to midpoint

            # Slider for selecting a single value
            slider_value = st.slider(
                f"{selected_param} Value",
                min_value=float(column_min),
                max_value=float(column_max),
                value=st.session_state["filters"][idx]["value"],  # Default to current value in session state
                #step=(column_max - column_min) / 100,
                key=f"slider_{tab_index}_{idx}"
            )
            # Update session state with the slider value
            st.session_state["filters"][idx]["value"] = slider_value

        # Column 2: Text Input for the value (mirrors the slider)
        with cols[2]:
            # Format the slider value as a default for the text box
            text_value = st.text_input(
                "Value",
                value=f"{slider_value:.2f}",
                key=f"text_value_{tab_index}_{idx}"
            )
            # Update session state with the entered value
            try:
                st.session_state["filters"][idx]["value"] = float(text_value)
            except ValueError:
                pass  # If invalid input, retain the previous slider value

        # Synchronize slider with text input
        with cols[1]:
            slider_value = st.session_state["filters"][idx]["value"]

        # Column 3: Slider for weightage
        with cols[3]:
            weightage = st.slider(
                "Weightage",
                min_value=0,
                max_value=100,
                value=st.session_state["filters"][idx].get("weightage", 50),
                step=5,
                key=f"weightage_{tab_index}_{idx}"
            )
            # Update weightage in session state
            st.session_state["filters"][idx]["weightage"] = weightage

        # Column 4: Delete Button for the current filter
        with cols[4]:
            st.markdown("<div style='height:29px;'></div>", unsafe_allow_html=True)  # Spacing
            if st.button("❌", key=f"remove_filter_{tab_index}_{idx}"):
                st.session_state["filters"].pop(idx)  # Remove the filter at the current index
                st.rerun()  # Force the app to re-render and reflect changes
    
    # 5. Display all active filters in an organized structure
    # st.subheader("Active Filters")
    selected_filters = [
        {
            "parameter": f["parameter"],
            "value": f["value"],
            "weightage": f["weightage"]
        }
        for f in st.session_state["filters"]
        if f.get("parameter") and f.get("value")  # Only include valid filters
    ]
    # st.json(organized_filters)  # Display as JSON

    # 6. Return the organized filters for downstream use
    return selected_filters