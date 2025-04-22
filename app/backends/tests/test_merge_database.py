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

def display_merged_database_summary(databases: dict):
    """
    Display the original and merged DataFrames for each category in Streamlit.
    
    :param databases: Dictionary of databases, where each category includes original and merged DataFrames.
    """
    st.title("Merged Database Summary")

    for category, data in databases.items():
        st.header(f"Category: {category.capitalize()}")

        # Display original DataFrames
        st.subheader("Original DataFrames")
        for i, df in enumerate(data["dataframes"]):
            st.write(f"Original DataFrame {i + 1}")
            st.dataframe(df)

        # Display merged DataFrame
        if "merged" in data:
            st.subheader("Merged DataFrame")
            st.dataframe(data["merged"])
        else:
            st.warning("No merged DataFrame available for this category.")