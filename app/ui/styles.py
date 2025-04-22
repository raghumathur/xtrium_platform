"""
Centralized CSS styles for consistent UI/UX
"""
from app.ui.theme import Colors, Spacing, FontSizes

def get_button_styles():
    return f"""
    /* Primary button */
    div[data-testid="stButton"] > button[kind="primary"] {{
        background-color: {Colors.PRIMARY};
        border: none;
        color: {Colors.TEXT_PRIMARY};
        font-weight: 500;
        font-size: {FontSizes.SM};
        padding: {Spacing.SM} {Spacing.MD};
        border-radius: 4px;
        transition: all 0.2s ease;
        height: 36px;
    }}
    
    /* Secondary button */
    div[data-testid="stButton"] > button[kind="secondary"] {{
        background-color: {Colors.COMPONENT_BG};
        border: 1px solid {Colors.COMPONENT_BORDER};
        color: {Colors.TEXT_PRIMARY};
        font-size: {FontSizes.SM};
        padding: {Spacing.SM} {Spacing.MD};
        border-radius: 4px;
        transition: all 0.2s ease;
        height: 36px;
    }}
    
    /* Default button (no kind specified) */
    div[data-testid="stButton"] > button:not([kind]) {{
        background-color: transparent;
        border: 1px solid {Colors.COMPONENT_BORDER};
        color: {Colors.TEXT_PRIMARY};
        font-size: {FontSizes.SM};
        padding: {Spacing.SM} {Spacing.MD};
        border-radius: 4px;
        transition: all 0.2s ease;
        height: 36px;
    }}
    
    /* Hover states */
    div[data-testid="stButton"] > button:hover {{
        background-color: {Colors.BUTTON_HOVER};
        border-color: {Colors.PRIMARY};
        color: {Colors.TEXT_PRIMARY};
    }}
    
    div[data-testid="stButton"] > button[kind="primary"]:hover {{
        opacity: 0.9;
    }}
    """

def get_input_styles():
    return f"""
    /* Global input styles */
    .stTextArea textarea, .stTextInput input, div[data-testid="stSelectbox"] > div > div {{
        background-color: {Colors.COMPONENT_BG} !important;
        border: 1px solid {Colors.COMPONENT_BORDER} !important;
        color: {Colors.TEXT_PRIMARY} !important;
        font-size: {FontSizes.BASE};
        padding: {Spacing.SM} {Spacing.MD};
        border-radius: 4px;
        transition: all 0.2s ease;
    }}
    
    .stTextArea textarea:focus, .stTextInput input:focus, div[data-testid="stSelectbox"] > div > div:focus {{
        border-color: {Colors.PRIMARY} !important;
        box-shadow: 0 0 0 1px {Colors.PRIMARY};
    }}
    
    /* Labels */
    .stTextArea label, .stTextInput label, div[data-testid="stSelectbox"] label {{
        color: {Colors.TEXT_SECONDARY};
        font-size: {FontSizes.SM};
        font-weight: 500;
        margin-bottom: {Spacing.XS};
    }}
    
    /* Selectbox specific */
    div[data-testid="stSelectbox"] {{
        margin-bottom: {Spacing.MD};
    }}
    
    div[data-testid="stSelectbox"] > div {{
        background-color: {Colors.BACKGROUND_TERTIARY};
        border-radius: 4px;
        padding: 2px;
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
    </style>
    """
