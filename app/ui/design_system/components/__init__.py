"""
Component-specific styles using design tokens
"""
from contextlib import contextmanager
import streamlit as st
from app.ui.design_system.tokens import Colors, Spacing, FontSizes

def get_button_styles():
    return f"""
    /* Global button styles */
    div[data-testid="stButton"] > button {{
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        background: none;
        border: 1px solid {Colors.DIVIDER};
        color: {Colors.TEXT_PRIMARY};
        font-size: {FontSizes.BASE};
        padding: {Spacing.SM} {Spacing.MD};
        border-radius: 4px;
        transition: all 0.2s ease;
        font-weight: 400;
        margin: 2px 0;
    }}
    div[data-testid="stButton"] > button:hover {{
        background-color: {Colors.HOVER_BG};
        border-color: {Colors.HOVER_BORDER};
        color: {Colors.PRIMARY};
    }}
    div[data-testid="stButton"] > button:active {{
        background-color: {Colors.BUTTON_ACTIVE};
    }}
    """

def get_input_styles():
    return f"""
    /* Global input styles */
    .stTextArea textarea, .stTextInput input {{
        background-color: {Colors.BACKGROUND_SECONDARY};
        border: 1px solid {Colors.DIVIDER};
        color: {Colors.TEXT_PRIMARY};
        font-size: {FontSizes.BASE};
        padding: {Spacing.MD};
        border-radius: 4px;
        transition: all 0.2s ease;
    }}
    .stTextArea textarea:focus, .stTextInput input:focus {{
        border-color: {Colors.PRIMARY};
        box-shadow: 0 0 0 1px {Colors.PRIMARY};
        background-color: {Colors.BACKGROUND};
    }}
    .stTextArea textarea:hover, .stTextInput input:hover {{
        border-color: {Colors.HOVER_BORDER};
        background-color: {Colors.BACKGROUND};
    }}
    """

def get_tab_styles():
    return f"""
    /* Global tab styles */
    div[role="tablist"] button {{
        background: none;
        border: none;
        color: {Colors.TEXT_PRIMARY};
        font-size: {FontSizes.BASE};
        padding: {Spacing.SM} {Spacing.MD};
        margin: 0 {Spacing.XS};
        border-radius: 4px;
        transition: background-color 0.2s;
    }}
    div[role="tablist"] button:hover {{
        background-color: {Colors.HOVER_BG};
    }}
    div[role="tablist"] button[aria-selected="true"] {{
        background-color: {Colors.BACKGROUND_SECONDARY};
        color: {Colors.PRIMARY};
    }}
    """

def get_sidebar_styles():
    return f"""
    /* Sidebar styles */
    .sidebar .sidebar-content {{
        background-color: {Colors.BACKGROUND_SECONDARY};
        padding: {Spacing.MD};
    }}
    .sidebar .block-container {{
        font-size: {FontSizes.SM} !important;
    }}
    .sidebar img {{
        margin-bottom: {Spacing.SM};
        padding: {Spacing.MD};
    }}
    """

def get_status_dot_styles():
    return f"""
    /* Status dot styles */
    .status-dot {{
        font-size: {FontSizes.XS};
        margin-top: {Spacing.MD};
        text-align: center;
    }}
    .status-dot.online {{ color: {Colors.STATUS_ONLINE}; }}
    .status-dot.away {{ color: {Colors.STATUS_AWAY}; }}
    .status-dot.offline {{ color: {Colors.STATUS_OFFLINE}; }}
    """

def get_card_styles():
    return f"""
    /* Card styles */
    .stcard-container {{
        background-color: {Colors.BACKGROUND_SECONDARY};
        border-radius: 10px;
        padding: {Spacing.XL};
        margin: {Spacing.MD} 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid {Colors.DIVIDER};
    }}
    .stcard-title {{
        font-size: {FontSizes.LG};
        font-weight: 600;
        margin-bottom: {Spacing.MD};
        color: {Colors.TEXT_PRIMARY};
        display: flex;
        align-items: center;
        gap: {Spacing.SM};
    }}
    .stcard-title-icon {{
        font-size: {FontSizes.XL};
        line-height: 1;
    }}
    .stcard-content {{
        margin-top: {Spacing.SM};
    }}
    """

@contextmanager
def card(title: str = None, icon: str = None, key: str = None):
    """A modern card component with consistent styling.
    
    Args:
        title: Optional title to display at the top of the card
        icon: Optional icon to display next to the title
        key: Optional unique key for the card
    """
    st.markdown(f'<div class="stcard-container" key="{key or ""}">',
               unsafe_allow_html=True)
    
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

def get_global_styles():
    return f"""
    <style>
    /* Global typography */
    .main .block-container {{
        font-size: {FontSizes.BASE} !important;
    }}
    .stMarkdown, .stText {{
        font-size: {FontSizes.BASE} !important;
    }}
    
    /* Headers */
    .main h1 {{
        font-size: {FontSizes.XL} !important;
        margin-bottom: {Spacing.LG};
    }}
    .main h2 {{
        font-size: {FontSizes.LG} !important;
        margin-bottom: {Spacing.MD};
    }}
    .main h3 {{
        font-size: {FontSizes.MD} !important;
        margin-bottom: {Spacing.SM};
    }}
    .main h4 {{
        font-size: {FontSizes.BASE} !important;
        margin-bottom: {Spacing.XS};
    }}
    
    /* Accessibility */
    .visually-hidden {{
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }}
    
    {get_button_styles()}
    {get_input_styles()}
    {get_tab_styles()}
    {get_sidebar_styles()}
    {get_status_dot_styles()}
    {get_card_styles()}
    </style>
    """
