"""Agent-Runtime-aware publish wrapper for LangChain projects."""

import os
from pathlib import Path
import subprocess
import sys
import yaml


def main() -> int:
    manifest_path = Path("agents-cli-manifest.yaml")
    if manifest_path.exists():
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        if manifest.get("deployment_target") == "agent_runtime":
            sys.stderr.write(
                "publish gemini-enterprise on agent_runtime requires ADK registration mode.\n"
                "Use deployment_target: cloud_run or gke to publish via A2A mode.\n"
            )
            return 2

    env = dict(os.environ)
    env["AGENTS_CLI_DISABLE_OVERRIDES"] = "1"
    return subprocess.call(["agents-cli", "publish", "gemini-enterprise", *sys.argv[1:]], env=env)


if __name__ == "__main__":
    sys.exit(main())
