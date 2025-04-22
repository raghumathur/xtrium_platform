# Core library imports
import os  # Provides functions for interacting with the operating system
import random  # Used for generating random values
import re

# Data manipulation libraries
import pandas as pd  # For working with structured data in DataFrames
import numpy as np  # For numerical computations

# Visualization libraries
import plotly.figure_factory as ff  # For creating advanced visualizations
import plotly.graph_objects as go  # For creating and customizing plots

# Streamlit libraries for interactive web applications
import streamlit as st  # Main Streamlit library for building the app
import streamlit_modal as st_modal  # For creating modals in Streamlit

# Machine learning libraries
from sklearn.metrics.pairwise import cosine_similarity  # For calculating pairwise similarity
from sklearn.cluster import AgglomerativeClustering  # For hierarchical clustering

# NLP-specific library
from sentence_transformers import SentenceTransformer  # For embedding text into vectors

# Typing for type hints
from typing import Dict, Union, List, Optional  # For providing type hints for function arguments and return values


def init_session_state():
    """
    Initialize and flush the Streamlit session state at the start of the application.

    This function checks if the session state has already been flushed. If not,
    it clears the existing session state to ensure a clean state at the start of
    the application, and then sets a flag (`session_flushed_at_init`) to prevent further flushing.

    Purpose:
        - To reset all session variables when the app is restarted or loaded fresh.
        - Prevents issues caused by residual session variables from previous runs.

    Usage:
        Call this function at the start of the Streamlit app to reset session state.

    Streamlit Features Used:
        - `st.session_state`: A built-in Streamlit object for persisting state variables
          across user interactions within the app.

    """
    layout_mode = "wide"  # or "centered"
    st.set_page_config(layout=layout_mode)   

    # Check if the session state has already been flushed
    # The "session_flushed" key acts as a flag to indicate if the session state was cleared
    if "session_flushed_at_init" not in st.session_state:
        # Clear the entire session state
        st.session_state.clear()

        # Set the "session_flushed" flag to True to avoid re-clearing in subsequent runs
        st.session_state.session_flushed_at_init = True
    


