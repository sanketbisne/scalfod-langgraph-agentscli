/**
 * 1-Click Native Google Slides Deck Generator
 * Title: "Powering the Agent Development Lifecycle with LangChain, LangGraph, and Google Agents CLI"
 *
 * HOW TO USE IN GOOGLE SLIDES / GOOGLE DRIVE:
 * 1. Open https://script.google.com and click "New Project" (or inside Google Slides: Extensions -> Apps Script).
 * 2. Paste this entire file into `Code.gs`.
 * 3. Select `createAgentsCliPresentation` and click "Run".
 * 4. Check the Execution Log for the direct URL to your newly generated 10-slide Google Slides deck!
 */

function createAgentsCliPresentation() {
  var deck = SlidesApp.create(
    "Powering the Agent Development Lifecycle with LangChain, LangGraph, and Google Agents CLI"
  );

  // Strict Design System Constants
  var FONT_HEADING = "Plus Jakarta Sans";
  var FONT_BODY = "Roboto";
  var FONT_CODE = "Roboto Mono";

  var COLOR_WHITE = "#FFFFFF";
  var COLOR_GRAY_BG = "#F8F9FA";
  var COLOR_DARK_BG = "#202124";
  var COLOR_DARK_CARD = "#171717";
  var COLOR_BLUE = "#4285F4";
  var COLOR_GREEN = "#34A853";
  var COLOR_YELLOW = "#FBBC04";
  var COLOR_RED = "#EA4335";
  var COLOR_TEXT_PRIMARY = "#202124";
  var COLOR_TEXT_MUTED = "#5F6368";
  var COLOR_TEXT_LIGHT = "#E8EAED";

  // Remove default initial blank slide after adding custom slides
  var initialSlide = deck.getSlides()[0];

  function addHeader(slide, tagText, tagColor, titleText, subtitleText, isDark) {
    slide.getBackground().setSolidFill(isDark ? COLOR_DARK_BG : COLOR_WHITE);

    // Top Accent Bar
    var bar = slide.insertShape(SlidesApp.ShapeType.RECTANGLE, 0, 0, 720, 6);
    bar.getFill().setSolidFill(tagColor);
    bar.getBorder().setTransparent();

    // Tag Pill
    var tag = slide.insertTextBox(tagText.toUpperCase(), 40, 24, 380, 22);
    tag.getText().getTextStyle()
      .setFontFamily(FONT_HEADING)
      .setFontSize(10)
      .setBold(true)
      .setForegroundColor(tagColor);

    // Title
    var title = slide.insertTextBox(titleText, 40, 44, 640, 48);
    title.getText().getTextStyle()
      .setFontFamily(FONT_HEADING)
      .setFontSize(22)
      .setBold(true)
      .setForegroundColor(isDark ? COLOR_WHITE : COLOR_TEXT_PRIMARY);

    // Subtitle
    if (subtitleText) {
      var sub = slide.insertTextBox(subtitleText, 40, 88, 640, 36);
      sub.getText().getTextStyle()
        .setFontFamily(FONT_BODY)
        .setFontSize(12)
        .setForegroundColor(isDark ? "#BDC1C6" : COLOR_TEXT_MUTED);
    }
  }

  function addCodeCard(slide, x, y, w, h, codeText) {
    var box = slide.insertShape(SlidesApp.ShapeType.ROUND_RECTANGLE, x, y, w, h);
    box.getFill().setSolidFill(COLOR_DARK_CARD);
    box.getBorder().setWeight(1).getLineFill().setSolidFill("#3C4043");
    var text = box.getText();
    text.setText(codeText);
    text.getTextStyle()
      .setFontFamily(FONT_CODE)
      .setFontSize(10)
      .setForegroundColor(COLOR_TEXT_LIGHT);
    return box;
  }

  function addInfoCard(slide, x, y, w, h, bgHex, borderHex, headingText, headingColor, bodyText) {
    var card = slide.insertShape(SlidesApp.ShapeType.ROUND_RECTANGLE, x, y, w, h);
    card.getFill().setSolidFill(bgHex);
    card.getBorder().setWeight(1.5).getLineFill().setSolidFill(borderHex);

    var tb = slide.insertTextBox(headingText + "\n\n" + bodyText, x + 12, y + 10, w - 24, h - 20);
    var fullText = tb.getText();
    fullText.getTextStyle()
      .setFontFamily(FONT_BODY)
      .setFontSize(11)
      .setForegroundColor(COLOR_TEXT_PRIMARY);

    fullText.getRange(0, headingText.length).getTextStyle()
      .setFontFamily(FONT_HEADING)
      .setFontSize(12)
      .setBold(true)
      .setForegroundColor(headingColor);
  }

  // =========================================================================
  // SLIDE 1: Title Slide
  // =========================================================================
  var s1 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  s1.getBackground().setSolidFill(COLOR_GRAY_BG);
  var topBar = s1.insertShape(SlidesApp.ShapeType.RECTANGLE, 0, 0, 720, 8);
  topBar.getFill().setSolidFill(COLOR_BLUE);
  topBar.getBorder().setTransparent();

  var s1Badge = s1.insertTextBox("GOOGLE CLOUD DEVELOPER SESSION  |  AGENTS CLI v1.8+", 48, 60, 500, 26);
  s1Badge.getText().getTextStyle()
    .setFontFamily(FONT_CODE)
    .setFontSize(11)
    .setBold(true)
    .setForegroundColor(COLOR_BLUE);

  var s1Title = s1.insertTextBox(
    "Powering the Agent Development Lifecycle with Any Framework",
    48, 95, 624, 110
  );
  s1Title.getText().getTextStyle()
    .setFontFamily(FONT_HEADING)
    .setFontSize(32)
    .setBold(true)
    .setForegroundColor(COLOR_TEXT_PRIMARY);

  var s1Sub = s1.insertTextBox(
    "Running LangChain, LangGraph, and Custom Governance Policies on Google Cloud with Agents CLI (v1.8+)",
    48, 210, 624, 60
  );
  s1Sub.getText().getTextStyle()
    .setFontFamily(FONT_BODY)
    .setFontSize(16)
    .setForegroundColor(COLOR_TEXT_MUTED);

  var s1Footer = s1.insertTextBox(
    "Live Repo: github.com/sanketbisne/scalfod-langgraph-agentscli",
    48, 340, 624, 34
  );
  s1Footer.getText().getTextStyle()
    .setFontFamily(FONT_CODE)
    .setFontSize(12)
    .setBold(true)
    .setForegroundColor(COLOR_BLUE);

  // =========================================================================
  // SLIDE 2: The Framework Lock-In Problem
  // =========================================================================
  var s2 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  addHeader(
    s2,
    "Slide 02 / Architecture Motivation",
    COLOR_BLUE,
    "The Framework Lock-In Problem",
    "Teams want Google Cloud deployment, Vertex AI evaluation, and A2A serving without being forced to rewrite LangChain or LangGraph agents in ADK.",
    false
  );
  addInfoCard(
    s2, 40, 135, 205, 220, "#FFF8F7", COLOR_RED,
    "1. Forking the CLI", COLOR_RED,
    "- High maintenance overhead\n- Breaks on every upstream release\n- Requires hand-merging upstream improvements\n- Diverges across internal teams"
  );
  addInfoCard(
    s2, 257, 135, 205, 220, "#FEF9E7", "#B06000",
    "2. Custom Wrapper Scripts", "#B06000",
    "- Parallel script command surface\n- Developers & coding assistants forget wrapper scripts and invoke the native CLI directly\n- Bypasses security checks"
  );
  addInfoCard(
    s2, 474, 135, 205, 220, "#E8F0FE", COLOR_BLUE,
    "3. Agents CLI Extensions", COLOR_BLUE,
    "- Declarative agents-cli-extension.yaml\n- Zero google-adk lock-in\n- Intercepts commands in-place\n- Pinned to exact Git commit SHAs"
  );

  // =========================================================================
  // SLIDE 3: Inside the Agents CLI Command Surface (6 vs. 18 Split)
  // =========================================================================
  var s3 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  addHeader(
    s3,
    "Slide 03 / Command Architecture",
    COLOR_GREEN,
    "Inside the Agents CLI Command Surface (6 vs. 18 Split)",
    "A single agents-cli-extension.yaml swaps only the 6 runtime commands and keeps the 18 production commands intact.",
    false
  );
  addInfoCard(
    s3, 40, 135, 310, 230, "#F8FAFF", COLOR_BLUE,
    "6 Framework-Coupled Commands [Overridden]", COLOR_BLUE,
    "Replaced by the LangChain extension:\n- run -> scripts/run.py (LangGraph invoke)\n- playground -> langgraph dev --port 8080\n- eval.generate -> scripts/eval_generate.py\n- publish.gemini-enterprise -> scripts/publish.py\n- eval.dataset / eval.optimize -> Clean refusal"
  );
  addInfoCard(
    s3, 370, 135, 310, 230, "#F6FEF8", COLOR_GREEN,
    "18+ Framework-Agnostic Commands [Native]", COLOR_GREEN,
    "Unchanged across ADK, LangChain, and LangGraph:\n- deploy (Cloud Run / GKE via FastAPI A2A)\n- eval grade / compare / analyze (Vertex AI)\n- infra (Terraform modules)\n- scaffold create / enhance / upgrade\n- extension add / list / update / remove\n- install / info / lint / login"
  );

  // =========================================================================
  // SLIDE 4: Act 1 - Scaffolding a Pure LangChain / LangGraph Project
  // =========================================================================
  var s4 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  addHeader(
    s4,
    "Slide 04 / Act 1: Scaffolding",
    COLOR_BLUE,
    "Act 1: Scaffolding a Pure LangChain / LangGraph Project",
    "Scaffolding and extension installation happen in a single command with zero google-adk dependency.",
    true
  );
  addCodeCard(
    s4, 40, 135, 640, 220,
    "# 1. Scaffold from the first-party LangChain extension template\n" +
    "$ agents-cli create scalfod-langgraph-agentscli \\\n" +
    "    --agent google/agents-cli/extensions/langchain/template@v1.8.0 \\\n" +
    "    -d cloud_run\n\n" +
    "$ cd scalfod-langgraph-agentscli && agents-cli install\n\n" +
    "# 2. Verify zero google-adk dependency in pyproject.toml and app/\n" +
    "$ grep -r \"google.adk\\|google-adk\" pyproject.toml app/\n" +
    "$ echo \"exit: $?\"\n" +
    "exit: 1   # Verified: Zero google-adk dependency!"
  );

  // =========================================================================
  // SLIDE 5: Project Structure & LangGraph State Graph
  // =========================================================================
  var s5 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  addHeader(
    s5,
    "Slide 05 / Codebase Structure",
    COLOR_YELLOW,
    "Project Structure & LangGraph State Graph",
    "In LangChain 1.0+, create_agent compiles directly into a LangGraph CompiledStateGraph.",
    false
  );
  addCodeCard(
    s5, 40, 135, 310, 230,
    "scalfod-langgraph-agentscli/\n" +
    "├── agents-cli-extension.yaml\n" +
    "├── agents-cli-manifest.yaml\n" +
    "├── langgraph.json\n" +
    "├── pyproject.toml\n" +
    "├── Dockerfile\n" +
    "├── app/\n" +
    "│   ├── agent.py       # CompiledStateGraph\n" +
    "│   ├── tools.py       # DeepCite tools\n" +
    "│   ├── fast_api_app.py\n" +
    "│   └── app_utils/a2a.py\n" +
    "├── scripts/\n" +
    "└── extensions/sbom-deploy/"
  );
  addCodeCard(
    s5, 370, 135, 310, 230,
    "# app/agent.py\n" +
    "from langchain.agents import create_agent\n" +
    "from langchain_google_genai import ChatGoogleGenerativeAI\n" +
    "from langgraph.graph.state import CompiledStateGraph\n\n" +
    "llm = ChatGoogleGenerativeAI(\n" +
    "    model=\"gemini-2.5-flash\", temperature=0\n" +
    ")\n\n" +
    "root_agent: CompiledStateGraph = create_agent(\n" +
    "    model=llm,\n" +
    "    tools=[\n" +
    "        create_research_plan,\n" +
    "        search_curated_kb,\n" +
    "        search_arxiv_papers,\n" +
    "        critique_research_draft,\n" +
    "    ],\n" +
    "    system_prompt=SYSTEM_PROMPT,\n" +
    ")"
  );

  // =========================================================================
  // SLIDE 6: DeepCite Agent Architecture (Plan -> Search -> Critique -> Report)
  // =========================================================================
  var s6 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  addHeader(
    s6,
    "Slide 06 / Agent Architecture",
    COLOR_BLUE,
    "DeepCite Agent Architecture (Plan -> Search -> Critique -> Report)",
    "Iterative ReAct + Self-Critique loop with grounded citations and deterministic CI fallbacks.",
    false
  );
  addInfoCard(
    s6, 40, 135, 152, 220, COLOR_GRAY_BG, COLOR_BLUE,
    "1. PLAN", COLOR_BLUE,
    "create_research_plan\n\nDecomposes user query into targeted sub-questions and search steps."
  );
  addInfoCard(
    s6, 202, 135, 152, 220, COLOR_GRAY_BG, "#B06000",
    "2. SEARCH", "#B06000",
    "search_curated_kb\nsearch_arxiv_papers\nsearch_wikipedia\n\nReturns passages with [KB-...] and [ARXIV-...] IDs."
  );
  addInfoCard(
    s6, 364, 135, 152, 220, COLOR_GRAY_BG, COLOR_RED,
    "3. CRITIQUE", COLOR_RED,
    "critique_research_draft\n\nVerifies >= 2 source IDs and sufficient technical depth before synthesis."
  );
  addInfoCard(
    s6, 526, 135, 154, 220, COLOR_GRAY_BG, COLOR_GREEN,
    "4. REPORT", COLOR_GREEN,
    "Markdown Synthesis\n\nProduces structured report with inline [SOURCE_ID] tags and ## References."
  );

  // =========================================================================
  // SLIDE 7: Running Locally & Visual Debugging in LangGraph Studio
  // =========================================================================
  var s7 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  addHeader(
    s7,
    "Slide 07 / Local Execution & Studio",
    COLOR_GREEN,
    "Running Locally & Visual Debugging in LangGraph Studio",
    "The [↑ langchain] suffix signals active command overrides and boots LangGraph Studio on port 8080.",
    true
  );
  addCodeCard(
    s7, 40, 135, 640, 225,
    "$ agents-cli --help | grep -E \"playground|run|research-report\"\n" +
    "  playground       Start the local LangGraph dev server.  [↑ langchain]\n" +
    "  run              Run the compiled agent graph with a single prompt.  [↑ langchain]\n" +
    "  research-report  Run DeepCite and export Markdown report.  [↑ langchain]\n\n" +
    "$ agents-cli info\n" +
    "  playground (override, project) <- langchain: uv run langgraph dev --no-browser --port 8080\n" +
    "  run        (override, project) <- langchain: uv run python scripts/run.py\n\n" +
    "$ agents-cli run \"How does the Google Agents CLI Extension System work?\"\n" +
    "$ agents-cli playground   # Launches LangGraph Studio on http://localhost:8080"
  );

  // =========================================================================
  // SLIDE 8: Framework-Agnostic Evaluations (eval generate + eval grade)
  // =========================================================================
  var s8 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  addHeader(
    s8,
    "Slide 08 / Evaluation Lifecycle",
    COLOR_BLUE,
    "Framework-Agnostic Evaluations (eval generate + eval grade)",
    "Trace generation drives the LangGraph graph; grading uses the native Vertex AI Evaluation Service.",
    false
  );
  addCodeCard(
    s8, 40, 135, 640, 225,
    "# Step 1 (Overridden by LangChain extension): Generate EvaluationDataset traces\n" +
    "$ agents-cli eval generate \\\n" +
    "    --dataset tests/eval/datasets/basic-dataset.json \\\n" +
    "    -o tests/eval/output/\n\n" +
    "# Step 2 (Native Vertex AI Evaluation Service): Grade traces against rubrics\n" +
    "$ agents-cli eval grade \\\n" +
    "    --traces tests/eval/output/basic-dataset.json \\\n" +
    "    --config tests/eval/eval_config.yaml\n\n" +
    "# Clean Refusal for ADK-only simulator subcommands:\n" +
    "$ agents-cli eval dataset synthesize\n" +
    "agents-cli eval dataset is not supported by the langchain extension:\n" +
    "it runs the agent through ADK's user simulator, which needs google-adk."
  );

  // =========================================================================
  // SLIDE 9: Authoring Custom Enterprise Extensions (sbom-deploy & research-report)
  // =========================================================================
  var s9 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  addHeader(
    s9,
    "Slide 09 / Custom Enterprise Extensions",
    COLOR_RED,
    "Authoring Custom Enterprise Extensions (sbom-deploy & research-report)",
    "AGENTS_CLI_DISABLE_OVERRIDES=1 lets wrapper scripts run pre-deploy checks and call native deploy without recursion.",
    true
  );
  addCodeCard(
    s9, 40, 135, 310, 225,
    "# agents-cli-extension.yaml\n" +
    "schema: agents-cli-extension/v1alpha1\n" +
    "name: sbom-deploy\n" +
    "requires:\n" +
    "  agents_cli: \">=1.5,<2\"\n" +
    "  on_incompatible: warn\n\n" +
    "commands:\n" +
    "  override:\n" +
    "    deploy:\n" +
    "      run: [\"bash\", \"scripts/sbom_then_deploy.sh\"]\n" +
    "  add:\n" +
    "    sbom-report:\n" +
    "      run: [\"bash\", \"scripts/sbom_report.sh\"]"
  );
  addCodeCard(
    s9, 370, 135, 310, 225,
    "#!/usr/bin/env bash\n" +
    "# scripts/sbom_then_deploy.sh\n" +
    "set -euo pipefail\n\n" +
    "syft dir:. -o cyclonedx-json > /tmp/sbom.cdx.json\n" +
    "grype sbom:/tmp/sbom.cdx.json --fail-on critical\n\n" +
    "# AGENTS_CLI_DISABLE_OVERRIDES=1 is set by loader\n" +
    "# Hits built-in deploy with zero recursion!\n" +
    "exec agents-cli deploy \"$@\""
  );

  // =========================================================================
  // SLIDE 10: Supply-Chain Pinning & Live Demo Wrap-Up
  // =========================================================================
  var s10 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  addHeader(
    s10,
    "Slide 10 / Supply-Chain Discipline & Wrap-Up",
    COLOR_GREEN,
    "Supply-Chain Pinning & Live Demo Wrap-Up",
    "Reproducible extension lockfiles, FastAPI A2A serving, and one-command Cloud Run deployment.",
    false
  );
  addInfoCard(
    s10, 40, 135, 205, 155, COLOR_GRAY_BG, COLOR_BLUE,
    "1. Exact SHA Pinning", COLOR_BLUE,
    "Git references resolve to exact commit SHAs in agents-cli-extensions.yaml."
  );
  addInfoCard(
    s10, 257, 135, 205, 155, COLOR_GRAY_BG, COLOR_GREEN,
    "2. Bit-for-Bit CI Restore", COLOR_GREEN,
    "agents-cli install restores reviewed extension code in CI without advancing pins."
  );
  addInfoCard(
    s10, 474, 135, 205, 155, COLOR_GRAY_BG, "#B06000",
    "3. Cloud Run A2A Contract", "#B06000",
    "Same FastAPI + A2A container contract (app.fast_api_app:app) deploys to Cloud Run."
  );
  addCodeCard(
    s10, 40, 305, 640, 60,
    "Clone & Run Live:  https://github.com/sanketbisne/scalfod-langgraph-agentscli\n" +
    "Quickstart:        uvx google-agents-cli setup && agents-cli install"
  );

  // Remove initial blank slide
  initialSlide.remove();

  Logger.log("Created Google Slides Deck: " + deck.getUrl());
}
