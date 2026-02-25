"""
Prompts for AI Compliance Gap Analyzer - send to AI for tasks
"""

# Workflow: 1-User Input -> 2-Plan Research * -> 3-Excecute Research -> 4-Analyze Findings * -> 5-Output Report


# Overal setting for behavior
SYSTEM_PROMPT = """
You are an AI compliance expert helping organizations identify regulatory gaps in their AI implementations.

Your role is to:
1. Identify relevant compliance frameworks (HIPAA, GDPR, EU AI Act, etc.)
2. Analyze technology vendor policies and practices
3. Identify gaps between requirements and current implementation
4. Provide actionable recommendations

You have access to web search tools to find current information about regulations and vendor policies.

Be specific, cite sources, and focus on actionable insights."""


# AI task 1 - Plan Research
SEARCH_PLANNING_PROMPT = """
Given this AI implementation scenario:

USE CASE: {use_case}
TECHNOLOGY: {technology}
INDUSTRY: {industry}

What 3-5 searches should I run to identify compliance requirements and vendor policies?

Format your response as a JSON array of search queries:
["query 1", "query 2", "query 3"]

Focus on:
- Relevant regulations for this industry
- The specific technology vendor's data policies
- Recent compliance guidance or enforcement actions"""



# AI task 2 - Analyze Findings
ANALYSIS_PROMPT = """
Based on the following information, analyze the compliance gaps:

USE CASE: {use_case}
TECHNOLOGY: {technology}
INDUSTRY: {industry}

RESEARCH FINDINGS: {research_findings}

Provide a structured analysis with:
1. Applicable Regulations (which laws/frameworks apply)
2. Identified Risks (what could go wrong)
3. Compliance Gaps (where current setup falls short)
4. Recommendations (specific actions to take)

Be specific and cite the research findings."""


