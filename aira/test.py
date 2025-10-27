from langsmith import Client
from dotenv import load_dotenv
import os

# Load .env file to get LANGCHAIN_API_KEY
load_dotenv()
print(f"LangSmith API Key loaded: {os.getenv('LANGCHAIN_API_KEY')[:4]}...")  # Debug: First 4 chars

# Initialize LangSmith client
client = Client()

# Fetch the latest run from your project
try:
    recent_runs = client.list_runs(project_name="crm-agent-hack", limit=1)
    for run in recent_runs:
        print("Run attributes:", dir(run))
        print("Run dictionary:", run.__dict__)
        break
except Exception as e:
    print("Test error:", str(e))