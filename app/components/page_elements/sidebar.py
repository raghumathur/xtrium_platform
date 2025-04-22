import streamlit as st
from app.ui.design_system.components import get_global_styles
from app.ui.navigation import get_sidebar_links
from app.ui.theme import Colors, Spacing, FontSizes

def render_workspace_selector():
    """Render the workspace selector dropdown."""
    workspaces = ["Default", "Project Alpha", "Client Beta", "Research"]
    st.sidebar.selectbox(
        "Active Workspace",
        workspaces,
        key="workspace_selector",
        label_visibility="visible"
    )

def render_quick_links():
    """Render quick navigation links in the sidebar."""
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "discovery"
    
    links = get_sidebar_links(st.session_state.active_tab)
    
    # Add custom link styles
    st.markdown("""
        <style>
        .sidebar-link {
            display: block;
            width: 100%;
            padding: 0.5rem 1rem;
            text-align: left;
            color: inherit;
            font-weight: normal;
            text-decoration: none !important;
            transition: all 0.2s ease;
            margin-bottom: 0.25rem;
            border-radius: 4px;
        }
        .sidebar-link:hover {
            background-color: rgba(255, 255, 255, 0.1);
            color: #1E90FF;
            text-decoration: none !important;
        }
        .sidebar-link.active {
            background: rgba(255, 255, 255, 0.15);
            color: #1E90FF;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Render quick links
    links_html = []
    for label, icon, section in links:
        link_class = "sidebar-link"
        if section == "manage_databases" and st.session_state.get("show_database_manager", False):
            link_class += " active"
        links_html.append(
            f'<a href="#{section}" class="{link_class}" onclick="handleLinkClick(\'{section}\')">{icon} {label}</a>'
        )
    
    # Add JavaScript to handle link clicks
    st.markdown("""
    <script>
    function handleLinkClick(section) {
        if (section === 'manage_databases') {
            // Toggle database manager visibility
            const sessionState = window.parent.streamlitPythonState;
            sessionState.show_database_manager = !sessionState.show_database_manager;
        }
    }
    </script>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("".join(links_html), unsafe_allow_html=True)
    
    # Show database manager if link is clicked
    if st.session_state.get("show_database_manager", False) and st.session_state.active_tab == "discovery":
        from app.pages.manage_databases import render_manage_databases_page
        with st.sidebar.expander("Database Manager", expanded=True):
            render_manage_databases_page()

def render_filter_section():
    """Render smart filters in the sidebar."""
    if st.session_state.active_tab == "discovery":
        with st.sidebar.expander("Smart Filters", expanded=True):
            st.selectbox(
                "Material Type",
                ["All", "Metals", "Polymers", "Ceramics"],
                key="filter_material_type"
            )
            st.selectbox(
                "Industry",
                ["All", "Automotive", "Aerospace", "Medical"],
                key="filter_industry"
            )
            st.selectbox(
                "Properties",
                ["All", "Mechanical", "Thermal", "Electrical"],
                key="filter_properties"
            )

def render_collaborators():
    """Render the collaborators section."""
    status_map = {
        "online": "<div class='status-dot online'>●</div>",
        "away": "<div class='status-dot away'>●</div>",
        "offline": "<div class='status-dot offline'>●</div>"
    }
    
    collaborators = [
        {"name": "John D.", "status": "online", "role": "Project Lead"},
        {"name": "Sarah M.", "status": "away", "role": "Materials Scientist"},
        {"name": "Alex K.", "status": "online", "role": "Data Analyst"},
        {"name": "Maria R.", "status": "offline", "role": "Supply Chain Specialist"}
    ]
    
    expander = st.sidebar.expander("Active Collaborators", expanded=True)
    
    with expander:
        for i, collab in enumerate(collaborators):
            if i > 0:
                expander.markdown(
                    f"<div style='border-top: 1px solid {Colors.DIVIDER}; margin: {Spacing.SM} 0;'></div>",
                    unsafe_allow_html=True
                )
            
            cols = expander.columns([0.1, 0.1, 0.8])
            cols[0].markdown(status_map[collab['status']], unsafe_allow_html=True)
            
            initials = ''.join(word[0].upper() for word in collab["name"].split())
            cols[1].markdown(f"<div style='margin-top: -10px;'><h2>{initials}</h2></div>", unsafe_allow_html=True)
            
            cols[2].markdown(
                f"<div style='margin-top: {Spacing.XS}; margin-left: {Spacing.MD};'>"
                f"<div style='font-size: {FontSizes.BASE}; margin-bottom: {Spacing.XS};'>"
                f"<span>{collab['name']}</span></div>"
                f"<div style='font-size: {FontSizes.XS}; font-style: italic; color: {Colors.TEXT_SECONDARY};'>{collab['role']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

def render_support():
    """Render support links."""
    st.sidebar.markdown("---")
    support_links = [
        ("Help Center", "❓"),
        ("Submit Feedback", "📝"),
        ("Feature Requests", "✨")
    ]
    for i, (label, icon) in enumerate(support_links):
        st.sidebar.button(f"{icon} {label}", key=f"support_link_{i}")

def render_logo():
    """Render the logo."""
    st.sidebar.image(
        "assets/images/xtrium.png",
        width=280
    )
    st.sidebar.markdown(
        "<p style='text-align: center; color: #FFFFFF; margin-top: -10px; font-size: 0.9em;'>"
        "Where Materials meet Applications</p>",
        unsafe_allow_html=True
    )

def render_global_search():
    """Render the global search component."""
    with st.sidebar.expander("🔍 Global Search", expanded=True):
        st.text_input("Search across all resources", placeholder="Search materials, suppliers...")
        
        # Recent searches
        st.markdown("**Recent Searches**")
        recent_searches = [
            "titanium suppliers usa",
            "composite materials cost",
            "ISO 9001 certification"
        ]
        for search in recent_searches:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.markdown(f"🕒 {search}")
            with col2:
                st.button("↗", key=f"search_{search}", help="Use this search")
        
        # Advanced search toggle
        st.checkbox("Enable Advanced Search", help="Search with additional filters")

def render_notifications():
    """Render the notifications center."""
    with st.sidebar.expander("🔔 Notifications", expanded=True):
        notifications = [
            {"type": "alert", "message": "Low inventory alert: Ti-6Al-4V", "time": "2h ago"},
            {"type": "price", "message": "Price increase: Carbon Fiber (5%)", "time": "5h ago"},
            {"type": "cert", "message": "ISO Cert expires in 30 days", "time": "1d ago"}
        ]
        
        for notif in notifications:
            icon = {
                "alert": "⚠️",
                "price": "💰",
                "cert": "📜"
            }[notif['type']]
            
            st.markdown(f"{icon} **{notif['message']}**")
            st.caption(f"_{notif['time']}_")
            st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)

def render_quick_actions():
    """Render quick action buttons."""
    st.sidebar.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.button("📝 New RFQ", use_container_width=True)
        st.button("📊 Report", use_container_width=True)
    with col2:
        st.button("➕ Supplier", use_container_width=True)
        st.button("📅 Meeting", use_container_width=True)

def render_sidebar():
    """Render the sidebar with all its components."""
    st.sidebar.markdown(get_global_styles(), unsafe_allow_html=True)
    
    render_logo()
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    render_workspace_selector()
    st.sidebar.markdown("---")
    render_quick_links()
    st.sidebar.markdown("---")
    render_global_search()  # New component
    st.sidebar.markdown("---")
    render_notifications()  # New component
    st.sidebar.markdown("---")
    render_quick_actions()  # New component
    st.sidebar.markdown("---")
    render_filter_section()
    st.sidebar.markdown("---")
    render_collaborators()
    render_support()
