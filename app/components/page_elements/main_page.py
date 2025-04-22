import streamlit as st
from app.components.page_elements.topbar import render_topbar
from app.components.page_elements.sidebar import render_sidebar
from app.pages.home import render_home_page
from app.pages.discovery import render_discovery_page
from app.pages.sustainability import render_sustainability_page
from app.pages.supply_chain import render_supply_chain_page
from app.pages.insights import render_insights_page
from app.pages.assistance import render_assistance_page

def render_main_page():
    """Render the main page with dynamic content based on the active tab."""
    # Render the fixed navigation components
    render_topbar()
    render_sidebar()
    
    # Add some spacing after the topbar
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    
    # Render the appropriate page based on the active tab
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "home"
    
    # Map of tab IDs to their render functions
    tab_pages = {
        "home": render_home_page,
        "discovery": render_discovery_page,
        "sustainability": render_sustainability_page,
        "supply_chain": render_supply_chain_page,
        "insights": render_insights_page,
        "assistance": render_assistance_page
    }
    
    # Render the active page
    active_tab = st.session_state.active_tab
    if active_tab in tab_pages:
        tab_pages[active_tab]()
    else:
        st.error(f"Page not found: {active_tab}")