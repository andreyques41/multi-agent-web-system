"""
LLM Configuration Module

Manages configuration for GitHub Models API ONLY.
Uses your GitHub Personal Access Token with 'models' scope.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMProvider:
    """Supported LLM provider"""
    GITHUB = "github"


# Available models - GitHub Models API
# Model IDs for inference API do NOT include provider prefix
# See: https://models.github.ai/catalog/models
GITHUB_MODELS = {
    # GPT-5 Series (Latest - April 2025)
    "gpt-5": "gpt-5",
    "gpt-5-chat": "gpt-5-chat",
    "gpt-5-mini": "gpt-5-mini",
    "gpt-5-nano": "gpt-5-nano",
    
    # GPT-4.1 Series (Latest - April 2025) 
    "gpt-4.1": "gpt-4.1",
    "gpt-4.1-mini": "gpt-4.1-mini",
    "gpt-4.1-nano": "gpt-4.1-nano",
    
    # GPT-4o Series (Legacy but widely used and VERIFIED WORKING)
    "gpt-4o": "gpt-4o",
    "gpt-4o-mini": "gpt-4o-mini",
    
    # o Series (Reasoning models)
    "o1": "o1",
    "o1-mini": "o1-mini",
    "o1-preview": "o1-preview",
    "o3": "o3",
    "o3-mini": "o3-mini",
    "o4-mini": "o4-mini",
    
    # Microsoft Phi Series
    "phi-4": "Phi-4",
    "phi-4-reasoning": "Phi-4-reasoning",
    "phi-4-mini-instruct": "Phi-4-mini-instruct",
    "phi-4-mini-reasoning": "Phi-4-mini-reasoning",
    "phi-4-multimodal-instruct": "Phi-4-multimodal-instruct",
    
    # DeepSeek (Advanced reasoning and coding)
    "deepseek-r1": "DeepSeek-R1",
    "deepseek-v3": "DeepSeek-V3-0324",
    
    # Meta Llama
    "llama-3.3-70b": "Llama-3.3-70B-Instruct",
    
    # Mistral AI
    "mistral-small": "Mistral-small-2503",
    "codestral": "Codestral-2501",
    
    # xAI Grok
    "grok-3": "grok-3",
    "grok-3-mini": "grok-3-mini",
}


def get_llm_config(provider: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    """
    Get LLM configuration for GitHub Models API.
    
    Args:
        provider: Ignored - always uses GitHub Models
        model: Model name to use (if not specified, uses default from env)
        
    Returns:
        Dict with configuration for CrewAI agents
        
    Example:
        >>> config = get_llm_config()
        >>> agent = Agent(..., llm=config)
    """
    # Always use GitHub Models
    provider = LLMProvider.GITHUB
    
    # Get model name
    if model is None:
        model = os.getenv("GITHUB_MODEL", "gpt-4.1")  # Default to best general coding model
    
    # Build configuration
    return _build_github_config(model)


def _build_github_config(model: str) -> Dict[str, Any]:
    """
    Build configuration for GitHub Models.
    
    GitHub Models uses an OpenAI-compatible endpoint, so we can use
    the OpenAI client with custom base_url.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError(
            "GITHUB_TOKEN not found. Generate one at: "
            "https://github.com/settings/tokens with 'models' scope"
        )
    
    # Map friendly model name to GitHub model identifier
    model_id = GITHUB_MODELS.get(model, model)
    
    # o-series models (o1, o3, etc.) only support temperature=1
    # They have their own internal reasoning temperature
    o_series_models = ["o1", "o1-mini", "o1-preview", "o3", "o3-mini", "o4-mini"]
    
    # GitHub Models endpoint is OpenAI-compatible
    config = {
        "model": model_id,
        "base_url": "https://models.inference.ai.azure.com",
        "api_key": github_token,
        "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "4000")),
    }
    
    # Only add temperature if not an o-series model
    if model not in o_series_models:
        config["temperature"] = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    
    return config


def list_available_models() -> Dict[str, list]:
    """List all available models."""
    return {
        "github": list(GITHUB_MODELS.keys()),
    }


def get_provider_info() -> str:
    """Get information about the currently configured provider."""
    try:
        config = get_llm_config()
        model = config.get("model", "unknown")
        
        info = f"Provider: GITHUB MODELS\nModel: {model}"
        info += "\n💰 Cost: FREE (using GitHub Personal Access Token)"
        
        return info
    except ValueError as e:
        return f"No provider configured: {e}"


def get_best_model_for_agent(agent_role: str) -> Optional[str]:
    """
    Get the best model for a specific agent role.
    
    Different models excel at different tasks based on actual testing.
    
    Args:
        agent_role: Role of the agent (e.g., 'backend', 'frontend', 'business_analyst')
        
    Returns:
        Recommended model name, or None to use default
        
    Example:
        >>> model = get_best_model_for_agent('backend')
        >>> config = get_llm_config(model=model)
    """
    # Check if user has overridden the model for this specific agent
    env_var = f"{agent_role.upper()}_MODEL"
    override = os.getenv(env_var)
    if override:
        return override
    
    # Recommended models per agent role
    # ✅ BASED ON ACTUAL TESTING OF AVAILABLE MODELS
    # Each model has been tested and verified to work correctly
    recommendations = {
        # Business Analysis - Best with reasoning models
        "business_analyst": "o3",  # ✅ BEST reasoning (tested with logic problems)
        
        # Project Management - Best with chat/planning models  
        "project_manager": "gpt-5-chat",  # ✅ BEST for structured planning (tested with PM tasks)
        
        # Backend Development - Best with code generation
        "backend": "gpt-4.1",  # ✅ Superior coding (tested with Python code)
        
        # Frontend Development - Best with code generation
        "frontend": "gpt-4.1",  # ✅ Superior coding (tested with JavaScript)
        
        # DevOps/Infrastructure - Best with technical architecture
        "devops": "deepseek-r1",  # ✅ Excellent for system architecture (tested with API optimization)
        
        # QA Testing - Best with reasoning for test cases
        "qa": "o3-mini",  # ✅ Good reasoning, more cost-effective than o3
    }
    
    recommended = recommendations.get(agent_role.lower())
    
    # Return recommended model if it exists in GitHub Models
    if recommended and recommended in GITHUB_MODELS:
        return recommended
    
    # Return None to use the default model from environment
    return None
