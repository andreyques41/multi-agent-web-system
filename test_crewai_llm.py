"""
Test script to understand how CrewAI handles LLMs
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("ENVIRONMENT VARIABLES")
print("=" * 60)
print(f"GITHUB_TOKEN: {'SET' if os.getenv('GITHUB_TOKEN') else 'NOT SET'}")
print(f"OPENAI_API_KEY: {'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")
print(f"LLM_PROVIDER: {os.getenv('LLM_PROVIDER', 'NOT SET')}")
print()

print("=" * 60)
print("TESTING LANGCHAIN ChatOpenAI")
print("=" * 60)
try:
    from langchain_openai import ChatOpenAI
    
    config = {
        "model": "gpt-4o",
        "base_url": "https://models.inference.ai.azure.com",
        "api_key": os.getenv("GITHUB_TOKEN"),
        "temperature": 0.7,
    }
    
    print(f"Creating ChatOpenAI with config:")
    for k, v in config.items():
        if k == "api_key":
            print(f"  {k}: {'*' * 20}")
        else:
            print(f"  {k}: {v}")
    
    llm = ChatOpenAI(**config)
    print("✅ ChatOpenAI created successfully")
    
    # Try a simple call
    from langchain_core.messages import HumanMessage
    response = llm.invoke([HumanMessage(content="Say 'test ok' in 2 words")])
    print(f"✅ Response: {response.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print()

print("=" * 60)
print("TESTING CREWAI AGENT")
print("=" * 60)
try:
    from crewai import Agent
    from langchain_openai import ChatOpenAI
    
    # Create LLM
    config = {
        "model": "gpt-4o",
        "base_url": "https://models.inference.ai.azure.com",
        "api_key": os.getenv("GITHUB_TOKEN"),
        "temperature": 0.7,
    }
    
    llm = ChatOpenAI(**config)
    print("✅ ChatOpenAI created")
    
    # Create Agent
    agent = Agent(
        role="Test Agent",
        goal="Test if CrewAI works",
        backstory="A test agent",
        llm=llm,
        verbose=True
    )
    print("✅ Agent created successfully")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
