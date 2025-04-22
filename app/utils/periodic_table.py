import json
import re
import os

def load_periodic_table(json_path="./assets/jsons/periodic_table.json"):
    """
    Load periodic table elements from a JSON file.

    :param json_path: Path to the JSON file containing the periodic table data.
    :return: List of element names sorted by atomic number.
    """
    # Determine the absolute project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

    # Ensure json_path is an absolute path
    if not os.path.isabs(json_path):
        json_path = os.path.join(project_root, json_path)

    with open(json_path, "r") as file:
        data = json.load(file)
    elements = sorted(data["elements"], key=lambda x: x["atomic_number"])
    return [f"{element['name']} ({element['symbol']})" for element in elements]

def extract_symbols(selected_elements):
    """
    Extracts the symbols of elements from the selected elements list.

    :param selected_elements: List of selected elements (e.g., "Hydrogen (H)").
    :return: List of symbols (e.g., ["H"]).
    """
    return [el.split("(")[-1].strip(" )") for el in selected_elements]

# Define a function to split a chemical formula into element symbols
def parse_formula(formula):
    """
    Splits a chemical formula into its component element symbols using regex.
    For example, "C6H12O6" -> ["C", "H", "O"]
    """
    # Match one or two capital letters optionally followed by lowercase letters
    pattern = r'[A-Z][a-z]?'
    return re.findall(pattern, formula)