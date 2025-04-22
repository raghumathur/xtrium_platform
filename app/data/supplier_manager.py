import pandas as pd
from pathlib import Path
import json

class SupplierManager:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent / "assets" / "databases" / "dashboard"
        self._suppliers = None
        self._load_suppliers()
    
    def _load_suppliers(self):
        """Load suppliers from CSV file."""
        if self._suppliers is None:
            self._suppliers = pd.read_csv(self.base_path / "suppliers.csv")
    
    def get_all_suppliers(self):
        """Get all suppliers."""
        return self._suppliers
    
    def search_suppliers(self, query=None, filters=None):
        """
        Search suppliers based on query and filters.
        
        Args:
            query (str): Search query for name, materials, or specialties
            filters (dict): Filters like region, certifications, etc.
        """
        df = self._suppliers.copy()
        
        if query:
            query = query.lower()
            df = df[
                df['Name'].str.lower().str.contains(query) |
                df['Materials'].str.lower().str.contains(query) |
                df['Specialties'].str.lower().str.contains(query)
            ]
        
        if filters:
            if filters.get('region'):
                df = df[df['Region'] == filters['region']]
            if filters.get('min_rating'):
                df = df[df['Rating'] >= filters['min_rating']]
            if filters.get('certification'):
                df = df[df['Certifications'].str.contains(filters['certification'])]
        
        return df
    
    def get_supplier_details(self, name):
        """Get detailed information about a specific supplier."""
        return self._suppliers[self._suppliers['Name'] == name].iloc[0].to_dict()
    
    def get_regions(self):
        """Get list of unique regions."""
        return sorted(self._suppliers['Region'].unique())
    
    def get_certifications(self):
        """Get list of unique certifications."""
        all_certs = []
        for certs in self._suppliers['Certifications'].str.split(', '):
            all_certs.extend(certs)
        return sorted(set(all_certs))
    
    def get_materials(self):
        """Get list of unique materials."""
        all_materials = []
        for materials in self._suppliers['Materials'].str.split(', '):
            all_materials.extend(materials)
        return sorted(set(all_materials))
