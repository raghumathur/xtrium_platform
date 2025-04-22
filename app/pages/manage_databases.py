import streamlit as st
import pandas as pd
from app.ui.theme import Colors, Spacing
from app.ui.design_system.components import get_global_styles

def render_database_stats(database_name, total_records, last_updated, sync_status):
    """Render statistics for a database."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{total_records:,}")
    with col2:
        st.metric("Last Updated", last_updated)
    with col3:
        st.metric("Sync Status", sync_status)
    with col4:
        st.button("🔄 Sync Now", key=f"sync_{database_name}", use_container_width=True)

def render_database_section(title, description, is_confidential=False):
    """Render a database management section."""
    st.markdown(f"### {title}")
    st.markdown(description)
    
    # Database actions
    col1, col2, col3 = st.columns(3)
    with col1:
        st.file_uploader(
            "Upload New Data",
            type=["csv", "xlsx", "json"],
            key=f"upload_{title.lower().replace(' ', '_')}"
        )
    with col2:
        st.selectbox(
            "Connect External Source",
            ["Select Source...", "SQL Database", "API Endpoint", "Cloud Storage"],
            key=f"source_{title.lower().replace(' ', '_')}"
        )
    with col3:
        if is_confidential:
            st.text_input("Access Key", type="password", key=f"key_{title.lower().replace(' ', '_')}")
    
    # Mock database stats
    render_database_stats(
        title.lower().replace(" ", "_"),
        12500,
        "2025-04-21",
        "✅ Synced"
    )
    
    # Data preview
    with st.expander("Preview Data"):
        st.dataframe(pd.DataFrame({
            "ID": range(1, 6),
            "Name": ["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5"],
            "Category": ["A", "B", "A", "C", "B"],
            "Last Modified": ["2025-04-21"] * 5
        }))
    
    st.markdown("---")

def render_confidentiality_settings():
    """Render confidentiality wall settings."""
    st.markdown("### 🔒 Confidentiality Settings")
    
    # Access control
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox(
            "Access Level",
            ["Public", "Team Only", "Restricted", "Confidential"],
            key="access_level"
        )
    with col2:
        st.multiselect(
            "Authorized Teams",
            ["Research", "Engineering", "Management", "External Partners"],
            key="authorized_teams"
        )
    
    # Encryption settings
    st.checkbox("Enable End-to-End Encryption", key="enable_encryption")
    st.checkbox("Require 2FA for Access", key="require_2fa")
    
    # Audit logging
    st.checkbox("Enable Audit Logging", key="enable_audit")
    
    st.markdown("---")

def render_manage_databases_page():
    """Render the database management page."""
    st.markdown(get_global_styles(), unsafe_allow_html=True)
    
    st.header("Manage Databases")
    st.write("Centralized database management for Xtrium's material and application data.")
    
    # Database health overview
    st.markdown("### 📊 Database Health Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Storage Used", "2.3 GB")
    with col2:
        st.metric("Last Backup", "2h ago")
    with col3:
        st.metric("System Status", "Healthy")
    
    st.markdown("---")
    
    # Materials Database
    render_database_section(
        "Materials Database",
        "Comprehensive material properties, specifications, and performance data."
    )
    
    # Applications Database
    render_database_section(
        "Applications Database",
        "Use cases, implementation examples, and success stories."
    )
    
    # Supply Chain Database
    render_database_section(
        "Supply Chain Database",
        "Supplier information, logistics data, and inventory tracking.",
        is_confidential=True
    )
    
    # Sustainability Database
    render_database_section(
        "Sustainability Database",
        "Environmental impact metrics, compliance data, and sustainability scores."
    )
    
    # Confidentiality Settings
    render_confidentiality_settings()
    
    # Global database actions
    st.markdown("### 🛠️ Global Actions")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("🔄 Sync All", use_container_width=True)
    with col2:
        st.button("💾 Backup All", use_container_width=True)
    with col3:
        st.button("📊 Export Report", use_container_width=True)
    with col4:
        st.button("⚙️ Settings", use_container_width=True)
