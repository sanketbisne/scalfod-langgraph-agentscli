"""Clean refusal wrapper for ADK-only commands in a LangChain/LangGraph project."""

import sys


def main() -> int:
    cmd = " ".join(sys.argv[1:3]) if len(sys.argv) >= 3 else "this command"
    sys.stderr.write(
        f"agents-cli {cmd} is not supported by the langchain extension:\n"
        "it runs the agent through ADK's user simulator / agent introspector, which needs google-adk\n"
        "in this project's venv.\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
