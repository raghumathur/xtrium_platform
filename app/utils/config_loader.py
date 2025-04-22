# Importing the OS module to work with file paths.
import os

# Importing the JSON module for handling JSON data.
import json

def load_config(config_path="app/config/config.json"):
    """
    Load configuration from a JSON file.

    This function reads a JSON file from the specified path, converts its relative path 
    to an absolute path based on the project root directory, parses its contents, 
    and returns the configuration data as a Python dictionary.

    :param config_path: (str) The relative path to the configuration file, 
                        relative to the project's root directory. Default is "app/config/config.json".
    :return: (dict) The configuration data loaded from the JSON file.
    """
    # Get the absolute path of the project's root directory (assumed to be two levels up from this script).
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

    # Ensure config_path is an absolute path
    if not os.path.isabs(config_path):
        config_path = os.path.join(project_root, config_path)
    
    # Join the project root directory with the relative config path to get the absolute path.
    # abs_config_path = os.path.join(project_root, config_path)
    
    # Open the specified configuration file in read mode.
    with open(config_path, "r") as file:
        # Parse the JSON content from the file and store it in the 'config' variable.
        config = json.load(file)

    # Replace `{BASE_DIR}` with the absolute project root in all paths
    for key, path in config["paths"].items():
        config["paths"][key] = path.replace("{BASE_DIR}", project_root)
    
    # Return the loaded configuration as a dictionary.
    return config