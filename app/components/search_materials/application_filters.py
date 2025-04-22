#==========================================================================================
# Import necessary modules and libraries from the application's utility helpers.

# Import the Streamlit library using a custom helper from the app's utilities.
# This ensures that the Streamlit library is accessed consistently throughout the application.

from app.utils.import_helpers import st
#==========================================================================================

def render_application_filters(tab_index, materials_df):
    """
    Render dynamic filters for the material recommendation process.

    :param tab_index: Unique identifier for Streamlit components.
    :param materials_df: DataFrame of materials.
    :return: List of active filters.
    """
    numerical_columns = [col for col in materials_df.select_dtypes(include='number').columns if col != "serial"]

    if not numerical_columns:
        st.warning("No numerical columns available for filtering materials.")
        return []

    if "filters" not in st.session_state:
        st.session_state["filters"] = []

    # Add filter button
    if st.button("➕ Add Filter", key=f"add_filter_button_{tab_index}"):
        st.session_state["filters"].append({
            "parameter": None,
            "value": None,
            "weightage": 50
        })

    for idx, filter_data in enumerate(st.session_state["filters"]):
        cols = st.columns([4, 4, 2, 2, 1])

        with cols[0]:
            selected_param = st.selectbox(
                "Parameter",
                options=numerical_columns,
                index=numerical_columns.index(filter_data.get("parameter")) if filter_data.get("parameter") else 0,
                key=f"param_{tab_index}_{idx}"
            )
            st.session_state["filters"][idx]["parameter"] = selected_param

        with cols[1]:
            if selected_param:
                column_min = materials_df[selected_param].min()
                column_max = materials_df[selected_param].max()

                slider_value = st.slider(
                    f"{selected_param} Value",
                    min_value=float(column_min),
                    max_value=float(column_max),
                    value=filter_data.get("value", (column_min + column_max) / 2),
                    key=f"slider_{tab_index}_{idx}"
                )
                st.session_state["filters"][idx]["value"] = slider_value

        with cols[3]:
            weightage = st.slider(
                "Weightage",
                min_value=0,
                max_value=100,
                value=filter_data.get("weightage", 50),
                step=5,
                key=f"weightage_{tab_index}_{idx}"
            )
            st.session_state["filters"][idx]["weightage"] = weightage

        with cols[4]:
            if st.button("❌", key=f"remove_filter_{tab_index}_{idx}"):
                st.session_state["filters"].pop(idx)
                st.rerun()

    active_filters = [
        f for f in st.session_state["filters"]
        if f.get("parameter") and f.get("value") is not None
    ]
    return active_filters