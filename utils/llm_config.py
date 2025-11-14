"""
LLM Configuration Module

Manages configuration for different AI model providers:
- GitHub Models (uses your GitHub Copilot subscription - FREE)
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3.5 Sonnet, etc.)
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMProvider:
    """Supported LLM providers"""
    GITHUB = "github"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


# Available models per provider
GITHUB_MODELS = {
    # GPT-5 Series (Latest - November 2025)
    "gpt-5.1": "openai/gpt-5.1",
    "gpt-5.1-codex": "openai/gpt-5.1-codex",  # Optimized for code
    "gpt-5": "openai/gpt-5",
    "gpt-5-codex": "openai/gpt-5-codex",  # Optimized for code
    
    # Claude 4 Series (Latest - November 2025)
    "claude-4.5-sonnet": "anthropic/claude-4.5-sonnet",  # Most advanced
    "claude-4-sonnet": "anthropic/claude-4-sonnet",
    
    # GPT-4 Series (Legacy but still available)
    "gpt-4o": "openai/gpt-4o",
    "gpt-4o-mini": "openai/gpt-4o-mini",
    "gpt-4": "openai/gpt-4",
    
    # Claude 3 Series (Legacy)
    "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
    
    # Open Source Models
    "llama-3.1-70b": "meta/llama-3.1-70b-instruct",
    "phi-3": "microsoft/phi-3-medium-4k-instruct",
}

OPENAI_MODELS = {
    # GPT-5 Series (if using OpenAI directly)
    "gpt-5.1": "gpt-5.1",
    "gpt-5.1-codex": "gpt-5.1-codex",
    "gpt-5": "gpt-5",
    "gpt-5-codex": "gpt-5-codex",
    
    # GPT-4 Series (Legacy)
    "gpt-4-turbo": "gpt-4-turbo-preview",
    "gpt-4": "gpt-4",
    "gpt-4o": "gpt-4o",
    "gpt-3.5-turbo": "gpt-3.5-turbo",
}

ANTHROPIC_MODELS = {
    # Claude 4 Series (Latest)
    "claude-4.5-sonnet": "claude-4.5-sonnet-20241114",
    "claude-4-sonnet": "claude-4-sonnet-20241114",
    
    # Claude 3 Series (Legacy)
    "claude-3.5-sonnet": "claude-3-5-sonnet-20241022",
    "claude-3-opus": "claude-3-opus-20240229",
    "claude-3-sonnet": "claude-3-sonnet-20240229",
}


def get_llm_config(provider: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    """
    Get LLM configuration based on environment variables.
    
    Priority order:
    1. GitHub Models (if GITHUB_TOKEN is set and provider not specified)
    2. OpenAI (if OPENAI_API_KEY is set)
    3. Anthropic (if ANTHROPIC_API_KEY is set)
    
    Args:
        provider: Force specific provider ('github', 'openai', 'anthropic')
        model: Model name to use (if not specified, uses default from env)
        
    Returns:
        Dict with configuration for CrewAI agents
        
    Example:
        >>> config = get_llm_config()
        >>> agent = Agent(..., llm=config)
    """
    # Determine provider
    if provider is None:
        provider = os.getenv("LLM_PROVIDER", "").lower()
        
        # Auto-detect based on available API keys
        if not provider:
            if os.getenv("GITHUB_TOKEN"):
                provider = LLMProvider.GITHUB
            elif os.getenv("OPENAI_API_KEY"):
                provider = LLMProvider.OPENAI
            elif os.getenv("ANTHROPIC_API_KEY"):
                provider = LLMProvider.ANTHROPIC
            else:
                raise ValueError(
                    "No LLM provider configured. Please set one of: "
                    "GITHUB_TOKEN, OPENAI_API_KEY, or ANTHROPIC_API_KEY"
                )
    
    # Get model name
    if model is None:
        if provider == LLMProvider.GITHUB:
            model = os.getenv("GITHUB_MODEL", "gpt-5.1-codex")  # Default to best coding model
        elif provider == LLMProvider.OPENAI:
            model = os.getenv("OPENAI_MODEL", "gpt-5.1-codex")
        elif provider == LLMProvider.ANTHROPIC:
            model = os.getenv("ANTHROPIC_MODEL", "claude-4.5-sonnet")
    
    # Build configuration
    config = _build_config(provider, model)
    
    return config


def _build_config(provider: str, model: str) -> Dict[str, Any]:
    """Build LLM configuration for the specified provider."""
    
    if provider == LLMProvider.GITHUB:
        return _build_github_config(model)
    elif provider == LLMProvider.OPENAI:
        return _build_openai_config(model)
    elif provider == LLMProvider.ANTHROPIC:
        return _build_anthropic_config(model)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


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
    
    # GitHub Models endpoint is OpenAI-compatible
    config = {
        "model": model_id,
        "base_url": "https://models.github.ai/inference",
        "api_key": github_token,
        "temperature": float(os.getenv("LLM_TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "4000")),
    }
    
    return config


def _build_openai_config(model: str) -> Dict[str, Any]:
    """Build configuration for OpenAI."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. Get one at: "
            "https://platform.openai.com/api-keys"
        )
    
    # Map friendly model name to OpenAI model identifier
    model_id = OPENAI_MODELS.get(model, model)
    
    config = {
        "model": model_id,
        "api_key": api_key,
        "temperature": float(os.getenv("LLM_TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "4000")),
    }
    
    return config


def _build_anthropic_config(model: str) -> Dict[str, Any]:
    """Build configuration for Anthropic Claude."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found. Get one at: "
            "https://console.anthropic.com/settings/keys"
        )
    
    # Map friendly model name to Anthropic model identifier
    model_id = ANTHROPIC_MODELS.get(model, model)
    
    config = {
        "model": model_id,
        "api_key": api_key,
        "temperature": float(os.getenv("LLM_TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "4000")),
    }
    
    return config


def list_available_models() -> Dict[str, list]:
    """List all available models by provider."""
    return {
        "github": list(GITHUB_MODELS.keys()),
        "openai": list(OPENAI_MODELS.keys()),
        "anthropic": list(ANTHROPIC_MODELS.keys()),
    }


def get_provider_info() -> str:
    """Get information about the currently configured provider."""
    try:
        config = get_llm_config()
        provider = os.getenv("LLM_PROVIDER", "").lower()
        
        if not provider:
            if os.getenv("GITHUB_TOKEN"):
                provider = "github"
            elif os.getenv("OPENAI_API_KEY"):
                provider = "openai"
            elif os.getenv("ANTHROPIC_API_KEY"):
                provider = "anthropic"
        
        model = config.get("model", "unknown")
        
        info = f"Provider: {provider.upper()}\nModel: {model}"
        
        if provider == "github":
            info += "\n💰 Cost: FREE (using GitHub Copilot subscription)"
        
        return info
    except ValueError as e:
        return f"No provider configured: {e}"
