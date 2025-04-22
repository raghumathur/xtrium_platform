import pandas as pd
from pathlib import Path
import numpy as np

class SustainabilityManager:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent / "assets" / "databases" / "dashboard"
        self._benchmarks = None
        self._material_data = None
        self._load_data()
    
    def _load_data(self):
        """Load sustainability data from CSV files."""
        if self._benchmarks is None:
            self._benchmarks = pd.read_csv(self.base_path / "industry_benchmarks.csv")
        if self._material_data is None:
            self._material_data = pd.read_csv(self.base_path / "material_sustainability.csv")
    
    def get_benchmarks(self, industry="Polymers"):
        """Get industry benchmarks."""
        return self._benchmarks[self._benchmarks["Industry"] == industry]
    
    def get_material_metrics(self, materials=None):
        """Get sustainability metrics for specified materials."""
        if materials:
            return self._material_data[self._material_data["Material"].isin(materials)]
        return self._material_data
    
    def calculate_portfolio_impact(self, materials, volumes):
        """Calculate sustainability impact of material portfolio."""
        df = self._material_data[self._material_data["Material"].isin(materials)]
        total_volume = sum(volumes.values())
        
        portfolio_impact = {
            "Carbon Footprint": 0.0,
            "Water Usage": 0.0,
            "Energy Usage": 0.0,
            "Cost Premium": 0.0,
            "Recycled Content": 0.0,
            "Bio-based Content": 0.0
        }
        
        for material in materials:
            volume_share = volumes.get(material, 0) / total_volume
            mat_data = df[df["Material"] == material].iloc[0]
            
            # Convert string values to float before multiplication
            portfolio_impact["Carbon Footprint"] += float(mat_data["Carbon Footprint"]) * volume_share
            portfolio_impact["Water Usage"] += float(mat_data["Water Usage"]) * volume_share
            portfolio_impact["Energy Usage"] += float(mat_data["Energy Usage"]) * volume_share
            portfolio_impact["Cost Premium"] += float(mat_data["Cost Premium"].strip('%')) * volume_share
            
            # Extract recycled content from 'Recycled Content Available' field
            recycled_content = float(mat_data["Recycled Content Available"].strip('Up to %').strip()) / 100.0
            portfolio_impact["Recycled Content"] += recycled_content * volume_share
            
            # Bio-based content (Yes/No/Partial)
            bio_based_map = {"Yes": 1.0, "Partial": 0.5, "No": 0.0}
            portfolio_impact["Bio-based Content"] += bio_based_map[mat_data["Bio-based"]] * volume_share
        
        return portfolio_impact
    
    def get_cost_savings_opportunities(self, current_materials):
        """Identify cost saving opportunities while maintaining sustainability."""
        df = self._material_data
        opportunities = []
        
        for material in current_materials:
            current = df[df["Material"] == material].iloc[0]
            current_cost = float(current["Cost Premium"].strip('%'))
            current_carbon = float(current["Carbon Footprint"])
            current_water = float(current["Water Usage"])
            
            # Find alternatives with better or similar sustainability metrics
            alternatives = df[
                (df["Material"] != material) &
                (df["Carbon Footprint"].astype(float) <= current_carbon * 1.1) &
                (df["Water Usage"].astype(float) <= current_water * 1.1)
            ]
            
            for _, alt in alternatives.iterrows():
                alt_cost = float(alt["Cost Premium"].strip('%'))
                if alt_cost < current_cost:
                    savings = current_cost - alt_cost
                    opportunities.append({
                        "Current Material": material,
                        "Alternative": alt["Material"],
                        "Cost Savings": f"{savings:.1f}%",
                        "Carbon Impact": f"{float(alt['Carbon Footprint']) - current_carbon:.1f}",
                        "Water Impact": f"{float(alt['Water Usage']) - current_water:.1f}"
                    })
        
        return opportunities
    
    def calculate_industry_position(self, metric, value):
        """Calculate industry position (percentile) for a given metric."""
        benchmark = self._benchmarks[self._benchmarks["Metric"].str.contains(metric, case=False)].iloc[0]
        
        if value <= benchmark["Industry Average"]:
            percentile = 50 * (value / benchmark["Industry Average"])
        else:
            percentile = 50 + 50 * ((value - benchmark["Industry Average"]) / 
                                  (benchmark["Top Quartile"] - benchmark["Industry Average"]))
        
        return min(100, max(0, percentile))
