"""
Test CrewAI's native LLM configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("TESTING CREWAI WITH MODEL STRING")
print("=" * 60)

# Set GitHub token as API key for OpenAI-compatible endpoint
os.environ["OPENAI_API_KEY"] = os.getenv("GITHUB_TOKEN")
os.environ["OPENAI_API_BASE"] = "https://models.inference.ai.azure.com"

try:
    from crewai import Agent
    
    # Pass model as string, let CrewAI handle it
    agent = Agent(
        role="Test Agent",
        goal="Test if CrewAI works with model string",
        backstory="A test agent",
        llm="gpt-4o",  # Just pass the model name
        verbose=True
    )
    print("✅ Agent created successfully with model string")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
