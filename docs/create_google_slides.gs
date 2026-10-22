/**
 * Google Cloud Next '27 Keynote Deck Generator (Sundar Pichai Keynote Style)
 * Uses internal Google typography: Google Sans Display, Google Sans, Google Sans Text, Google Sans Mono
 *
 * HOW TO GENERATE IN GOOGLE SLIDES:
 * 1. Go to https://script.google.com -> "New Project"
 * 2. Paste this entire file into Code.gs
 * 3. Select `createCloudNext27KeynoteDeck` and click "Run"
 * 4. Open the generated Google Slides URL logged in the Execution Log!
 */

function createCloudNext27KeynoteDeck() {
  var deck = SlidesApp.create(
    "Google Cloud Next '27 Keynote | Open Agent Development Lifecycle (Agents CLI v1.8+)"
  );

  // Official Google Typographic Trio
  var FONT_DISPLAY = "Google Sans Display";
  var FONT_HEADING = "Google Sans";
  var FONT_BODY = "Google Sans Text";
  var FONT_MONO = "Google Sans Mono";

  // Google Cloud Next '27 Keynote Palette
  var STAGE_DARK = "#0E1015";
  var CARD_DARK = "#161922";
  var CODE_DARK = "#131314";
  var BORDER_DARK = "#2D3343";
  var STAGE_LIGHT = "#FFFFFF";
  var CARD_LIGHT = "#F8F9FA";
  var BORDER_LIGHT = "#DADCE0";

  var GOOGLE_BLUE = "#4285F4";
  var GOOGLE_BLUE_LIGHT = "#8AB4F8";
  var GOOGLE_RED = "#EA4335";
  var GOOGLE_RED_LIGHT = "#F28B82";
  var GOOGLE_YELLOW = "#FBBC04";
  var GOOGLE_YELLOW_LIGHT = "#FDD663";
  var GOOGLE_GREEN = "#34A853";
  var GOOGLE_GREEN_LIGHT = "#81C995";

  var TEXT_WHITE = "#FFFFFF";
  var TEXT_MUTED_DARK = "#9AA0A6";
  var TEXT_PRIMARY_LIGHT = "#202124";
  var TEXT_MUTED_LIGHT = "#5F6368";

  var initialSlide = deck.getSlides()[0];

  function addFourColorBar(slide) {
    var colors = [GOOGLE_BLUE, GOOGLE_RED, GOOGLE_YELLOW, GOOGLE_GREEN];
    for (var i = 0; i < 4; i++) {
      var seg = slide.insertShape(SlidesApp.ShapeType.RECTANGLE, i * 180, 0, 180, 5);
      seg.getFill().setSolidFill(colors[i]);
      seg.getBorder().setTransparent();
    }
  }

  function addSpeakerNotes(slide, scriptText) {
    try {
      slide.getNotesPage().getSpeakerNotesShape().getText().setText(scriptText);
    } catch (e) {}
  }

  function setupKeynoteSlide(slide, isDark, eyebrowText, eyebrowColor, titleText, subtitleText, slideNumStr, notesText) {
    slide.getBackground().setSolidFill(isDark ? STAGE_DARK : STAGE_LIGHT);
    addFourColorBar(slide);

    var eyebrow = slide.insertTextBox(eyebrowText.toUpperCase(), 44, 22, 480, 20);
    eyebrow.getText().getTextStyle()
      .setFontFamily(FONT_HEADING)
      .setFontSize(9)
      .setBold(true)
      .setForegroundColor(eyebrowColor);

    var numBox = slide.insertTextBox(slideNumStr, 630, 22, 50, 20);
    numBox.getText().getTextStyle()
      .setFontFamily(FONT_MONO)
      .setFontSize(9)
      .setForegroundColor(isDark ? TEXT_MUTED_DARK : TEXT_MUTED_LIGHT);

    var title = slide.insertTextBox(titleText, 44, 42, 632, 46);
    title.getText().getTextStyle()
      .setFontFamily(FONT_DISPLAY)
      .setFontSize(24)
      .setBold(true)
      .setForegroundColor(isDark ? TEXT_WHITE : TEXT_PRIMARY_LIGHT);

    if (subtitleText) {
      var sub = slide.insertTextBox(subtitleText, 44, 86, 632, 32);
      sub.getText().getTextStyle()
        .setFontFamily(FONT_BODY)
        .setFontSize(12)
        .setForegroundColor(isDark ? TEXT_MUTED_DARK : TEXT_MUTED_LIGHT);
    }

    if (notesText) {
      addSpeakerNotes(slide, notesText);
    }
  }

  function addBentoTile(slide, x, y, w, h, bgHex, borderHex, kickerText, kickerColor, headingText, headingColor, bodyText, bodyColor) {
    var rect = slide.insertShape(SlidesApp.ShapeType.ROUND_RECTANGLE, x, y, w, h);
    rect.getFill().setSolidFill(bgHex);
    rect.getBorder().setWeight(1).getLineFill().setSolidFill(borderHex);

    var fullStr = kickerText + "\n" + headingText + "\n\n" + bodyText;
    var tb = slide.insertTextBox(fullStr, x + 12, y + 10, w - 24, h - 18);
    var t = tb.getText();
    t.getTextStyle().setFontFamily(FONT_BODY).setFontSize(10).setForegroundColor(bodyColor);

    var kLen = kickerText.length;
    var hLen = headingText.length;
    t.getRange(0, kLen).getTextStyle()
      .setFontFamily(FONT_MONO)
      .setFontSize(8)
      .setBold(true)
      .setForegroundColor(kickerColor);
    t.getRange(kLen + 1, kLen + 1 + hLen).getTextStyle()
      .setFontFamily(FONT_DISPLAY)
      .setFontSize(14)
      .setBold(true)
      .setForegroundColor(headingColor);
  }

  function addTerminalBlock(slide, x, y, w, h, codeStr) {
    var box = slide.insertShape(SlidesApp.ShapeType.ROUND_RECTANGLE, x, y, w, h);
    box.getFill().setSolidFill(CODE_DARK);
    box.getBorder().setWeight(1).getLineFill().setSolidFill("#3C4043");
    var t = box.getText();
    t.setText(codeStr);
    t.getTextStyle()
      .setFontFamily(FONT_MONO)
      .setFontSize(9.5)
      .setForegroundColor("#E8EAED");
  }

  // =========================================================================
  // SLIDE 01: Keynote Opening (Dark Stage)
  // =========================================================================
  var s1 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  s1.getBackground().setSolidFill(STAGE_DARK);
  addFourColorBar(s1);
  addSpeakerNotes(
    s1,
    "Good morning everyone, and welcome to Google Cloud Next '27. Over the past year, developers have moved from building single-agent prototypes to running mission-critical agentic systems in production. Today we are opening up the entire Agent Development Lifecycle to every framework: from ADK to LangChain, LangGraph, and beyond."
  );

  var s1Pill = s1.insertTextBox("GOOGLE CLOUD NEXT '27  |  OPENING KEYNOTE  |  AGENTS CLI v1.8+", 48, 54, 540, 24);
  s1Pill.getText().getTextStyle().setFontFamily(FONT_MONO).setFontSize(10).setBold(true).setForegroundColor(GOOGLE_BLUE_LIGHT);

  var s1Hero = s1.insertTextBox("Every agent framework.\nOne production lifecycle.", 48, 95, 624, 115);
  s1Hero.getText().getTextStyle().setFontFamily(FONT_DISPLAY).setFontSize(38).setBold(true).setForegroundColor(TEXT_WHITE);

  var s1Sub = s1.insertTextBox(
    "Running LangChain, LangGraph, and custom enterprise governance policies natively on Google Cloud with the Agents CLI Extension System.",
    48, 215, 600, 55
  );
  s1Sub.getText().getTextStyle().setFontFamily(FONT_BODY).setFontSize(15).setForegroundColor("#BDC1C6");

  var s1Repo = s1.insertTextBox("Live Repo: github.com/sanketbisne/scalfod-langgraph-agentscli", 48, 340, 624, 30);
  s1Repo.getText().getTextStyle().setFontFamily(FONT_MONO).setFontSize(11).setBold(true).setForegroundColor(GOOGLE_GREEN_LIGHT);

  // =========================================================================
  // SLIDE 02: Sundar's Big Numbers Impact Slide (Dark Stage)
  // =========================================================================
  var s2 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupKeynoteSlide(
    s2, true,
    "By The Numbers", GOOGLE_BLUE_LIGHT,
    "Decoupling the lifecycle from the runtime.",
    "Why re-architect 24 CLI commands when only 6 depend on the agent framework?",
    "02 / 10",
    "When we looked inside Agents CLI, we saw that out of 24 commands, 18 are completely framework-agnostic. Only 6 commands touch the agent runtime. By making those 6 commands extensible, developers get the entire Google Cloud lifecycle with 0% framework lock-in."
  );
  addBentoTile(
    s2, 44, 130, 200, 225, CARD_DARK, BORDER_DARK,
    "PRODUCTION LIFECYCLE", GOOGLE_BLUE_LIGHT,
    "18+ Native Commands", TEXT_WHITE,
    "deploy, eval grade, eval compare, infra, scaffold, lint, and login work out of the box for any framework.",
    TEXT_MUTED_DARK
  );
  addBentoTile(
    s2, 260, 130, 200, 225, CARD_DARK, BORDER_DARK,
    "RUNTIME INTERCEPTION", GOOGLE_GREEN_LIGHT,
    "6 Overridden Commands", TEXT_WHITE,
    "run, playground, eval.generate, and publish hot-swap cleanly via agents-cli-extension.yaml.",
    TEXT_MUTED_DARK
  );
  addBentoTile(
    s2, 476, 130, 200, 225, CARD_DARK, BORDER_DARK,
    "PURE LANGGRAPH", GOOGLE_YELLOW_LIGHT,
    "0% ADK Lock-In", TEXT_WHITE,
    "Zero google-adk dependency in pyproject.toml. Pure LangChain and LangGraph code in production.",
    TEXT_MUTED_DARK
  );

  // =========================================================================
  // SLIDE 03: The Developer Dilemma (Clean Light Stage)
  // =========================================================================
  var s3 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupKeynoteSlide(
    s3, false,
    "Why Extensions Matter", GOOGLE_BLUE,
    "Ending the tradeoff between velocity and choice.",
    "Teams want Google Cloud deployment, Vertex AI evaluation, and A2A serving without rewriting LangGraph agents.",
    "03 / 10",
    "Previously, teams using non-ADK frameworks or enforcing custom security gates had to either fork the CLI or write bash wrapper scripts that developers and coding agents forget to use. Extensions solve both in-place."
  );
  addBentoTile(
    s3, 44, 130, 200, 225, CARD_LIGHT, BORDER_LIGHT,
    "LEGACY PATH 1", GOOGLE_RED,
    "Forking the CLI", TEXT_PRIMARY_LIGHT,
    "Permanent maintenance tax. Breaks on every upstream release and requires manual rebasing.",
    TEXT_MUTED_LIGHT
  );
  addBentoTile(
    s3, 260, 130, 200, 225, CARD_LIGHT, BORDER_LIGHT,
    "LEGACY PATH 2", "#B06000",
    "Bash Wrapper Scripts", TEXT_PRIMARY_LIGHT,
    "Parallel command surface. Developers and AI coding assistants call the native CLI directly and bypass policies.",
    TEXT_MUTED_LIGHT
  );
  addBentoTile(
    s3, 476, 130, 200, 225, "#E8F0FE", GOOGLE_BLUE,
    "CLOUD NEXT '27 STANDARD", GOOGLE_BLUE,
    "Agents CLI Extensions", TEXT_PRIMARY_LIGHT,
    "Declarative agents-cli-extension.yaml overrides commands in-place, pinned by exact Git commit SHA.",
    TEXT_PRIMARY_LIGHT
  );

  // =========================================================================
  // SLIDE 04: Inside the Command Surface (6 vs 18 Split)
  // =========================================================================
  var s4 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupKeynoteSlide(
    s4, false,
    "Command Surface Architecture", GOOGLE_GREEN,
    "Inside the Agents CLI Command Surface (6 vs. 18 Split)",
    "A single agents-cli-extension.yaml swaps only the 6 runtime commands and keeps the 18 production commands intact.",
    "04 / 10",
    "Here is the exact breakdown. On the left, the 6 commands overridden by the LangChain extension. On the right, the 18 native Google Cloud commands that work identically across every framework."
  );
  addBentoTile(
    s4, 44, 130, 306, 230, "#F8FAFF", GOOGLE_BLUE,
    "[↑ LANGCHAIN] OVERRIDES", GOOGLE_BLUE,
    "6 Framework-Coupled Commands", TEXT_PRIMARY_LIGHT,
    "- run -> uv run python scripts/run.py\n- playground -> uv run langgraph dev --port 8080\n- eval.generate -> uv run python scripts/eval_generate.py\n- publish.gemini-enterprise -> scripts/publish.py\n- eval.dataset / eval.optimize -> Clean refusal wrapper",
    TEXT_PRIMARY_LIGHT
  );
  addBentoTile(
    s4, 370, 130, 306, 230, "#F6FEF8", GOOGLE_GREEN,
    "NATIVE BUILT-IN LIFECYCLE", GOOGLE_GREEN,
    "18+ Framework-Agnostic Commands", TEXT_PRIMARY_LIGHT,
    "- deploy (Cloud Run / GKE via FastAPI A2A)\n- eval grade / eval compare / eval analyze\n- infra (Terraform modules)\n- scaffold create / enhance / upgrade\n- extension add / list / update / remove\n- install / info / lint / login",
    TEXT_PRIMARY_LIGHT
  );

  // =========================================================================
  // SLIDE 05: Live Demo Act I - Scaffolding (Dark Stage)
  // =========================================================================
  var s5 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupKeynoteSlide(
    s5, true,
    "Live Demo | Act 1", GOOGLE_BLUE_LIGHT,
    "Scaffold a pure LangGraph project in one command.",
    "Scaffolding and extension installation happen together with zero google-adk dependency.",
    "05 / 10",
    "Let's walk through the commands. We run agents-cli create pointing at the LangChain template tag. Immediately, our project is wired up, and grepping for google-adk confirms zero ADK dependencies."
  );
  addTerminalBlock(
    s5, 44, 130, 632, 230,
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
  // SLIDE 06: Project Structure & CompiledStateGraph
  // =========================================================================
  var s6 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupKeynoteSlide(
    s6, false,
    "Codebase Architecture", "#B06000",
    "Project Structure & LangGraph CompiledStateGraph",
    "In LangChain 1.0+, create_agent compiles directly into a LangGraph CompiledStateGraph.",
    "06 / 10",
    "On the left is the generated project structure. On the right is app/agent.py, where create_agent compiles our Gemini model and tools into a LangGraph CompiledStateGraph."
  );
  addTerminalBlock(
    s6, 44, 130, 306, 230,
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
    "└── extensions/sbom-deploy/"
  );
  addTerminalBlock(
    s6, 370, 130, 306, 230,
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
  // SLIDE 07: DeepCite Agent Architecture
  // =========================================================================
  var s7 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupKeynoteSlide(
    s7, false,
    "Reference Workload", GOOGLE_BLUE,
    "DeepCite Architecture (Plan -> Search -> Critique -> Report)",
    "Iterative self-reflection workflow that verifies inline citations before synthesizing the final report.",
    "07 / 10",
    "DeepCite implements a four-stage research loop: Plan sub-questions, Search curated and live scientific sources, Critique the draft for citation coverage, and synthesize a Cited Markdown Report."
  );
  addBentoTile(
    s7, 44, 130, 150, 225, CARD_LIGHT, GOOGLE_BLUE,
    "STAGE 01", GOOGLE_BLUE,
    "Plan", TEXT_PRIMARY_LIGHT,
    "create_research_plan decomposes user prompts into sub-questions.",
    TEXT_MUTED_LIGHT
  );
  addBentoTile(
    s7, 204, 130, 150, 225, CARD_LIGHT, "#B06000",
    "STAGE 02", "#B06000",
    "Search", TEXT_PRIMARY_LIGHT,
    "search_curated_kb, search_arxiv_papers, and search_wikipedia_summary.",
    TEXT_MUTED_LIGHT
  );
  addBentoTile(
    s7, 364, 130, 150, 225, CARD_LIGHT, GOOGLE_RED,
    "STAGE 03", GOOGLE_RED,
    "Critique", TEXT_PRIMARY_LIGHT,
    "critique_research_draft verifies >= 2 source IDs and technical depth.",
    TEXT_MUTED_LIGHT
  );
  addBentoTile(
    s7, 524, 130, 152, 225, CARD_LIGHT, GOOGLE_GREEN,
    "STAGE 04", GOOGLE_GREEN,
    "Report", TEXT_PRIMARY_LIGHT,
    "Synthesizes Markdown with inline [KB-...] and [ARXIV-...] citations.",
    TEXT_MUTED_LIGHT
  );

  // =========================================================================
  // SLIDE 08: Running Locally & LangGraph Studio + Evals (Dark Stage)
  // =========================================================================
  var s8 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupKeynoteSlide(
    s8, true,
    "Live Demo | Act 2 & Act 3", GOOGLE_GREEN_LIGHT,
    "LangGraph Studio & Framework-Agnostic Evaluations",
    "Boot LangGraph Studio via agents-cli playground and grade traces with Vertex AI Eval Service.",
    "08 / 10",
    "Running agents-cli playground boots LangGraph Studio on port 8080. And for evaluation, eval generate drives the LangGraph graph while native eval grade scores the output using Vertex AI."
  );
  addTerminalBlock(
    s8, 44, 130, 306, 230,
    "# 1. Local Run & LangGraph Studio\n" +
    "$ agents-cli --help | grep -E \"playground|run\"\n" +
    "  playground  Start LangGraph server [↑ langchain]\n" +
    "  run         Run compiled graph     [↑ langchain]\n\n" +
    "$ agents-cli info\n" +
    "$ agents-cli run \"How do extensions work?\"\n" +
    "$ agents-cli playground  # Port 8080"
  );
  addTerminalBlock(
    s8, 370, 130, 306, 230,
    "# 2. Overridden Generate + Native Grade\n" +
    "$ agents-cli eval generate \\\n" +
    "    --dataset tests/eval/datasets/basic-dataset.json \\\n" +
    "    -o tests/eval/output/\n\n" +
    "$ agents-cli eval grade \\\n" +
    "    --traces tests/eval/output/basic-dataset.json \\\n" +
    "    --config tests/eval/eval_config.yaml\n\n" +
    "# Clean refusal on ADK-only simulator:\n" +
    "$ agents-cli eval dataset synthesize"
  );

  // =========================================================================
  // SLIDE 09: Custom Enterprise Extensions (Dark Stage)
  // =========================================================================
  var s9 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupKeynoteSlide(
    s9, true,
    "Live Demo | Act 4", GOOGLE_RED_LIGHT,
    "Authoring Custom Enterprise Extensions (sbom-deploy)",
    "AGENTS_CLI_DISABLE_OVERRIDES=1 lets wrapper scripts run Syft + Grype checks and call native deploy without recursion.",
    "09 / 10",
    "Platform teams can wrap deploy with an SBOM scan using the exact same manifest format. Because the loader sets AGENTS_CLI_DISABLE_OVERRIDES=1, calling exec agents-cli deploy delegates to the native command with zero recursion."
  );
  addTerminalBlock(
    s9, 44, 130, 306, 230,
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
  addTerminalBlock(
    s9, 370, 130, 306, 230,
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
  // SLIDE 10: Sundar's Closing Bento Grid Summary (Dark Stage)
  // =========================================================================
  var s10 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupKeynoteSlide(
    s10, true,
    "Google Cloud Next '27 Summary", GOOGLE_BLUE_LIGHT,
    "The Open Agent Development Lifecycle",
    "github.com/sanketbisne/scalfod-langgraph-agentscli",
    "10 / 10",
    "To wrap up: with Agents CLI v1.8+, you get complete framework choice with LangChain and LangGraph, local visual debugging in LangGraph Studio, Vertex AI evaluations, custom SBOM deploy gates, SHA lockfiles, and one-command Cloud Run A2A deployment. Thank you!"
  );
  addBentoTile(
    s10, 44, 125, 200, 110, CARD_DARK, BORDER_DARK,
    "01 | OPEN FRAMEWORKS", GOOGLE_BLUE_LIGHT,
    "LangChain & LangGraph", TEXT_WHITE,
    "Zero google-adk dependency; unified CompiledStateGraph.",
    TEXT_MUTED_DARK
  );
  addBentoTile(
    s10, 260, 125, 200, 110, CARD_DARK, BORDER_DARK,
    "02 | VISUAL DEBUGGING", GOOGLE_GREEN_LIGHT,
    "LangGraph Studio", TEXT_WHITE,
    "agents-cli playground launches Studio on port 8080.",
    TEXT_MUTED_DARK
  );
  addBentoTile(
    s10, 476, 125, 200, 110, CARD_DARK, BORDER_DARK,
    "03 | QUALITY FLYWHEEL", GOOGLE_YELLOW_LIGHT,
    "Vertex AI Evaluations", TEXT_WHITE,
    "Overridden eval generate + native Vertex AI eval grade.",
    TEXT_MUTED_DARK
  );
  addBentoTile(
    s10, 44, 245, 200, 110, CARD_DARK, BORDER_DARK,
    "04 | POLICY AS CODE", GOOGLE_RED_LIGHT,
    "SBOM Pre-Deploy Gates", TEXT_WHITE,
    "Syft + Grype checks with AGENTS_CLI_DISABLE_OVERRIDES=1.",
    TEXT_MUTED_DARK
  );
  addBentoTile(
    s10, 260, 245, 200, 110, CARD_DARK, BORDER_DARK,
    "05 | SUPPLY CHAIN", GOOGLE_BLUE_LIGHT,
    "SHA Lockfile Pinning", TEXT_WHITE,
    "Bit-for-bit reproducible CI via agents-cli-extensions.yaml.",
    TEXT_MUTED_DARK
  );
  addBentoTile(
    s10, 476, 245, 200, 110, CARD_DARK, BORDER_DARK,
    "06 | PRODUCTION SERVING", GOOGLE_GREEN_LIGHT,
    "Cloud Run + A2A", TEXT_WHITE,
    "Standard FastAPI + A2A container contract on port 8080.",
    TEXT_MUTED_DARK
  );

  initialSlide.remove();
  Logger.log("Created Cloud Next '27 Keynote Google Slides Deck: " + deck.getUrl());
}
