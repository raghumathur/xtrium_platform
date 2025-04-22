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

# Import the recommend_materials_for_application function from the materials recommendation module
# This function provides recommendations for materials based on the selected application.
# It likely uses some kind of algorithm or logic to identify materials that are suitable
# for a given use case or set of requirements.
from app.components.search_materials.materials_recommend import recommend_materials_for_application

# Import the render_application_filters function from the application filters module
# This function is used to render application-specific filters in the UI.
# These filters allow users to narrow down their search or selection of materials based
# on criteria like application type, material properties, or other attributes.
from app.components.search_materials.application_filters import render_application_filters
from app.utils.property_filters import applications_property_filters
#==========================================================================================

def render_material_recommendation(applications_df, materials_df):
    """
    Renders the Material Recommendation Engine based on selected applications and filters.

    :param applications_df: Unified applications database DataFrame.
    :param materials_df: Unified materials database DataFrame.
    """
    # st.markdown("## Material Recommendation Engine")
    
    # Create two columns for paint type and color selection
    col1, col2 = st.columns(2)
    
    # Select paint type in first column
    with col1:
        paint_types = ["Select paint type..."] + sorted(applications_df["paint_type"].dropna().unique().tolist())
        selected_paint_type = st.selectbox(
            "Select Paint Type",
            options=paint_types,
            key="selected_paint_type"
        )
    
    # Color picker in second column
    with col2:
        selected_color = st.color_picker(
            "Select Paint Color",
            value="#000000",  # Default to black
            key="selected_paint_color"
        )
    
    if not selected_paint_type or selected_paint_type == "Select paint type...":
        st.warning("Please select a paint type to proceed.")
        return
    
    # Filter applications by paint type and select an application
    filtered_applications = applications_df[applications_df["paint_type"] == selected_paint_type]
    applications = ["Select application..."] + sorted(filtered_applications["use_case"].dropna().unique().tolist())
    selected_application = st.selectbox(
        "Select an Application",
        options=applications,
        key="selected_application"
    )
    
    if not selected_application or selected_application == "Select application...":
        st.warning("Please select an application to proceed.")
        return

    """
    # Monitor selected_materials for changes and reset filters if needed
    if "selected_application" not in st.session_state:
        st.session_state["selected_application"] = None    

    # Check if the selected material has changed
    if st.session_state["selected_materials"] != selected_application:
        st.session_state["filters"] = []  # Reset filters
        st.session_state["selected_materials"] = selected_application
        #st.info("Filters reset due to material change.")
    """
    
    # Get the selected application row
    application_row = filtered_applications[filtered_applications["use_case"] == selected_application].iloc[0]
    #st.write(application_row)

    # Add dynamic filters for material properties
    #selected_filters = render_application_filters(tab_index="material_recommendation", materials_df=materials_df)
    selected_filters = applications_property_filters(tab_index="material_recommendation", materials_df=materials_df)
    #st.write(selected_filters)

    # Suggest materials button
    st.divider()
    if st.button("Suggest Materials", key="suggest_material_button"):
        # Generate recommendations
        recommended_materials = recommend_materials_for_application(application_row, materials_df, selected_filters)

        # Display recommendations
        display_material_recommendations(recommended_materials)

def display_material_recommendations(recommendations_df):
    """
    Display recommended materials in a user-friendly format.

    :param recommendations_df: DataFrame containing material recommendations.
    """
    if recommendations_df.empty:
        st.warning("No materials match the selected criteria.")
        return

    for idx, row in recommendations_df.iterrows():
        material_name = row.get("Material Name", "Unknown")
        material_formula = row.get("Chemical Formula", None)
        property_overlap = row.get("Property Overlap", None)
        match_score = row.get("Match Score", 0)

        with st.expander(material_name, icon=":material/insights:"): # icons=waves, science, bolt, assessment, trending up, storage, timeline
            st.markdown(f"#### Material: {material_name}")
            st.markdown(f"#### Chemical Formula: {material_formula}")
            #st.markdown(f"##### Property Overlap: {property_overlap}")
            st.markdown(f"###### {property_overlap}")

            # st.divider()
            st.progress(int(match_score))
            # st.markdown(f"**Match Score:** {match_score}%")
            #st.markdown("---")
            st.markdown(
                f"""
                <div style="text-align: center; font-weight: bold; font-size: 16px;">
                    Properties Match Score: {match_score}%
                </div>
                """,
                unsafe_allow_html=True,
            )
            #st.divider()
            sustainability_rating = get_sustainability_score();
            confidence_score = get_confidence_score(match_score, sustainability_rating)

            # Normalize all scores to 5-star ratings
            match_score_normalized = (match_score / 100) * 5
            confidence_score_normalized = (confidence_score / 10) * 5
            sustainability_score_normalized = sustainability_rating

            # Create individual charts
            match_chart = create_gauge_chart(match_score_normalized, "Compatibility Score")
            confidence_chart = create_gauge_chart(confidence_score_normalized, "Overall Confidence Score")
            sustainability_chart = create_gauge_chart(sustainability_score_normalized, "Sustainability Score")

            #st.divider()            
            col1, col2, col3 = st.columns([3,5,3])
            with col1:
                st.plotly_chart(match_chart, use_container_width=True, key=f"match_chart_{idx}")
            with col2:
                st.plotly_chart(confidence_chart, use_container_width=True, key=f"confidence_chart_{idx}")
            with col3:
                st.plotly_chart(sustainability_chart, use_container_width=True, key=f"sustainability_chart_{idx}")
            #st.divider()
            #supp_modal = modal("key=supp_key_{idx}", title="Suppliers Info")
            #modalbutton = st.button(label='Commercial Info')
            #if modalbutton:
            #    with supp_modal.contaoner():
            #            st.markdown('test')
            display_business_card(
                name="Company A",
                contact_email="company_a@example.com",
                contact_number="+1234567890",
                #availability="In Stock",
                cost_range="$180 - $200",
                rating=4.5,
                certifications="ISO 9001, CE"
            )
            display_business_card(
                name="Company B",
                contact_email="supplier_b@example.com",
                contact_number="+9876543210",
                #availability="Limited",
                cost_range="$50 - $150",
                rating=4.0,
                certifications="RoHS"
            )


def find_materials():
    """
    Processes input data to identify and recommend materials based on selected applications and dynamic filters.

    Args:
        databases (list): A list of databases containing materials, applications, and other relevant information.

    Steps:
        1. Extract dataframes from the provided databases.
        2. Call the render_material_recommendation function with the extracted data.
    """
    # Step 1: Extract DataFrames
    # Extract relevant dataframes (e.g., materials and applications) from the input databases.
    materials_df, applications_df, *_ = extract_dataframes(st.session_state.databases)

    # Step 2: Call render_material_recommendation
    # Pass the extracted dataframes to the rendering function.
    render_material_recommendation(applications_df, materials_df)

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
    environmental_scores = np.random.normal(loc=7, scale=1, size=200)
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
    regulatory_scores = np.random.normal(loc=6, scale=1, size=200)
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

    st.plotly_chart(dist_chart, use_container_width=True)

    return star_rating

def get_confidence_score(match_score, sustainability_rating):
    # Calculate confidence score (example calculation)
    w_m, w_s = 0.6, 0.4  # Weights
    M = (match_score / 100) * 10  # Scale match score to 10
    S = (sustainability_rating / 5) * 10  # Scale sustainability to 10
    confidence_score = (w_m * M + w_s * S) / (w_m + w_s)

    return confidence_score

# Define a function to display a business card
#def display_business_card(name, contact_email, contact_number, availability, cost_range, rating, certifications):
def display_business_card(name, contact_email, contact_number, cost_range, rating, certifications):
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
                font-size: 10px;
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
                <h4>{name}</h4>
                <div class="card-grid">
                    <div>
                        <p><b>Email:</b> <a href="mailto:{contact_email}" style="color:#4da6ff;">{contact_email}</a></p>
                        <p><b>Phone:</b> <a href="tel:{contact_number}" style="color:#4da6ff;">{contact_number}</a></p>
                    </div>
                    <div>
                        <p><b>Cost Range:</b> {cost_range}</p>
                        <p><b>Rating:</b> {rating} ⭐</p>
                        <p><b>Certifications:</b> {certifications}</p>
                    </div>
                </div>
                <div class="action-buttons">
                    <a href="mailto:{contact_email}" target="_blank"><button>Email</button></a>
                    <a href="tel:{contact_number}" target="_blank"><button>Call</button></a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )