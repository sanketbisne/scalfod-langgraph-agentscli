"""FastAPI application exposing the LangGraph CompiledStateGraph over HTTP and A2A routes."""

from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import root_agent
from app.app_utils.a2a import register_a2a_routes
from app.app_utils.telemetry import setup_telemetry

setup_telemetry()

app = FastAPI(
    title="DeepCite LangGraph Agent (Agents CLI)",
    description="LangChain / LangGraph CompiledStateGraph served via FastAPI + A2A protocol.",
    version="0.1.0",
)

register_a2a_routes(app, root_agent)


class InvokeRequest(BaseModel):
    prompt: str


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "framework": "langchain-langgraph"}


@app.post("/invoke")
async def invoke_agent(req: InvokeRequest) -> dict[str, str]:
    result = root_agent.invoke({"messages": [("user", req.prompt)]})
    messages = result.get("messages", [])
    final_text = messages[-1].content if messages else ""
    if isinstance(final_text, list):
        final_text = "\n".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in final_text
        )
    return {"response": str(final_text)}
