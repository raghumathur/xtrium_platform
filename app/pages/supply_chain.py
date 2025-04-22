import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from app.data.supplier_manager import SupplierManager

def render_supplier_details(supplier_data):
    """Render detailed information about a supplier."""
    # Create three columns for key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Quality Score", f"{supplier_data['Quality Score']:.1f}", "5.0 max")
    with col2:
        st.metric("On-Time Delivery", supplier_data['On-Time Delivery'], "Target: 95%")
    with col3:
        st.metric("Response Time", f"{supplier_data['Response Time']}h", "Target: 24h")
    
    # Company information
    st.subheader("Company Information")
    info_cols = st.columns([2, 1])
    with info_cols[0]:
        st.write(f"**Founded:** {supplier_data['Founded']}")
        st.write(f"**Annual Revenue:** ${supplier_data['Annual Revenue']}")
        st.write(f"**Website:** [{supplier_data['Website']}](https://{supplier_data['Website']})")
        st.write(f"**Materials:** {supplier_data['Materials']}")
        st.write(f"**Specialties:** {supplier_data['Specialties']}")
    with info_cols[1]:
        st.write(f"**Email:** {supplier_data['Email']}")
        st.write(f"**Phone:** {supplier_data['Phone']}")
        st.write(f"**Address:** {supplier_data['Address']}")
    
    # Certifications
    st.subheader("Certifications")
    for cert in supplier_data['Certifications'].split(', '):
        st.markdown(f"🏅 {cert}")
    
    # Contact form
    st.subheader("Contact Supplier")
    form_key = f"contact_form_{supplier_data['Name'].lower().replace(' ', '_')}"
    with st.form(form_key):
        subject = st.text_input("Subject")
        message = st.text_area("Message")
        files = st.file_uploader("Attach Files", accept_multiple_files=True)
        submitted = st.form_submit_button("Send Message")
        if submitted:
            st.success("Message sent! The supplier will contact you shortly.")

def render_supply_chain_page():
    st.header("Supply Chain Management")
    
    # Initialize supplier manager
    supplier_mgr = SupplierManager()
    
    # Suppliers section
    st.markdown("<div id='suppliers'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🏭 Suppliers")
    
    # Overview metrics
    suppliers_df = supplier_mgr.get_all_suppliers()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Suppliers", len(suppliers_df), "+3")
    with col2:
        st.metric("Average Rating", f"{suppliers_df['Rating'].mean():.1f}", "+0.2")
    with col3:
        st.metric("Global Regions", len(suppliers_df['Region'].unique()), None)
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["🔍 Supplier Discovery", "📊 Supply Chain Analytics"])
    
    with tab1:
        # Search and filter section
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input("Search by name, materials, or specialties", 
                                        placeholder="e.g., polymers, composites, specialty chemicals")
        
        with col2:
            region_filter = st.selectbox("Region", ["All"] + supplier_mgr.get_regions())
        
        # Advanced filters in an expander
        with st.expander("Advanced Filters"):
            filter_cols = st.columns(3)
            with filter_cols[0]:
                min_rating = st.slider("Minimum Rating", 1.0, 5.0, 4.0, 0.1)
            with filter_cols[1]:
                certification = st.selectbox("Certification", ["Any"] + supplier_mgr.get_certifications())
            with filter_cols[2]:
                material_type = st.selectbox("Material Type", ["Any"] + supplier_mgr.get_materials())
        
        # Apply filters
        filters = {
            'region': region_filter if region_filter != "All" else None,
            'min_rating': min_rating,
            'certification': certification if certification != "Any" else None
        }
        
        filtered_suppliers = supplier_mgr.search_suppliers(search_query, filters)
        
        # Display results
        st.subheader(f"Found {len(filtered_suppliers)} Suppliers")
        
        # Create map with custom styling
        st.markdown("""
            <style>
            .folium-map {
                width: 100% !important;
                margin: 0 auto;
            }
            </style>
        """, unsafe_allow_html=True)
        
        m = folium.Map(location=[20, 0], zoom_start=2, width='100%')
        for _, supplier in filtered_suppliers.iterrows():
            folium.Marker(
                [supplier['Latitude'], supplier['Longitude']],
                popup=supplier['Name'],
                tooltip=f"{supplier['Name']} ({supplier['Country']})"
            ).add_to(m)
        folium_static(m, width=1200)
        
        # Display supplier cards
        st.subheader("Supplier Details")
        for _, supplier in filtered_suppliers.iterrows():
            with st.expander(f"{supplier['Name']} - {supplier['Country']}", expanded=False):
                render_supplier_details(supplier)
        
        # Supplier comparison section
        st.markdown("---")
        st.subheader("📆 Compare Suppliers")
        
        # Select suppliers to compare
        supplier_names = filtered_suppliers['Name'].tolist()
        col1, col2 = st.columns(2)
        with col1:
            supplier1 = st.selectbox("Select First Supplier", supplier_names, key="supplier1")
        with col2:
            remaining_suppliers = [s for s in supplier_names if s != supplier1]
            supplier2 = st.selectbox("Select Second Supplier", remaining_suppliers, key="supplier2")
        
        if supplier1 and supplier2:
            # Get supplier data
            s1_data = filtered_suppliers[filtered_suppliers['Name'] == supplier1].iloc[0]
            s2_data = filtered_suppliers[filtered_suppliers['Name'] == supplier2].iloc[0]
            
            # Create comparison tabs
            comp_tab1, comp_tab2, comp_tab3 = st.tabs(["📊 Performance Metrics", "📋 Company Info", "🏅 Certifications"])
            
            with comp_tab1:
                # Performance metrics comparison
                metrics = [
                    ("Quality Score", "Quality Score", "Higher is better"),
                    ("On-Time Delivery", "On-Time Delivery", "Higher is better"),
                    ("Response Time", "Response Time", "Lower is better"),
                    ("Rating", "Rating", "Higher is better")
                ]
                
                for metric, key, note in metrics:
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        val1 = float(s1_data[key]) if isinstance(s1_data[key], str) and s1_data[key].replace('.', '').isdigit() else s1_data[key]
                        st.metric(f"{supplier1} {metric}", val1)
                    with col2:
                        val2 = float(s2_data[key]) if isinstance(s2_data[key], str) and s2_data[key].replace('.', '').isdigit() else s2_data[key]
                        st.metric(f"{supplier2} {metric}", val2)
                    with col3:
                        st.caption(note)
            
            with comp_tab2:
                # Company information comparison
                info_fields = [
                    "Founded", "Annual Revenue", "Materials", "Specialties", "Region", "Country"
                ]
                
                for field in info_fields:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**{supplier1}**")
                        st.write(s1_data[field])
                    with col2:
                        st.write(f"**{supplier2}**")
                        st.write(s2_data[field])
                    st.markdown("---")
            
            with comp_tab3:
                # Certifications comparison
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**{supplier1} Certifications**")
                    for cert in s1_data['Certifications'].split(', '):
                        st.markdown(f"🏅 {cert}")
                with col2:
                    st.write(f"**{supplier2} Certifications**")
                    for cert in s2_data['Certifications'].split(', '):
                        st.markdown(f"🏅 {cert}")
                
                # Find common and unique certifications
                s1_certs = set(s1_data['Certifications'].split(', '))
                s2_certs = set(s2_data['Certifications'].split(', '))
                common_certs = s1_certs.intersection(s2_certs)
                
                if common_certs:
                    st.markdown("**Common Certifications**")
                    for cert in common_certs:
                        st.markdown(f"✨ {cert}")
    
    # Inventory section
    st.markdown("<div id='inventory'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📦 Inventory Management")
    inventory_col1, inventory_col2 = st.columns(2)
    with inventory_col1:
        st.metric("Total SKUs", "1,250", "+50")
        st.metric("Stock Value", "$2.5M", "+$200K")
    with inventory_col2:
        st.metric("Stockouts", "12", "-3")
        st.metric("Turnover Rate", "4.2x", "+0.3")
    
    with tab2:
        # Supply Chain Analytics content
        st.subheader("Supply Chain Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            # Regional distribution
            st.write("**Supplier Distribution by Region**")
            region_dist = suppliers_df['Region'].value_counts()
            st.bar_chart(region_dist)
        
        with col2:
            # Material type distribution
            st.write("**Material Type Distribution**")
            material_dist = pd.Series([item.strip() for items in suppliers_df['Materials'].str.split(',') for item in items]).value_counts().head(10)
            st.bar_chart(material_dist)
        
        # Risk assessment
        st.subheader("Risk Assessment")
        risks = {
            "Supply Disruption": 0.3,
            "Cost Volatility": 0.6,
            "Quality Issues": 0.2,
            "Regulatory Compliance": 0.4,
            "Geopolitical Risk": 0.5
        }
        for risk, value in risks.items():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.write(risk)
            with col2:
                st.progress(value)
                st.caption(f"{'Low' if value < 0.3 else 'Medium' if value < 0.7 else 'High'} Risk")
    
    # Cost Analysis section
    st.markdown("<div id='cost_analysis'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("💰 Cost Analysis")
    
    # Create tabs for different cost views
    cost_tab1, cost_tab2 = st.tabs(["Cost Overview", "Cost Trends"])
    
    with cost_tab1:
        # Cost metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Cost per Unit", "$245", "-$12")
        with col2:
            st.metric("Total Procurement Cost", "$1.2M", "+$50K")
        with col3:
            st.metric("Cost Savings YTD", "$125K", "+15%")
        
        # Cost breakdown
        st.subheader("Cost Breakdown")
        cost_data = pd.DataFrame({
            'Category': ['Raw Materials', 'Transportation', 'Storage', 'Processing', 'Other'],
            'Cost': [450000, 280000, 150000, 220000, 100000]
        })
        
        # Calculate percentages
        total_cost = cost_data['Cost'].sum()
        cost_data['Percentage'] = (cost_data['Cost'] / total_cost * 100).round(1)
        cost_data['Label'] = cost_data.apply(lambda x: f"${x['Cost']:,.0f} ({x['Percentage']}%)", axis=1)
        
        # Create bar chart
        st.bar_chart(cost_data.set_index('Category')['Cost'])
        
        # Display detailed breakdown
        st.write("**Detailed Breakdown:**")
        for _, row in cost_data.iterrows():
            st.write(f"- {row['Category']}: {row['Label']}")
    
    with cost_tab2:
        # Monthly cost trends
        st.subheader("Monthly Cost Trends")
        
        # Generate sample monthly data
        months = pd.date_range(start='2024-01-01', end='2024-12-31', freq='ME')
        monthly_costs = pd.DataFrame({
            'Month': months,
            'Raw Materials': np.random.normal(450000, 20000, len(months)),
            'Transportation': np.random.normal(280000, 15000, len(months)),
            'Storage': np.random.normal(150000, 5000, len(months))
        })
        
        # Plot trends
        monthly_costs.set_index('Month', inplace=True)
        st.line_chart(monthly_costs)
        
        # Cost saving opportunities
        st.subheader("Cost Saving Opportunities")
        opportunities = [
            {
                "title": "Bulk Purchase Discounts",
                "potential_savings": "$35,000",
                "implementation": "Medium",
                "impact": "High"
            },
            {
                "title": "Optimized Shipping Routes",
                "potential_savings": "$28,000",
                "implementation": "Low",
                "impact": "Medium"
            },
            {
                "title": "Inventory Optimization",
                "potential_savings": "$42,000",
                "implementation": "High",
                "impact": "High"
            }
        ]
        
        for opp in opportunities:
            with st.expander(f"{opp['title']} - Potential Savings: {opp['potential_savings']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Implementation Difficulty:** {opp['implementation']}")
                with col2:
                    st.write(f"**Impact:** {opp['impact']}")

    
    # Risk Assessment section
    st.markdown("<div id='risk_assessment'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("⚠️ Risk Assessment")
    # Performance metrics
    metrics_cols = st.columns(2)
    with metrics_cols[0]:
        st.write("Average Response Time by Region")
        response_time = suppliers_df.groupby('Region')['Response Time'].mean().sort_values()
        st.bar_chart(response_time)
    with metrics_cols[1]:
        st.write("Quality Score Distribution")
        st.line_chart(suppliers_df['Quality Score'].value_counts().sort_index())
