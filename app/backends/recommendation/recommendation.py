#==========================================================================================
# Import the pandas library as 'pd' for working with structured data such as DataFrames.
# Pandas is commonly used for data manipulation and analysis.

from app.utils.import_helpers import st, pd
#==========================================================================================

def extract_min_max(range_value):
    """
    Extracts the minimum and maximum values from a hyphen-separated range string.

    Args:
        range_value (str): The range string in the format "min-max" (e.g., "1.0-3.0").

    Returns:
        tuple: A tuple of (min_value, max_value) as floats.

    Raises:
        ValueError: If the range string is invalid.
    """
    try:
        # Split the range string by hyphen and convert to float
        min_value, max_value = map(float, range_value.split('-'))
        return min_value, max_value
    except Exception as e:
        raise ValueError(f"Invalid range format: '{range_value}'. Expected 'min-max'. Error: {e}")

def calculate_match_for_filters(material_row, application_row, selected_filters):
    """
    Calculate the match score between a material and an application based on filters.

    Args:
        material_row (pd.Series): The row representing the selected material's properties.
        application_row (pd.Series): The row representing an application's requirements.
        selected_filters (list): List of filters with 'property', 'range', and 'weightage'.

    Returns:
        float: The calculated match score between 0 and 100.
    """
    total_weighted_score = 0
    total_weight = 0

    #st.write(selected_filters)

    for filter_item in selected_filters:
        property = filter_item["property"]  # Property to evaluate
        weightage = filter_item["weightage"]  # Weightage for this filter
        material_value = filter_item.get("value", None)  # Value from the filter
        application_range = application_row.get(property, None)  # Range from the application

        # Skip if property or range is missing in either application or material
        if material_value is None or application_range is None:
            continue

        try:
            # Extract min and max from the hyphen-separated range
            application_min, application_max = extract_min_max(application_range)
        except ValueError as e:
            print(f"Error parsing application range for {property}: {e}")
            return 0  # Invalid range means no match

        # Calculate match score based on proximity to range
        if application_min <= material_value <= application_max:
            match_score = 100  # Fully within range
        else:
            # Penalty for values outside the range
            distance = min(abs(material_value - application_min), abs(material_value - application_max))
            range_size = abs(application_max - application_min)
            match_score = max(0, 100 - (distance / range_size) * 100)

        # Add weighted score
        weighted_score = match_score * weightage
        total_weighted_score += weighted_score
        total_weight += weightage

    # Normalize the score to 0-100 if weight is non-zero
    return total_weighted_score / total_weight if total_weight > 0 else 0

def calculate_match_by_name(material_name, application_name):
    """
    Assign a perfect match score if only material and application names are being compared.

    Args:
        material_name (str): The name of the material.
        application_name (str): The name of the application.

    Returns:
        float: A perfect match score of 100.
    """
    return 100 if material_name and application_name else 0

def calculate_application_match(material_row, application_row, selected_filters):
    """
    Calculate the match score between a material and an application.

    Args:
        material_row (pd.Series): The row representing the selected material's properties.
        application_row (pd.Series): The row representing an application's requirements.
        selected_filters (list): Filters for matching logic.

    Returns:
        float: The calculated match score.
    """
    # print(material_row, application_row)
    # st.write(material_row, application_row)

    if not selected_filters:  # If no filters are selected, match by name
        material_name = material_row.get("name", None)
        application_name = application_row.get("chemical_formula", None)
        print(material_name, application_name)
        return calculate_match_by_name(material_name, application_name)

    # Otherwise, calculate match based on filters
    return calculate_match_for_filters(material_row, application_row, selected_filters)

def recommend_applications_for_material(material_row, applications_df, selected_filters):
    """
    Recommend applications for a selected material based on filters or name matching.

    Args:
        material_row (pd.Series): The selected material's row.
        applications_df (pd.DataFrame): DataFrame containing applications.
        selected_filters (list): Filters for matching logic.

    Returns:
        pd.DataFrame: Applications sorted by match scores.
    """

    recommendations = []

    for _, application_row in applications_df.iterrows():
        try:
            # Calculate match score
            score = calculate_application_match(material_row, application_row, selected_filters)

            if score > 0:  # Add to recommendations if score is positive
                recommendations.append({
                    "Use-Case": application_row.get("use_case", "N/A"),
                    "Industry": application_row.get("industry", "N/A"),
                    "Property Overlap": application_row.get("property_overlap", "N/A"),
                    "Match_Score": round(score, 2)
                })
        except Exception as e:
            print(f"Error calculating match for application {application_row.get('application_name', 'unknown')}: {e}")

    # Convert recommendations to a DataFrame and sort by score
    if recommendations:
        return pd.DataFrame(recommendations).sort_values(by="Match_Score", ascending=False)
    else:
        return pd.DataFrame(columns=["Use-Case", "Industry", "Property Overlap", "Match_Score"])