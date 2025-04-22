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

# `Optional`: A type hint from Python's `typing` module, indicating that a value can either be of the specified type 
#             or `None`. For example, `Optional[str]` means a variable can be either a string or `None`.

from app.utils.import_helpers import os, pd, Dict, Union, List, Optional
#==========================================================================================

def list_database_files(database_dir: str) -> List[str]:
    """
    List all files in the database directory.

    :param database_dir: Path to the directory containing database files.
    :return: A list of file paths for the files in the directory.
    """
    file_paths = []
    for file in os.listdir(database_dir):
        file_paths.append(os.path.join(database_dir, file))
    
    print(f"Found {len(file_paths)} files in the database directory.")
    return file_paths

def read_file(file_path: str) -> Optional[pd.DataFrame]:
    """
    Reads a file into a pandas DataFrame if the file type is supported.

    :param file_path: Path to the file.
    :return: A pandas DataFrame if the file is successfully read, otherwise None.
    """
    # Supported file extensions and their respective pandas readers
    file_readers = {
        ".csv": pd.read_csv,
        ".json": pd.read_json,
        ".xlsx": pd.read_excel
    }

    # Get file extension
    file_ext = os.path.splitext(file_path)[1].lower()

    # Check if file type is supported
    if file_ext in file_readers:
        try:
            return file_readers[file_ext](file_path)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    else:
        print(f"Unsupported file type: {file_ext} for file {file_path}")
        return None
    
def load_databases(database_dir: str) -> Dict[str, Dict[str, Union[List[pd.DataFrame], List[str]]]]:
    """
    Load all databases from a directory, handling multiple file types and organizing them by category.

    :param database_dir: Directory containing database files.
    :return: A dictionary where keys are database categories (e.g., "materials", "applications"),
             and values are dictionaries with two keys:
             - "dataframes": A list of pandas DataFrames for that category.
             - "names": A list of corresponding file names (formatted).
    """

    print("database_dir", database_dir)
    # Initialize the dictionary to store categorized databases
    categories = ["materials", "applications", "costs", "suppliers"]
    databases: Dict[str, Dict[str, Union[List[pd.DataFrame], List[str]]]] = {
        category: {"dataframes": [], "names": []} for category in categories
    }

    # Get file paths
    file_paths = list_database_files(database_dir)

    # Process each file
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        formatted_name = file_name.replace("_", " ").replace(os.path.splitext(file_name)[1], "").title()

        # Read file into a DataFrame
        df = read_file(file_path)
        if df is None:
            continue

        # Ensure numeric data stored as strings are converted to floating-point numbers
        # df = df.apply(pd.to_numeric, errors="ignore")

        # Assign to the correct category
        for category in categories:
            if category in file_name.lower():
                databases[category]["dataframes"].append(df)
                databases[category]["names"].append(formatted_name)
                break
        else:
            print(f"Database category not supported for file: {file_name}")

        # Optionally augment databases with API data
        # augment_with_api_data(databases)

    return databases

def augment_with_api_data(databases: Dict[str, Dict[str, Union[List[pd.DataFrame], List[str]]]]) -> None:
    """
    Augment databases with data from APIs for certain categories.

    :param databases: The dictionary of databases to augment.
    """
    # Example: Fetch materials data from an API and add it to the "materials" category
    materials_api_data = ingest_data_from_api("https://api.example.com/materials", {"param": "value"})
    if not materials_api_data.empty:  # Add only if data is available
        databases["materials"]["dataframes"].append(materials_api_data)
        databases["materials"]["names"].append("API Materials Data")

    # Similar API calls can be added for other categories as needed

def ingest_data_from_api(api_endpoint: str, api_params: dict) -> pd.DataFrame:
    """
    Fetch data from an API and return it as a pandas DataFrame.

    :param api_endpoint: The API endpoint URL.
    :param api_params: Parameters for the API request.
    :return: A pandas DataFrame containing the fetched data.
    """
    import requests

    print(f"Fetching data from API: {api_endpoint}")
    try:
        response = requests.get(api_endpoint, params=api_params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        data = response.json()  # Assuming API returns JSON data
        return pd.DataFrame(data)  # Convert JSON data to pandas DataFrame
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
    
def add_new_file(
    file_path: str, database_category, databases: Dict[str, Dict[str, Union[List[pd.DataFrame], List[str]]]]
) -> None:
    """
    Add a new file to the appropriate category in the databases dictionary.

    :param file_path: Path to the new file to be added.
    :param databases: Existing databases dictionary to update.
    """
    file_name = os.path.basename(file_path)
    formatted_name = file_name.replace("_", " ").replace(os.path.splitext(file_name)[1], "").title()

    # Read file into a DataFrame
    df = read_file(file_path)
    if df is None:
        return

    # Assign to the correct category
    # categories = list(databases.keys())
    # for category in categories:
    
    if database_category in file_name.lower():
        databases[database_category]["dataframes"].append(df)
        databases[database_category]["names"].append(formatted_name)

        # Trigger re-merging for the category
        # databases[category]["merged"] = merge_category_dataframes(databases[category]["dataframes"])
        # print(f"File {formatted_name} added to category '{category}' and merged.")
        
        print(f"File {formatted_name} added to category '{database_category}'.")
        return

    # If no matching category is found
    print(f"Database category not supported for file: {file_name}")

def get_industry_verticals(applications_df):
    """
    Extract unique industry verticals from the applications database.

    :param applications_df: DataFrame containing applications data.
    :return: List of unique industry verticals.
    """
    if "Industry" in applications_df.columns:
        return sorted(applications_df["Industry"].dropna().unique().tolist())
#    else:
#        raise ValueError("The applications database does not contain an 'Industry' column.")