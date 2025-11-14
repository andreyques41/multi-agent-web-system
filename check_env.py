import os
from dotenv import load_dotenv

load_dotenv()

# Set up for GitHub Models
github_token = os.getenv("GITHUB_TOKEN")
if github_token:
    os.environ["OPENAI_API_KEY"] = github_token
    os.environ["OPENAI_API_BASE"] = "https://models.inference.ai.azure.com"

print("Variables de entorno:")
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'NOT SET')[:20]}...")
print(f"OPENAI_API_BASE: {os.getenv('OPENAI_API_BASE', 'NOT SET')}")
print(f"GITHUB_TOKEN: {os.getenv('GITHUB_TOKEN', 'NOT SET')[:20]}...")
