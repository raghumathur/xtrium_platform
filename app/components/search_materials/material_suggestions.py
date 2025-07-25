#==========================================================================================
# Import necessary libraries and modules

# Streamlit is used for building interactive web applications.
# This `st` alias is used throughout Streamlit-based apps for ease of use.

# Importing NumPy library, used for array manipulation and mathematical operations.

# Import the random module to generate random numbers or selections.
# It is part of Python's standard library and is used for operations like shuffling or generating random data.

# Import the figure factory module from Plotly, an interactive graphing library.
# `ff` is used for creating specialized plots like dendrograms, violin plots, and table visualizations.

# Import the graph_objects module from Plotly.
# `go` is used for building figures from low-level components such as traces (lines, bars, etc.).
from app.utils.import_helpers import st, st_modal, pd, np, random, ff, go

# Import the extract_dataframes function from the app's backend module
# This function is responsible for retrieving and preparing dataframes from the database.
# The dataframes may include materials data, application-specific information, or other relevant data
# needed for the application's functionality.
from app.backends.database.dataframes import extract_dataframes

# Import from the recommendation module.
# We'll adapt the application recommendation functions for material recommendations
from app.backends.recommendation.recommendation import extract_min_max

# Initialize session state variables
if "run_suggestion" not in st.session_state:
    st.session_state["run_suggestion"] = False

if "selected_material_for_details" not in st.session_state:
    st.session_state["selected_material_for_details"] = None
#==========================================================================================

def calculate_material_match(material_row, application_properties, property_weights=None):
    """
    Calculate the match score between a material and an application based on property matching.
    
    Args:
        material_row (pd.Series): The row representing the material's properties
        application_properties (dict): Dictionary of application property names to values
        property_weights (dict, optional): Dictionary of property names to importance weights
        
    Returns:
        float: The calculated match score between 0 and 100
    """
    total_weighted_score = 0
    total_weight = 0
    
    # Default weights if not provided
    if property_weights is None:
        property_weights = {prop: 1.0 for prop in application_properties.keys()}
    
    for prop, app_value in application_properties.items():
        # Skip if property is not in material or weight is zero
        if prop not in material_row or prop not in property_weights or property_weights.get(prop, 0) == 0:
            continue
            
        # Get material value and weight
        material_value = pd.to_numeric(material_row[prop], errors='coerce')
        weight = property_weights.get(prop, 1.0)
        
        # Skip if material value is NaN
        if pd.isna(material_value):
            continue
            
        # Calculate match score based on proximity
        # For simplicity, we'll use a linear distance-based score
        # Closer values get higher scores
        max_diff = max(abs(app_value * 0.5), 1.0)  # Use 50% of app value as max difference, minimum 1.0
        diff = abs(material_value - app_value)
        
        if diff == 0:
            match_score = 100  # Perfect match
        else:
            match_score = max(0, 100 - (diff / max_diff) * 100)
            match_score = min(match_score, 100)  # Cap at 100
        
        # Add weighted score
        weighted_score = match_score * weight
        total_weighted_score += weighted_score
        total_weight += weight
    
    # Return normalized score if we have weights, otherwise 0
    return total_weighted_score / total_weight if total_weight > 0 else 0

def recommend_materials_for_application(materials_df, application_properties, property_weights=None):
    """
    Recommend materials for a selected application based on property matching.
    
    Args:
        materials_df (pd.DataFrame): DataFrame containing materials data
        application_properties (dict): Dictionary of application property names to values
        property_weights (dict, optional): Dictionary of property names to importance weights
        
    Returns:
        pd.DataFrame: Materials sorted by match scores
    """
    recommendations = []
    
    for idx, material_row in materials_df.iterrows():
        try:
            # Calculate match score
            score = calculate_material_match(material_row, application_properties, property_weights)
            
            if score > 0:  # Add to recommendations if score is positive
                material_data = material_row.to_dict()
                material_data['Match_Score'] = round(score, 2)
                recommendations.append(material_data)
        except Exception as e:
            print(f"Error calculating match for material {material_row.get('name', 'unknown')}: {e}")
    
    # Convert recommendations to DataFrame and sort by score
    if recommendations:
        return pd.DataFrame(recommendations).sort_values(by="Match_Score", ascending=False)
    else:
        # Return empty DataFrame with proper columns
        return pd.DataFrame(columns=list(materials_df.columns) + ["Match_Score"])

def direct_property_matching(application_row, materials_df):
    """
    Basic property matching that compares application properties with material properties ranges.
    
    Steps:
    1. Find common numeric property columns between application and materials
    2. For each material, check if its properties match the application requirements
    3. Calculate a match score based on how many properties match
    4. Return materials sorted by match score
        
    Args:
        application_row: DataFrame row containing application properties
        materials_df: DataFrame containing all materials data
        
    Returns:
        pd.DataFrame: Materials with match scores, sorted by match score
    """
    # Initialize results list
    results = []
    
    # Get all columns in the application row that have numeric values or range values
    application_property_cols = []
    application_property_values = {}
    
    for col, value in application_row.items():
        # Skip non-property columns
        if col in ['Use-case', 'Industry', 'Commercial name', 'Chemical Name', 'Chemical Formula', 'Property Overlap']:
            continue
            
        # Handle range values (e.g., "10-20")
        if isinstance(value, str) and '-' in value:
            try:
                # Extract min and max from range
                min_val, max_val = map(float, value.split('-'))
                application_property_cols.append(col)
                application_property_values[col] = (min_val, max_val)
            except (ValueError, TypeError):
                pass
        # Handle direct numeric values
        elif isinstance(value, (int, float)) and not pd.isna(value):
            application_property_cols.append(col)
            # For single values, create a small range around it (±5%)
            value_range = value * 0.05
            application_property_values[col] = (value - value_range, value + value_range)
    
    # Process each material
    for idx, material_row in materials_df.iterrows():
        # Track matches and total properties compared
        property_matches = 0
        total_properties = 0
        matching_properties = []
        
        # Compare each property from the application
        for prop in application_property_cols:
            # Skip if property doesn't exist in material
            if prop not in material_row or pd.isna(material_row[prop]):
                continue
                
            # Get the application's required range for this property
            app_min, app_max = application_property_values[prop]
            
            # Get the material's value for this property
            material_value = material_row[prop]
            
            # Count this as a property we're comparing
            total_properties += 1
            
            # Check if material property falls within application's required range
            if app_min <= material_value <= app_max:
                property_matches += 1
                matching_properties.append(prop)
                
        # Calculate match score if we compared any properties
        if total_properties > 0:
            match_score = (property_matches / total_properties) * 100
            
            # Add to results
            material_name = material_row.get("chemical_formula", f"Material {idx+1}")
            commercial_name = material_row.get("commercial_name", "N/A")
            
            results.append({
                "material_name": material_name,
                "commercial_name": commercial_name,
                "property_overlap": material_row.get("property_overlap", "N/A"),
                "match_score": round(match_score, 1),
                "matching_properties": property_matches,
                "total_properties": total_properties
            })
    
    # Convert to DataFrame and sort by match score
    if results:
        results_df = pd.DataFrame(results).sort_values(by="match_score", ascending=False)
        # Keep only materials with at least one matching property
        results_df = results_df[results_df["matching_properties"] > 0]
        return results_df
    else:
        return pd.DataFrame(columns=["material_name", "commercial_name", "property_overlap", "match_score", 
                                    "matching_properties", "total_properties"])

def display_material_recommendations(recommendations_df, suppliers_df=None):
    """
    Display recommended materials in a user-friendly format with multiple view options.

    Args:
        recommendations_df (pd.DataFrame): DataFrame containing recommended materials with match scores.
        suppliers_df (pd.DataFrame, optional): DataFrame containing supplier information for materials.
    """
    if recommendations_df.empty:
        st.warning("No materials found matching the selected criteria.")
        return

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["List View", "Table View", "Chart View"])
    
    with tab1:
        # List view with expandable details
        st.markdown("#### Top Material Matches")
        
        # Display top 10 materials
        for idx, row in recommendations_df.head(10).iterrows():
            with st.expander(f"{row['commercial_name']} - {row['match_score']}% match"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Material:** {row['material_name']}")
                    st.markdown(f"**Commercial Name:** {row['commercial_name']}")
                    st.markdown(f"**Property Overlap:** {row['property_overlap']}")
                    st.markdown(f"**Match Score:** {row['match_score']}%")
                    st.markdown(f"**Matching Properties:** {row['matching_properties']} of {row['total_properties']}")
                
                with col2:
                    # Show supplier info if available
                    if suppliers_df is not None and not suppliers_df.empty:
                        try:
                            material_suppliers = suppliers_df[suppliers_df['material_name'] == row['material_name']]
                            if not material_suppliers.empty:
                                st.markdown("**Suppliers:**")
                                for s_idx, supplier in material_suppliers.iterrows():
                                    st.markdown(f"- {supplier.get('supplier_name', 'Unknown')}")
                                    st.markdown(f"  Lead time: {supplier.get('lead_time', 'N/A')}")
                                    st.markdown(f"  Cost: {supplier.get('cost', 'N/A')}")
                        except Exception as e:
                            st.error(f"Error displaying supplier info: {str(e)}")
                
                # Add a button to view detailed material properties
                if st.button(f"View Detailed Properties for {row['commercial_name']}", key=f"view_details_{idx}"):
                    st.session_state["selected_material_for_details"] = row['material_name']
    
    with tab2:
        # Table view with sortable columns
        st.markdown("#### Material Matches - Table View")
        
        # Create a more user-friendly table with selected columns
        display_df = recommendations_df[[
            "commercial_name", "material_name", "match_score", 
            "matching_properties", "total_properties", "property_overlap"
        ]].copy()
        
        # Rename columns for better readability
        display_df.columns = [
            "Commercial Name", "Material Name", "Match Score (%)", 
            "Matching Properties", "Total Properties", "Property Overlap"
        ]
        
        # Display the table with sorting enabled
        st.dataframe(display_df.style.format({
            "Match Score (%)": "{:.1f}"
        }))
    
    with tab3:
        # Chart view showing match scores
        st.markdown("#### Material Match Scores")
        
        # Prepare data for chart
        chart_data = recommendations_df.head(15).copy()  # Top 15 materials
        
        # Create a horizontal bar chart using Plotly
        fig = go.Figure()
        
        # Add bar chart trace
        fig.add_trace(go.Bar(
            y=chart_data['commercial_name'],
            x=chart_data['match_score'],
            orientation='h',
            marker=dict(
                color=chart_data['match_score'],
                colorscale='Viridis',
                colorbar=dict(title="Match Score"),
            ),
            text=chart_data['match_score'].apply(lambda x: f"{x:.1f}%"),
            textposition='auto',
            name="Match Score"
        ))
        
        # Update layout
        fig.update_layout(
            title="Top 15 Material Matches by Score",
            xaxis_title="Match Score (%)",
            yaxis_title="Material",
            yaxis=dict(autorange="reversed"),  # Highest score at the top
            height=500,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)

def get_recommendations(materials_df, selected_application_row, selected_filters, suppliers_df, elements=None, supply_chain=None, sustainability=None):
    """
    Suggest materials based on application properties and material property ranges.
    
    Args:
        materials_df (pd.DataFrame): DataFrame containing materials data
        selected_application_row (pd.Series): The selected application's properties
        selected_filters (dict): Dictionary of selected filters
        suppliers_df (pd.DataFrame): DataFrame containing supplier information
        elements (list, optional): List of constituent elements to focus on
        supply_chain (dict or pd.DataFrame, optional): Supply chain preferences or costs dataframe
        sustainability (dict, optional): Sustainability preferences
        
    Returns:
        pd.DataFrame: DataFrame of recommended materials with match scores
    """
    # Extract application properties for matching
    application_properties = {}
    for col in selected_application_row.index:
        if col not in ['Use-case', 'Industry', 'Commercial name', 'Chemical Name', 'Chemical Formula']:
            try:
                # Try to convert to numeric value
                val = pd.to_numeric(selected_application_row[col])
                application_properties[col] = val
            except:
                # Skip non-numeric properties
                pass
    
    # Filter materials by constituent elements if specified
    if elements and len(elements) > 0:
        from app.utils.material_helpers import filter_by_elements
        materials_df = filter_by_elements(materials_df, elements)
    
    # Extract property weights from selected filters
    property_weights = {}
    if selected_filters and "property_weights" in selected_filters:
        property_weights = selected_filters["property_weights"]
        
    # Handle costs_df if supply_chain is actually a DataFrame
    costs_df = None
    if isinstance(supply_chain, pd.DataFrame):
        costs_df = supply_chain
        supply_chain = {}
    
    # Add Suggest Button
    st.divider()
    if st.button("Suggest Materials", key="suggest_button"):
        st.session_state["run_suggestion"] = True
    
    # Check session state to run the logic
    if st.session_state.get("run_suggestion", False):
        try:
            # Use our direct property matching logic
            recommendations = direct_property_matching(selected_application_row, materials_df)
            
            if recommendations.empty:
                st.warning("No matching materials found based on properties. Check application properties or expand your criteria.")
            else:
                st.markdown("### Suggested Materials")
                # Display recommendations
                display_material_recommendations(recommendations, suppliers_df)
                
        except Exception as e:
            st.error(f"An error occurred while generating recommendations: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
    
    return direct_property_matching(selected_application_row, materials_df)

def find_materials():
    """
    Processes input data to identify and recommend materials based on selected applications and dynamic filters.

    Steps:
        1. Extract dataframes from the provided databases.
        2. Generate material recommendations based on selected application and filters.
    """
    # Check if databases exist in session state
    if "databases" not in st.session_state:
        st.warning("No databases loaded. Please select databases first.")
        return pd.DataFrame()
    
    # Extract dataframes from the database
    try:
        # Make sure st.session_state.databases is properly initialized
        if isinstance(st.session_state.databases, dict):
            materials_df, applications_df, costs_df, suppliers_df = extract_dataframes(st.session_state.databases)
        
        # Get the selected application from session state
        if "selected_application" in st.session_state and st.session_state["selected_application"] is not None:
            selected_application = st.session_state["selected_application"]
            
            # Get the matching preferences from session state
            matching_preferences = st.session_state.get("matching_preferences", {})
            
            # Get the selected application row
            selected_application_row = applications_df[applications_df["Use-case"] == selected_application].iloc[0]
            
            # Call get_recommendations with the selected application and preferences
            return get_recommendations(
                materials_df=materials_df,
                selected_application_row=selected_application_row,
                selected_filters=matching_preferences,
                suppliers_df=suppliers_df,
                elements=matching_preferences.get("constituent_elements", []),
                supply_chain=matching_preferences.get("supply_chain", {}) if "supply_chain" in matching_preferences else costs_df,
                sustainability=matching_preferences.get("sustainability", {})
            )
        else:
            st.warning("Please select an application first.")
            return pd.DataFrame()  # Return empty DataFrame if no application is selected
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return pd.DataFrame()
