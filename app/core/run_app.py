# Importing the streamlit module from the import_helpers module
from app.utils.import_helpers import st

# Import the helper function to initialize session state in the application
from app.utils.import_helpers import init_session_state

# Importing the `load_config` function from the configuration loader module
# This is used to read and load configuration settings for the application
from app.utils.config_loader import load_config

# Importing the `init_database` function from the data ingestion module
# This is responsible for initializing and loading the necessary databases
from app.core.data_ingestion import init_database

# Importing the `render_main_page` function from the main page components module
# This is used to render the main landing page of the application
from app.components.page_elements.main_page import render_main_page
from app.components.page_elements.sidebar import render_sidebar

def run_xtrium():
    """
    Main entry point for the Xtrium app.
    
    This function orchestrates the initialization of configurations and databases,
    and renders the main page of the application. It serves as the starting point
    when the app is run.
    """
    # Call the function to initialize session state
    # This function ensures that necessary session state variables are set up correctly
    # before proceeding with any further operations in the application.
    init_session_state()

    # Load the application configuration settings and store them in the streamlit session state.
    # The configuration file typically contains important parameters such as database paths,
    # API keys, and other settings required for the app's functionality.
    if "config" not in st.session_state:
        st.session_state.config = load_config()

    # Initialize and load all the necessary databases.
    # The `init_database` function uses the loaded configuration to set up connections
    # and prepare databases for use within the app.
    databases_initialized = init_database()

    # (Commented Out) Initialize or reset session state for filters.
    # Streamlit's `st.session_state` is used to store variables that persist across reruns.
    # Uncommenting these lines would reset specific filters and selections for the user.
    # st.session_state["filters"] = []                  # Stores user-applied filters
    # st.session_state["filtered_compounds"] = []      # Stores filtered compounds
    # st.session_state["shortlisted_compounds"] = []   # Stores shortlisted compounds for further actions

    # Initialize sidebar state
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "home"
    if "page" not in st.session_state:
        st.session_state.page = None

    # Render the top pane of the application.
    # The top pane typically displays key metrics or summaries.
    #render_top_pane()

    # Step 4: Render the main landing page.
    # This function generates the main interface of the application,
    # passing the loaded configuration and databases as arguments.
    #render_main_page(config, databases)
    render_main_page()
