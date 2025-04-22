import streamlit as st
import pandas as pd

def get_suppliers(material_id, suppliers_df):
    """
    Retrieve suppliers for a given material ID.

    :param material_id: Material ID to look up suppliers.
    :param suppliers_df: DataFrame containing supplier data.
    :return: List of suppliers.
    """
    return suppliers_df[suppliers_df["Material_ID"] == material_id]

def display_supplier_info(suppliers_df):
    st.dataframe(get_suppliers("mp-1265539"), suppliers_df)

"""
def show_suppliers_info():
    with st.modal("Suppliers for Selected Material"):
        st.write(f"### Suppliers for Material ID: {selected_material}")
        for _, row in filtered_df.iterrows():
            st.write(f"**Supplier Name**: {row['Supplier Name']}")
            st.write(f"**Contact Info**: {row['Contact Info']}")
            st.write(f"**Availability**: {row['Availability']}")
            st.write(f"**Cost Range**: {row['Cost Range']}")
            st.write(f"**Rating**: {row['Rating']} ⭐")
            st.write("---")
"""