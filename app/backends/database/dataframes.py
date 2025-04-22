#==========================================================================================
# Import the Streamlit library using a custom helper from the app's utilities
from app.utils.import_helpers import st
#==========================================================================================

def extract_dataframes(databases):
        # Ensure materials database and merged DataFrame exist
    if "materials" in databases and "merged" in databases["materials"]:
        materials_df = databases["materials"]["merged"]
    else:
        st.warning("There was an issue accessing the database")
        print("Materials database or merged DataFrame not available.")

    # Ensure applications database and merged DataFrame exist
    if "applications" in databases and "merged" in databases["materials"]:
        applications_df = databases["applications"]["merged"]
    else:
        st.warning("There was an issue accessing the database")
        print("Applications database or merged DataFrame not available.")

    # Ensure costs database and merged DataFrame exist
    if "costs" in databases:
        costs_df = databases["costs"]["merged"]
    else:
        st.warning("There was an issue accessing the database")
        print("Costs database or merged DataFrame not available.")

    # Ensure suppliers database and merged DataFrame exist
    if "suppliers" in databases:
        suppliers_df = databases["suppliers"]["merged"]
    else:
        st.warning("There was an issue accessing the database")
        print("Suppliers database or merged DataFrame not available.")

    return materials_df, applications_df, costs_df, suppliers_df