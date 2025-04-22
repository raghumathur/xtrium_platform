import streamlit as st
from contextlib import contextmanager

@contextmanager
def card(title: str = None, icon: str = None, key: str = None):
    """A modern card component with consistent styling.
    
    Args:
        title: Optional title to display at the top of the card
        icon: Optional icon to display next to the title
        key: Optional unique key for the card
    """
    # Card styling
    st.markdown("""
        <style>
        .stcard-container {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .stcard-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: rgb(250, 250, 250);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .stcard-title-icon {
            font-size: 1.5rem;
            line-height: 1;
        }
        .stcard-content {
            margin-top: 0.5rem;
        }
        </style>
        <div class="stcard-container" key="{key}">
    """.format(key=key or ""), unsafe_allow_html=True)
    
    if title:
        if icon:
            st.markdown(f'<div class="stcard-title"><span class="stcard-title-icon">{icon}</span>{title}</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="stcard-title">{title}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="stcard-content">', unsafe_allow_html=True)
    
    try:
        yield
    finally:
        st.markdown('</div></div>', unsafe_allow_html=True)
