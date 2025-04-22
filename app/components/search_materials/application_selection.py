#==========================================================================================
# Import necessary modules and libraries from the application's utility helpers.

# Import the Streamlit library using a custom helper from the app's utilities.
# This ensures that the Streamlit library is accessed consistently throughout the application.

from app.utils.import_helpers import st
#==========================================================================================

def render_application_selection(applications_df):
    """
    Handles the application selection functionality, including
    "Filter by Industry Vertical" and "Select Specific Applications".

    :param applications_df: Unified applications database DataFrame.
    """
    selection_type = st.radio(
        "How would you like to filter applications?",
        ["Select industry vertical", "Select field of research"],
        key="application_selection_type"
    )

    if selection_type == "Select industry vertical":
        query_column = "industry"
    elif selection_type == "Select field of research":
        query_column = "field_of_science"

    appname_column = "use_case"
    # Check if "Industry Vertical" column exists
    if query_column in applications_df.columns:
        # Multiselect for industry verticals
        selected_ifos = st.multiselect(
            "Select Industry Vertical(s) / Field of Study",
            options=sorted(applications_df[query_column].dropna().unique().tolist()),
            key="selected_ifos"
        )

        # Display applications matching selected industries
        if selected_ifos:
            if appname_column in applications_df.columns:
                filtered_applications = applications_df[
                    applications_df[query_column].isin(selected_ifos)
                ][appname_column].tolist()

                st.multiselect(
                    "Applications in Selected Industries",
                    options=filtered_applications,
                    key="filtered_applications"
                )
            else:
                st.warning("There was an issue accessing the database")
                print(f"The column 'application_name' does not exist in the applications database.")
        else:
            st.info("Select industry verticals to view related applications.")
    else:
        st.warning("There was an issue accessing the database")
        print(f"The column 'industry_column' does not exist in the applications database.")
        st.warning()
        # return