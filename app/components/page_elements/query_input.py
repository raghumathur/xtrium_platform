import streamlit as st
from app.ui.design_system.components import get_global_styles
from app.ui.design_system.tokens import Spacing

def render_query_input():
    # Apply global styles which include input styling
    st.markdown(get_global_styles(), unsafe_allow_html=True)
    """
    Render the natural language query input section.
    """
    # Natural Language Query Section
    query_col, submit_col = st.columns([15, 1])
    with query_col:
        query = st.text_area(
            #"AI Assistant Input",  # Label for accessibility
            " ",  # Label for accessibility
            placeholder="Hello, I am the Xtrium AI assistant! Ask me questions about materials or applications needs...",
            height=100,
            key="nl_query"
        )
    with submit_col:
        st.markdown(f"<div style='height:{Spacing.XL};'></div>", unsafe_allow_html=True)  # Add vertical spacing
        st.button("➤", key="submit_query", use_container_width=True)
