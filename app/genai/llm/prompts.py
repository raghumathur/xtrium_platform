from typing import Dict, Optional

class DeepseekPrompts:
    """Prompt templates for Deepseek models."""
    
    @staticmethod
    def detect_persona_intent(query: str) -> str:
        return f"""You are analyzing a materials science query. Determine the user's persona and intent.

Input: "{query}"

Think step by step:
1. Look for role-specific keywords
2. Identify the main action/request
3. Consider technical context

Output a JSON object with:
- persona: manufacturer, designer, or inventory_manager
- intent: explore_applications, find_materials, analyze_market, find_suppliers, or sell_inventory
- confidence: 0.0 to 1.0

Response (JSON only):"""

    @staticmethod
    def analyze_material(query: str, properties: Optional[Dict] = None) -> str:
        properties_text = "None provided" if not properties else "\n".join(
            f"- {k}: {v.get('value')} {v.get('unit', '')}"
            for k, v in properties.items()
        )
        
        return f"""As a materials science expert, analyze this query and material properties.

Query: "{query}"

Material Properties:
{properties_text}

Consider:
1. Material characteristics and performance
2. Industry applications and use cases
3. Market potential and opportunities
4. Technical requirements and constraints

Provide a detailed analysis focusing on:
1. Material suitability
2. Application recommendations
3. Technical insights
4. Market opportunities

Response:"""

    @staticmethod
    def find_suppliers(materials: list) -> str:
        materials_list = "\n".join(f"- {m}" for m in materials)
        return f"""Find suppliers for these materials:

{materials_list}

For each material, provide:
1. Supplier recommendations
2. Location and availability
3. Quality certifications
4. Lead time estimates

Response:"""

    @staticmethod
    def find_buyers(query: str, properties: Optional[Dict] = None) -> str:
        properties_text = "None provided" if not properties else "\n".join(
            f"- {k}: {v.get('value')} {v.get('unit', '')}"
            for k, v in properties.items()
        )
        
        return f"""Help find potential buyers for excess material inventory.

Material Query: "{query}"

Properties:
{properties_text}

Identify:
1. Industries that could use this material
2. Potential applications
3. Market demand indicators
4. Value propositions

Response:"""
