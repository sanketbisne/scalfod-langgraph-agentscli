"""Drop-in replacement for `agents-cli eval generate` driving the LangGraph CompiledStateGraph."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
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
    parser = argparse.ArgumentParser(description="Generate evaluation traces from a dataset.")
    parser.add_argument("--dataset", "-d", required=True, help="Path to input evaluation dataset JSON.")
    parser.add_argument("--output-dir", "-o", default="tests/eval/output", help="Output directory for generated traces.")
    args, _ = parser.parse_known_args()

    dataset_path = Path(args.dataset)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_data = json.loads(dataset_path.read_text(encoding="utf-8"))
    cases = raw_data if isinstance(raw_data, list) else raw_data.get("eval_cases", [])

    generated_cases = []
    for idx, case in enumerate(cases, start=1):
        prompt = case.get("prompt") or case.get("input") or ""
        print(f"[eval.generate] Running case {idx}/{len(cases)}: {prompt[:60]}...")
        result = root_agent.invoke({"messages": [("user", prompt)]})
        messages = result.get("messages", [])

        tool_trajectory = []
        for msg in messages:
            for tc in getattr(msg, "tool_calls", []) or []:
                tool_trajectory.append(
                    {
                        "tool_name": tc.get("name"),
                        "tool_input": tc.get("args", {}),
                    }
                )

        final_response = _extract_text(messages[-1].content) if messages else ""
        enriched = dict(case)
        enriched["response"] = final_response
        enriched["actual_tool_trajectory"] = tool_trajectory
        generated_cases.append(enriched)

    output_file = output_dir / dataset_path.name
    output_payload = (
        generated_cases
        if isinstance(raw_data, list)
        else {**raw_data, "eval_cases": generated_cases}
    )
    output_file.write_text(json.dumps(output_payload, indent=2), encoding="utf-8")
    print(f"[eval.generate] Wrote {len(generated_cases)} trace(s) to {output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
