"""Drop-in replacement for `agents-cli run` driving the LangGraph CompiledStateGraph."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from app.agent import root_agent


def _extract_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    return str(content)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the compiled LangGraph agent with a single prompt.")
    parser.add_argument("prompt", nargs="?", default="What's the weather in San Francisco?", help="Prompt to send to the agent.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print intermediate tool calls and JSON events.")
    args, _ = parser.parse_known_args()

    result = root_agent.invoke({"messages": [("user", args.prompt)]})
    messages = result.get("messages", [])

    if args.verbose:
        for msg in messages:
            msg_type = getattr(msg, "type", "unknown")
            tool_calls = getattr(msg, "tool_calls", None)
            if tool_calls:
                print(json.dumps({"type": msg_type, "tool_calls": tool_calls}, indent=2))

    if messages:
        print(_extract_text(messages[-1].content))
    return 0


if __name__ == "__main__":
    sys.exit(main())
