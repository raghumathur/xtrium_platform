from abc import ABC, abstractmethod
from typing import Dict, Optional
import pandas as pd
from sentence_transformers import SentenceTransformer

class BaseAgent(ABC):
    """Base class for all GenAI agents."""
    
    def __init__(self):
        """Initialize the base agent."""
        # Initialize embeddings model
        self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize database references
        self.materials_df: Optional[pd.DataFrame] = None
        self.applications_df: Optional[pd.DataFrame] = None
        self.suppliers_df: Optional[pd.DataFrame] = None
    
    def _init_embeddings(self):
        """Initialize the embeddings model."""
        self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def load_databases(self, materials_df: pd.DataFrame, applications_df: pd.DataFrame, suppliers_df: pd.DataFrame):
        """Load the required databases."""
        self.materials_df = materials_df
        self.applications_df = applications_df
        self.suppliers_df = suppliers_df
    
    @abstractmethod
    def chat(self, query: str, context: Dict, filters: list) -> Dict:
        """Process a chat query and return a response."""
        pass
    
    def _get_text_similarity(self, query_embedding, target_embedding) -> float:
        """Calculate cosine similarity between two text embeddings."""
        from scipy.spatial.distance import cosine
        return 1 - cosine(query_embedding, target_embedding)
