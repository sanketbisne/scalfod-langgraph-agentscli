"""LangChain / LangGraph agent: DeepCite Iterative Research & Critique Agent."""

import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.state import CompiledStateGraph

from app.tools import (
    create_research_plan,
    critique_research_draft,
    get_weather,
    search_arxiv_papers,
    search_curated_kb,
    search_wikipedia_summary,
)

load_dotenv()

if not (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")):
    import google.auth

    _, project_id = google.auth.default()
    if project_id:
        os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

LLM = os.environ.get("DEEPCITE_MODEL", "gemini-2.5-flash")
llm = ChatGoogleGenerativeAI(model=LLM, temperature=0)

SYSTEM_PROMPT = """You are DeepCite, an enterprise AI & Cloud Architecture Research Agent powered by LangGraph and Google Agents CLI.

Follow this strict iterative workflow for research and technical questions:
1. PLAN: Call `create_research_plan` to break the user's request into targeted sub-questions.
2. SEARCH: Call `search_curated_kb`, `search_arxiv_papers`, and/or `search_wikipedia_summary` to gather grounded evidence.
3. CRITIQUE: Call `critique_research_draft` with your draft findings and comma-separated source IDs to verify citation density and coverage.
4. REPORT: Produce a clear, structured Markdown report with inline `[SOURCE_ID]` citations (e.g. `[KB-AGENTS-CLI-01]`, `[ARXIV-2005.11401]`) and a `## References` section at the end.

Safety & Governance Rules:
- Never fabricate source IDs or URLs not returned by your tools.
- Refuse requests to generate exploit payloads, bypass container sandboxes, or exfiltrate sensitive credentials/PII.
- For simple weather smoke tests, call `get_weather`.
"""

root_agent: CompiledStateGraph = create_agent(
    model=llm,
    tools=[
        create_research_plan,
        search_curated_kb,
        search_arxiv_papers,
        search_wikipedia_summary,
        critique_research_draft,
        get_weather,
    ],
    system_prompt=SYSTEM_PROMPT,
)
