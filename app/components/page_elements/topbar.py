import streamlit as st
from app.ui.design_system.components import get_global_styles
from app.ui.navigation import get_tab_items
from app.ui.theme import Colors

def render_user_menu():
    """Render user menu dropdown."""
    menu_items = {
        "Profile": "profile",
        "Settings": "settings",
        "API Keys": "api_keys",
        "Logout": "logout"
    }
    
    # Add custom styles for the menu
    st.markdown("""
        <style>
        /* Container styles */
        div[data-testid="stSelectbox"] {
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        /* Button styles */
        div[data-testid="stSelectbox"] > div > div {
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 4px;
            color: white;
            padding: 0.5rem;
            line-height: 1.5;
        }
        div[data-testid="stSelectbox"] > div > div:hover {
            background-color: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)
    
    selected = st.selectbox(
        "",
        ["👤 User"] + list(menu_items.keys()),
        label_visibility="collapsed",
        key="user_menu"
    )
    
    if selected in menu_items:
        st.session_state.page = menu_items[selected]

def render_quick_actions():
    """Render quick action buttons in the topbar."""
    # Add styles for the buttons
    st.markdown("""
        <style>
        /* Topbar button styles */
        div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 4px;
        }
        div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
            background-color: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns([1, 1])
    
    # Search button
    with cols[0]:
        if st.button("🔍", key="search_button"):
            st.session_state.show_search = True
    
    # User menu
    with cols[1]:
        render_user_menu()

def render_topbar():
    """Render the top navigation bar with dynamic tabs."""
    # Add topbar styling
    st.markdown("""
        <style>
        header[data-testid="stHeader"] {
            background-color: rgb(17, 17, 17);
        }
        
        div[data-testid="stToolbar"] {
            visibility: hidden;
        }
        
        button[kind="secondary"] {
            background-color: transparent;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.8);
        }
        
        button[kind="secondary"]:hover {
            border-color: rgba(255, 255, 255, 0.2);
            color: white;
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        /* Style the user menu dropdown */
        div[data-testid="stSelectbox"] {
            margin-top: -0.25rem;
        }
        
        div[data-testid="stSelectbox"] > div > div {
            background-color: transparent !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
            height: 2.4rem !important;
            min-height: 2.4rem !important;
            margin-top: 0.25rem;
        }
        
        div[data-testid="stSelectbox"] > div > div:hover {
            border-color: rgba(255, 255, 255, 0.2) !important;
        }
        
        div[data-testid="stSelectbox"] > div > div > div {
            color: rgba(255, 255, 255, 0.8) !important;
            line-height: 1.6 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Create columns for tabs and actions
    tabs_col, actions_col = st.columns([7, 1])
    
    # Render tabs in the first column
    with tabs_col:
        # Initialize active tab if not present
        if "active_tab" not in st.session_state:
            st.session_state.active_tab = "home"
        
        # Get all tab items
        tab_items = get_tab_items()
        
        # Create a row of buttons for navigation
        cols = st.columns(len(tab_items) + 1)
        
        # Create buttons for tabs
        for i, ((tab_id, icon, label), col) in enumerate(zip(tab_items, cols[:-1])):
            with col:
                is_active = tab_id == st.session_state.active_tab
                if st.button(f"{icon} {label}", key=f"tab_{tab_id}", use_container_width=True):
                    st.session_state.active_tab = tab_id
                    if "page" in st.session_state:
                        del st.session_state.page
                    st.rerun()
        
        # Add user menu dropdown in the last column
        with cols[-1]:
            # User Actions dropdown without any actions
            st.selectbox(
                "",
                ["👤 User Actions", "Profile", "Settings", "Sign Out"],
                key="user_menu",
                label_visibility="collapsed"
            )
    
    # Render quick actions in the second column
    #with actions_col:
        #render_quick_actions()
