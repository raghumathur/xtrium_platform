import json
from pathlib import Path
from typing import Dict, Optional
from .base import LLMProvider, LLMConfig
from .huggingface import HuggingFaceProvider
from .deepseek import DeepseekProvider

class LLMFactory:
    """Factory for creating LLM providers."""
    
    def __init__(self, config_path: str = "app/config/llm_providers.json"):
        """Initialize the LLM factory."""
        self.providers: Dict[str, Dict] = {}
        self._load_providers(config_path)
    
    def _load_providers(self, config_path: str):
        """Load provider configurations from JSON."""
        with open(config_path) as f:
            self.providers = json.load(f)
    
    def create_provider(
        self,
        provider_type: str,
        provider_name: str,
        model_name: str,
        api_key: Optional[str] = None
    ) -> LLMProvider:
        """Create an LLM provider instance."""
        # Get provider config
        provider = self.providers.get(provider_type, {}).get(provider_name, {}).get(model_name)
        if not provider:
            raise ValueError(f"Provider not found: {provider_type}/{provider_name}/{model_name}")
        
        # Create config
        config = LLMConfig(
            name=provider["name"],
            type=provider["type"],
            requires_auth=provider["requires_auth"],
            supported_features=provider["supported_features"],
            config=provider["config"],
            api_key=api_key
        )
        
        # Validate auth
        if config.requires_auth and not api_key:
            raise ValueError(f"API key required for {provider_name}")
        
        # Create provider instance
        if config.type == "huggingface":
            return HuggingFaceProvider(config)
        elif config.type == "deepseek":
            return DeepseekProvider(config)
        else:
            raise ValueError(f"Unsupported provider type: {config.type}")
    
    def list_providers(self) -> Dict:
        """List all available providers and models."""
        return {
            provider_type: {
                provider_name: list(models.keys())
                for provider_name, models in providers.items()
            }
            for provider_type, providers in self.providers.items()
        }
    
    def get_provider_config(
        self,
        provider_type: str,
        provider_name: str,
        model_name: str
    ) -> Dict:
        """Get configuration for a specific provider."""
        return self.providers.get(provider_type, {}).get(provider_name, {}).get(model_name, {})
