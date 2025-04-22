import streamlit as st

def apply_custom_css():
    """
    Apply custom CSS for global styling of the Streamlit app.
    """
    st.markdown(
        """
        <style>
        /* Global Style */
        body {
            background-color: #121212;
            color: white;
            font-family: "Arial", sans-serif;
            font-size: 18px;
        }

        /* Sidebar Styling */
        .css-1d391kg {
            background-image: url('../../assets/images/sidebar_bg.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }

        /* Main Page Background */
        .stApp {
            #background: linear-gradient(to right, #121212, #121212 70%, #800000 30%);
            color: white;
        }

        /* Top Pane Styling */
        .top-pane {
            background-color: #600000;
            padding: 18px;
            border-bottom: 4px solid #ff0000;
        }
        .top-pane h1, .top-pane p {
            margin: 0;
            color: white;
            text-align: center;
        }
        .top-pane a {
            color: #ff0000;
            text-decoration: none;
            font-weight: bold;
        }
        .top-pane a:hover {
            text-decoration: underline;
        }

        /* Tab Styling */
        div.stTabs div[data-baseweb="tab-list"] {
            display: flex;
            justify-content: center;
        }
        div.stTabs button {
            flex-grow: 1;
            font-size: 18px;
            text-align: center;
            color: #333;
            border: none;
        }
        div.stTabs button:hover {
            background-color: #ffe6e6;
        }
        div.stTabs button[aria-selected="true"] {
            background-color: #800000;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def apply_custom_button_css(button_id, color, hover_color, border_radius):
    """
    Generate CSS for a specific button.
    """
    st.markdown(
        f"""
        <style>
        #{button_id} {{
            background-color: {color};
            color: white;
            border: none;
            border-radius: {border_radius};
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }}
        #{button_id}:hover {{
            background-color: {hover_color};
            cursor: pointer;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def style_sidebar_css(bgcolor: str = "#2a2f4f", title_fontsize: str = "26px", text_fontsize: str = "24px"):
    """
    Function to style the Streamlit sidebar dynamically.

    Parameters:
        bgcolor (str): Background color of the sidebar (default: light gray).
        title_fontsize (str): Font size for the sidebar title (default: 20px).
        text_fontsize (str): Font size for regular text in the sidebar (default: 16px).
    """
    custom_css = f"""
    <style>
    /* Style for the entire sidebar */
    [data-testid="stSidebar"] {{
        font-family: 'Arial', sans-serif;
        background-color: {bgcolor};
    }}

    /* Style for the sidebar title */
    [data-testid="stSidebar"] h1 {{
        font-size: {title_fontsize};
        color: #FFFFFF;
    }}

    /* Style for regular text in the sidebar */
    [data-testid="stSidebar"] p {{
        font-size: {text_fontsize};
        color: #FFFFFF;
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# def style_tabs_css(bgcolor: str = "#2a2f4f", title_fontsize: str = "26px", text_fontsize: str = "24px"):
def style_tabs_css():
    st.markdown(
    """
    <style>
    /* Tab Styling */
    div.stTabs div[data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
    }
    div.stTabs button {
        flex-grow: 1;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
        color: #eee4b1;
        border: none;
    }
    div.stTabs button:hover {
        background-color: #eeeeee;
    }
    div.stTabs button[aria-selected="true"] {
        background-color: #2a2f4f;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def style_global_css():
    """
    Apply custom CSS for global styling of the Streamlit app.
    """
    # Apply custom CSS to increase font size
    st.markdown(
        """
        <style>
        /* General font size for body text */
        body {
            font-size: 18px;
        }

        /* Specific header font sizes */
        h1 {
            font-size: 24px !important;
        }
        h2 {
            font-size: 20px !important;
        }
        h3 {
            font-size: 18px !important;
        }

        /* Increase font size for streamlit text elements */
        .stMarkdown p {
            font-size: 18px;
        }

        /* For buttons or other interactive elements */
        .stButton button {
            font-size: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def style_textarea_css():
    # Inject custom CSS for the text area
    st.markdown(
        """
        <style>
        /* Target the text area */
        div[data-testid="stTextArea"] textarea {
            background-color: #222831; /* Set background color (e.g., AliceBlue) */
            color: #ffffff; /* Set text color (e.g., Navy) */
            font-size: 16px; /* Set font size */
            border: 2px solid #000080; /* Optional: Add a border */
            border-radius: 8px; /* Optional: Add rounded corners */
            padding: 10px; /* Optional: Add padding */
        }
        </style>
        """,
        unsafe_allow_html=True
    )