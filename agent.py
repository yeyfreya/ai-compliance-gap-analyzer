"""
AI Compliance Gap Analyzer - Main Agent
Orchestrates research and analysis workflow.
"""

import os
import re
import json
import time
import csv
from datetime import datetime
import anthropic
from dotenv import load_dotenv
from langfuse import observe, get_client as get_langfuse_client
from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor

from tools import search_web, format_search_results
from prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT, SEARCH_PLANNING_PROMPT

load_dotenv()

# Initialize Langfuse (reads LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST from env)
langfuse = get_langfuse_client()
AnthropicInstrumentor().instrument()

# Initialize Claude client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# Function 1: plan_searches() - Ask Claude what to search
@observe()
def plan_searches(use_case: str, technology: str, industry: str) -> dict:
    """
    Ask Claude to plan what searches to run, with extended thinking enabled.

    Returns:
        dict with keys: queries (list[str]), thinking (str), tokens_in (int), tokens_out (int)
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
            max_tokens=5000,
            thinking={"type": "enabled", "budget_tokens": 3000},
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except anthropic.APIError as e:
        print(f"⚠️ Claude API error during search planning: {e}")
        return {
            "queries": [
                f"{industry} AI regulations compliance",
                f"{technology} data retention policy",
                f"{technology} GDPR compliance"
            ],
            "thinking": None,
            "tokens_in": 0,
            "tokens_out": 0,
        }

    thinking_text = ""
    response_text = ""
    for block in response.content:
        if block.type == "thinking":
            thinking_text = block.thinking
        elif block.type == "text":
            response_text = block.text

    tokens_in = response.usage.input_tokens
    tokens_out = response.usage.output_tokens

    try:
        start = response_text.find('[')
        end = response_text.rfind(']') + 1
        json_str = response_text[start:end]
        queries = json.loads(json_str)

        print(f"✅ Planned {len(queries)} searches")
        return {
            "queries": queries,
            "thinking": thinking_text,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
        }
    except (json.JSONDecodeError, ValueError, IndexError):
        print("⚠️ Couldn't parse search plan, using defaults")
        return {
            "queries": [
                f"{industry} AI regulations compliance",
                f"{technology} data retention policy",
                f"{technology} GDPR compliance"
            ],
            "thinking": thinking_text,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
        }


# Function 2: conduct_research() - Execute searches
@observe()
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
@observe()
def analyze_compliance(use_case: str, technology: str, industry: str, research_findings: str) -> dict:
    """
    Analyze compliance gaps based on research, with extended thinking enabled.

    Returns:
        dict with keys: analysis (str), thinking (str), tokens_in (int), tokens_out (int)
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
            max_tokens=16000,
            thinking={"type": "enabled", "budget_tokens": 8000},
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except anthropic.APIError as e:
        print(f"❌ Claude API error during analysis: {e}")
        return {
            "analysis": f"[Analysis failed: Claude API returned an error — {e}. Research data was collected successfully. Please retry.]",
            "thinking": None,
            "tokens_in": 0,
            "tokens_out": 0,
        }

    thinking_text = ""
    analysis_text = ""
    for block in response.content:
        if block.type == "thinking":
            thinking_text = block.thinking
        elif block.type == "text":
            analysis_text = block.text

    return {
        "analysis": analysis_text,
        "thinking": thinking_text,
        "tokens_in": response.usage.input_tokens,
        "tokens_out": response.usage.output_tokens,
    }


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

    timing = result.get('timing', {})
    timing_line = ""
    if timing:
        timing_line = (
            f"**Generation Time:** {timing['total_sec']}s total "
            f"(planning: {timing['planning_sec']}s, "
            f"research: {timing['research_sec']}s, "
            f"analysis: {timing['analysis_sec']}s)  \n"
        )

    header = (
        f"# Compliance Gap Analysis Report\n\n"
        f"**Version:** {version}  \n"
        f"**Use Case:** {result['use_case']}  \n"
        f"**Technology:** {result['technology']}  \n"
        f"**Industry:** {result['industry']}  \n"
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n"
        f"{timing_line}\n"
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
@observe()
def run_analysis(use_case: str, technology: str, industry: str, version: str = "v0.4") -> dict:
    """
    Main function to run complete compliance gap analysis.

    Returns dict with: use_case, technology, industry, search_queries, analysis,
    timing, planning_thinking, analysis_thinking, token_usage.
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

    total_start = time.time()

    # Step 1: Plan searches (returns dict with queries, thinking, tokens)
    t0 = time.time()
    plan_result = plan_searches(use_case, technology, industry)
    search_queries = plan_result["queries"]
    time_planning = time.time() - t0

    # Step 2: Conduct research
    t0 = time.time()
    research_findings = conduct_research(search_queries)
    time_research = time.time() - t0

    # Step 3: Analyze compliance (returns dict with analysis, thinking, tokens)
    t0 = time.time()
    analysis_result = analyze_compliance(use_case, technology, industry, research_findings)
    analysis = analysis_result["analysis"]
    time_analysis = time.time() - t0

    time_total = time.time() - total_start

    timing = {
        'planning_sec': round(time_planning, 1),
        'research_sec': round(time_research, 1),
        'analysis_sec': round(time_analysis, 1),
        'total_sec': round(time_total, 1),
    }

    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE")
    print(f"⏱️  Total: {timing['total_sec']}s "
          f"(plan: {timing['planning_sec']}s, "
          f"research: {timing['research_sec']}s, "
          f"analysis: {timing['analysis_sec']}s)")
    print("="*60)

    result = {
        'use_case': use_case,
        'technology': technology,
        'industry': industry,
        'search_queries': search_queries,
        'analysis': analysis,
        'timing': timing,
        'planning_thinking': plan_result.get("thinking"),
        'analysis_thinking': analysis_result.get("thinking"),
        'token_usage': {
            'planning': {'input': plan_result.get("tokens_in", 0), 'output': plan_result.get("tokens_out", 0)},
            'analysis': {'input': analysis_result.get("tokens_in", 0), 'output': analysis_result.get("tokens_out", 0)},
        },
    }

    report_path = save_report(result, version=version)
    append_test_log(result, version=version, report_path=report_path)
    return result


# Function 6: append_test_log() - Track performance across runs
def append_test_log(result: dict, version: str, report_path: str) -> None:
    """Append one row to reports/test-log.csv after every successful run."""
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "test-log.csv")

    timing = result.get('timing', {})
    row = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'version': version,
        'use_case': result['use_case'],
        'technology': result['technology'],
        'industry': result['industry'],
        'num_queries': len(result.get('search_queries', [])),
        'planning_sec': timing.get('planning_sec', ''),
        'research_sec': timing.get('research_sec', ''),
        'analysis_sec': timing.get('analysis_sec', ''),
        'total_sec': timing.get('total_sec', ''),
        'report_file': os.path.basename(report_path),
    }

    file_exists = os.path.exists(log_path)
    with open(log_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(f"📊 Test log updated: {log_path}")


# Test scenarios
TEST_SCENARIOS = {
    "hr": {
        "use_case": "AI-powered resume screening tool",
        "technology": "OpenAI GPT-4 API",
        "industry": "Enterprise HR tech (US-based)",
    },
    "healthcare": {
        "use_case": "AI diagnostic assistant that analyzes medical images and suggests diagnoses",
        "technology": "Google Gemini API",
        "industry": "US hospital network (healthcare)",
    },
    "fintech": {
        "use_case": "AI credit scoring model that evaluates loan applications",
        "technology": "AWS SageMaker",
        "industry": "UK neobank (financial services)",
    },
    "education": {
        "use_case": "AI essay grading and feedback tool for student assignments",
        "technology": "Anthropic Claude API",
        "industry": "US K-12 school district (education)",
    },
    "regtech": {
        "use_case": "AI agent powered compliance gap analyzer",
        "technology": "Anthropic Claude Sonnet 4.5",
        "industry": "RegTech / AI compliance SaaS — serving early-stage AI startups",
    },
}

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2 or sys.argv[1] not in TEST_SCENARIOS:
        print("Usage: python agent.py <scenario>")
        print("\nAvailable scenarios:")
        for key, s in TEST_SCENARIOS.items():
            print(f"  {key:12s} -- {s['use_case']}")
        sys.exit(1)

    scenario = TEST_SCENARIOS[sys.argv[1]]
    result = run_analysis(**scenario)

    if "error" in result:
        print(f"\n❌ {result['error']}")
    else:
        print("\n" + "="*60)
        print("COMPLIANCE ANALYSIS REPORT")
        print("="*60)
        print(result['analysis'])