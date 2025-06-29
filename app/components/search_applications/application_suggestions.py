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
from app.utils.import_helpers import st, np, pd, random, ff, go

# Import specific functions from the recommendation module.
# `calculate_application_match`: A function used to compute the compatibility or "match" score
# between a given material and a specific application. Likely based on predefined parameters.
# `recommend_applications_for_material`: A function used to recommend the most relevant applications
# for a given material based on its properties or characteristics.

from app.backends.recommendation.recommendation import calculate_application_match, recommend_applications_for_material

#==========================================================================================

def get_recommendations(applications_df, selected_material_row, selected_filters, suppliers_df, domains=None, supply_chain=None, sustainability=None):
    """
    Suggest applications based on material properties and application property ranges.

    Args:
        applications_df (pd.DataFrame): Unified applications database DataFrame.
        selected_material_row (pd.Series): The selected material's properties.
        selected_filters (list): Property weights and filters for importance matching.
        suppliers_df (pd.DataFrame): Supplier information dataframe.
        domains (list, optional): Selected application domains for focusing recommendations.
        supply_chain (dict, optional): Supply chain preferences including domestic preference, lead time and cost.
        sustainability (dict, optional): Sustainability preferences including carbon footprint and recycling requirements.
    """
    # Initialize session state for filters
    if "filters" not in st.session_state:
        st.session_state["filters"] = []

    # Add Suggest Button
    st.divider()
    if st.button("Suggest Applications", key="suggest_button"):
        st.session_state["run_suggestion"] = True

    # Check session state to run the logic
    if st.session_state.get("run_suggestion", False):
        try:
            # Filter applications by domain if domains are specified
            filtered_applications = applications_df
            if domains and len(domains) > 0:
                # Filter applications by selected domains/industries
                filtered_applications = applications_df[applications_df['industry'].isin(domains)]
                if filtered_applications.empty:
                    # If no applications match the domains, display a warning and use all applications
                    st.warning("No applications found in the selected domains. Showing all relevant applications instead.")
                    filtered_applications = applications_df
            
            # Use our simplified direct property matching logic
            recommendations = direct_property_matching(selected_material_row, filtered_applications)
            
            if recommendations.empty:
                st.warning("No matching applications found based on properties. Check material properties or expand your criteria.")
            else:
                st.markdown("### Suggested Applications")
                # Display recommendations
                display_recommendations(recommendations, suppliers_df)
                
            # Reset the suggestion flag
            st.session_state["run_suggestion"] = False
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            st.session_state["run_suggestion"] = False
    #else:
        # If button not clicked, show a message
        #st.info("Click 'Suggest Applications' to find applications matching this material's properties.")

def display_recommendations(recommendations_df, suppliers_df):
    """
    Display the recommendations DataFrame in a well-formatted way.
    
    Args:
        recommendations_df (pd.DataFrame): The DataFrame containing recommendations.
    """
    if recommendations_df.empty:
        st.warning("No applications match the selected criteria.")
        return

    # Iterate over each row in the recommendations DataFrame
    for idx, row in recommendations_df.iterrows():
        use_case = row.get("use_case", "Unknown")
        industry = row.get("industry", "Unknown")
        property_overlap = row.get("property_overlap", "Unknown")
        match_score = row.get("match_score", 0)

        # Display the formatted recommendation with "Industry | Use-case" format
        with st.expander(f"{industry} | {use_case}"):
            # Create two columns for layout
            col1, col2 = st.columns([5,5])
            
            # Left column: Use case information
            with col1:
                st.markdown(f"#### Use Case: {use_case}")
                st.markdown(f"**Industry:** {industry}")
                st.markdown(f"**Property Overlap:** {property_overlap}")
            
            # Right column: Match score progress bar
            with col2:
                st.markdown('<div style="background-color:rgba(38, 39, 48, 0.03); padding:1.5em; border-radius:8px;">', unsafe_allow_html=True)
                
                # Property Match Score
                st.markdown(f'<div style="margin-bottom:1.5em"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em"><span style="color:#888888;font-size:1em;font-weight:500">Property Match Score</span><span style="color:#00cc96;font-weight:500">{match_score}%</span></div><div style="background-color:rgba(38, 39, 48, 0.1);height:6px;border-radius:3px"><div style="width:{match_score}%;height:100%;background-color:#00cc96"></div></div></div>', unsafe_allow_html=True)
                
                # Sustainability Score
                st.markdown(f'<div style="margin-bottom:1.5em"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em"><span style="color:#888888;font-size:1em;font-weight:500">Sustainability Score (Demo Locked)</span><span style="color:#888888;font-weight:500">n/a</span></div><div style="background-color:rgba(38, 39, 48, 0.1);height:6px;border-radius:3px"><div style="width:100%;height:100%;background-color:#888888"></div></div></div>', unsafe_allow_html=True)
                
                # Supply Chain Score
                st.markdown(f'<div style="margin-bottom:1.5em"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em"><span style="color:#888888;font-size:1em;font-weight:500">Supply Chain Score (Demo Locked)</span><span style="color:#888888;font-weight:500">n/a</span></div><div style="background-color:rgba(38, 39, 48, 0.1);height:6px;border-radius:3px"><div style="width:100%;height:100%;background-color:#888888"></div></div></div>', unsafe_allow_html=True)
                
                # Xtrium Confidence Score
                st.markdown(f'<div style="margin-top:0.75em;padding-top:0.75em;border-top:1px solid rgba(38, 39, 48, 0.1)"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5em"><span style="color:#888888;font-size:1.1em;font-weight:600">Xtrium Confidence Score</span><span style="color:#4dabf7;font-weight:600">{match_score}%</span></div><div style="background-color:rgba(77, 171, 247, 0.2);height:8px;border-radius:4px"><div style="width:{match_score}%;height:100%;background-color:#4dabf7"></div></div></div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

            # Contact form with collapsible section using HTML/CSS
            st.markdown("""<div style='margin-top:1em;'>
                <details style='border-radius:4px; padding:8px;'>
                    <summary style='cursor:pointer; padding:4px; user-select:none;'>
                        📧 Contact Organization
                    </summary>
                    <div style='padding:12px 8px 4px 8px;'>
            """, unsafe_allow_html=True)
            
            # Add organization selection dropdown
            organization = st.selectbox(
                "Select Organization to Contact",
                options=[],  # Empty list for now
                index=None,  # No default selection
                placeholder="Choose an organization",
                key=f"org_select_{idx}_{use_case}_{industry}"  # Add truly unique key with row index
            )
            
            with st.form(key=f"contact_{idx}_{use_case}_{industry}"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Your Name")
                with col2:
                    email = st.text_input("Your Email")
                message = st.text_area("Message", placeholder=f"Enter your message for {use_case}...")
                if st.form_submit_button("Send Inquiry"):
                    st.success("Thank you! Your inquiry has been sent.")
        
            st.markdown("</div></details></div>", unsafe_allow_html=True)

                #st.progress(int(match_score))  # Convert Match Score to integer
                #st.markdown(
                #    f"""
                #    <div style="text-align: center; font-weight: bold; font-size: 16px;">
                #        Properties Match Score: {match_score}% 
                #    </div>
                #    """,
                #    unsafe_allow_html=True,
                #)

# Create gauge charts
def create_gauge_chart(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 14}},
        domain={'x': [0, 1], 'y': [0, 1]},  # Full domain
        gauge={
            'axis': {'range': [0, 5], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 1], 'color': "red"},
                {'range': [1, 2], 'color': "orange"},
                {'range': [2, 3], 'color': "yellow"},
                {'range': [3, 4], 'color': "lightgreen"},
                {'range': [4, 5], 'color': "green"}
            ],
        }
    ))
    # Adjust margins to remove padding
    # fig.update_layout(
    #    margin=dict(t=50, b=50, l=10, r=10)  # Set top, bottom, left, right margins
    #)
    return fig

def direct_property_matching(material_row, applications_df):
    """
    Basic property matching that compares material properties with application property ranges.
    
    Steps:
    1. Find common numeric property columns between material and applications
    2. For each application, check if material properties fall within required ranges
    3. Calculate match scores based on how well properties match requirements
    
    Args:
        material_row (pd.Series): The selected material's properties
        applications_df (pd.DataFrame): DataFrame of applications with property requirements
        
    Returns:
        pd.DataFrame: Applications with match scores, sorted by match score
    """
    # Initialize results list
    results = []
    
    # Get all columns in the material row that have numeric values
    material_numeric_cols = []
    for col in material_row.index:
        if isinstance(material_row[col], (int, float)) and not pd.isna(material_row[col]):
            material_numeric_cols.append(col)
    
    # Process each application
    for idx, application_row in applications_df.iterrows():
        # Track matches and total properties compared
        property_matches = 0
        total_properties = 0
        matching_properties = []
        
        for prop in material_numeric_cols:
            # Skip if property doesn't exist in application or it's not a range
            if prop not in application_row or not isinstance(application_row[prop], str):
                continue
                
            # Try to extract min-max values from the range string
            try:
                # Extract range from format like "10-20" or ">=5" or "<=30"
                range_str = application_row[prop]
                
                # Handle different range formats
                if '-' in range_str:
                    # Format: "min-max"
                    min_val, max_val = map(float, range_str.split('-'))
                elif '>=' in range_str:
                    # Format: ">=min"
                    min_val = float(range_str.replace('>=', '').strip())
                    max_val = float('inf')
                elif '<=' in range_str:
                    # Format: "<=max"
                    min_val = float('-inf')
                    max_val = float(range_str.replace('<=', '').strip())
                elif '>' in range_str:
                    # Format: ">min"
                    min_val = float(range_str.replace('>', '').strip())
                    max_val = float('inf')
                    # Add small epsilon to make it strictly greater than
                    min_val += 0.0001
                elif '<' in range_str:
                    # Format: "<max"
                    min_val = float('-inf')
                    max_val = float(range_str.replace('<', '').strip())
                    # Subtract small epsilon to make it strictly less than
                    max_val -= 0.0001
                else:
                    # Try to interpret as a single value (equality)
                    min_val = max_val = float(range_str)
            except (ValueError, TypeError):
                # Skip if can't parse range
                continue
                
            # Count this as a property we're comparing
            total_properties += 1
            
            # Check if material property falls within range
            material_value = material_row[prop]
            if min_val <= material_value <= max_val:
                property_matches += 1
                matching_properties.append(prop)
                
        # Calculate match score if we compared any properties
        if total_properties > 0:
            match_score = (property_matches / total_properties) * 100
            
            # Add to results
            results.append({
                "use_case": application_row.get("use_case", f"Semiconductor Application {idx+1}"),
                "industry": application_row.get("industry", "N/A"),
                "property_overlap": application_row.get("property_overlap", "N/A"),
                "match_score": round(match_score, 1),
                "matching_properties": property_matches,
                "total_properties": total_properties
            })
    
    # Convert to DataFrame and sort by match score
    if results:
        results_df = pd.DataFrame(results).sort_values(by="match_score", ascending=False)
        # Keep only applications with at least one matching property
        results_df = results_df[results_df["matching_properties"] > 0]
        return results_df
    else:
        return pd.DataFrame(columns=["use_case", "industry", "property_overlap", "match_score", 
                                    "matching_properties", "total_properties"])
