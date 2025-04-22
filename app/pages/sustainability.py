import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from app.data.sustainability_manager import SustainabilityManager

def render_benchmarking(sustainability_mgr, materials, volumes):
    st.markdown("<div id='benchmarking'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🎯 Industry Benchmarking")
    # Calculate portfolio impact
    impact = sustainability_mgr.calculate_portfolio_impact(materials, volumes)
    benchmarks = sustainability_mgr.get_benchmarks()
    
    # Create radar chart for benchmarking
    categories = ['Carbon Footprint', 'Water Usage', 'Energy Usage', 'Recycled Content', 'Bio-based Content']
    fig = go.Figure()
    
    # Scale values to 0-10
    # 0 range for visualization
    def scale_value(value, metric):
        if metric in ['Recycled Content', 'Bio-based Content']:
            return value * 100  # Convert from 0-1 to 0-100
        scaling_factors = {
            'Carbon Footprint': 35,  # Typical range 0-35
            'Water Usage': 50,       # Typical range 0-50
            'Energy Usage': 85,      # Typical range 0-85
        }
        return (value / scaling_factors.get(metric, 1)) * 100
    
    # Your performance
    fig.add_trace(go.Scatterpolar(
        r=[scale_value(impact[cat], cat) for cat in categories],
        theta=categories,
        fill='toself',
        name='Your Performance'
    ))
    
    # Industry average
    fig.add_trace(go.Scatterpolar(
        r=[float(benchmarks[benchmarks['Metric'] == cat]['Industry Average'].iloc[0])
           for cat in categories],
        theta=categories,
        fill='toself',
        name='Industry Average'
    ))
    
    # Top quartile
    fig.add_trace(go.Scatterpolar(
        r=[float(benchmarks[benchmarks['Metric'] == cat]['Top Quartile'].iloc[0])
           for cat in categories],
        theta=categories,
        fill='toself',
        name='Industry Leaders'
    ))
    
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
    st.plotly_chart(fig)

def render_material_analysis(sustainability_mgr):
    st.markdown("<div id='material'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🧪 Material Portfolio Analysis")
    # Material selection with volumes
    st.write("**Select Materials and Volumes**")
    materials_data = {}
    cols = st.columns(3)
    
    all_materials = sustainability_mgr.get_material_metrics()['Material'].tolist()
    selected_materials = st.multiselect("Select materials", all_materials,
                                      default=all_materials[:3])
    
    if selected_materials:
        for i, material in enumerate(selected_materials):
            with cols[i % 3]:
                materials_data[material] = st.number_input(
                    f"{material} (tons/year)",
                    min_value=0, value=1000, step=100
                )
        
        # Get detailed metrics
        metrics = sustainability_mgr.get_material_metrics(selected_materials)
        
        # Material comparison chart
        fig = px.parallel_coordinates(metrics,
            dimensions=['Material', 'Carbon Footprint', 'Water Usage', 'Energy Usage',
                       'Cost Premium', 'Market Growth'],
            title="Material Sustainability Metrics")
        st.plotly_chart(fig)
        
        # Cost impact analysis
        st.subheader("💰 Cost Impact Analysis")
        opportunities = sustainability_mgr.get_cost_savings_opportunities(selected_materials)
        
        if opportunities:
            st.write("**Cost Saving Opportunities:**")
            for opp in opportunities:
                st.info(
                    f"Replace {opp['Current Material']} with {opp['Alternative']}:\n" +
                    f"- Cost Savings: {opp['Cost Savings']}\n" +
                    f"- Carbon Impact: {opp['Carbon Impact']} kg CO2e/ton\n" +
                    f"- Water Impact: {opp['Water Impact']} m3/ton"
                )
        else:
            st.success("Your material selection is optimized for cost and sustainability.")

def render_supply_chain_impact(sustainability_mgr):
    st.markdown("<div id='supply-chain'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🌐 Enhanced Supply Chain Analysis")
    # Create sample supplier data with more dimensions
    supplier_data = pd.DataFrame({
        'Supplier': ['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D'],
        'Carbon Score': [85, 72, 93, 68],
        'Water Score': [78, 88, 90, 75],
        'Cost Index': [95, 82, 75, 98],
        'Quality Score': [92, 88, 95, 85],
        'Volume': [1000, 800, 1200, 500],
        'Innovation Score': [88, 92, 85, 70]
    })
    
    # Create bubble chart with multiple dimensions
    fig = px.scatter(supplier_data,
        x='Carbon Score',
        y='Water Score',
        size='Volume',
        color='Cost Index',
        hover_name='Supplier',
        hover_data=['Quality Score', 'Innovation Score'],
        title='Multi-dimensional Supplier Sustainability Matrix')
    
    fig.update_layout(
        xaxis_title="Carbon Performance",
        yaxis_title="Water Management",
        coloraxis_colorbar_title="Cost Index")
    
    st.plotly_chart(fig)
    
    # Supplier recommendations
    st.write("**📋 Strategic Recommendations:**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Short-term Actions:**\n" +
                "1. Shift 20% volume from Supplier D to C\n" +
                "2. Joint innovation project with Supplier B\n" +
                "3. Cost optimization workshop with Supplier C")
    
    with col2:
        st.success("**Long-term Strategy:**\n" +
                  "1. Develop Supplier D's sustainability capabilities\n" +
                  "2. Expand relationship with Supplier C\n" +
                  "3. Establish innovation hub with top performers")

def render_sustainability_page():
    """Render the sustainability analysis page."""
    st.title("Sustainability Analysis")
    st.write("""This section provides tools and insights for analyzing and improving 
             the sustainability of your materials and supply chain.""")
    
    # Initialize sustainability manager
    sustainability_mgr = SustainabilityManager()
    
    # Quick stats in main content area
    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
    with metrics_col1:
        st.metric("Overall Score", "78/100", "+5")
    with metrics_col2:
        st.metric("Cost Savings", "$2.1M", "15%")
    with metrics_col3:
        st.metric("Carbon Reduction", "25%", "Target: 30%")
    
    # Render each section with real materials
    materials = ["PET", "HDPE", "PP"]
    volumes = {mat: vol for mat, vol in zip(materials, [1000, 800, 1200])}
    
    render_benchmarking(sustainability_mgr, materials, volumes)
    render_material_analysis(sustainability_mgr)
    render_supply_chain_impact(sustainability_mgr)
    
    # Action center with cost implications
    st.subheader("🎬 Action Center")
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        st.warning(
            "⚠️ **Priority Actions & Cost Impact**\n\n" +
            "1. ISO 14001 audit preparation (-$25K)\n" +
            "2. Water reduction program (+$150K/year savings)\n" +
            "3. Supplier sustainability program (-$50K, +$300K/year savings)"
        )
    
    with action_col2:
        st.success(
            "✅ **Value Creation Opportunities**\n\n" +
            "1. Bio-based materials transition (+$2.1M market opportunity)\n" +
            "2. Circular economy program (+$800K/year savings)\n" +
            "3. Green premium products (+15% margin potential)"
        )
