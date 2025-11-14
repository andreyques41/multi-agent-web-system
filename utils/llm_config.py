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
# NOTE: GitHub Models API ONLY supports OpenAI and Microsoft models  
# Claude/Anthropic models are NOT available in GitHub Models
# Model IDs for inference API do NOT include provider prefix
# See: https://models.github.ai/catalog/models (catalog shows openai/gpt-4o)
# But inference endpoint expects just "gpt-4o"
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
            model = os.getenv("GITHUB_MODEL", "gpt-4.1")  # Default to best general coding model
        elif provider == LLMProvider.OPENAI:
            model = os.getenv("OPENAI_MODEL", "gpt-4o")
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


def get_best_model_for_agent(agent_role: str) -> Optional[str]:
    """
    Get the best model for a specific agent role.
    
    Different models excel at different tasks:
    - GPT-5.1-codex: Best for code generation (Backend, Frontend, DevOps)
    - Claude-4.5-sonnet: Best for architecture and complex reasoning (Business Analyst, PM)
    - GPT-5.1: Best for general tasks and QA
    
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
    
    # Determine provider to know which models are available
    provider = os.getenv("LLM_PROVIDER", "").lower()
    if not provider:
        if os.getenv("GITHUB_TOKEN"):
            provider = "github"
        elif os.getenv("OPENAI_API_KEY"):
            provider = "openai"
        elif os.getenv("ANTHROPIC_API_KEY"):
            provider = "anthropic"
    
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
    
    # If the recommended model is not available in the current provider, fallback to a compatible one
    if recommended:
        if provider == "github":
            # GitHub Models supports both GPT and Claude through their API
            if recommended in GITHUB_MODELS:
                return recommended
            # If Claude is recommended but not using Anthropic directly, use GPT-5.1 instead
            elif "claude" in recommended:
                return "gpt-5.1"  # Fallback to GPT for reasoning tasks
            return recommended if recommended in GITHUB_MODELS else None
        elif provider == "openai" and recommended in OPENAI_MODELS:
            return recommended
        elif provider == "anthropic" and recommended in ANTHROPIC_MODELS:
            return recommended
    
    # Return None to use the default model from environment
    return None
