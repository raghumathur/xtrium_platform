from typing import Dict, List, Optional
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from .base import LLMProvider, LLMConfig

class HuggingFaceProvider(LLMProvider):
    """Provider for HuggingFace models."""
    
    def _validate_config(self):
        """Validate HuggingFace configuration."""
        required_fields = ["name", "torch_dtype", "trust_remote_code"]
        for field in required_fields:
            if field not in self.config.config:
                raise ValueError(f"Missing required field '{field}' in HuggingFace config")
    
    def _initialize_model(self):
        """Initialize HuggingFace model and tokenizer."""
        # Set device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.name,
            trust_remote_code=self.config.config["trust_remote_code"]
        )
        
        # Load model
        dtype = getattr(torch, self.config.config["torch_dtype"])
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.name,
            torch_dtype=dtype,
            trust_remote_code=self.config.config["trust_remote_code"]
        ).to(self.device)
        
        # Set generation config
        self.generation_config = {
            k: v for k, v in self.config.config.items()
            if k not in ["torch_dtype", "trust_remote_code"]
        }
        
        # Add special token IDs
        self.generation_config.update({
            "pad_token_id": self.tokenizer.pad_token_id,
            "eos_token_id": self.tokenizer.eos_token_id
        })
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using the model."""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        # Update generation config with any provided kwargs
        gen_config = {**self.generation_config, **kwargs}
        
        outputs = self.model.generate(
            inputs["input_ids"],
            **gen_config
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response in a chat context."""
        # Format messages into a prompt
        prompt = ""
        for msg in messages:
            role = msg["role"].capitalize()
            content = msg["content"]
            prompt += f"{role}: {content}\n\n"
        
        prompt += "Assistant: "
        
        # Generate response
        full_response = self.generate(prompt, **kwargs)
        
        # Extract just the assistant's response
        return full_response.split("Assistant: ")[-1].strip()
    
    def embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using the model."""
        if not self.supports_feature("embeddings"):
            raise NotImplementedError("This model does not support embeddings")
        
        # Tokenize texts
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate embeddings
        with torch.no_grad():
            outputs = self.model.get_input_embeddings()(inputs["input_ids"])
        
        # Average pooling
        masks = inputs["attention_mask"].unsqueeze(-1)
        embeddings = (outputs * masks).sum(1) / masks.sum(1)
        
        return embeddings.cpu().numpy().tolist()
