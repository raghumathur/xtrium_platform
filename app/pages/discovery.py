import streamlit as st
from app.components.page_elements.query_input import render_query_input
from app.components.page_elements.search_tabs import render_search_tabs

def render_discovery_page():
    # Check if we should show database manager based on URL fragment
    fragment = st.query_params.get("_anchor")
    if fragment == "manage_databases":
        st.session_state.show_database_manager = True
    
    st.header("Discovery Companion")
    st.write("Hi! I am the Xtrium AI Assistant! Ask me about materials, applications, or sustainability metrics for your requirements")
    
    # Render the query input section
    render_query_input()
    
    # Render the search tabs
    render_search_tabs()
