import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
1
from assets.temp_data.db_connector import DatabaseConnector
from app.utils.visualization import MaterialVisualizer

def render_supply_chain_analysis():
    st.title("Supply Chain Analysis")

    db = DatabaseConnector()

    # Get all materials
    materials = db.get_materials()

    if not materials.get('materials'):
        st.error("No materials data available.")
        return

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(materials['materials'])

    # Supply Chain Risk Overview
    st.header("Supply Chain Risk Overview")

    # Risk Distribution
    fig_risk = px.histogram(
        df,
        x="supply_chain_risk_score",
        nbins=20,
        title="Distribution of Supply Chain Risk Scores",
        labels={"supply_chain_risk_score": "Risk Score", "count": "Number of Materials"}
    )
    fig_risk.update_layout(showlegend=False)
    st.plotly_chart(fig_risk)

    # Risk vs. Cost Analysis
    if all(col in df.columns for col in ['supply_chain_risk_score', 'cost_per_kg', 'category', 'availability_score']):
        fig_cost = px.scatter(
            df,
            x="supply_chain_risk_score",
            y="cost_per_kg",
            color="category",
            size="availability_score",
            hover_data=["name", "manufacturer"],
            title="Supply Chain Risk vs. Cost Analysis",
            labels={
                "supply_chain_risk_score": "Risk Score",
                "cost_per_kg": "Cost ($/kg)",
                "category": "Material Category"
            }
        )
        st.plotly_chart(fig_cost)
    else:
        st.warning("Missing required columns for risk vs. cost analysis")

    # Manufacturer Analysis
    st.header("Manufacturer Performance")
    manufacturer_data = db.get_manufacturer_analysis()
    if manufacturer_data:
        st.plotly_chart(MaterialVisualizer.create_manufacturer_analysis_chart(manufacturer_data))

    # Material Selection and Analysis
    st.header("Material Supply Chain Details")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        selected_category = st.selectbox(
            "Filter by Category",
            options=["All"] + sorted(df["category"].unique().tolist())
        )

    with col2:
        max_risk = st.slider(
            "Maximum Supply Chain Risk Score",
            min_value=0.0,
            max_value=10.0,
            value=10.0
        )

    # Filter materials
    filtered_df = df.copy()
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]
    filtered_df = filtered_df[filtered_df["supply_chain_risk_score"] <= max_risk]

    # Display filtered materials
    if not filtered_df.empty:
        # Material selection
        selected_material = st.selectbox(
            "Select Material for Detailed Analysis",
            options=filtered_df["name"].tolist()
        )

        if selected_material:
            material_data = filtered_df[filtered_df["name"] == selected_material].iloc[0]

            # Material supply chain dashboard
            col1, col2 = st.columns(2)

            with col1:
                # Supply Chain Risk Gauge
                st.plotly_chart(MaterialVisualizer.create_supply_chain_risk_chart(material_data))

                # Material Info
                st.subheader("Supply Chain Information")
                st.write(f"**Manufacturer:** {material_data['manufacturer']}")
                st.write(f"**Availability Score:** {material_data['availability_score']}/10")
                st.write(f"**Cost per kg:** ${material_data['cost_per_kg']:.2f}")

            with col2:
                # Availability Gauge
                fig_availability = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=material_data['availability_score'],
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Availability Score"},
                    gauge={
                        'axis': {'range': [0, 10]},
                        'steps': [
                            {'range': [0, 3], 'color': "red"},
                            {'range': [3, 7], 'color': "yellow"},
                            {'range': [7, 10], 'color': "green"}
                        ]
                    }
                ))
                st.plotly_chart(fig_availability)

            # Risk Analysis
            st.subheader("Risk Analysis")

            # Create radar chart for risk factors
            risk_factors = {
                'Supply Chain Risk': material_data['supply_chain_risk_score']/10,
                'Cost Risk': min(material_data['cost_per_kg']/1000, 1),
                'Availability Risk': (10 - material_data['availability_score'])/10,
                'Sustainability Risk': (10 - material_data['sustainability_score'])/10
            }

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=list(risk_factors.values()),
                theta=list(risk_factors.keys()),
                fill='toself',
                name=material_data['name']
            ))

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
                ),
                showlegend=False
            )
            st.plotly_chart(fig_radar)

            # Supply Chain Recommendations
            st.subheader("Supply Chain Recommendations")

            # Get risk level
            risk_level = 'high' if material_data['supply_chain_risk_score'] > 7 else \
                        'medium' if material_data['supply_chain_risk_score'] > 4 else 'low'

            recommendations = db.get_supply_chain_recommendations(
                risk_level=risk_level,
                material_category=material_data['category']
            )

            if recommendations:
                for rec in recommendations:
                    with st.expander(f"🔍 {rec['recommendation_type'].title()} Strategy - Priority {rec['priority']}"):
                        st.write(rec['recommendation_text'])
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Implementation Cost:** {'💰' * rec['implementation_cost']}")
                        with col2:
                            st.write(f"**Estimated Impact:** {rec['estimated_impact']*100:.0f}%")
            else:
                st.info("No specific recommendations available for this material.")
    else:
        st.warning("No materials found matching the selected criteria.")