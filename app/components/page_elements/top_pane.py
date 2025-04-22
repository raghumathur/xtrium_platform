# %%
import streamlit as st

# %%
def render_top_pane():
    """
    Renders the top pane with title, tagline, and links.
    """

    # Add custom CSS for positioning links in the top right corner
    st.markdown(
        """
        <style>
        .top-right-links {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
            display: flex;
            gap: 15px;
            background-color: white; /* Optional: Makes it visible over other content */
            padding: 5px 10px; /* Optional: Adds padding around the links */
            border-radius: 5px; /* Optional: Rounded corners for better aesthetics */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Optional: Subtle shadow for emphasis */
        }
        .top-right-links a {
            text-decoration: none;
            color: #1a73e8; /* Google's blue */
            font-weight: bold;
            font-size: 16px;
        }
        .top-right-links a:hover {
            text-decoration: underline;
            color: #0b51c7; /* Darker blue on hover */
        }
        </style>
        <div class="top-right-links">
            <a href="https://example.com" target="_blank">Home</a>
            <a href="https://example.com/docs" target="_blank">Docs</a>
            <a href="https://example.com/contact" target="_blank">Contact</a>
        </div>
        """,
        unsafe_allow_html=True
    )    
    st.markdown(
        """
        <style>
            .top-pane h3 {
                text-align: center;
            }
        </style>        
        <div class="top-pane">
            <p>
                <a href="https://example.com/docs" target="_blank">Documentation</a> |
                <a href="https://xtrium.net/" target="_blank">Home Page</a> |
                <a href="https://xtrium.net/contact" target="_blank">Contact</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )