"""
AI Compliance Gap Analyzer - Main Agent
Orchestrates research and analysis workflow.
"""

# File setup

import os
import re
import json
from datetime import datetime
import anthropic
from dotenv import load_dotenv
from tools import search_web, format_search_results
from prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT, SEARCH_PLANNING_PROMPT

load_dotenv()

# Initialize Claude client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# Function 1: plan_searches() - Ask Claude what to search
def plan_searches(use_case: str, technology: str, industry: str) -> list:
    """
    Ask Claude to plan what searches to run.
    
    Returns:
        List of search query strings
    """
    print("\n📋 Planning research strategy...")
    
    prompt = SEARCH_PLANNING_PROMPT.format(
        use_case=use_case, 
        technology=technology, 
        industry=industry
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except anthropic.APIError as e:
        print(f"⚠️ Claude API error during search planning: {e}")
        return [
            f"{industry} AI regulations compliance",
            f"{technology} data retention policy",
            f"{technology} GDPR compliance"
        ]

    response_text = response.content[0].text

    try:
        start = response_text.find('[')
        end = response_text.rfind(']') + 1
        json_str = response_text[start:end]
        queries = json.loads(json_str)

        print(f"✅ Planned {len(queries)} searches")
        return queries
    except (json.JSONDecodeError, ValueError, IndexError):
        print("⚠️ Couldn't parse search plan, using defaults")
        return [
            f"{industry} AI regulations compliance",
            f"{technology} data retention policy",
            f"{technology} GDPR compliance"
        ]


# Function 2: conduct_research() - Execute searches  
def conduct_research(queries: list) -> str:
    """
    Execute searches and compile results.
    
    Args:
        queries: List of search query strings
        
    Returns:
        Formatted string of all research findings
    """
    print("\n🔬 Conducting research...")
    
    all_results = []
    
    for query in queries:
        # Search using our tools.py function
        search_response = search_web(query, max_results=3)
        results = search_response.get('results', [])
        
        if results:
            all_results.append(f"\n=== Search: {query} ===")
            all_results.append(format_search_results(results))
    
    return "\n".join(all_results)


# Function 3: analyze_compliance() - Ask Claude to analyze
def analyze_compliance(use_case: str, technology: str, industry: str, research_findings: str) -> str:
    """
    Analyze compliance gaps based on research.
    
    Args:
        use_case: What the AI system does
        technology: Technology being used
        industry: Industry context
        research_findings: Compiled research from conduct_research()
        
    Returns:
        Structured compliance analysis report
    """
    print("\n🧠 Analyzing compliance gaps...")

    prompt = ANALYSIS_PROMPT.format(
        use_case=use_case, 
        technology=technology, 
        industry=industry, 
        research_findings=research_findings
    )
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except anthropic.APIError as e:
        print(f"❌ Claude API error during analysis: {e}")
        return f"[Analysis failed: Claude API returned an error — {e}. Research data was collected successfully. Please retry.]"

    return response.content[0].text


# Function 4: save_report() - Persist results to a file
def save_report(result: dict, version: str = "v0.1", output_dir: str | None = None) -> str:
    """
    Save the analysis report to a timestamped file named after the use case.

    Args:
        result: Dictionary returned by run_analysis()
        version: Code version tag (e.g., "v0.1", "v0.2")
        output_dir: Directory to save in (defaults to this script's directory)

    Returns:
        Path to the saved report file
    """
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    reports_dir = os.path.join(output_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    slug = re.sub(r'[^a-z0-9]+', '-', result['use_case'].lower()).strip('-')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{version}_{slug}_{timestamp}.md"
    filepath = os.path.join(reports_dir, filename)

    header = (
        f"# Compliance Gap Analysis Report\n\n"
        f"**Version:** {version}  \n"
        f"**Use Case:** {result['use_case']}  \n"
        f"**Technology:** {result['technology']}  \n"
        f"**Industry:** {result['industry']}  \n"
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n\n"
        f"---\n\n"
        f"## Search Queries Used\n\n"
    )
    queries_section = "\n".join(f"- {q}" for q in result['search_queries']) + "\n\n"
    body = f"---\n\n## Analysis\n\n{result['analysis']}\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header + queries_section + body)

    print(f"\n💾 Report saved to: {filepath}")
    return filepath


# Function 5: run_analysis() - Orchestrate everything
def run_analysis(use_case: str, technology: str, industry: str, version: str = "v0.2") -> dict:
    """
    Main function to run complete compliance gap analysis.
    
    Args:
        use_case: What the AI system does
        technology: Technology being used  
        industry: Industry context
        version: Code version tag for report naming (e.g., "v0.1")
        
    Returns:
        Dictionary with all analysis results
    """
    inputs = {"use_case": use_case, "technology": technology, "industry": industry}
    for field, value in inputs.items():
        if not value or not value.strip():
            return {"error": f"Missing required field: {field}"}
        if len(value) > 500:
            return {"error": f"Field '{field}' exceeds 500 character limit ({len(value)} chars)"}

    print("\n" + "="*60)
    print("🚀 AI COMPLIANCE GAP ANALYZER")
    print("="*60)

    print(f"\nUse Case: {use_case}")
    print(f"Technology: {technology}")
    print(f"Industry: {industry}")

    # Step 1: Plan searches
    search_queries = plan_searches(use_case, technology, industry)

    # Step 2: Conduct research
    research_findings = conduct_research(search_queries)

    # Step 3: Analyze compliance
    analysis = analyze_compliance(use_case, technology, industry, research_findings)

    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE")
    print("="*60)
    
    result = {
        'use_case': use_case,
        'technology': technology,
        'industry': industry,
        'search_queries': search_queries,
        'analysis': analysis
    }

    save_report(result, version=version)
    return result


# Test code
if __name__ == "__main__":
    result = run_analysis(
        use_case="AI-powered resume screening tool",
        technology="OpenAI GPT-4 API",
        industry="Enterprise HR tech (US-based)"
    )
    
    print("\n" + "="*60)
    print("COMPLIANCE ANALYSIS REPORT")
    print("="*60)
    print(result['analysis'])