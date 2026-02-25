import anthropic
from tavily import TavilyClient
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

print("Testing imports...")
print("✅ All packages imported successfully")

# Test Claude API
print("\nTesting Claude API...")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=100,
    messages=[{"role": "user", "content": "Say 'API works'"}]
)
print(f"✅ Claude says: {message.content[0].text}")

# Test Tavily
print("\nTesting Tavily API...")
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
results = tavily.search(query="test", max_results=1)
print(f"✅ Tavily returned {len(results.get('results', []))} result(s)")

print("\n🎉 All systems ready to go!")