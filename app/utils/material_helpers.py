"""
Helper functions for material selection and filtering.
"""
from app.utils.import_helpers import pd, np
from app.utils.periodic_table import extract_symbols, parse_formula

def extract_material_types(materials_df):
    """
    Extract unique material types from the dataframe.
    
    Args:
        materials_df (pd.DataFrame): Materials dataframe
        
    Returns:
        list: Sorted list of unique material types
    """
    # First check if a 'type' column exists
    if "type" in materials_df.columns:
        return sorted(materials_df["type"].dropna().unique().tolist())
    
    # If no type column, try to infer from material name or other properties
    # This is a simplified approach - would need refinement with domain knowledge
    material_types = []
    
    # Check if we have a category or class column
    for col in ["category", "class", "material_class"]:
        if col in materials_df.columns:
            return sorted(materials_df[col].dropna().unique().tolist())
    
    # If no explicit type columns, use these defaults
    return ["Polymer", "Metal", "Ceramic", "Composite", "Alloy", "Semiconductor"]


def filter_by_elements(materials_df, element_symbols):
    """
    Filter materials containing all specified elements.
    
    Args:
        materials_df (pd.DataFrame): Materials dataframe with standardized schema
        element_symbols (list): List of element symbols to filter by
        
    Returns:
        pd.DataFrame: Filtered materials dataframe
    """
    if not element_symbols:
        return materials_df
    
    # Handle potential NaN or non-string values in chemical_formula column
    def check_formula_contains_elements(formula):
        if pd.isna(formula):
            return False
        try:
            parsed_elements = parse_formula(str(formula))
            return all(symbol in parsed_elements for symbol in element_symbols)
        except Exception:
            return False
    
    return materials_df[
        materials_df["chemical_formula"].apply(check_formula_contains_elements)
    ]


def filter_by_material_types(materials_df, material_types):
    """
    Filter materials by type.
    
    Args:
        materials_df (pd.DataFrame): Materials dataframe
        material_types (list): List of material types to include
        
    Returns:
        pd.DataFrame: Filtered materials dataframe
    """
    if not material_types:
        return materials_df
        
    # First check if a 'type' column exists
    if "type" in materials_df.columns:
        return materials_df[materials_df["type"].isin(material_types)]
    
    # Try alternative columns
    for col in ["category", "class", "material_class"]:
        if col in materials_df.columns:
            return materials_df[materials_df[col].isin(material_types)]
            
    # If no matching columns, return original dataframe
    return materials_df


def create_display_to_name_map(materials_df):
    """
    Create a mapping from display names to actual material names.
    
    Args:
        materials_df (pd.DataFrame): Materials dataframe with standardized schema
        
    Returns:
        dict: Mapping from display names to actual material formulas
    """
    display_to_name = {}
    
    for _, row in materials_df.iterrows():
        # Handle potential missing values in any column
        chemical_formula = str(row['chemical_formula']) if pd.notna(row.get('chemical_formula')) else 'Unknown'
        
        # Use commercial_name if available, otherwise use canonical_name if available
        if pd.notna(row.get('commercial_name')):
            display_name = f"{row['commercial_name']} ({chemical_formula})"
        elif pd.notna(row.get('canonical_name')):
            display_name = f"{row['canonical_name']} ({chemical_formula})"
        else:
            display_name = chemical_formula
            
        # Map display name to chemical formula (used as the identifier)
        display_to_name[display_name] = chemical_formula
        
    return display_to_name
