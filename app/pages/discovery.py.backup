import streamlit as st
from app.genai.agents.paint_discovery_agent import PaintDiscoveryAgent

def create_material_card(material_data):
    """Create a card displaying material information."""
    with st.container():
        st.markdown(f"**{material_data['material_name']} ({material_data['chemical_type']})** - {material_data['primary_function']}")
        st.markdown(f"Properties: {material_data['properties']}")
        st.markdown(f"Sustainability: {material_data['sustainability_metrics']}")
        st.markdown(f"Current Uses: {material_data['current_applications']}")
        st.markdown("---")

def create_application_card(app):
    """Create an expandable card for displaying application information."""
    with st.expander(f"🎯 {app['industry']} - {app['application']}"):
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.write("##### Technical Details")
            st.write(f"**Component:** {app['component']}")
            st.write(f"**Required Properties:** {app['required_properties']}")
        
        with col2:
            st.write("##### Impact & Supply Chain")
            st.write(f"**Sustainability:** {app['sustainability_impact']}")
            st.write(f"**Supply Chain:** {app['supply_chain_notes']}")

def render_discovery_page():    
    st.header("Discovery Companion")
    st.write("Hi! I am the Xtrium AI Assistant! Ask me about materials, applications, or sustainability metrics for your  requirements")
    st.divider()
    # Chat input
    prompt = st.chat_input("What would you like to know?")
    if prompt:
        # Get response from agent
        agent = PaintDiscoveryAgent()
        response = agent.chat(prompt)
        
        # Display response
        if "applications" in response:
            st.subheader("🎯 Potential Applications")
            for app in response["applications"]:
                create_application_card(app)
            st.subheader("📊 Market Insights")
            st.write(response["market_insights"])
        elif "materials" in response:
            st.subheader("🧪 Recommended Materials")
            for material in response["materials"]:
                create_material_card(material)
            st.subheader("⛓️ Supply Chain Insights")
            st.info(response["supply_chain"])
        elif "error" in response:
            st.error(response["error"])

if __name__ == "__main__":
    render_discovery_page()
