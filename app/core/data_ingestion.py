#==========================================================================================
# Import necessary modules and libraries from the application's utility helpers.

# Import the Streamlit library using a custom helper from the app's utilities.
# This ensures that the Streamlit library is accessed consistently throughout the application.

from app.utils.import_helpers import st

# Import the function to load databases from a specific backend module.
# This function is likely responsible for reading data from multiple databases.
from app.backends.database.database_reader import load_databases

# Import the function to merge multiple databases into one.
# This function likely handles the logic of combining databases based on certain rules or requirements.
from app.backends.database.database_merger import merge_databases

# Uncomment the following lines if you need to include test stubs for debugging or testing purposes.

# Import a function to display a summary of the loaded databases.
# This can be helpful for testing or understanding the structure of the databases.
# from app.backends.tests.test_load_database import display_database_summary

# Import a function to display a summary of the merged database.
# This is useful for testing the results of the database merging process.
# from app.backends.tests.test_merge_database import display_merged_database_summary
#==========================================================================================

def data_ingestion(datapath):
    """
    Function to handle the data ingestion process for a specific use case.
    
    This function performs the following steps:
    1. Loads multiple databases categorized into Materials, Applications, Costs, and Suppliers.
    2. Provides optional debugging stubs to verify the loaded data.
    3. Merges the data from the loaded databases for further processing.
    4. Returns the processed databases, allowing flexibility to determine their final use.
    
    Args:
        datapath (str): The file path or directory where the databases are stored.

    Returns:
        dict: A dictionary of merged DataFrames for each category (e.g., Materials, Applications).
        Note: The return value can be customized based on specific requirements.
    """
    # Step 1: Load all databases within each category (Materials, Applications, Costs, Suppliers)
    # This function (load_databases) is assumed to read the databases from the provided `datapath`.
    # It organizes and loads the databases into memory, grouped by their respective categories.
    databases = load_databases(datapath)
    
    # ===========================================================================
    # DEBUGGING STUB: Uncomment the following line to debug/test if the
    # load_databases function worked correctly. This will display a summary
    # of all the loaded databases to ensure they were ingested properly.
    #
    # Example use: Uncomment temporarily to verify data loading during development.
    #
    # display_database_summary(databases)
    # ===========================================================================
    
    # Step 2: Merge DataFrames within each category
    # After loading the databases, this step consolidates the data by merging 
    # multiple DataFrames in each category into a single cohesive DataFrame.
    # The function merge_databases performs the merging logic.
    databases = merge_databases(databases)

    # ===========================================================================
    # DEBUGGING STUB: Uncomment the following line to debug/test if the
    # merge_databases function worked correctly. This will display a summary
    # of the merged databases to ensure the data was processed correctly.
    #
    # Example use: Uncomment temporarily to verify data merging during development.
    #
    # display_merged_database_summary(databases)
    # ===========================================================================
    
    # TODO: Future development step
    # The function currently returns the merged databases, but this may need 
    # to be modified based on specific downstream requirements, such as writing 
    # the data to files, returning only certain categories, or performing additional processing.
    return databases

def init_database():
    """
    Initializes the database by checking and setting up the session state in Streamlit.

    Parameters:
    config (dict): A dictionary containing configuration settings, including paths to database files.

    Returns:
    object: The loaded database object from session state, or `None` if the database is not yet loaded.
    """
    
    # Check if the `databases` key is already present in the session state.
    # If not, initialize `databases` to None and set the loading flag to False.
    if "databases" not in st.session_state:
        st.session_state["databases"] = None  # Placeholder for the database object.
        st.session_state["databases_initialized"] = False  # Flag indicating whether databases are loaded.

    # Proceed with data ingestion only if the databases have not already been loaded.
    if not st.session_state["databases_initialized"]:
        # Display a loading spinner while the database is being loaded.
        with st.spinner("Loading databases... Please wait."):
            # Call the `data_ingestion` function with the configured path to load the databases.
            st.session_state["databases"] = data_ingestion(st.session_state.config["paths"]["databases"])
            # Update the flag to indicate that the databases are now loaded.
            st.session_state["databases_initialized"] = True

    # Retrieve the database object from the session state for further use.
    # databases = st.session_state["databases"]

    # Return the loaded database object. (Further decision on the return value might be needed.)
    return st.session_state["databases_initialized"]
