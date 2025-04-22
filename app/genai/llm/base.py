from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class LLMConfig:
    """Configuration for an LLM provider."""
    name: str
    type: str
    requires_auth: bool
    supported_features: List[str]
    config: Dict[str, Any]
    api_key: Optional[str] = None

class LLMProvider(ABC):
    """Base class for all LLM providers."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self._validate_config()
        self._initialize_model()
    
    @abstractmethod
    def _validate_config(self):
        """Validate the provider configuration."""
        pass
    
    @abstractmethod
    def _initialize_model(self):
        """Initialize the model and any required resources."""
        pass
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response for the given prompt."""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response in a chat context."""
        pass
    
    @abstractmethod
    def embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for the given texts."""
        pass
    
    def supports_feature(self, feature: str) -> bool:
        """Check if the provider supports a specific feature."""
        return feature in self.config.supported_features
