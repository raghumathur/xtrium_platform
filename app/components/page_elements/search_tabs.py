import streamlit as st
from app.components.search_applications.material_selection import find_applications
from app.components.search_materials.material_suggestions import find_materials
from app.ui.design_system.components import get_global_styles

def render_search_tabs():
    """Render the search tabs for Find Materials and Find Applications."""
    # Apply global styles which include tab styling
    st.markdown(get_global_styles(), unsafe_allow_html=True)
    
    tabs = st.tabs(["Find Applications", "Find Materials"])
    
    # Tab Logic for Find Applications
    with tabs[0]:
        find_applications()
    
    # Tab Logic for Find Materials
    with tabs[1]:
        find_materials()