"""Zero-dependency OpenXML (.pptx) generator for Google Slides import.

Generates `docs/Cloud_Next_27_Agents_CLI_LangGraph.pptx` (16:9 widescreen) with:
- Google Sans Display, Google Sans, Google Sans Text, and Google Sans Mono typography
- Google Cloud Next '27 dark stage (#0E1015) and light stage (#FFFFFF) slides
- 4-color Google top bar, rounded Bento Grid tiles, and dark terminal code cards
- Built-in smooth fade transitions (<p:transition>) recognized by Google Slides
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape
import zipfile

PT = 12700  # 1 point = 12,700 EMUs
SLIDE_W = 960 * PT  # 12,192,000 EMUs (16:9 widescreen, matches 960x540 pt canvas)
SLIDE_H = 540 * PT  # 6,858,000 EMUs


def _hex(color: str) -> str:
    return color.lstrip("#").upper()


class SlideBuilder:
    def __init__(self, bg_hex: str) -> None:
        self.bg_hex = _hex(bg_hex)
        self.shapes: list[str] = []
        self._id = 2

    def _next_id(self) -> int:
        val = self._id
        self._id += 1
        return val

    def add_rect(
        self,
        x_pt: float,
        y_pt: float,
        w_pt: float,
        h_pt: float,
        fill_hex: str,
        border_hex: str | None = None,
        rounded: bool = False,
    ) -> None:
        sid = self._next_id()
        x, y, w, h = int(x_pt * PT), int(y_pt * PT), int(w_pt * PT), int(h_pt * PT)
        geom = "roundRect" if rounded else "rect"
        av = '<a:avLst><a:gd name="adj" fmla="val 6000"/></a:avLst>' if rounded else "<a:avLst/>"
        ln_xml = (
            f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{_hex(border_hex)}"/></a:solidFill></a:ln>'
            if border_hex
            else "<a:ln><a:noFill/></a:ln>"
        )
        self.shapes.append(
            f"""<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{sid}" name="Shape {sid}"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
    <a:prstGeom prst="{geom}">{av}</a:prstGeom>
    <a:solidFill><a:srgbClr val="{_hex(fill_hex)}"/></a:solidFill>
    {ln_xml}
  </p:spPr>
</p:sp>"""
        )

    def add_textbox(
        self,
        x_pt: float,
        y_pt: float,
        w_pt: float,
        h_pt: float,
        paragraphs: list[tuple[str, str, int, str, bool]],
        fill_hex: str | None = None,
        border_hex: str | None = None,
        rounded: bool = False,
        pad_pt: float = 8.0,
    ) -> None:
        """paragraphs: list of (text, font_family, size_pt, color_hex, bold)."""
        sid = self._next_id()
        x, y, w, h = int(x_pt * PT), int(y_pt * PT), int(w_pt * PT), int(h_pt * PT)
        geom = "roundRect" if rounded else "rect"
        av = '<a:avLst><a:gd name="adj" fmla="val 5000"/></a:avLst>' if rounded else "<a:avLst/>"
        fill_xml = (
            f'<a:solidFill><a:srgbClr val="{_hex(fill_hex)}"/></a:solidFill>'
            if fill_hex
            else "<a:noFill/>"
        )
        ln_xml = (
            f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{_hex(border_hex)}"/></a:solidFill></a:ln>'
            if border_hex
            else "<a:ln><a:noFill/></a:ln>"
        )
        pad = int(pad_pt * PT)

        p_xml_list: list[str] = []
        for text, font, size_pt, color_hex, is_bold in paragraphs:
            lines = text.split("\n")
            for line in lines:
                sz = int(size_pt * 100)
                b_attr = ' b="1"' if is_bold else ' b="0"'
                escaped = escape(line)
                p_xml_list.append(
                    f"""<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPct val="120000"/></a:lnSpc></a:pPr>
  <a:r>
    <a:rPr lang="en-US" sz="{sz}"{b_attr} dirty="0">
      <a:solidFill><a:srgbClr val="{_hex(color_hex)}"/></a:solidFill>
      <a:latin typeface="{escape(font)}"/>
      <a:cs typeface="{escape(font)}"/>
    </a:rPr>
    <a:t>{escaped}</a:t>
  </a:r>
</a:p>"""
                )

        body_p = "\n".join(p_xml_list)
        self.shapes.append(
            f"""<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{sid}" name="TextBox {sid}"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
    <a:prstGeom prst="{geom}">{av}</a:prstGeom>
    {fill_xml}
    {ln_xml}
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" lIns="{pad}" tIns="{pad}" rIns="{pad}" bIns="{pad}" anchor="t"/>
    <a:lstStyle/>
    {body_p}
  </p:txBody>
</p:sp>"""
        )

    def add_four_color_bar(self) -> None:
        colors = ["4285F4", "EA4335", "FBBC04", "34A853"]
        for i, c in enumerate(colors):
            self.add_rect(i * 240, 0, 240, 6, c)

    def add_header(
        self,
        is_dark: bool,
        eyebrow: str,
        eyebrow_color: str,
        title: str,
        subtitle: str,
        slide_num: str,
    ) -> None:
        self.add_four_color_bar()
        self.add_textbox(
            48, 22, 600, 24,
            [(eyebrow.upper(), "Google Sans", 10, eyebrow_color, True)],
            pad_pt=2,
        )
        self.add_textbox(
            840, 22, 72, 24,
            [(slide_num, "Google Sans Mono", 10, "9AA0A6" if is_dark else "5F6368", False)],
            pad_pt=2,
        )
        self.add_textbox(
            48, 46, 864, 48,
            [(title, "Google Sans Display", 28, "FFFFFF" if is_dark else "202124", True)],
            pad_pt=2,
        )
        self.add_textbox(
            48, 92, 864, 34,
            [(subtitle, "Google Sans Text", 13, "BDC1C6" if is_dark else "5F6368", False)],
            pad_pt=2,
        )

    def add_bento_card(
        self,
        x_pt: float,
        y_pt: float,
        w_pt: float,
        h_pt: float,
        bg_hex: str,
        border_hex: str,
        kicker: str,
        kicker_color: str,
        heading: str,
        heading_color: str,
        body: str,
        body_color: str,
    ) -> None:
        self.add_textbox(
            x_pt,
            y_pt,
            w_pt,
            h_pt,
            [
                (kicker, "Google Sans Mono", 9, kicker_color, True),
                (heading, "Google Sans Display", 17, heading_color, True),
                ("", "Google Sans Text", 6, body_color, False),
                (body, "Google Sans Text", 11, body_color, False),
            ],
            fill_hex=bg_hex,
            border_hex=border_hex,
            rounded=True,
            pad_pt=14,
        )

    def add_code_card(
        self,
        x_pt: float,
        y_pt: float,
        w_pt: float,
        h_pt: float,
        title: str,
        title_color: str,
        code_text: str,
    ) -> None:
        self.add_textbox(
            x_pt,
            y_pt,
            w_pt,
            h_pt,
            [
                (title, "Google Sans", 10, title_color, True),
                ("", "Google Sans Mono", 4, "E8EAED", False),
                (code_text, "Google Sans Mono", 10, "E8EAED", False),
            ],
            fill_hex="131314",
            border_hex="3C4043",
            rounded=True,
            pad_pt=14,
        )

    def to_xml(self) -> str:
        shapes_xml = "\n".join(self.shapes)
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg>
      <p:bgPr>
        <a:solidFill><a:srgbClr val="{self.bg_hex}"/></a:solidFill>
        <a:effectLst/>
      </p:bgPr>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
      {shapes_xml}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
  <p:transition spd="med"><p:fade/></p:transition>
</p:sld>"""


def build_slides() -> list[SlideBuilder]:
    slides: list[SlideBuilder] = []

    # SLIDE 1: Hero Opening (Dark Stage)
    s1 = SlideBuilder("0E1015")
    s1.add_four_color_bar()
    s1.add_textbox(
        56, 56, 700, 28,
        [("GOOGLE CLOUD NEXT '27  |  DEVELOPER SESSION  |  AGENTS CLI v1.8+", "Google Sans Mono", 11, "8AB4F8", True)],
    )
    s1.add_textbox(
        56, 115, 848, 145,
        [
            ("Every agent framework.", "Google Sans Display", 46, "FFFFFF", True),
            ("One production lifecycle.", "Google Sans Display", 46, "8AB4F8", True),
        ],
    )
    s1.add_textbox(
        56, 275, 820, 75,
        [
            (
                "Running LangChain, LangGraph, and custom enterprise governance policies natively on Google Cloud with the Agents CLI Extension System.",
                "Google Sans Text",
                17,
                "BDC1C6",
                False,
            )
        ],
    )
    s1.add_textbox(
        56, 455, 848, 38,
        [("Live Repo: github.com/sanketbisne/scalfod-langgraph-agentscli", "Google Sans Mono", 12, "81C995", True)],
        fill_hex="161922",
        border_hex="2D3343",
        rounded=True,
        pad_pt=10,
    )
    slides.append(s1)

    # SLIDE 2: Big Numbers Impact Slide (Dark Stage)
    s2 = SlideBuilder("0E1015")
    s2.add_header(
        True,
        "By The Numbers",
        "8AB4F8",
        "Decoupling the lifecycle from the runtime.",
        "Out of 24 CLI commands, 18 are framework-agnostic and only 6 touch the agent runtime.",
        "02 / 10",
    )
    s2.add_bento_card(
        48, 145, 276, 330, "161922", "2D3343",
        "PRODUCTION LIFECYCLE", "8AB4F8",
        "18+ Native Commands", "FFFFFF",
        "deploy, eval grade, eval compare, infra, scaffold, lint, and login work unchanged across ADK, LangChain, and LangGraph.",
        "9AA0A6",
    )
    s2.add_bento_card(
        342, 145, 276, 330, "161922", "2D3343",
        "RUNTIME INTERCEPTION", "81C995",
        "6 Overridden Commands", "FFFFFF",
        "run, playground, eval.generate, and publish hot-swap via a single agents-cli-extension.yaml manifest.",
        "9AA0A6",
    )
    s2.add_bento_card(
        636, 145, 276, 330, "161922", "2D3343",
        "PURE LANGGRAPH", "FDD663",
        "0% ADK Lock-In", "FFFFFF",
        "Zero google-adk dependency required in pyproject.toml. Pure LangChain and LangGraph code in production.",
        "9AA0A6",
    )
    slides.append(s2)

    # SLIDE 3: The Framework Lock-In Problem (Light Stage)
    s3 = SlideBuilder("FFFFFF")
    s3.add_header(
        False,
        "The Framework Lock-In Problem",
        "1A73E8",
        "Ending the tradeoff between velocity and choice.",
        "Teams want Google Cloud deployment, Vertex AI evaluation, and A2A serving without rewriting LangGraph agents.",
        "03 / 10",
    )
    s3.add_bento_card(
        48, 145, 276, 330, "F8F9FA", "DADCE0",
        "LEGACY PATH 1", "C5221F",
        "Forking the CLI", "202124",
        "Maintain a divergent internal copy and manually rebase on every upstream release.\n\nResult: Permanent maintenance tax.",
        "5F6368",
    )
    s3.add_bento_card(
        342, 145, 276, 330, "F8F9FA", "DADCE0",
        "LEGACY PATH 2", "B06000",
        "Custom Wrapper Scripts", "202124",
        "Build parallel shell scripts around the CLI. Developers and coding agents call native CLI directly.\n\nResult: Bypassed governance gates.",
        "5F6368",
    )
    s3.add_bento_card(
        636, 145, 276, 330, "E8F0FE", "1A73E8",
        "CLOUD NEXT '27 STANDARD", "1A73E8",
        "Agents CLI Extensions", "202124",
        "Declarative agents-cli-extension.yaml overrides commands in-place, pinned by exact Git commit SHA.\n\nResult: Zero fork + 100% enforcement.",
        "202124",
    )
    slides.append(s3)

    # SLIDE 4: Inside the Command Surface (6 vs. 18 Split)
    s4 = SlideBuilder("FFFFFF")
    s4.add_header(
        False,
        "Command Surface Architecture",
        "137333",
        "Inside the Agents CLI Command Surface (6 vs. 18 Split)",
        "A single agents-cli-extension.yaml swaps only the 6 runtime commands and keeps the 18 production commands intact.",
        "04 / 10",
    )
    s4.add_bento_card(
        48, 145, 420, 330, "F8FAFF", "4285F4",
        "[↑ LANGCHAIN] OVERRIDES", "1967D2",
        "6 Framework-Coupled Commands", "202124",
        "- run -> uv run python scripts/run.py\n"
        "- playground -> uv run langgraph dev --port 8080\n"
        "- eval.generate -> uv run python scripts/eval_generate.py\n"
        "- publish.gemini-enterprise -> scripts/publish.py\n"
        "- eval.dataset / eval.optimize -> Clean refusal wrapper",
        "3C4043",
    )
    s4.add_bento_card(
        492, 145, 420, 330, "F6FEF8", "34A853",
        "NATIVE BUILT-IN COMMANDS", "137333",
        "18+ Framework-Agnostic Commands", "202124",
        "- deploy (Cloud Run / GKE via FastAPI A2A)\n"
        "- eval grade / eval compare / eval analyze (Vertex AI)\n"
        "- infra (Terraform modules)\n"
        "- scaffold create / enhance / upgrade\n"
        "- extension add / list / update / remove\n"
        "- install / info / lint / login",
        "3C4043",
    )
    slides.append(s4)

    # SLIDE 5: Act 1 - Scaffolding a Pure LangChain / LangGraph Project
    s5 = SlideBuilder("0E1015")
    s5.add_header(
        True,
        "Live Demo | Act 1",
        "8AB4F8",
        "Scaffold a pure LangGraph project in one command.",
        "Scaffolding and extension installation happen together with zero google-adk dependency.",
        "05 / 10",
    )
    s5.add_code_card(
        48, 145, 864, 330,
        "TERMINAL  |  SCAFFOLD & VERIFY ZERO ADK LOCK-IN",
        "8AB4F8",
        "# 1. Scaffold directly from the first-party LangChain extension template\n"
        "$ agents-cli create scalfod-langgraph-agentscli \\\n"
        "    --agent google/agents-cli/extensions/langchain/template@v1.8.0 \\\n"
        "    -d cloud_run\n\n"
        "$ cd scalfod-langgraph-agentscli && agents-cli install\n"
        "Agents CLI v1.8.0 | Fetching remote template: google/agents-cli/extensions/langchain/template@v1.8.0\n"
        "> Connected to project: your-project | Your agent project is ready.\n\n"
        "# 2. Verify zero google-adk dependency in pyproject.toml and app/\n"
        "$ grep -r \"google.adk\\|google-adk\" pyproject.toml app/ ; echo \"exit: $?\"\n"
        "exit: 1   # Verified: Zero google-adk dependency!",
    )
    slides.append(s5)

    # SLIDE 6: Project Structure & LangGraph State Graph
    s6 = SlideBuilder("FFFFFF")
    s6.add_header(
        False,
        "Codebase Architecture",
        "B06000",
        "Project Structure & LangGraph CompiledStateGraph",
        "In LangChain 1.0+, create_agent compiles directly into a LangGraph CompiledStateGraph.",
        "06 / 10",
    )
    s6.add_code_card(
        48, 145, 420, 330,
        "PROJECT STRUCTURE",
        "FDD663",
        "scalfod-langgraph-agentscli/\n"
        "├── agents-cli-extension.yaml  # Project overrides\n"
        "├── agents-cli-manifest.yaml   # Target: cloud_run\n"
        "├── langgraph.json             # LangGraph Studio\n"
        "├── pyproject.toml             # Zero google-adk\n"
        "├── Dockerfile                 # FastAPI A2A :8080\n"
        "├── app/\n"
        "│   ├── agent.py               # CompiledStateGraph\n"
        "│   ├── tools.py               # DeepCite tools\n"
        "│   ├── fast_api_app.py        # FastAPI A2A server\n"
        "│   └── app_utils/a2a.py       # /.well-known/agent.json\n"
        "└── extensions/sbom-deploy/    # Custom SBOM gate",
    )
    s6.add_code_card(
        492, 145, 420, 330,
        "app/agent.py",
        "81C995",
        "from langchain.agents import create_agent\n"
        "from langchain_google_genai import ChatGoogleGenerativeAI\n"
        "from langgraph.graph.state import CompiledStateGraph\n\n"
        "llm = ChatGoogleGenerativeAI(\n"
        "    model=\"gemini-2.5-flash\", temperature=0\n"
        ")\n\n"
        "root_agent: CompiledStateGraph = create_agent(\n"
        "    model=llm,\n"
        "    tools=[\n"
        "        create_research_plan,\n"
        "        search_curated_kb,\n"
        "        search_arxiv_papers,\n"
        "        critique_research_draft,\n"
        "    ],\n"
        "    system_prompt=SYSTEM_PROMPT,\n"
        ")",
    )
    slides.append(s6)

    # SLIDE 7: DeepCite Agent Architecture (Plan -> Search -> Critique -> Report)
    s7 = SlideBuilder("FFFFFF")
    s7.add_header(
        False,
        "Reference Workload",
        "1A73E8",
        "DeepCite Architecture (Plan -> Search -> Critique -> Report)",
        "Iterative self-reflection loop that enforces multi-source retrieval and citation verification.",
        "07 / 10",
    )
    s7.add_bento_card(
        48, 145, 204, 330, "F8F9FA", "4285F4",
        "01 | PLAN", "1A73E8",
        "create_research_plan", "202124",
        "Decomposes complex prompts into 3 targeted sub-questions and recommends search queries.",
        "5F6368",
    )
    s7.add_bento_card(
        268, 145, 204, 330, "F8F9FA", "FBBC04",
        "02 | SEARCH", "B06000",
        "search_curated_kb / arxiv", "202124",
        "Retrieves grounded evidence with explicit IDs ([KB-...], [ARXIV-...], [WIKI-...]) and offline fallbacks.",
        "5F6368",
    )
    s7.add_bento_card(
        488, 145, 204, 330, "F8F9FA", "EA4335",
        "03 | CRITIQUE", "C5221F",
        "critique_research_draft", "202124",
        "Audits draft claims for >= 2 distinct citations and depth; triggers revision if incomplete.",
        "5F6368",
    )
    s7.add_bento_card(
        708, 145, 204, 330, "F8F9FA", "34A853",
        "04 | REPORT", "137333",
        "Cited Markdown Output", "202124",
        "Synthesizes final Markdown brief with inline [SOURCE_ID] tags and a verified ## References section.",
        "5F6368",
    )
    slides.append(s7)

    # SLIDE 8: Running Locally & Visual Debugging + Evaluations (Dark Stage)
    s8 = SlideBuilder("0E1015")
    s8.add_header(
        True,
        "Live Demo | Act 2 & Act 3",
        "81C995",
        "LangGraph Studio & Vertex AI Evaluations",
        "Boot LangGraph Studio via agents-cli playground and grade traces with Vertex AI Eval Service.",
        "08 / 10",
    )
    s8.add_code_card(
        48, 145, 420, 330,
        "1. RUN & INSPECT IN LANGGRAPH STUDIO",
        "8AB4F8",
        "$ agents-cli --help | grep -E \"playground|run \"\n"
        "  playground  Start LangGraph server. [↑ langchain]\n"
        "  run         Run compiled graph.     [↑ langchain]\n\n"
        "$ agents-cli info\n"
        "$ agents-cli run \"How do extensions work?\"\n"
        "WARNING:root:agents-cli: applying 6 extension command(s)\n\n"
        "$ agents-cli playground\n"
        "> Boots LangGraph Studio on http://localhost:8080",
    )
    s8.add_code_card(
        492, 145, 420, 330,
        "2. OVERRIDDEN GENERATE + NATIVE GRADE",
        "81C995",
        "# Overridden: Drives LangGraph CompiledStateGraph\n"
        "$ agents-cli eval generate \\\n"
        "    --dataset tests/eval/datasets/basic-dataset.json \\\n"
        "    -o tests/eval/output/\n\n"
        "# Native: Scores traces via Vertex AI Eval Service\n"
        "$ agents-cli eval grade \\\n"
        "    --traces tests/eval/output/basic-dataset.json \\\n"
        "    --config tests/eval/eval_config.yaml\n\n"
        "# Clean refusal on ADK-only simulator:\n"
        "$ agents-cli eval dataset synthesize",
    )
    slides.append(s8)

    # SLIDE 9: Custom Enterprise Governance Extension (Dark Stage)
    s9 = SlideBuilder("0E1015")
    s9.add_header(
        True,
        "Live Demo | Act 4",
        "F28B82",
        "Authoring Custom Enterprise Extensions (sbom-deploy)",
        "AGENTS_CLI_DISABLE_OVERRIDES=1 lets wrapper scripts run Syft + Grype checks and call native deploy without recursion.",
        "09 / 10",
    )
    s9.add_code_card(
        48, 145, 420, 330,
        "extensions/sbom-deploy/agents-cli-extension.yaml",
        "FDD663",
        "schema: agents-cli-extension/v1alpha1\n"
        "name: sbom-deploy\n"
        "description: Scan project SBOM, then run native deploy.\n"
        "requires:\n"
        "  agents_cli: \">=1.5,<2\"\n"
        "  on_incompatible: warn\n\n"
        "commands:\n"
        "  override:\n"
        "    deploy:\n"
        "      run: [\"bash\", \"scripts/sbom_then_deploy.sh\"]\n"
        "  add:\n"
        "    sbom-report:\n"
        "      run: [\"bash\", \"scripts/sbom_report.sh\"]",
    )
    s9.add_code_card(
        492, 145, 420, 330,
        "extensions/sbom-deploy/scripts/sbom_then_deploy.sh",
        "81C995",
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n\n"
        "echo \"[sbom-deploy] Generating CycloneDX SBOM...\"\n"
        "syft dir:. -o cyclonedx-json > /tmp/sbom.cdx.json\n\n"
        "echo \"[sbom-deploy] Scanning for critical CVEs...\"\n"
        "grype sbom:/tmp/sbom.cdx.json --fail-on critical\n\n"
        "# Loader sets AGENTS_CLI_DISABLE_OVERRIDES=1\n"
        "# Delegates to built-in deploy with zero recursion!\n"
        "exec agents-cli deploy \"$@\"",
    )
    slides.append(s9)

    # SLIDE 10: Closing Bento Grid Summary (Dark Stage)
    s10 = SlideBuilder("0E1015")
    s10.add_header(
        True,
        "Google Cloud Next '27 Summary",
        "8AB4F8",
        "The Open Agent Development Lifecycle",
        "Clone & Run Live: github.com/sanketbisne/scalfod-langgraph-agentscli",
        "10 / 10",
    )
    s10.add_bento_card(
        48, 140, 276, 155, "161922", "2D3343",
        "01 | OPEN FRAMEWORKS", "8AB4F8",
        "LangChain & LangGraph", "FFFFFF",
        "First-party template with zero google-adk dependency and unified CompiledStateGraph.",
        "9AA0A6",
    )
    s10.add_bento_card(
        342, 140, 276, 155, "161922", "2D3343",
        "02 | VISUAL DEBUGGING", "81C995",
        "LangGraph Studio", "FFFFFF",
        "agents-cli playground launches LangGraph server on port 8080.",
        "9AA0A6",
    )
    s10.add_bento_card(
        636, 140, 276, 155, "161922", "2D3343",
        "03 | QUALITY FLYWHEEL", "FDD663",
        "Vertex AI Evaluations", "FFFFFF",
        "Overridden eval generate pairs with native Vertex AI eval grade.",
        "9AA0A6",
    )
    s10.add_bento_card(
        48, 315, 276, 155, "161922", "2D3343",
        "04 | POLICY AS CODE", "F28B82",
        "SBOM Pre-Deploy Gates", "FFFFFF",
        "Syft + Grype checks with AGENTS_CLI_DISABLE_OVERRIDES=1.",
        "9AA0A6",
    )
    s10.add_bento_card(
        342, 315, 276, 155, "161922", "2D3343",
        "05 | SUPPLY CHAIN", "8AB4F8",
        "SHA Lockfile Pinning", "FFFFFF",
        "Bit-for-bit reproducible CI via agents-cli-extensions.yaml.",
        "9AA0A6",
    )
    s10.add_bento_card(
        636, 315, 276, 155, "161922", "2D3343",
        "06 | PRODUCTION SERVING", "81C995",
        "Cloud Run + A2A", "FFFFFF",
        "Standard FastAPI + A2A container contract on port 8080.",
        "9AA0A6",
    )
    slides.append(s10)

    return slides


def write_pptx(output_path: Path) -> None:
    slides = build_slides()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    slide_ct_overrides = "\n".join(
        f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, len(slides) + 1)
    )
    content_types_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
{slide_ct_overrides}
</Types>"""

    root_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""

    sld_id_entries = "\n".join(
        f'    <p:sldId id="{255 + i}" r:id="rId{i + 2}"/>'
        for i in range(1, len(slides) + 1)
    )
    presentation_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>
  <p:sldIdLst>
{sld_id_entries}
  </p:sldIdLst>
  <p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="screen16x9"/>
  <p:notesSz cx="{SLIDE_H}" cy="{SLIDE_W}"/>
</p:presentation>"""

    pres_rels_entries = "\n".join(
        f'  <Relationship Id="rId{i + 2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, len(slides) + 1)
    )
    pres_rels_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>
{pres_rels_entries}
</Relationships>"""

    slide_master_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg>
      <p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst>
    <p:sldLayoutId id="2147483649" r:id="rId1"/>
  </p:sldLayoutIdLst>
</p:sldMaster>"""

    slide_master_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>"""

    slide_layout_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
             type="blank" preserve="1">
  <p:cSld name="Blank">
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>"""

    slide_layout_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>"""

    slide_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>"""

    theme_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="GoogleCloudNext27">
  <a:themeElements>
    <a:clrScheme name="GoogleCloud">
      <a:dk1><a:srgbClr val="202124"/></a:dk1>
      <a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="0E1015"/></a:dk2>
      <a:lt2><a:srgbClr val="F8F9FA"/></a:lt2>
      <a:accent1><a:srgbClr val="4285F4"/></a:accent1>
      <a:accent2><a:srgbClr val="EA4335"/></a:accent2>
      <a:accent3><a:srgbClr val="FBBC04"/></a:accent3>
      <a:accent4><a:srgbClr val="34A853"/></a:accent4>
      <a:accent5><a:srgbClr val="8AB4F8"/></a:accent5>
      <a:accent6><a:srgbClr val="81C995"/></a:accent6>
      <a:hlink><a:srgbClr val="4285F4"/></a:hlink>
      <a:folHlink><a:srgbClr val="9B72CB"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="GoogleSansScheme">
      <a:majorFont>
        <a:latin typeface="Google Sans Display"/>
        <a:ea typeface=""/>
        <a:cs typeface=""/>
      </a:majorFont>
      <a:minorFont>
        <a:latin typeface="Google Sans Text"/>
        <a:ea typeface=""/>
        <a:cs typeface=""/>
      </a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="GoogleFormat">
      <a:fillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      </a:fillStyleLst>
      <a:lnStyleLst>
        <a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
        <a:ln w="25400"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
        <a:ln w="38100"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
      </a:lnStyleLst>
      <a:effectStyleLst>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle><a:effectLst/></a:effectStyle>
      </a:effectStyleLst>
      <a:bgFillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      </a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>"""

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("_rels/.rels", root_rels_xml)
        zf.writestr("ppt/presentation.xml", presentation_xml)
        zf.writestr("ppt/_rels/presentation.xml.rels", pres_rels_xml)
        zf.writestr("ppt/slideMasters/slideMaster1.xml", slide_master_xml)
        zf.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", slide_master_rels_xml)
        zf.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout_xml)
        zf.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", slide_layout_rels_xml)
        zf.writestr("ppt/theme/theme1.xml", theme_xml)

        for idx, slide in enumerate(slides, start=1):
            zf.writestr(f"ppt/slides/slide{idx}.xml", slide.to_xml())
            zf.writestr(f"ppt/slides/_rels/slide{idx}.xml.rels", slide_rels_xml)

    print(f"Generated {len(slides)}-slide PPTX at: {output_path} ({output_path.stat().st_size} bytes)")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "docs" / "Cloud_Next_27_Agents_CLI_LangGraph.pptx"
    write_pptx(out)
