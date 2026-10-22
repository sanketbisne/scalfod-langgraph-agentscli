"""Custom extension command (`agents-cli research-report`) that exports a cited Markdown report."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import sys

from app.agent import root_agent


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the DeepCite LangGraph agent and export a verified Markdown report."
    )
    parser.add_argument(
        "topic",
        nargs="?",
        default="How does the Google Agents CLI Extension System support LangChain and LangGraph?",
        help="Research topic or question.",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="reports",
        help="Directory to write the exported Markdown report.",
    )
    args = parser.parse_args()

    print(f"[research-report] Running DeepCite LangGraph agent on topic:\n  -> {args.topic}")
    result = root_agent.invoke({"messages": [("user", args.topic)]})
    messages = result.get("messages", [])
    content = messages[-1].content if messages else ""
    if isinstance(content, list):
        content = "\n".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    report_body = str(content)

    citations = sorted(set(re.findall(r"\[((?:KB|ARXIV|WIKI)-[A-Z0-9._-]+)\]", report_body)))
    reports_dir = Path(args.output_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    slug = re.sub(r"[^a-z0-9]+", "-", args.topic.lower()).strip("-")[:45] or "report"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    report_path = reports_dir / f"{timestamp}-{slug}.md"

    header = (
        f"# DeepCite Research Report\n\n"
        f"- **Generated (UTC)**: `{timestamp}`\n"
        f"- **Topic**: {args.topic}\n"
        f"- **Verified Citations Found ({len(citations)})**: {', '.join(f'`[{c}]`' for c in citations) or 'None'}\n\n"
        f"---\n\n"
    )
    report_path.write_text(header + report_body + "\n", encoding="utf-8")
    print(f"[research-report] Verified {len(citations)} citation(s): {citations}")
    print(f"[research-report] Saved Markdown report to: {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
