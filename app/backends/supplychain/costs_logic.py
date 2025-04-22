import streamlit as st

def costs_filter(costs_df):
        # Unique options for dropdowns
    unique_geolocations = costs_df["geolocation"].dropna().unique().tolist()
    unique_currencies = costs_df["currency"].dropna().unique().tolist()

    # Checkbox to include cost filter
    include_cost_filter = st.checkbox("Include Cost Filter")

    if include_cost_filter:
        cols = st.columns([3, 3, 2])  # Define layout for cost slider and dropdowns

        # Slider for cost range
        with cols[0]:
            cost_min = costs_df["cost"].min()
            cost_max = costs_df["cost"].max()
            selected_cost = st.slider(
                "Cost Range",
                min_value=float(cost_min),
                max_value=float(cost_max),
                value=(float(cost_min), float(cost_max)),
                help="Adjust the cost range for filtering."
            )

        # Dropdown for Geolocation
        with cols[1]:
            selected_geolocation = st.selectbox(
                "Geolocation",
                options=unique_geolocations,
                help="Select a geolocation for the cost filter."
            )

        # Dropdown for Currency
        with cols[2]:
            selected_currency = st.selectbox(
                "Currency",
                options=unique_currencies,
                help="Select a currency for the cost filter."
            )

        # Dropdown for Unit of Sales
        # with cols[3]:
        #    selected_unit_of_sales = st.selectbox(
        #        "Unit of Sales",
        #        options=unique_units_of_sales,
        #        help="Select the unit of sales for the cost filter."
        #    )
    