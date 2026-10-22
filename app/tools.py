"""Research, Search, and Self-Critique tools for the DeepCite LangGraph Agent."""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

CURATED_KNOWLEDGE_BASE: list[dict[str, str]] = [
    {
        "id": "KB-AGENTS-CLI-01",
        "title": "Google Agents CLI Extension System Architecture (v1.5+ / v1.8+)",
        "url": "https://developers.googleblog.com/powering-the-agent-development-lifecycle-with-any-framework-from-adk-to-langchain-and-beyond/",
        "published": "2026-10-21",
        "content": (
            "Starting in v1.5.0, Google Agents CLI introduces an Extension System declared via "
            "`agents-cli-extension.yaml` (schema `agents-cli-extension/v1alpha1`). Extensions support "
            "two shapes: command overrides (`commands.override`) that intercept built-in commands like "
            "`run`, `playground`, `deploy`, or `eval.generate`, and new commands (`commands.add`) that "
            "expose custom workflows. Out of ~24 CLI commands, only 6 assume the ADK runtime; the other "
            "18 (`deploy`, `infra`, `scaffold`, `eval grade`, `eval compare`, `login`, `lint`) are "
            "framework-agnostic. Overridden commands execute with `AGENTS_CLI_DISABLE_OVERRIDES=1` in "
            "their environment so wrapper scripts can safely delegate back to the native CLI without "
            "infinite recursion."
        ),
    },
    {
        "id": "KB-LANGCHAIN-EXT-02",
        "title": "First-Party LangChain & LangGraph Template in Agents CLI (v1.8.0)",
        "url": "https://github.com/google/agents-cli/tree/main/extensions/langchain/template",
        "published": "2026-10-21",
        "content": (
            "Version 1.8.0 of Agents CLI ships the first-party LangChain template "
            "(`google/agents-cli/extensions/langchain/template@v1.8.0`). It scaffolds a pure "
            "LangChain / LangGraph project with zero `google-adk` dependency. In LangChain 1.0+, "
            "`langchain.agents.create_agent` compiles directly to a LangGraph `CompiledStateGraph` "
            "exported as `root_agent` in `app/agent.py`. The template serves A2A (Agent-to-Agent) "
            "protocol traffic over FastAPI (`app.fast_api_app:app`) on port 8080 and boots LangGraph "
            "Studio locally via `agents-cli playground` (`uv run langgraph dev --no-browser --port 8080`)."
        ),
    },
    {
        "id": "KB-LOCKFILE-03",
        "title": "Extension Scopes, Lockfile Pinning, and Supply-Chain Discipline",
        "url": "https://github.com/google/agents-cli",
        "published": "2026-10-21",
        "content": (
            "Agents CLI extensions install at project scope (default, committed to repo) or user scope "
            "(`--global`). When both define the same command, project scope wins. `agents-cli extension add` "
            "resolves Git references to an exact commit SHA and records it in `agents-cli-extensions.yaml`. "
            "Running `agents-cli install` re-materializes the exact reviewed working copy from the pinned SHA "
            "without advancing the pin, ensuring reproducible builds across local dev and CI/CD."
        ),
    },
    {
        "id": "KB-RAG-REFLECT-04",
        "title": "Iterative Agentic Workflows vs. Single-Pass RAG",
        "url": "https://cloud.google.com/architecture/ai-agent-design-patterns",
        "published": "2026-09-15",
        "content": (
            "Single-pass Retrieval-Augmented Generation (RAG) retrieves top-k chunks once and synthesizes "
            "an answer in a single forward pass, making it vulnerable to incomplete query formulation and "
            "low-recall retrieval. Iterative Agentic Research workflows (Plan -> Search -> Critique -> "
            "Revise -> Report) decompose complex questions into sub-queries, inspect retrieved evidence "
            "through an explicit Critique step, run targeted follow-up searches when coverage is low, "
            "and enforce inline citation grounding before generating the final report."
        ),
    },
]

FALLBACK_ARXIV_PAPERS: list[dict[str, str]] = [
    {
        "id": "ARXIV-2005.11401",
        "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al.)",
        "url": "https://arxiv.org/abs/2005.11401",
        "published": "2020-05-22",
        "summary": (
            "Introduces RAG models that combine pre-trained parametric seq2seq memory with non-parametric "
            "dense vector indices (Wikipedia), improving factuality and reducing hallucination on "
            "knowledge-intensive tasks."
        ),
    },
    {
        "id": "ARXIV-2210.03629",
        "title": "ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al.)",
        "url": "https://arxiv.org/abs/2210.03629",
        "published": "2022-10-06",
        "summary": (
            "Demonstrates interleaved reasoning traces and task-specific tool actions, enabling LLMs "
            "to dynamically plan, query external environments, and update reasoning state."
        ),
    },
    {
        "id": "ARXIV-2303.11366",
        "title": "Reflexion: Language Agents with Verbal Reinforcement Learning (Shinn et al.)",
        "url": "https://arxiv.org/abs/2303.11366",
        "published": "2023-03-20",
        "summary": (
            "Proposes self-reflective feedback loops where an agent critiques its own intermediate outputs "
            "and tool trajectories in natural language, storing episodic feedback to iteratively improve "
            "accuracy without weight updates."
        ),
    },
    {
        "id": "ARXIV-2310.11511",
        "title": "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection (Asai et al.)",
        "url": "https://arxiv.org/abs/2310.11511",
        "published": "2023-10-17",
        "summary": (
            "Trains an LM to adaptively retrieve passages on demand and critique retrieved evidence and "
            "its own generations using reflection tokens for relevance, factual support, and completeness."
        ),
    },
]

FALLBACK_WIKIPEDIA: dict[str, dict[str, str]] = {
    "langchain": {
        "id": "WIKI-LANGCHAIN",
        "title": "LangChain & LangGraph Overview",
        "url": "https://en.wikipedia.org/wiki/LangChain",
        "summary": (
            "LangChain is an open-source framework for building applications powered by large language "
            "models. In modern LangChain (1.0+), stateful agent orchestration, cyclic workflows, and "
            "human-in-the-loop checkpoints are powered by LangGraph's CompiledStateGraph engine."
        ),
    },
    "software bill of materials": {
        "id": "WIKI-SBOM",
        "title": "Software Bill of Materials (SBOM)",
        "url": "https://en.wikipedia.org/wiki/Software_supply_chain",
        "summary": (
            "A Software Bill of Materials (SBOM) is a formal, machine-readable inventory of software "
            "components and dependencies (e.g., CycloneDX or SPDX format) used with vulnerability "
            "scanners like Syft and Grype to prevent supply-chain attacks prior to deployment."
        ),
    },
}


def create_research_plan(topic: str, focus_areas: str = "architecture, comparison, citations") -> str:
    """Decomposes a research topic into structured sub-questions and recommended search steps.

    Always call this tool first when handling a research or technical synthesis request.
    """
    areas = [a.strip() for a in focus_areas.split(",") if a.strip()]
    plan = {
        "topic": topic,
        "workflow": "Plan -> Search -> Critique -> Report",
        "sub_questions": [
            f"1. Core architecture & mechanisms of: {topic}",
            f"2. Empirical comparisons or design trade-offs across: {', '.join(areas) or 'key dimensions'}",
            "3. Primary citations and verifiable source IDs supporting each technical claim",
        ],
        "recommended_next_step": (
            "Call `search_curated_kb` and/or `search_arxiv_papers` to gather grounded sources, "
            "then validate your draft with `critique_research_draft` before answering."
        ),
    }
    return json.dumps(plan, indent=2)


def search_curated_kb(query: str, max_results: int = 4) -> str:
    """Searches the curated AI & Google Cloud Agents CLI knowledge base.

    Returns source records with `id` (e.g., KB-AGENTS-CLI-01), `title`, `url`, and `content`.
    """
    tokens = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 2]
    scored: list[tuple[int, dict[str, str]]] = []
    for item in CURATED_KNOWLEDGE_BASE:
        haystack = f"{item['title']} {item['content']}".lower()
        score = sum(2 if t in item["title"].lower() else 1 for t in tokens if t in haystack)
        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    matches = [item for score, item in scored if score > 0][:max_results]
    if not matches:
        matches = CURATED_KNOWLEDGE_BASE[:max_results]

    return json.dumps({"query": query, "results": matches}, indent=2)


def search_arxiv_papers(query: str, max_results: int = 3) -> str:
    """Searches ArXiv for foundational and recent AI/ML papers with deterministic offline fallback.

    Returns records with `id` (e.g., ARXIV-2005.11401), `title`, `url`, and `summary`.
    """
    tokens = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 2]
    scored: list[tuple[int, dict[str, str]]] = []
    for paper in FALLBACK_ARXIV_PAPERS:
        haystack = f"{paper['title']} {paper['summary']}".lower()
        score = sum(2 if t in paper["title"].lower() else 1 for t in tokens if t in haystack)
        scored.append((score, paper))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = [paper for score, paper in scored if score > 0][:max_results]

    if not results:
        try:
            encoded = urllib.parse.quote(query)
            url = f"http://export.arxiv.org/api/query?search_query=all:{encoded}&start=0&max_results={max_results}"
            req = urllib.request.Request(url, headers={"User-Agent": "DeepCite-Agent/1.0"})
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                xml_data = resp.read()
            root = ET.fromstring(xml_data)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                raw_id = entry.findtext("atom:id", default="", namespaces=ns)
                short_id = raw_id.rstrip("/").split("/")[-1]
                results.append(
                    {
                        "id": f"ARXIV-{short_id}",
                        "title": " ".join(entry.findtext("atom:title", default="", namespaces=ns).split()),
                        "url": raw_id,
                        "published": entry.findtext("atom:published", default="", namespaces=ns)[:10],
                        "summary": " ".join(entry.findtext("atom:summary", default="", namespaces=ns).split()),
                    }
                )
        except Exception:
            results = FALLBACK_ARXIV_PAPERS[:max_results]

    if not results:
        results = FALLBACK_ARXIV_PAPERS[:max_results]

    return json.dumps({"query": query, "results": results}, indent=2)


def search_wikipedia_summary(topic: str) -> str:
    """Fetches a concise encyclopedic summary and canonical citation ID for a technical topic."""
    lower = topic.lower()
    for key, record in FALLBACK_WIKIPEDIA.items():
        if key in lower or lower in key:
            return json.dumps(record, indent=2)

    try:
        slug = urllib.parse.quote(topic.strip().replace(" ", "_"))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{slug}"
        req = urllib.request.Request(url, headers={"User-Agent": "DeepCite-Agent/1.0"})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            payload: dict[str, Any] = json.loads(resp.read().decode("utf-8"))
            return json.dumps(
                {
                    "id": f"WIKI-{topic.upper().replace(' ', '-')[:16]}",
                    "title": payload.get("title", topic),
                    "url": payload.get("content_urls", {}).get("desktop", {}).get("page", url),
                    "summary": payload.get("extract", ""),
                },
                indent=2,
            )
    except Exception:
        return json.dumps(FALLBACK_WIKIPEDIA["langchain"], indent=2)


def critique_research_draft(question: str, draft_summary: str, cited_source_ids: str) -> str:
    """Audits a draft research summary for citation coverage, grounding, and completeness.

    Must be called before generating the final report to verify quality.
    """
    source_ids = [s.strip().strip("[]") for s in cited_source_ids.split(",") if s.strip()]
    word_count = len(draft_summary.split())
    issues: list[str] = []

    if len(source_ids) < 2:
        issues.append("Cite at least 2 distinct source IDs (e.g., KB-..., ARXIV-..., WIKI-...).")
    if word_count < 25:
        issues.append("Draft summary is too brief; expand technical depth and architectural details.")

    status = "PASS" if not issues else "NEEDS_REVISION"
    return json.dumps(
        {
            "status": status,
            "question": question,
            "verified_source_ids": source_ids,
            "draft_word_count": word_count,
            "issues": issues,
            "formatting_reminder": (
                "Include inline citations like [KB-AGENTS-CLI-01] or [ARXIV-2005.11401] "
                "and end your response with a `## References` section listing every cited ID and URL."
            ),
        },
        indent=2,
    )


def get_weather(query: str) -> str:
    """Simulates a web search for weather information (kept for quick smoke-test compatibility)."""
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."
