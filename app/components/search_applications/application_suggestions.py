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
from app.utils.import_helpers import st, np, random, ff, go

# Import specific functions from the recommendation module.
# `calculate_application_match`: A function used to compute the compatibility or "match" score
# between a given material and a specific application. Likely based on predefined parameters.
# `recommend_applications_for_material`: A function used to recommend the most relevant applications
# for a given material based on its properties or characteristics.

from app.backends.recommendation.recommendation import calculate_application_match, recommend_applications_for_material

#==========================================================================================

def get_recommendations(applications_df, selected_material_row, selected_filters, suppliers_df, domains=None, supply_chain=None, sustainability=None):
    """
    Suggest applications based on material properties and application matching preferences.

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
                filtered_applications = applications_df[applications_df['Industry'].isin(domains)]
                if filtered_applications.empty:
                    # If no applications match the domains, display a warning and use all applications
                    st.warning("No applications found in the selected domains. Showing all relevant applications instead.")
                    filtered_applications = applications_df
                    
            # Apply supply chain and sustainability filters as pre-filters if applicable
            if supply_chain and supply_chain.get('domestic_preferred', False):
                # Filter for domestic suppliers if that preference is set
                try:
                    if 'DomesticSupply' in filtered_applications.columns:
                        filtered_applications = filtered_applications[filtered_applications['DomesticSupply'] == True]
                except Exception as e:
                    st.info(f"Could not filter by domestic supply: {e}")
            
            if sustainability and sustainability.get('recycling_required', False):
                # Filter for recyclable materials if that preference is set
                try:
                    if 'Recyclable' in filtered_applications.columns:
                        filtered_applications = filtered_applications[filtered_applications['Recyclable'] == True]
                except Exception as e:
                    st.info(f"Could not filter by recyclability: {e}")
            
            # Get recommendations based on the filtered applications and material properties
            suggested_applications = recommend_applications_for_material(
                selected_material_row,
                filtered_applications,
                selected_filters
            )
            
            # Apply additional ranking based on supply chain and sustainability preferences
            if not suggested_applications.empty and (supply_chain or sustainability):
                try:
                    # Example of adjusting scores based on preferences - this would be expanded
                    # with more sophisticated logic as outlined in the Material-Application Matching improvements
                    for idx, row in suggested_applications.iterrows():
                        score_adj = 0
                        
                        # Adjust for lead time if preference set
                        if supply_chain and 'LeadTime' in row and 'lead_time_max' in supply_chain:
                            if row['LeadTime'] <= supply_chain['lead_time_max']:
                                score_adj += 5  # Bonus for meeting lead time requirements
                        
                        # Apply the score adjustment
                        if score_adj != 0:
                            suggested_applications.at[idx, 'Match_Score'] = min(100, row['Match_Score'] + score_adj)
                except Exception as e:
                    st.info(f"Could not apply all preference adjustments: {e}")
            if not suggested_applications.empty:
                st.markdown("### Suggested Applications")
                display_recommendations(suggested_applications, suppliers_df)
            else:
                st.warning("No applications match the selected criteria.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Reset the flag after execution
    st.session_state["run_suggestion"] = False

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
#        col1, col2 = st.columns([2,8])
#        with col1:
#            st.write("image here")
#        with col2:
        use_case = row.get("Use-Case", "Unknown")
        industry = row.get("Industry", "Unknown")
        property_overlap = row.get("Property Overlap", "Unknown")
        match_score = row.get("Match_Score", 0)

        # Display the formatted recommendation
        #with st.expander(use_case, icon=":material/insights:"): # icons=waves, science, bolt, assessment, trending up, storage, timeline
        with st.expander(use_case):
            st.markdown(f"#### Use Case: {use_case}")
            st.markdown(f"**Industry:** {industry}")
            st.markdown(f"**Property Overlap:** {property_overlap}")
            
            # st.divider()
            # Display the match score as a progress bar
            st.progress(int(match_score))  # Convert Match Score to integer
            #st.markdown(f"**Properties Match Score:** {match_score}%")
            st.markdown(
                f"""
                <div style="text-align: center; font-weight: bold; font-size: 16px;">
                    Properties Match Score: {match_score}% 
                    <p> </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # st.divider()
            sustainability_rating = get_sustainability_score()
            confidence_score = get_confidence_score(match_score, sustainability_rating)

            # Normalize all scores to 5-star ratings
            match_score_normalized = (match_score / 100) * 5
            confidence_score_normalized = (confidence_score / 10) * 5
            sustainability_score_normalized = sustainability_rating

            # Create individual charts
            match_chart = create_gauge_chart(match_score_normalized, "Compatibility Score")
            confidence_chart = create_gauge_chart(confidence_score_normalized, "Overall Confidence Score")
            sustainability_chart = create_gauge_chart(sustainability_score_normalized, "Sustainability Score")

            # st.divider()            
            col1, col2, col3 = st.columns([3,5,3])
            with col1:
                st.plotly_chart(match_chart, use_container_width=True, key=f"match_chart_{idx}")
            with col2:
                st.plotly_chart(confidence_chart, use_container_width=True, key=f"confidence_chart_{idx}")
            with col3:
                st.plotly_chart(sustainability_chart, use_container_width=True, key=f"sustainability_chart_{idx}")
            # st.divider()

            # Contact suppliers button
            #    st.info(f"Contacting suppliers for use case: {use_case}")
            #if st.button("Commercial Information", key=f"contact_{use_case}"):
            #if st.button("Show Supplier Card", key=f"somekey_{idx}"):
            # Get supplier data for this application
            supplier_data = suppliers_df.iloc[0].to_dict() if not suppliers_df.empty else {
                'Name': 'Business Contact A',
                'Email': 'buscon_a@example.com',
                'Phone': '+1234567890',
                'Website': 'supplier-a.example.com',
                'Quality Score': 4.5,
                'Rating': 4.5,
                'Response Time': 24,
                'Certifications': 'ISO 9001, CE'
            }
            display_business_card(supplier_data)
            # Get second supplier data
            supplier_data = suppliers_df.iloc[1].to_dict() if len(suppliers_df) > 1 else {
                'Name': 'Business Contact B',
                'Email': 'buscon_b@example.com',
                'Phone': '+9876543210',
                'Website': 'supplier-b.example.com',
                'Quality Score': 4.0,
                'Rating': 4.0,
                'Response Time': 48,
                'Certifications': 'RoHS'
            }
            display_business_card(supplier_data)


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

def get_sustainability_score():
    # Add histogram data based on sustainability dimensions
    # Environmental scores (e.g., greenhouse gas emissions, resource depletion)
    environmental_scores = np.random.normal(loc=6, scale=1, size=200)
    environmental_mean = np.mean(environmental_scores)  # Environmental
    environmental_weight = 0.4

    # Social scores (e.g., labor practices, community impact)
    social_scores = np.random.normal(loc=8, scale=1.5, size=200)
    social_mean = np.mean(social_scores)         # Social
    social_weight = 0.3

    # Economic scores (e.g., cost-effectiveness, lifecycle value)
    economic_scores = np.random.normal(loc=7, scale=2, size=200)
    economic_mean = np.mean(economic_scores)       # Economic Viability
    economic_weight = 0.2

    # Regulatory/geopolitical risk (e.g., political stability, compliance risks)
    regulatory_scores = np.random.normal(loc=7, scale=1, size=200)
    regulatory_mean = np.mean(regulatory_scores)     # Regulatory Risk
    regulatory_weight = 0.1

    # Calculate Sustainability Score
    sustainability_score = (environmental_weight * environmental_mean + 
                            social_weight * social_mean + 
                            economic_weight * economic_mean + 
                            regulatory_weight * regulatory_mean)/(
                                    environmental_weight + 
                                    social_weight + 
                                    economic_weight + 
                                    regulatory_weight)

    # Convert to star rating out of 5
    star_rating = (sustainability_score / 10) * 5

    # Group data together
    hist_data = [environmental_scores, social_scores, economic_scores, regulatory_scores]

    # Updated group labels
    group_labels = ['Environmental Impact', 'Social Impact', 'Economic Viability', 'Regulatory Risk']

    # Create distplot with custom bin_size
    bin_sizes = [0.5, 0.75, 1, 0.5]

    dist_chart = ff.create_distplot(
        hist_data, group_labels, bin_size=bin_sizes
    )

    # Update layout to fix axes
    dist_chart.update_layout(
        xaxis=dict(
            title="Sustainability Score (out of 10)",
            range=[0, 10]  # Fix the x-axis range to 0-10
        ),
        yaxis=dict(
            title="Sustainability Impact",
            range=[0, None]  # Start y-axis at 0, upper limit adjusts automatically
        )
        #,
        #title="Sustainability Score Distribution Across Key Dimensions"
    )

    st.plotly_chart(dist_chart, use_container_width=True)

    # Display the chart in Streamlit
    # st.markdown(f"**Material Sustainability Analysis**")
    
    # st.markdown(
    # f"""
    # <div style="text-align: center; font-weight: bold; font-size: 16px;">
    #     Material Sustainability Analysis
    # </div>
    # """,
    # unsafe_allow_html=True,
    # )
    
    return star_rating

def get_confidence_score(match_score, sustainability_rating):
    # Calculate confidence score (example calculation)
    w_m, w_s = 0.6, 0.4  # Weights
    M = (match_score / 100) * 10  # Scale match score to 10
    S = (sustainability_rating / 5) * 10  # Scale sustainability to 10
    confidence_score = (w_m * M + w_s * S) / (w_m + w_s)

    return confidence_score

# Define a function to display a business card
def display_business_card(supplier_data):
    # Create a container for the business card
    with st.container():
        st.markdown(
            """
            <style>
            .business-card {
                background-color: #222; /* Matches dark themes */
                color: #f1f1f1;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin-bottom: 20px;
            }
            .business-card h3 {
                margin: 0;
                color: #ffae42;
            }
            .business-card p {
                margin: 5px 0;
                line-height: 1.5;
            }
            .card-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }
            .action-buttons button {
                margin-right: 10px;
                font-size: 14px;
                padding: 8px 12px;
                background-color: #007bff;
                border: none;
                border-radius: 5px;
                color: white;
                cursor: pointer;
                font-weight: bold;
                text-decoration: none;
            }
            .action-buttons button:hover {
                background-color: #0056b3;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="business-card">
                <h4>{supplier_data['Name']}</h4>
                <div class="card-grid">
                    <div>
                        <p><b>Email:</b> <a href="mailto:{supplier_data['Email']}" style="color:#4da6ff;">{supplier_data['Email']}</a></p>
                        <p><b>Phone:</b> <a href="tel:{supplier_data['Phone']}" style="color:#4da6ff;">{supplier_data['Phone']}</a></p>
                        <p><b>Website:</b> <a href="https://{supplier_data['Website']}" style="color:#4da6ff;" target="_blank">{supplier_data['Website']}</a></p>
                    </div>
                    <div>
                        <p><b>Quality Score:</b> {supplier_data['Quality Score']:.1f} / 5.0</p>
                        <p><b>Rating:</b> {supplier_data.get('Rating', 4.5)} ⭐</p>
                        <p><b>Response Time:</b> {supplier_data['Response Time']}h</p>
                        <p><b>Certifications:</b> {supplier_data['Certifications'].split(', ')[0] if supplier_data['Certifications'] else 'N/A'}</p>
                    </div>
                </div>
                <div class="action-buttons">
                    <a href="mailto:{supplier_data['Email']}" target="_blank"><button>Email</button></a>
                    <a href="tel:{supplier_data['Phone']}" target="_blank"><button>Call</button></a>
                    <a href="https://{supplier_data['Website']}" target="_blank"><button>Visit Website</button></a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )