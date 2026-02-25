"""
Tools for AI Compliance Gap Analyzer
search + utility functions used by the agent

Agent Workflow:
1. User Input
2. Plan Research (Claude) → prompts.py
3. Execute Research (Tavily) → tools.py ← THIS FILE
4. Analyze Findings (Claude) → prompts.py
5. Output Report
"""


import os
from tavily import TavilyClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Tavily client once (reused for all searches)
# DESIGN DECISION: Created at file level for efficiency
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


#search_web() - Use Tavily to search the web for information
def search_web(query: str, max_results: int = 3) -> dict:
    """
    Search the web for compliance-related information.
    
    Args:
        query: Search query string (e.g., "HIPAA requirements for AI")
        max_results: Maximum number of results to return (default: 3)
        
    Returns:
        Dictionary with 'results' list, or 'error' key if search fails
    """
    
    try:
        print(f"\n🔍 Searching: {query}")

        response = tavily.search(
            query=query, 
            max_results=max_results,
            search_depth="advanced"
            )
        
        #extract & clean results
        results = []
        for result in response.get('results', []): #get results from response, default to empty list if no results
            results.append({ #append result to results list
                'title': result.get('title', ''),
                'url': result.get('url', ''),
                'content': result.get('content', '')[:500] #limit content to 500 characters
            })
        
        print(f"\n🔍 Found {len(results)} results")
        return {'results': results} #return results as dictionary with 'results' key

    except Exception as e:
        print(f"\n❌ Search failed: {str(e)}")
        return {'results': [], 'error': str(e)} #return both empty results and error message


def format_search_results(search_results: list) -> str:
    """
    Format search results into readable text for Claude.

    Args:
        search_results: List of search result dictionaries from search_web()

    Returns:
        Formatted string combing all results
    """

    # Guard clause: handle empty results early
    if not search_results or 'results' not in search_results:
        return "No search results found"

    formatted = []

    for i, result in enumerate(search_results['results'], 1):
        formatted.append(f"\n --- Result {i} ---")
        formatted.append(f"Title: {result.get('title', 'N/A')}")
        formatted.append(f"URL: {result.get('url', 'N/A')}")
        formatted.append(f"Content: {result.get('content', 'N/A')}")

    # Join all parts with newlines into one string
    return "\n".join(formatted)



