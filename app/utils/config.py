import json
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """Manage configuration files for the application."""
    
    def __init__(self, config_dir: str = "app/config"):
        """Initialize the config manager."""
        self.config_dir = Path(config_dir)
        self.configs = {}
        self._load_configs()
    
    def _load_configs(self):
        """Load all JSON configuration files."""
        for config_file in self.config_dir.glob("*.json"):
            with open(config_file) as f:
                self.configs[config_file.stem] = json.load(f)
    
    def get_config(self, name: str) -> Dict[str, Any]:
        """Get a specific configuration by name."""
        return self.configs.get(name, {})
    
    def get_property_config(self, property_name: str) -> Dict[str, Any]:
        """Get configuration for a specific material property."""
        properties = self.configs.get("properties", {}).get("material_properties", {})
        return properties.get(property_name, {})
    
    def get_ui_config(self, section: str) -> Dict[str, Any]:
        """Get UI configuration for a specific section."""
        return self.configs.get("ui_config", {}).get(section, {})
    
    def get_model_config(self, model_type: str) -> Dict[str, Any]:
        """Get configuration for a specific model type."""
        return self.configs.get("models", {}).get(model_type, {})
