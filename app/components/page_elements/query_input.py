import streamlit as st
from app.ui.design_system.components import get_global_styles
from app.ui.design_system.tokens import Spacing
#from app.components.page_elements.render_demo_results import render_report
#from app.components.page_elements.render_demo_results_adhesives import render_report_adhesives
#from app.components.page_elements.render_demo_results_henkel import render_report_adhesives2

def render_query_input():
    # Apply global styles which include input styling
    st.markdown(get_global_styles(), unsafe_allow_html=True)
    """
    Render the natural language query input section.
    """
    # Natural Language Query Section
    query_col, submit_col = st.columns([20, 1])
    with query_col:
        query = st.text_area(
            #"AI Assistant Input",  # Label for accessibility
            " ",  # Label for accessibility
            placeholder="I'm the Xtrium AI Assistant! \nAsk me anything about material performance, substitutions, or applications…",
            height=100,
            key="nl_query"
        )
    with submit_col:
        st.markdown(f"<div style='height:{Spacing.XL};'></div>", unsafe_allow_html=True)  # Add vertical spacing
        st.markdown(
            """
            <style>
            div[data-testid='stButton'] button {
                display: flex;
                justify-content: center;
                align-items: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        submitted = st.button("➤", key="submit_query", use_container_width=True)
        
    # Handle button click
    # if submitted and query:
    #    render_report(query)