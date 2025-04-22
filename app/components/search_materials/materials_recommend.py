import streamlit as st
import pandas as pd
import numpy as np

def extract_min_max(range_value):
    """
    Extracts the minimum and maximum values from a hyphen-separated range string.

    Args:
        range_value (str): Range string in the format "min-max" (e.g., "1.0-3.0").

    Returns:
        tuple: Min and max values as floats.
    """
    try:
        min_value, max_value = map(float, range_value.split('-'))
        return min_value, max_value
    except Exception:
        raise ValueError(f"Invalid range format: {range_value}")


def calculate_material_match(application_row, material_row, selected_filters):
    """
    Calculate the match score between an application and a material based on selected filters.

    :param application_row: Series representing the application row.
    :param material_row: Series representing the material row.
    :param selected_filters: List of filters.
    :return: Match score (0-100).
    """
    #st.write(application_row)
    #st.write(material_row)
    total_score = 0
    total_weight = 0

    for filter_item in selected_filters:
        parameter = filter_item["property"]

        expected_value = application_row.get(parameter, None)
        material_value = material_row.get(parameter, None)
        filter_value = filter_item["value"]
        weightage = filter_item["weightage"]

        #if expected_value is None or material_value is None:
        if not isinstance(material_value, (int, float)) or np.isnan(material_value) or expected_value is None:    
            continue
        
        # st.write(parameter)
        # st.write(expected_value)
        # st.write(material_value)
        # st.write(filter_value)

        try:
            app_min, app_max = extract_min_max(expected_value)
            #st.write(app_min, app_max)
        except ValueError:
            continue

        if app_min <= material_value <= app_max:
            match_score = 100
        else:
            range_diff = max(abs(material_value - app_min), abs(material_value - app_max))
            range_size = abs(app_max - app_min)
            match_score = max(0, 100 - (range_diff / range_size) * 100)

        weighted_score = match_score * weightage
        total_score += weighted_score
        total_weight += weightage

    return total_score / total_weight if total_weight > 0 else 0


def recommend_materials_for_application(application_row, materials_df, selected_filters):
    """
    Recommend materials based on application requirements.

    :param application_row: Series representing the application row.
    :param materials_df: DataFrame containing materials.
    :param selected_filters: Filters for recommendation logic.
    :return: DataFrame of recommended materials.
    """
    recommendations = []

    for _, material_row in materials_df.iterrows():
        score = calculate_material_match(application_row, material_row, selected_filters)
        if score > 0:
            recommendations.append({
                "Material Name": material_row["remarks"],
                "Chemical Formula": material_row["name"],
                "Property Overlap": application_row["property_overlap"],
                "Match Score": round(score, 2)
            })

    # Handle case where no recommendations are found
    if not recommendations:
        # Return an empty DataFrame with the required columns
        return pd.DataFrame(columns=["Material Name", "Chemical Formula", "Property Overlap", "Match Score"])

    return pd.DataFrame(recommendations).sort_values(by="Match Score", ascending=False)