import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta
from app.ui.theme import Colors
from app.data.dashboard_manager import DashboardDataManager

# Initialize the dashboard data manager
data_manager = DashboardDataManager()

def render_home_page():
    st.header("Dashboard")
    
    # Add smooth scrolling CSS
    st.markdown("""
        <style>
            html {
                scroll-behavior: smooth;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Add metric styling
    st.markdown("""
        <style>
            div[data-testid="stMetricValue"] > div {
                font-size: 2rem !important;
                font-weight: 600 !important;
            }
            div[data-testid="stMetricLabel"] > label {
                font-size: 1.25rem !important;
                font-weight: 500 !important;
            }
            div[data-testid="stMetricDelta"] > div {
                font-size: 1.2rem !important;
                font-weight: 500 !important;
            }
            div[data-testid="metric-container"] {
                padding: 1rem !important;
                gap: 0.5rem !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Overview metrics section anchor
    st.markdown("<div id='metrics'></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        [data-testid="stMetricValue"] {
            font-size: 24px;
        }
        [data-testid="stMetricDelta"] svg {
            display: none;
        }
        .sustainability-score {
            text-align: center;
            padding: 1rem;
            border-radius: 10px;
            background: linear-gradient(135deg, #1a5d1a, #2d862d);
            color: white;
        }
        .supply-risk {
            text-align: center;
            padding: 1rem;
            border-radius: 10px;
            background: linear-gradient(135deg, #8B0000, #CD5C5C);
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    # Fetch metrics from database
    metrics = [
        ("Active Projects", "normal"),
        ("Total Materials", "normal"),
        ("Team Members", "normal"),
        ("Saved Searches", "normal")
    ]
    
    for (metric, delta_color), col in zip(metrics, [col1, col2, col3, col4]):
        value, change, change_type = data_manager.get_metric_value(metric)
        # Convert values to integers
        value = int(float(value))
        change = int(float(change))
        # Add + or - based on change type
        formatted_change = f"{'+' if change_type == 'increase' else '-' if change_type == 'decrease' else ''}{change}"
        with col:
            st.metric(metric, str(value), formatted_change, delta_color=delta_color)
    
    # Section divider
    st.markdown(f"<hr style='margin: 2rem 0; border: none; border-top: 2px solid {Colors.DIVIDER};'>", unsafe_allow_html=True)
    
    # Project Status Overview
    st.markdown("<div id='projects'></div>", unsafe_allow_html=True)
    #st.markdown("---")
    st.markdown("### 📃 Project Status and Progress")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Active Projects")
        # Get project data from database
        projects = data_manager.get_project_data()
        
        # Create progress bars chart
        base = alt.Chart(projects).encode(
            y=alt.Y('Project:N', sort='-x', title=None)
        )
        
        # Background bar
        background = base.mark_bar(color='#eee', height=20).encode(
            x=alt.X('Progress:Q', title='Completion %',
                    scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(grid=True))
        )
        
        # Colored progress bar
        progress = base.mark_bar(height=20).encode(
            x='Progress:Q',
            color=alt.Color('Status:N', scale=alt.Scale(
                domain=['On Track', 'Delayed', 'At Risk'],
                range=['#2ECC71', '#F1C40F', '#E74C3C']
            )),
            tooltip=['Project', 'Progress', 'Status', 'DueDate']
        )
        
        # Combine the charts
        chart = (background + progress).properties(height=200)
        st.altair_chart(chart, use_container_width=True)
    
    with col2:
        st.markdown("#### Project Metrics")
        # Get project metrics from database
        metrics = data_manager.get_project_metrics()
        col1, col2 = st.columns(2)
        
        # Display project statistics
        with col1:
            for metric in ['Active Projects', 'Avg Completion']:
                value, change, change_type = data_manager.get_metric_value(metric)
                # Convert values to integers
                value = int(float(value))
                change = int(float(change))
                suffix = '%' if 'Completion' in metric else ''
                # Add + or - based on change type
                formatted_change = f"{'+' if change_type == 'increase' else '-' if change_type == 'decrease' else ''}{change}"
                st.metric(
                    metric,
                    f"{value}{suffix}",
                    f"{formatted_change} {'%' if 'Completion' in metric else 'this month'}",
                    delta_color="normal"
                )
        
        with col2:
            for metric in ['On Track Projects', 'At Risk Projects']:
                value, change, change_type = data_manager.get_metric_value(metric)
                # Convert values to integers
                value = int(float(value))
                change = int(float(change))
                # Add + or - based on change type
                formatted_change = f"{'+' if change_type == 'increase' else '-' if change_type == 'decrease' else ''}{change}"
                st.metric(
                    metric.replace('Projects', ''),
                    f"{value}%",
                    f"{formatted_change} projects",
                    delta_color="normal" if 'On Track' in metric else "off"
                )
        
        # Get project phases from database
        st.markdown("#### Project Phases")
        phases_data = data_manager.get_project_phases()
        
        chart = alt.Chart(phases_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Projects", type="quantitative"),
            color=alt.Color(
                field="Phase",
                type="nominal",
                scale=alt.Scale(scheme='category10')
            ),
            tooltip=['Phase', 'Projects']
        ).properties(height=200)
        
        st.altair_chart(chart, use_container_width=True)
        
    
    # Section divider
    st.markdown(f"<hr style='margin: 2rem 0; border: none; border-top: 2px solid {Colors.DIVIDER};'>", unsafe_allow_html=True)
    
    # Material Matches and Industry Applications
    st.markdown("<div id='materials'></div>", unsafe_allow_html=True)
    st.markdown("### 🔍 Material and Application Insights")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top Material Matches")
        # Get material matches from database
        matches_data = data_manager.get_material_matches()
        
        # Create material matches chart
        chart = alt.Chart(matches_data).mark_bar().encode(
            x=alt.X('Match Score:Q', title='Match Score (%)'),
            y=alt.Y('Material:N', sort='-x'),
            color=alt.Color('Match Score:Q', scale=alt.Scale(
                domain=[80, 100],
                range=['#3498DB', '#2ECC71']
            )),
            tooltip=['Material', 'Match Score', 'Applications', 'Properties']
        ).properties(height=200)
        
        st.altair_chart(chart, use_container_width=True)
        
        # Key material insights
        st.markdown("##### Key Material Insights")
        insights = [
            "🌟 **Best Match:** Ti-6Al-4V - 98% match for aerospace applications",
            "📈 **Trending:** 35% increase in PEEK applications",
            "💰 **Cost Effective:** Al 7075 offers 25% cost reduction"
        ]
        for insight in insights:
            st.markdown(insight)
    
    with col2:
        st.markdown("#### Industry Applications")
        # Get industry data from database
        industry_data = data_manager.get_industry_data()
        
        # Create bubble chart for industry applications
        chart = alt.Chart(industry_data).mark_circle().encode(
            x=alt.X('Projects:Q', title='Active Projects'),
            y=alt.Y('Materials:Q', title='Materials Used'),
            size=alt.Size('Growth:Q', scale=alt.Scale(range=[100, 500]), title='Growth %'),
            color=alt.Color('Industry:N', scale=alt.Scale(scheme='category10')),
            tooltip=['Industry', 'Projects', 'Materials', 'Growth']
        ).properties(height=250)
        
        st.altair_chart(chart, use_container_width=True)
        
        # Industry insights
        st.markdown("##### Industry Trends")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            🚀 **Aerospace**
            - 25% YoY growth
            - 15 active projects
            - 25 materials
            """)
            st.markdown("""
            💉 **Medical**
            - 30% YoY growth
            - 12 active projects
            - 18 materials
            """)
        with col2:
            st.markdown("""
            🚗 **Automotive**
            - 15% YoY growth
            - 10 active projects
            - 20 materials
            """)
            st.markdown("""
            🔌 **Energy**
            - 10% YoY growth
            - 6 active projects
            - 12 materials
            """)
    
    # Section divider
    st.markdown(f"<hr style='margin: 2rem 0; border: none; border-top: 2px solid {Colors.DIVIDER};'>", unsafe_allow_html=True)
    
    # Sustainability and Supply Chain Overview
    st.markdown("<div id='sustainability'></div>", unsafe_allow_html=True)
    st.markdown("### 🌱 Sustainability and Supply Chain Overview")
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        # Sustainability Score Card
        st.markdown("""
            <div class='sustainability-score'>
                <h4 style='margin:0'>Overall Sustainability Score</h4>
                <h1 style='margin:0.5rem 0'>87.6%</h1>
                <p style='margin:0'>+8 points from last month</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Environmental Impact Metrics
        st.markdown("#### Environmental Impact")
        impact_data = pd.DataFrame({
            'Metric': ['Carbon Footprint', 'Water Usage', 'Waste Reduction'],
            'Current': [75, 82, 90],
            'Target': [85, 85, 95]
        })
        
        for _, row in impact_data.iterrows():
            st.markdown(f"**{row['Metric']}**")
            progress = row['Current'] / row['Target']
            st.progress(progress)
            st.caption(f"Current: {row['Current']}% of Target")
    
    with col2:
        # Supply Chain Risk Analysis
        st.markdown("""
            <div class='supply-risk'>
                <h4 style='margin:0'>Supply Chain Risk Level</h4>
                <h1 style='margin:0.5rem 0'>Medium</h1>
                <p style='margin:0'>3 materials need attention</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Material Sourcing Map
        st.markdown("#### Material Sourcing Status")
        # Get sourcing status from database
        sourcing_data = data_manager.get_sourcing_status()
        
        chart = alt.Chart(sourcing_data).mark_bar().encode(
            x=alt.X('Count:Q', title='Number of Materials'),
            y=alt.Y('Status:N', sort='-x'),
            color=alt.Color('Status:N', scale=alt.Scale(
                domain=['On Track', 'Delayed', 'At Risk', 'Completed'],
                range=['#2ECC71', '#F1C40F', '#E74C3C', '#3498DB']
            ))
        ).properties(height=150)
        
        st.altair_chart(chart, use_container_width=True)
    
    with col3:
        # Quick Insights
        st.markdown("#### Key Insights")
        # Get insights from database
        insights = data_manager.get_sustainability_insights()
        
        # Display Green Score insights
        green_score = insights[insights['Category'] == 'Green Score']
        st.markdown("🌿 **Green Score**")
        for _, row in green_score.iterrows():
            if row['Metric'] == 'Carbon Reduction':
                st.markdown(f"- {row['Value']}% carbon vs. last year")
            elif row['Metric'] == 'Renewable Materials':
                st.markdown(f"- {row['Value']}% renewable materials")
            elif row['Metric'] == 'Eco Certifications':
                st.markdown(f"- {row['Value']} new eco certifications")
        
        # Display Supply Chain insights
        supply_chain = insights[insights['Category'] == 'Supply Chain']
        st.markdown("⛓️ **Supply Chain**")
        for _, row in supply_chain.iterrows():
            if row['Metric'] == 'Supplier Reliability':
                st.markdown(f"- {row['Value']}% supplier reliability")
            elif row['Metric'] == 'Alternative Sources':
                st.markdown(f"- {row['Value']} alternative sources found")
            elif row['Metric'] == 'Pending Optimizations':
                st.markdown(f"- {row['Value']} optimizations pending")
    
    # Sustainability Trends and Risk Assessment
    st.markdown("### 📈 Trends and Risk Assessment")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Sustainability Trends")
        # Get sustainability trends from database
        trends_data = data_manager.get_sustainability_trends()
        
        # Melt the dataframe for Altair
        trends_melted = pd.melt(
            trends_data,
            id_vars=['Date'],
            value_vars=['Carbon Score', 'Water Score', 'Waste Score', 'Energy Usage', 'Cost Savings'],
            var_name='Metric',
            value_name='Score'
        )
        
        # Create line chart
        chart = alt.Chart(trends_melted).mark_line(point=True).encode(
            x=alt.X('Date:T', title='Month'),
            y=alt.Y('Score:Q', scale=alt.Scale(domain=[0, 100])),
            color=alt.Color('Metric:N', scale=alt.Scale(
                domain=['Carbon Score', 'Water Score', 'Waste Score', 'Energy Usage', 'Cost Savings'],
                range=['#2ECC71', '#3498DB', '#E67E22', '#9B59B6', '#F1C40F']
            )),
            tooltip=['Metric', 'Score', 'Date']
        ).properties(
            height=250
        ).configure_axis(
            grid=True
        ).configure_point(
            size=60
        )
        
        st.altair_chart(chart, use_container_width=True)
    
    with col2:
        st.markdown("#### Material Risk Matrix")
        # Create sample risk data
        risk_data = pd.DataFrame({
            'Material': ['Titanium', 'Carbon Fiber', 'Aluminum', 'Steel', 'Copper'],
            'Supply Risk': [8, 6, 3, 2, 5],
            'Environmental Impact': [4, 3, 5, 7, 6],
            'Cost': [100, 80, 40, 30, 50]
        })
        
        # Create scatter plot
        chart = alt.Chart(risk_data).mark_circle().encode(
            x=alt.X('Supply Risk:Q', scale=alt.Scale(domain=[0, 10])),
            y=alt.Y('Environmental Impact:Q', scale=alt.Scale(domain=[0, 10])),
            size=alt.Size('Cost:Q', scale=alt.Scale(range=[100, 500])),
            color=alt.Color('Material:N', scale=alt.Scale(scheme='category10')),
            tooltip=['Material', 'Supply Risk', 'Environmental Impact', 'Cost']
        ).properties(height=250)
        
        # Add quadrant lines
        vline = alt.Chart(pd.DataFrame({'x': [5]})).mark_rule(strokeDash=[5, 5]).encode(x='x:Q')
        hline = alt.Chart(pd.DataFrame({'y': [5]})).mark_rule(strokeDash=[5, 5]).encode(y='y:Q')
        
        # Combine charts
        final_chart = (chart + vline + hline).configure_axis(
            grid=True
        ).configure_view(
            strokeWidth=0
        )
        
        st.altair_chart(final_chart, use_container_width=True)
        
        # Add legend for quadrants
        st.caption("""
        **Risk Matrix Quadrants:**
        - Top Right: High Risk, High Impact
        - Top Left: Low Risk, High Impact
        - Bottom Right: High Risk, Low Impact
        - Bottom Left: Low Risk, Low Impact
        *Circle size represents relative cost*
        """)
    

    # Activity Timeline
    st.markdown("<div id='activity'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🕒 Recent Activity and Actions")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Get recent activities from database
        activities_df = data_manager.get_recent_activities()
        activities = activities_df.to_dict('records')
        current_time = pd.Timestamp.now()
        
        for activity in activities:
            icon = {
                "report": "📄",
                "analysis": "📊",
                "optimization": "⚡",
                "update": "🔄"
            }[activity["type"]]
            
            activity_time = pd.to_datetime(activity["time"])
            time_diff = current_time - activity_time
            if time_diff.days > 0:
                time_str = f"{time_diff.days}d ago"
            elif time_diff.seconds // 3600 > 0:
                time_str = f"{time_diff.seconds // 3600}h ago"
            else:
                time_str = f"{time_diff.seconds // 60}m ago"
            
            st.info(
                f"{icon} **{activity['desc']}**\n"
                f"└ {activity['impact']}\n"
                f"└ *{time_str}*"
            )
    
    with col2:
        st.markdown("#### Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            st.button("📊 Report", key="report_btn", use_container_width=True)
            st.button("🔍 Analyze", key="analyze_btn", use_container_width=True)
        with col2:
            st.button("⚡ Optimize", key="optimize_btn", use_container_width=True)
            st.button("🌱 Track", key="track_btn", use_container_width=True)
        
        # Add upcoming tasks
        st.markdown("#### Upcoming Tasks")
        tasks = [
            "🎯 Q2 Sustainability Review",
            "📦 Supply Chain Audit",
            "🔧 Process Optimization"
        ]
        for task in tasks:
            st.markdown(f"- {task}")
