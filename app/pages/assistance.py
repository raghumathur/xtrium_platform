import streamlit as st

def render_assistance_page():
    st.header("Assistance Center")
    
    # Help Center section
    st.markdown("<div id='help_center'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("❓ Help Center")
    help_col1, help_col2 = st.columns(2)
    with help_col1:
        st.button("🔍 Search Help Articles", use_container_width=True)
        st.button("❓ FAQs", use_container_width=True)
        st.button("💬 Live Chat Support", use_container_width=True)
    with help_col2:
        st.button("📚 Browse Categories", use_container_width=True)
        st.button("🎯 Quick Start Guide", use_container_width=True)
        st.button("📞 Contact Support", use_container_width=True)
    
    # Documentation section
    st.markdown("<div id='documentation'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📚 Documentation")
    doc_categories = [
        "Getting Started",
        "User Guide",
        "API Reference",
        "Best Practices",
        "Integration Guide"
    ]
    for category in doc_categories:
        st.markdown(f"- [{category}](#)")
    
    # Support Tickets section
    st.markdown("<div id='support_tickets'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🎟️ Support Tickets")
    ticket_col1, ticket_col2 = st.columns(2)
    with ticket_col1:
        st.button("Create New Ticket", use_container_width=True)
        st.button("View My Tickets", use_container_width=True)
    with ticket_col2:
        st.metric("Open Tickets", "2")
        st.metric("Avg. Response Time", "2h")
    
    # Training section
    st.markdown("<div id='training'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🎓 Training")
    training_options = [
        "Getting Started with Xtrium",
        "Advanced Material Search",
        "Supply Chain Optimization",
        "Sustainability Analytics",
        "Custom Reports & Dashboards"
    ]
    for course in training_options:
        with st.expander(course):
            st.write("Course description and modules will be displayed here.")
    
    # Support status
    st.sidebar.success("Support Status: Online")
