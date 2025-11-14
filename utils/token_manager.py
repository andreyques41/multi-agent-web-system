"""
Token Management Utilities

Manages token counting and truncation to prevent 413 errors.
"""

import tiktoken
from typing import Any


def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """
    Count tokens in a text string for a given model.
    
    Args:
        text: Text to count tokens for
        model: Model name (determines encoding)
        
    Returns:
        int: Number of tokens
    """
    try:
        # Map our model names to tiktoken encodings
        encoding_map = {
            "gpt-4o": "cl100k_base",
            "gpt-4.1": "cl100k_base",
            "gpt-5-chat": "cl100k_base",
            "o3": "cl100k_base",
            "o3-mini": "cl100k_base",
            "o1-mini": "cl100k_base",
        }
        
        encoding_name = encoding_map.get(model, "cl100k_base")
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(text))
    except Exception as e:
        # Fallback: rough estimate (1 token ≈ 4 characters)
        return len(text) // 4


def truncate_to_token_limit(text: str, max_tokens: int, model: str = "gpt-4o") -> str:
    """
    Truncate text to fit within token limit, keeping beginning and end.
    
    Args:
        text: Text to truncate
        max_tokens: Maximum tokens allowed
        model: Model name (determines encoding)
        
    Returns:
        str: Truncated text
    """
    current_tokens = count_tokens(text, model)
    
    if current_tokens <= max_tokens:
        return text
    
    # Keep first 60% and last 40% of the token budget
    keep_start_tokens = int(max_tokens * 0.6)
    keep_end_tokens = int(max_tokens * 0.4)
    
    try:
        encoding_map = {
            "gpt-4o": "cl100k_base",
            "gpt-4.1": "cl100k_base",
            "gpt-5-chat": "cl100k_base",
            "o3": "cl100k_base",
            "o3-mini": "cl100k_base",
            "o1-mini": "cl100k_base",
        }
        
        encoding_name = encoding_map.get(model, "cl100k_base")
        encoding = tiktoken.get_encoding(encoding_name)
        
        tokens = encoding.encode(text)
        
        # Keep start and end tokens
        truncated_tokens = (
            tokens[:keep_start_tokens] + 
            tokens[-keep_end_tokens:]
        )
        
        truncated_text = encoding.decode(truncated_tokens)
        
        # Add marker to show truncation
        marker = f"\n\n[... Content truncated: {current_tokens} tokens → {max_tokens} tokens ...]\n\n"
        
        # Find a good split point (middle of text)
        mid_point = len(truncated_text) // 2
        start_part = truncated_text[:mid_point]
        end_part = truncated_text[mid_point:]
        
        return start_part + marker + end_part
        
    except Exception as e:
        # Fallback: character-based truncation
        chars_per_token = len(text) / current_tokens
        max_chars = int(max_tokens * chars_per_token)
        
        keep_start_chars = int(max_chars * 0.6)
        keep_end_chars = int(max_chars * 0.4)
        
        marker = f"\n\n[... Content truncated: ~{current_tokens} tokens → ~{max_tokens} tokens ...]\n\n"
        
        return text[:keep_start_chars] + marker + text[-keep_end_chars:]


def summarize_task_output(output: str, max_tokens: int = 1500, model: str = "gpt-4o") -> str:
    """
    Summarize task output to a fixed token budget.
    Keeps key information while reducing size.
    
    Args:
        output: Task output to summarize
        max_tokens: Maximum tokens for summary
        model: Model name
        
    Returns:
        str: Summarized output
    """
    current_tokens = count_tokens(output, model)
    
    if current_tokens <= max_tokens:
        return output
    
    # Extract key sections (first and last parts tend to have key info)
    lines = output.split('\n')
    
    # Keep first 40% and last 40% of lines, drop middle 20%
    total_lines = len(lines)
    keep_start = int(total_lines * 0.4)
    keep_end = int(total_lines * 0.4)
    
    summary_lines = (
        lines[:keep_start] +
        [f"\n[... Middle section truncated to fit {max_tokens} token limit ...]\n"] +
        lines[-keep_end:]
    )
    
    summary = '\n'.join(summary_lines)
    
    # If still too large, use hard truncation
    if count_tokens(summary, model) > max_tokens:
        summary = truncate_to_token_limit(summary, max_tokens, model)
    
    return summary


def get_safe_token_limit(model: str) -> dict:
    """
    Get safe token limits for a model (leaves headroom for system prompts).
    
    Args:
        model: Model name
        
    Returns:
        dict: {
            'total': Total model limit,
            'context': Safe limit for context passing,
            'response': Safe limit for response generation
        }
    """
    # Model limits based on actual testing
    model_limits = {
        "gpt-4o": 8000,
        "gpt-4.1": 8000,
        "gpt-5-chat": 4000,
        "o3": 4000,
        "o3-mini": 4000,
        "o1-mini": 4000,
        "gpt-4o-mini": 8000,
        "deepseek-r1": 4000,
        "phi-4": 4000,
    }
    
    total = model_limits.get(model, 4000)
    
    # Reserve space for system prompts, task description, etc.
    # Context: 50% of total (for passing previous outputs)
    # Response: 30% of total (for agent's response)
    # System/Task: 20% reserved (not returned)
    
    return {
        'total': total,
        'context': int(total * 0.5),  # 50% for context
        'response': int(total * 0.3),  # 30% for response
    }


# Example usage in task callbacks
class TaskOutputManager:
    """Manages task outputs to prevent token overflow."""
    
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.limits = get_safe_token_limit(model)
        self.task_outputs = {}
    
    def store_output(self, task_id: str, output: str) -> str:
        """Store task output with automatic truncation."""
        truncated = summarize_task_output(
            output, 
            max_tokens=self.limits['context'],
            model=self.model
        )
        self.task_outputs[task_id] = truncated
        return truncated
    
    def get_output(self, task_id: str) -> str:
        """Retrieve stored task output."""
        return self.task_outputs.get(task_id, "")
    
    def get_combined_context(self, task_ids: list) -> str:
        """Get combined context from multiple tasks, with truncation."""
        contexts = [self.get_output(tid) for tid in task_ids if tid in self.task_outputs]
        combined = "\n\n---\n\n".join(contexts)
        
        # Ensure combined context fits within limit
        return truncate_to_token_limit(
            combined,
            max_tokens=self.limits['context'],
            model=self.model
        )
