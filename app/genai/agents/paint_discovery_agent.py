from typing import Dict

class PaintDiscoveryAgent:
    def __init__(self):
        pass

    def chat(self, query: str) -> Dict:
        """Return static responses based on query."""
        if "material" in query.lower():
            return self._get_materials_response()
        elif "application" in query.lower():
            return self._get_applications_response()
        else:
            return {"error": "Please ask about materials or applications for your paint and coating needs."}

    def _get_applications_response(self) -> Dict:
        """Return static response for applications mode."""
        return {
            "applications": [
                {
                    "industry": "Semiconductor",
                    "application": "Clean Room Equipment",
                    "component": "Processing chamber walls",
                    "required_properties": "Chemical resistance, particle-free, easy-clean",
                    "sustainability_impact": "Extends equipment life by 40%",
                    "supply_chain_notes": "Local suppliers available in major semiconductor hubs"
                },
                {
                    "industry": "Aerospace",
                    "application": "Engine Components",
                    "component": "Thrust reverser coating",
                    "required_properties": "Heat resistant to 200°C, wear resistant",
                    "sustainability_impact": "Reduces fuel consumption by 2%",
                    "supply_chain_notes": "Qualified by major aerospace OEMs"
                },
                {
                    "industry": "Medical",
                    "application": "Sterilization Equipment",
                    "component": "Autoclave chambers",
                    "required_properties": "Steam resistant, antimicrobial, FDA compliant",
                    "sustainability_impact": "Reduces contamination by 99.9%",
                    "supply_chain_notes": "Medical-grade certified manufacturing"
                },
                {
                    "industry": "Energy",
                    "application": "Solar Panels",
                    "component": "Protective encapsulation",
                    "required_properties": "UV resistant, weatherproof, self-cleaning",
                    "sustainability_impact": "Increases panel efficiency by 5%",
                    "supply_chain_notes": "Global distribution network"
                },
                {
                    "industry": "Marine",
                    "application": "Offshore Platforms",
                    "component": "Structural coating",
                    "required_properties": "Saltwater resistant, anti-corrosive, impact resistant",
                    "sustainability_impact": "Extends structure life by 25%",
                    "supply_chain_notes": "Available at major ports worldwide"
                }
            ],
            "market_insights": "Market Overview:\n\n• Market Size: $4.2B (2024), growing at 6.1% CAGR\n• Key Growth Segments:\n  - Aerospace & Defense: 32% market share\n  - Electronics: 28% market share\n  - Medical: 20% market share\n  - Energy: 15% market share\n  - Marine: 5% market share\n• Regional Leaders:\n  - APAC: 42% (electronics, marine)\n  - North America: 31% (aerospace, medical)\n  - Europe: 27% (energy, medical)"
        }

    def _get_materials_response(self) -> Dict:
        """Return static response for materials mode."""
        return {
            "materials": [
                {
                    "material_name": "EpoTherm 200",
                    "chemical_type": "Modified Epoxy",
                    "primary_function": "High-temp coating",
                    "properties": "200°C stable, chemical resistant",
                    "sustainability_metrics": "45% bio-based content",
                    "current_applications": "Aerospace, Industrial"
                },
                {
                    "material_name": "DuraImide Plus",
                    "chemical_type": "Polyimide Hybrid",
                    "primary_function": "Protective coating",
                    "properties": "Thermal shock resistant, flexible",
                    "sustainability_metrics": "Zero VOC",
                    "current_applications": "Electronics, Medical"
                },
                {
                    "material_name": "NanoGuard X1",
                    "chemical_type": "Nanocomposite",
                    "primary_function": "Advanced barrier coating",
                    "properties": "Self-healing, ultra-thin, transparent",
                    "sustainability_metrics": "100% recyclable",
                    "current_applications": "Electronics, Solar"
                },
                {
                    "material_name": "MarineTech Pro",
                    "chemical_type": "Silicone Hybrid",
                    "primary_function": "Marine protection",
                    "properties": "Salt-spray resistant, anti-fouling",
                    "sustainability_metrics": "Copper-free, reef safe",
                    "current_applications": "Marine, Offshore"
                },
                {
                    "material_name": "BioShield Elite",
                    "chemical_type": "Bio-based Polymer",
                    "primary_function": "Medical coating",
                    "properties": "Antimicrobial, biocompatible",
                    "sustainability_metrics": "80% bio-based, biodegradable",
                    "current_applications": "Medical, Food Processing"
                }
            ],
            "supply_chain": "Supply Chain & Sustainability:\n\n• Manufacturing Capacity:\n  - 12 major producers globally\n  - 85% capacity utilization\n  - 3 new facilities under construction\n• Environmental Impact:\n  - 45% lower carbon footprint\n  - VOC: <50 g/L\n  - 60% renewable raw materials\n• Certifications:\n  - ISO 14001\n  - REACH compliant\n  - FDA approved\n  - NSF certified\n  - Green Label Plus"
        }
