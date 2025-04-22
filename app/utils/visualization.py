import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class MaterialVisualizer:
    @staticmethod
    def create_radar_chart(material, comparison_material=None):
        properties = ['tensile_strength', 'elastic_modulus', 'thermal_conductivity', 
                     'cost_per_kg', 'sustainability_score']

        fig = go.Figure()

        # Normalize values
        max_values = {
            'tensile_strength': 1000,
            'elastic_modulus': 200,
            'thermal_conductivity': 400,
            'cost_per_kg': 100,
            'sustainability_score': 10
        }

        values = [material[prop]/max_values[prop] for prop in properties]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=properties,
            fill='toself',
            name=material['name']
        ))

        if comparison_material:
            comp_values = [comparison_material[prop]/max_values[prop] for prop in properties]
            fig.add_trace(go.Scatterpolar(
                r=comp_values,
                theta=properties,
                fill='toself',
                name=comparison_material['name']
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True
        )
        return fig

    @staticmethod
    def create_supply_chain_risk_chart(material):
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=material['supply_chain_risk_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 10]},
                'steps': [
                    {'range': [0, 3], 'color': "lightgreen"},
                    {'range': [3, 7], 'color': "yellow"},
                    {'range': [7, 10], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': material['supply_chain_risk_score']
                }
            }
        ))
        fig.update_layout(title="Supply Chain Risk Score")
        return fig

    @staticmethod
    def create_risk_vs_cost_scatter(materials_df):
        fig = px.scatter(
            materials_df,
            x="supply_chain_risk_score",
            y="cost_per_kg",
            color="category",
            size="availability_score",
            hover_data=["name", "manufacturer"],
            title="Supply Chain Risk vs. Cost Analysis"
        )
        fig.update_layout(
            xaxis_title="Supply Chain Risk Score",
            yaxis_title="Cost ($/kg)"
        )
        return fig

    @staticmethod
    def create_manufacturer_analysis_chart(manufacturer_data):
        df = pd.DataFrame(manufacturer_data)
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df['manufacturer'],
            y=df['material_count'],
            name='Material Count'
        ))

        fig.add_trace(go.Scatter(
            x=df['manufacturer'],
            y=df['avg_risk_score'],
            name='Avg Risk Score',
            yaxis='y2'
        ))

        fig.update_layout(
            title='Manufacturer Analysis',
            yaxis=dict(title='Material Count'),
            yaxis2=dict(
                title='Average Risk Score',
                overlaying='y',
                side='right'
            ),
            showlegend=True
        )
        return fig