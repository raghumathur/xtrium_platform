import streamlit as st

def render_insights_page():
    st.header("Market Insights")
    
    # Market Trends section
    st.markdown("<div id='market_trends'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📈 Market Trends")
    trend_col1, trend_col2 = st.columns(2)
    with trend_col1:
        st.metric("Market Growth", "+12%", "vs last quarter")
        st.write("Top Growing Segments:")
        st.write("1. Advanced Composites")
        st.write("2. Sustainable Materials")
        st.write("3. Smart Materials")
    with trend_col2:
        st.metric("Innovation Index", "89/100", "+5")
        st.write("Emerging Technologies:")
        st.write("1. Self-healing Materials")
        st.write("2. Nano-engineered Materials")
        st.write("3. Bio-based Polymers")
    
    # Industry Reports section
    st.markdown("<div id='industry_reports'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📑 Industry Reports")
    for i in range(3):
        with st.expander(f"Industry Report {i+1}", expanded=True):
            st.write(f"Sample report {i+1} with key findings and recommendations")
    
    # Analytics section
    st.markdown("<div id='analytics'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📊 Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Data Points Analyzed", "1.2M", "+50K")
        st.metric("Accuracy Score", "95%", "+2%")
    with col2:
        st.metric("Predictions Made", "250K", "+15K")
        st.metric("Model Performance", "92%", "+3%")
    
    # Forecasting section
    st.markdown("<div id='forecasting'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🎯 Forecasting")
    forecast_col1, forecast_col2 = st.columns(2)
    with forecast_col1:
        st.metric("Market Size 2025", "$2.8B", "+15%")
        st.write("Growth Drivers:")
        st.write("1. Sustainable Materials Adoption")
        st.write("2. Industry 4.0 Integration")
    with forecast_col2:
        st.metric("R&D Investment", "$450M", "+25%")
        st.write("Focus Areas:")
        st.write("1. Smart Manufacturing")
        st.write("2. Green Technologies")
