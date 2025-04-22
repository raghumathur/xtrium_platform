#==========================================================================================
# Importing modules, classes, and type hints from a custom helper module `import_helpers`.
# This module is located in the `app.utils` package and streamlines the import of commonly used items.

# `os`: A built-in Python module that provides functions to interact with the operating system, 
#       such as handling file paths, directories, and environment variables.

# `pd`: An alias for the popular data analysis library `pandas`. 
#       It is used for manipulating and analyzing data stored in DataFrames.

# `Dict`: A type hint from Python's `typing` module, used to annotate dictionaries with specific key and value types.
#         For example, `Dict[str, int]` represents a dictionary with string keys and integer values.

# `Union`: A type hint from Python's `typing` module, allowing the specification of multiple possible types 
#          for a variable. For example, `Union[int, str]` means a variable can be either an integer or a string.

# `List`: A type hint from Python's `typing` module, used to annotate lists with a specific element type.
#         For example, `List[int]` represents a list containing integers.

from app.utils.import_helpers import st, pd, Dict, Union, List
#==========================================================================================

# Assuming load_databases() is already implemented and imported
# from your_database_module import load_databases
 
def display_database_summary(databases: Dict[str, Dict[str, Union[List[pd.DataFrame], List[str]]]]):
    """
    Display a summary of databases in Streamlit.
    
    :param databases: The dictionary of loaded databases.
    """
    st.title("Database Summary")

    # Iterate over each category
    for category, data in databases.items():
        st.header(f"Category: {category.capitalize()}")

        # Display file names
        st.subheader("Files:")
        st.write(data["names"])

        # Display dataframes
        for name, df in zip(data["names"], data["dataframes"]):
            st.subheader(f"Preview of {name}")
            st.dataframe(df.head())  # Show the first few rows of the DataFrame