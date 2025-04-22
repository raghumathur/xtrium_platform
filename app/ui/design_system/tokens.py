"""
Design tokens - the foundational values used across the UI
"""

class Colors:
    # Main theme colors - hardcoded
    PRIMARY = "#1E90FF"  # Dodger Blue
    BACKGROUND = "#021526"  # Deep Navy
    BACKGROUND_SECONDARY = "#0A2337"  # Lighter Navy
    TEXT_PRIMARY = "#FFFFFF"  # White
    
    # Extended theme colors - hardcoded but organized
    TEXT_SECONDARY = "#95A5A6"  # Grey for secondary text
    TEXT_MUTED = "rgba(255,255,255,0.7)"  # Semi-transparent white
    
    # Status colors
    STATUS_ONLINE = "#2ECC71"  # Green
    STATUS_AWAY = "#F1C40F"  # Yellow
    STATUS_OFFLINE = "#95A5A6"  # Grey
    
    # Interactive elements
    HOVER_BG = "rgba(255,255,255,0.1)"  # Subtle white
    HOVER_BORDER = "rgba(255,255,255,0.3)"  # More visible white
    DIVIDER = "rgba(255,255,255,0.1)"  # Very subtle white
    
    # Button colors
    BUTTON_PRIMARY = PRIMARY  # Same as primary theme color
    BUTTON_SECONDARY = "#0066CC"  # Darker blue
    BUTTON_HOVER = "#f0f2f6"  # Light grey
    BUTTON_ACTIVE = "#e6e9ef"  # Slightly darker grey

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
