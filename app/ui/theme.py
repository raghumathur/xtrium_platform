"""
Xtrium Theme System
Centralized color and styling configuration
"""

def get_theme_value(key: str, default: str) -> str:
    """Get a theme value from Streamlit config with fallback"""
    try:
        return st.get_option(f"theme.{key}")
    except:
        return default

class Colors:
    # Main theme colors
    PRIMARY = "#1E90FF"  # Dodger Blue
    BACKGROUND = "#021526"  # Deep Navy
    BACKGROUND_SECONDARY = "#0A2337"  # Lighter Navy
    BACKGROUND_TERTIARY = "#0E2D45"  # Even Lighter Navy for components
    TEXT_PRIMARY = "#FFFFFF"  # White
    TEXT_HEADING = "#E4F1FF"  # Slightly blue-tinted white for headings
    
    # Extended theme colors
    TEXT_SECONDARY = "#95A5A6"  # Grey for secondary text
    TEXT_MUTED = "rgba(255,255,255,0.7)"  # Semi-transparent white
    
    # Status colors
    STATUS_ONLINE = "#2ECC71"  # Green
    STATUS_AWAY = "#F1C40F"  # Yellow
    STATUS_OFFLINE = "#95A5A6"  # Grey
    
    # Interactive elements
    HOVER_BG = "rgba(30,144,255,0.1)"  # Subtle primary color
    HOVER_BORDER = "rgba(30,144,255,0.3)"  # More visible primary
    DIVIDER = "rgba(255,255,255,0.1)"  # Subtle white
    
    # Component backgrounds
    COMPONENT_BG = BACKGROUND_TERTIARY  # For inputs, selects, etc
    COMPONENT_BORDER = "rgba(255,255,255,0.15)"  # Slightly visible border
    
    # Button colors
    BUTTON_PRIMARY = PRIMARY
    BUTTON_SECONDARY = "#0066CC"
    BUTTON_HOVER = "rgba(30,144,255,0.15)"
    BUTTON_ACTIVE = "rgba(30,144,255,0.25)"

class Spacing:
    # Base unit is rem for better scaling
    XS = "0.25rem"
    SM = "0.5rem"
    MD = "1rem"
    LG = "1.5rem"
    XL = "2rem"

class FontSizes:
    # Using em for better scaling
    XS = "0.8em"
    SM = "0.9em"
    BASE = "1.0em"
    MD = "1.1em"
    LG = "1.2em"
    XL = "1.5em"

def get_global_styles():
    return f"""
        <style>
        /* Reset and base styles */
        .main .block-container {{ font-size: {FontSizes.BASE} !important; }}
        .stMarkdown, .stText {{ font-size: {FontSizes.BASE} !important; }}
        
        /* Heading styles */
        .main h1, [data-testid="stMarkdownContainer"] h1 {{
            color: {Colors.TEXT_HEADING} !important;
            font-size: {FontSizes.XL} !important;
            font-weight: 600;
            letter-spacing: 0.02em;
            margin: {Spacing.LG} 0;
        }}
        
        .main h2, [data-testid="stMarkdownContainer"] h2 {{
            color: {Colors.TEXT_HEADING} !important;
            font-size: {FontSizes.LG} !important;
            font-weight: 500;
            margin: {Spacing.MD} 0;
        }}
        
        .main h3, [data-testid="stMarkdownContainer"] h3 {{
            color: {Colors.TEXT_HEADING} !important;
            font-size: {FontSizes.MD} !important;
            font-weight: 500;
            margin: {Spacing.SM} 0;
        }}
        
        /* Regular text */
        .main p, [data-testid="stMarkdownContainer"] p {{
            color: {Colors.TEXT_MUTED};
            line-height: 1.6;
        }}
        
        /* Topbar styling */
        [data-testid="stHeader"] {{
            background-color: {Colors.BACKGROUND_SECONDARY} !important;
            border-bottom: 1px solid {Colors.DIVIDER};
            padding: {Spacing.SM} {Spacing.MD};
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 999;
            height: 60px;
            display: flex;
            align-items: center;
        }}
        
        [data-testid="stHeader"] > div {{
            max-width: none;
            padding: 0;
            display: flex;
            align-items: center;
            width: 100%;
            height: 100%;
        }}
        
        /* User dropdown styling */
        [data-testid="stHeader"] button[kind="secondary"] {{
            height: 36px;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            padding: 0 {Spacing.MD};
            background-color: transparent;
            border: 1px solid {Colors.DIVIDER};
            color: {Colors.TEXT_PRIMARY};
            font-size: {FontSizes.SM};
            display: flex;
            align-items: center;
            gap: {Spacing.SM};
        }}
        
        [data-testid="stHeader"] button[kind="secondary"]:hover {{
            background-color: {Colors.HOVER_BG};
            border-color: {Colors.HOVER_BORDER};
        }}
        
        /* Adjust main content to account for fixed header */
        .main .block-container {{
            margin-top: 60px;
            padding-top: {Spacing.LG};
        }}
        
        /* Topbar navigation */
        .stTabs [role="tablist"] {{
            background-color: {Colors.BACKGROUND};
            border-bottom: 1px solid {Colors.COMPONENT_BORDER};
            gap: 1px;
            padding: {Spacing.XS} {Spacing.XS};
            border-radius: 4px;
        }}
        
        .stTabs [role="tab"] {{
            background-color: {Colors.COMPONENT_BG};
            border: 1px solid {Colors.COMPONENT_BORDER};
            color: {Colors.TEXT_SECONDARY};
            font-size: {FontSizes.SM};
            font-weight: 500;
            padding: {Spacing.XS} {Spacing.MD};
            border-radius: 4px;
            transition: all 0.2s;
            margin: 0;
            height: 32px;
            min-width: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .stTabs [role="tab"]:hover {{
            background-color: {Colors.BUTTON_HOVER};
            border-color: {Colors.PRIMARY};
            color: {Colors.TEXT_PRIMARY};
        }}
        
        .stTabs [role="tab"][aria-selected="true"] {{
            background-color: {Colors.PRIMARY};
            border-color: {Colors.PRIMARY};
            color: {Colors.TEXT_PRIMARY};
        }}
        
        /* Headers */
        .main h1 {{ 
            font-size: {FontSizes.XL} !important; 
            color: {Colors.TEXT_PRIMARY};
            margin-bottom: {Spacing.LG};
            padding-bottom: {Spacing.SM};
            border-bottom: 1px solid {Colors.DIVIDER};
        }}
        .main h2 {{ 
            font-size: {FontSizes.LG} !important;
            color: {Colors.TEXT_PRIMARY};
            margin: {Spacing.LG} 0 {Spacing.MD};
        }}
        .main h3 {{ 
            font-size: {FontSizes.MD} !important;
            color: {Colors.TEXT_PRIMARY};
            margin: {Spacing.MD} 0;
        }}
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2px;
            background-color: {Colors.BACKGROUND_SECONDARY};
            padding: 0.5rem 0.5rem 0;
            border-radius: 4px 4px 0 0;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            height: 40px;
            background-color: transparent;
            border: none;
            color: {Colors.TEXT_SECONDARY};
            border-radius: 4px 4px 0 0;
            padding: 0 {Spacing.MD};
            font-size: {FontSizes.SM};
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {Colors.PRIMARY} !important;
            color: {Colors.TEXT_PRIMARY} !important;
        }}
        
        /* Selectbox styling */
        div[data-testid="stSelectbox"] {{
            background-color: {Colors.BACKGROUND_SECONDARY};
            border-radius: 4px;
            padding: 2px;
        }}
        
        div[data-testid="stSelectbox"] > div > div {{
            background-color: transparent;
            border: 1px solid {Colors.DIVIDER};
            color: {Colors.TEXT_PRIMARY};
        }}
        
        div[data-testid="stSelectbox"] label {{
            color: {Colors.TEXT_SECONDARY};
            font-size: {FontSizes.SM} !important;
            font-weight: 500;
        }}
        
        /* Sidebar styling */
        .sidebar .block-container {{
            background-color: {Colors.BACKGROUND_SECONDARY};
            padding: {Spacing.MD};
            border-radius: 4px;
        }}
        
        .sidebar [data-testid="stSidebar"] {{
            background-color: {Colors.BACKGROUND};
            border-right: 1px solid {Colors.DIVIDER};
        }}
        
        /* Sidebar link styling */
        section[data-testid="stSidebar"] a {{
            text-decoration: none;
            color: inherit;
        }}
        
        /* Quick Links */
        .nav-link {{
            width: 100%;
            display: flex;
            align-items: center;
            padding: {Spacing.SM} {Spacing.MD};
            margin: 2px 0;
            color: {Colors.TEXT_SECONDARY};
            text-decoration: none;
            border-radius: 4px;
            transition: all 0.2s;
        }}
        
        .nav-link:hover {{
            background-color: {Colors.HOVER_BG};
            color: {Colors.TEXT_PRIMARY};
            border-right: 2px solid {Colors.PRIMARY};
        }}
        
        .nav-link.active {{
            background-color: {Colors.PRIMARY};
            color: {Colors.TEXT_PRIMARY};
            font-weight: 500;
        }}
        
        .nav-icon {{
            margin-right: {Spacing.SM};
            font-size: {FontSizes.LG};
            width: 24px;
            text-align: center;
        }}
        
        /* Metrics styling */
        [data-testid="stMetric"] {{
            background-color: {Colors.BACKGROUND_SECONDARY};
            padding: {Spacing.SM} {Spacing.MD};
            border-radius: 4px;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {Colors.TEXT_SECONDARY} !important;
            font-size: {FontSizes.SM} !important;
            font-weight: 500;
            margin-bottom: {Spacing.XS};
        }}
        
        [data-testid="stMetricValue"] {{
            color: {Colors.TEXT_PRIMARY} !important;
            font-size: {FontSizes.LG} !important;
            font-weight: 600;
        }}
        
        [data-testid="stMetricDelta"] {{
            color: {Colors.TEXT_SECONDARY} !important;
            font-size: {FontSizes.SM} !important;
            font-weight: normal;
        }}
        
        /* Project metrics specific */
        [data-testid="stMetricValue"][style*="font-size: 3rem"] {{
            font-size: {FontSizes.LG} !important;
        }}
        </style>
    """
