def get_global_styles():
    return """
    <style>
        /* Icon Button Styles */
        button[data-testid^="stButton"] {
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Specific styles for icon-only buttons */
        button[data-testid^="stButton"]:has(div:only-child:is([data-testid="stMarkdownContainer"]):has(p:only-child:is(:matches(contains("❌"), contains("➤"), contains("🗑️"))))) {
            width: auto !important;
            min-width: 40px !important;
            padding: 0.25rem !important;
        }

        /* Center align all button content */
        button[data-testid^="stButton"] > div[data-testid="stMarkdownContainer"] {
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Remove margin from button text */
        button[data-testid^="stButton"] > div[data-testid="stMarkdownContainer"] p {
            margin: 0;
        }
    </style>
    """
