#==========================================================================================
# Import necessary modules and libraries from the application's utility helpers.

# Import the Streamlit library using a custom helper from the app's utilities.
# This ensures that the Streamlit library is accessed consistently throughout the application.

# Import the pandas library as 'pd' for working with structured data such as DataFrames.
# Pandas is commonly used for data manipulation and analysis.

from app.utils.import_helpers import st, pd, np
#==========================================================================================

def materials_property_filters(tab_index, materials_df, selected_material_row):

    # Initialize session state to store filters
    # Session state to store filter rows
    if "filters" not in st.session_state:
        st.session_state["filters"] = []

    # Prepare a list of df columns to be represented as filters
    # Columns that are not filters
    not_filters = ["material_id", "name", "remarks", "property_overlap", "commercial_name", "chemical_name", "reference"]

    """
    # Filter columns to exclude NaN/None and omitted columns
    columns_that_are_filters = [
        col for col in materials_df.columns
        if col not in not_filters and not materials_df[col].isna().all()
    ]
    used_filters = [filter_row.get("selected_filter") for filter_row in st.session_state["filters"] if filter_row.get("selected_filter")]
    available_filters = [col for col in columns_that_are_filters if col not in used_filters]
    """

    # Update available and used filters dynamically
    available_filters, used_filters = update_available_filters(
        selected_material_row, st.session_state["filters"], not_filters
    )

    # Add Filter Button
    if st.button("➕ Add Filter", key=f"add_filter_button_{tab_index}"):
        if available_filters:
            st.session_state["filters"].append({"selected_filter": None})  # Add an empty filter row
        else:
            st.warning("No filters remaining to add.")
    
    selected_filters = []

    # Render each filter row
    for idx, filter_row in enumerate(st.session_state["filters"]):    # Create layout for the current filter row with 6 columns
        cols = st.columns([4, 4, 2, 2, 1])

        # Column 0: Drop-down for selecting the filter parameter
        with cols[0]:
            # Create a selectbox to choose a column
            selected_filter = st.selectbox(
                #"", 
                f"Select a Property to Filter By", 
                #columns_that_are_filters,
                available_filters + [filter_row.get("selected_filter")] if filter_row.get("selected_filter") else available_filters,
                #available_filters,
                index=(available_filters + [filter_row.get("selected_filter")]).index(filter_row.get("selected_filter"))
                if filter_row.get("selected_filter") else 0,
                key=f"filter_select_{idx}"
            )
            filter_row["selected_filter"] = selected_filter

        with cols[1]:
            # Handle column type and display appropriate widget
            if selected_filter:
                col_data = materials_df[selected_filter]
                if is_numeric_or_convertible(col_data):  # Check if column is numeric
                    # Slider for numeric columns
                    min_value = col_data.min()
                    max_value = col_data.max()
                    selected_value = st.slider(
                        #f"Select Range for {selected_filter} (Filter {idx+1})",
                        f"Select Range for {selected_filter}",
                        min_value=float(min_value),
                        max_value=float(max_value),
                        value=float(min_value),
                        step=0.1,
                        key=f"filter_value_slider_{idx}"
                    )
                    filter_row["selected_value"] = selected_value
                    print(f"Filtering {selected_filter} with: {selected_value}")

                elif pd.api.types.is_string_dtype(col_data):  # Check if column is text
                    # Selectbox for text columns
                    unique_values = col_data.dropna().unique()  # Get unique values excluding NaN
                    selected_value = st.selectbox(
                        #f"Select Value for {selected_filter} (Filter {idx+1})",
                        f"",
                        options=unique_values,
                        key=f"filter_value_selectbox_{idx}"
                    )
                    filter_row["selected_value"] = selected_value
                    print(f"Filtering {selected_filter} by value: {selected_value}")
                else:
                    print(f"{selected_filter} is neither numeric nor text.")
                    
                filter_row["selected_value"] = selected_value

        with cols[2]:
            # Handle column type and display appropriate widget
            if selected_filter:
                col_data = materials_df[selected_filter]
                if is_numeric_or_convertible(col_data):  # Check if column is numeric
                    manual_value = st.number_input(
                        #f"Manually Enter Value for {selected_filter} (Filter {idx+1})",
                        f"",
                        min_value=float(min_value),
                        max_value=float(max_value),
                        value=filter_row.get("selected_value", float(min_value)),
                        #value=selected_value,
                        step=0.1,
                        key=f"filter_manual_{idx}"
                    )
        if manual_value != filter_row["selected_value"]:
            filter_row["selected_value"] = manual_value
            st.rerun()

        # Column 3: Slider for weightage
        with cols[3]:
            weightage = st.slider(
                #f"Weightage (Filter {idx+1})",
                f"Weightage",
                min_value=0,
                max_value=100,
                #value=st.session_state["filters"][idx].get("weightage", 50),
                #value=50,
                value=filter_row.get("weightage", 50),
                step=5,
                key=f"weightage_slider_{idx}"
            )
            filter_row["weightage"] = weightage

        # Collect the filter's data
        if selected_filter and selected_value is not None:
            selected_filters.append({
                "property": selected_filter,
                "value": selected_value,
                "weightage": weightage
            })
        # Column 4: Delete Button for the current filter
        with cols[4]:
            st.markdown("<div style='height:29px;'></div>", unsafe_allow_html=True)  # Spacing
            if st.button("❌", key=f"remove_filter_{idx}"):
                st.session_state["filters"].pop(idx)  # Remove the filter at the current index
                st.rerun()  # Force the app to re-render and reflect changes

    return selected_filters

def applications_property_filters(tab_index, materials_df):

    # Initialize session state to store filters
    # Session state to store filter rows
    if "filters" not in st.session_state:
        st.session_state["filters"] = []

    # Prepare a list of df columns to be represented as filters
    # Columns that are not filters
    not_filters = ["material_id", "name", "remarks", "property_overlap", "commercial_name", "chemical_name", "reference"]

    # Filter columns to exclude NaN/None and omitted columns
    columns_that_are_filters = [
        col for col in materials_df.columns
        if col not in not_filters and not materials_df[col].isna().all()
    ]
    used_filters = [filter_row.get("selected_filter") for filter_row in st.session_state["filters"] if filter_row.get("selected_filter")]
    available_filters = [col for col in columns_that_are_filters if col not in used_filters]

    """
    # Update available and used filters dynamically
    available_filters, used_filters = update_available_filters_app(
        materials_df, st.session_state["filters"], not_filters
    )
    """

    # Add Filter Button
    if st.button("➕ Add Filter", key=f"add_filter_button_{tab_index}"):
        if available_filters:
            st.session_state["filters"].append({"selected_filter": None})  # Add an empty filter row
        else:
            st.warning("No filters remaining to add.")
    
    selected_filters = []

    # Render each filter row
    for idx, filter_row in enumerate(st.session_state["filters"]):    # Create layout for the current filter row with 6 columns
        cols = st.columns([4, 4, 2, 2, 1])

        # Column 0: Drop-down for selecting the filter parameter
        with cols[0]:
            # Create a selectbox to choose a column
            selected_filter = st.selectbox(
                #"", 
                f"Select a Property to Filter By", 
                columns_that_are_filters,
                #available_filters + [filter_row.get("selected_filter")] if filter_row.get("selected_filter") else available_filters,
                #available_filters,
                #index=(available_filters + [filter_row.get("selected_filter")]).index(filter_row.get("selected_filter"))
                #if filter_row.get("selected_filter") else 0,
                key=f"filter_select_app_{idx}"
            )
            filter_row["selected_filter"] = selected_filter

        with cols[1]:
            # Handle column type and display appropriate widget
            if selected_filter:
                col_data = materials_df[selected_filter]
                if is_numeric_or_convertible(col_data):  # Check if column is numeric
                    # Slider for numeric columns
                    min_value = col_data.min()
                    max_value = col_data.max()
                    selected_value = st.slider(
                        #f"Select Range for {selected_filter} (Filter {idx+1})",
                        f"Select Range for {selected_filter}",
                        min_value=float(min_value),
                        max_value=float(max_value),
                        value=float(min_value),
                        step=0.1,
                        key=f"filter_value_slider_app_{idx}"
                    )
                    filter_row["selected_value"] = selected_value
                    print(f"Filtering {selected_filter} with: {selected_value}")

                elif pd.api.types.is_string_dtype(col_data):  # Check if column is text
                    # Selectbox for text columns
                    unique_values = col_data.dropna().unique()  # Get unique values excluding NaN
                    selected_value = st.selectbox(
                        #f"Select Value for {selected_filter} (Filter {idx+1})",
                        f"",
                        options=unique_values,
                        key=f"filter_value_selectbox_app_{idx}"
                    )
                    filter_row["selected_value"] = selected_value
                    print(f"Filtering {selected_filter} by value: {selected_value}")
                else:
                    print(f"{selected_filter} is neither numeric nor text.")
                    
                filter_row["selected_value"] = selected_value

        with cols[2]:
            # Handle column type and display appropriate widget
            if selected_filter:
                col_data = materials_df[selected_filter]
                if is_numeric_or_convertible(col_data):  # Check if column is numeric
                    manual_value = st.number_input(
                        #f"Manually Enter Value for {selected_filter} (Filter {idx+1})",
                        "",
                        min_value=float(min_value),
                        max_value=float(max_value),
                        value=filter_row.get("selected_value", float(min_value)),
                        #value=selected_value,
                        step=0.1,
                        key=f"filter_manual_app_{idx}"
                    )
        if manual_value != filter_row["selected_value"]:
            filter_row["selected_value"] = manual_value
            st.rerun()

        # Column 3: Slider for weightage
        with cols[3]:
            weightage = st.slider(
                #f"Weightage (Filter {idx+1})",
                f"Weightage",
                min_value=0,
                max_value=100,
                #value=st.session_state["filters"][idx].get("weightage", 50),
                #value=50,
                value=filter_row.get("weightage", 50),
                step=5,
                key=f"weightage_slider_app_{idx}"
            )
            filter_row["weightage"] = weightage

        # Collect the filter's data
        if selected_filter and selected_value is not None:
            selected_filters.append({
                "property": selected_filter,
                "value": selected_value,
                "weightage": weightage
            })
        # Column 4: Delete Button for the current filter
        with cols[4]:
            st.markdown("<div style='height:29px;'></div>", unsafe_allow_html=True)  # Spacing
            if st.button("❌", key=f"remove_filter_app_{idx}"):
                st.session_state["filters"].pop(idx)  # Remove the filter at the current index
                st.rerun()  # Force the app to re-render and reflect changes

    return selected_filters

# Function to check if a column is numeric or convertible to numeric
def is_numeric_or_convertible(col_data):
    if pd.api.types.is_numeric_dtype(col_data):
        return True
    try:
        # Attempt to convert the column to numeric
        pd.to_numeric(col_data.dropna(), errors="raise")
        return True
    except ValueError:
        return False
    
def update_available_filters(selected_material_row, filters, not_filters):
    """
    Calculate columns available for filtering based on selected_material_row.
    Excludes used filters and columns marked as not_filters.
    """
    # Exclude columns marked as not_filters or containing NaN values
    all_filter_columns = [
        col for col in selected_material_row.index
        if col not in not_filters and pd.notna(selected_material_row[col])
    ]
    # Exclude already used filters
    used_filters = [filter_row.get("selected_filter") for filter_row in filters if filter_row.get("selected_filter")]
    available_filters = [col for col in all_filter_columns if col not in used_filters]
    return available_filters, used_filters

def update_available_filters_app(materials_df, filters, not_filters):
    """
    Calculate columns available for filtering based on selected_material_row.
    Excludes used filters and columns marked as not_filters.
    """
    # Exclude columns marked as not_filters or containing NaN values
    all_filter_columns = [
        col for col in materials_df.index
        if col not in not_filters and pd.notna(materials_df[col])
    ]
    # Exclude already used filters
    used_filters = [filter_row.get("selected_filter") for filter_row in filters if filter_row.get("selected_filter")]
    available_filters = [col for col in all_filter_columns if col not in used_filters]
    return available_filters, used_filters