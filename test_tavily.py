from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

response = tavily.search(query="HIPAA compliance requirements", max_results=3)

print(response)

