"""Agent-to-Agent (A2A) protocol routes for LangGraph CompiledStateGraph."""

from typing import Any
from fastapi import FastAPI
from langgraph.graph.state import CompiledStateGraph


def register_a2a_routes(app: FastAPI, graph: CompiledStateGraph) -> None:
    """Registers the /.well-known/agent.json card and A2A task execution endpoint."""

    @app.get("/.well-known/agent.json")
    async def agent_card() -> dict[str, Any]:
        return {
            "name": "deepcite-langgraph-agent",
            "description": "Iterative Research & Critique Agent built with LangChain/LangGraph and Google Agents CLI",
            "version": "0.1.0",
            "protocol": "a2a/v1",
            "capabilities": {
                "streaming": False,
                "pushNotifications": False,
            },
            "skills": [
                {
                    "id": "deepcite-research",
                    "name": "Iterative Technical Research & Citation Verification",
                    "description": "Plans, searches, critiques, and synthesizes cited technical reports.",
                }
            ],
        }

    @app.post("/a2a/tasks/send")
    async def a2a_send_task(payload: dict[str, Any]) -> dict[str, Any]:
        task_id = payload.get("id", "task-1")
        message = payload.get("message", {})
        parts = message.get("parts", [])
        prompt = " ".join(p.get("text", "") for p in parts if isinstance(p, dict)).strip()
        if not prompt:
            prompt = str(payload.get("prompt", "Hello"))

        result = graph.invoke({"messages": [("user", prompt)]})
        messages = result.get("messages", [])
        final_text = messages[-1].content if messages else ""
        if isinstance(final_text, list):
            final_text = "\n".join(
                b.get("text", "") if isinstance(b, dict) else str(b) for b in final_text
            )

        return {
            "id": task_id,
            "status": {"state": "completed"},
            "artifacts": [
                {
                    "name": "research-response",
                    "parts": [{"type": "text", "text": str(final_text)}],
                }
            ],
        }
