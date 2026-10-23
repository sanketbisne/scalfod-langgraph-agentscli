/**
 * 1-to-1 High-Fidelity Google Cloud Next '27 Deck Generator for Google Slides
 * Matches the HTML presentation deck layout, colors, badges, giant numbers,
 * 3-Layer Stack Cake (Slide 4), 4-Stage top-bordered cards (Slide 7),
 * syntax-highlighted terminal colors, and Bento Grid + CTA bar (Slide 10).
 *
 * HOW TO RUN IN GOOGLE SLIDES:
 * 1. Open https://slides.google.com -> Blank Presentation
 * 2. Click Extensions -> Apps Script
 * 3. Paste this file into Code.gs and click "Run" on `createCloudNext27Deck`
 */

function createCloudNext27Deck() {
  var deck = SlidesApp.getActivePresentation();
  if (!deck) {
    deck = SlidesApp.create(
      "Google Cloud Next '27 | Open Agent Development Lifecycle (Agents CLI v1.8+)"
    );
  }

  var FONT_DISPLAY = "Google Sans Display";
  var FONT_HEADING = "Google Sans";
  var FONT_BODY = "Google Sans Text";
  var FONT_MONO = "Google Sans Mono";

  var existingSlides = deck.getSlides();

  function addRect(slide, x, y, w, h, fillHex, borderHex, borderW, isRound) {
    var shapeType = isRound ? SlidesApp.ShapeType.ROUND_RECTANGLE : SlidesApp.ShapeType.RECTANGLE;
    var s = slide.insertShape(shapeType, x, y, w, h);
    if (fillHex) {
      s.getFill().setSolidFill(fillHex);
    } else {
      s.getFill().setTransparent();
    }
    if (borderHex) {
      s.getBorder().setWeight(borderW || 1).getLineFill().setSolidFill(borderHex);
    } else {
      s.getBorder().setTransparent();
    }
    return s;
  }

  function addStyledBox(slide, x, y, w, h, fillHex, borderHex, borderW, isRound, lines) {
    var s = addRect(slide, x, y, w, h, fillHex, borderHex, borderW, isRound);
    s.setContentAlignment(SlidesApp.ContentAlignment.TOP);
    var fullStr = lines.map(function(l) { return l.text; }).join("\n");
    if (!fullStr) return s;

    var tr = s.getText();
    tr.setText(fullStr);
    var pos = 0;
    for (var i = 0; i < lines.length; i++) {
      var item = lines[i];
      var len = item.text.length;
      if (len > 0) {
        var sub = tr.getRange(pos, pos + len);
        sub.getTextStyle()
          .setFontFamily(item.font || FONT_BODY)
          .setFontSize(item.size || 10)
          .setForegroundColor(item.color || "#FFFFFF")
          .setBold(!!item.bold);
      }
      pos += len + 1;
    }
    return s;
  }

  function addFourColorBar(slide) {
    var colors = ["#4285F4", "#EA4335", "#FBBC04", "#34A853"];
    for (var i = 0; i < 4; i++) {
      addRect(slide, i * 180, 0, 180, 4, colors[i], null, 0, false);
    }
  }

  function setupHeaderAndFooter(slide, isDark, eyebrow, eyebrowCol, title, subtitle, numStr, footLeft, footRight, footRightCol) {
    slide.getBackground().setSolidFill(isDark ? "#0E1015" : "#FFFFFF");
    addFourColorBar(slide);

    addStyledBox(slide, 36, 14, 480, 18, null, null, 0, false, [
      { text: eyebrow.toUpperCase(), font: FONT_HEADING, size: 8.5, color: eyebrowCol, bold: true }
    ]);
    addStyledBox(slide, 620, 14, 64, 18, null, null, 0, false, [
      { text: numStr, font: FONT_MONO, size: 8.5, color: isDark ? "#9AA0A6" : "#5F6368", bold: false }
    ]);
    addStyledBox(slide, 36, 30, 648, 34, null, null, 0, false, [
      { text: title, font: FONT_DISPLAY, size: 20, color: isDark ? "#FFFFFF" : "#202124", bold: true }
    ]);
    if (subtitle) {
      addStyledBox(slide, 36, 62, 648, 24, null, null, 0, false, [
        { text: subtitle, font: FONT_BODY, size: 10, color: isDark ? "#BDC1C6" : "#5F6368", bold: false }
      ]);
    }
    if (footLeft) {
      addRect(slide, 36, 370, 648, 1, isDark ? "#2D3343" : "#DADCE0", null, 0, false);
      addStyledBox(slide, 36, 374, 440, 20, null, null, 0, false, [
        { text: footLeft, font: FONT_BODY, size: 8, color: isDark ? "#9AA0A6" : "#5F6368", bold: false }
      ]);
      addStyledBox(slide, 480, 374, 204, 20, null, null, 0, false, [
        { text: footRight || "", font: FONT_MONO, size: 8, color: footRightCol || (isDark ? "#8AB4F8" : "#5F6368"), bold: true }
      ]);
    }
  }

  // =========================================================================
  // SLIDE 01: Hero Opening (Dark Stage #0E1015)
  // =========================================================================
  var s1 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  s1.getBackground().setSolidFill("#0E1015");
  addFourColorBar(s1);
  addStyledBox(s1, 42, 28, 250, 22, "#162038", "#3B5998", 1, true, [
    { text: "Google Cloud Next '27  •  Developer Session", font: FONT_HEADING, size: 8, color: "#8AB4F8", bold: true }
  ]);
  addStyledBox(s1, 300, 28, 120, 22, null, null, 0, false, [
    { text: "agents-cli v1.8+", font: FONT_MONO, size: 8, color: "#9AA0A6", bold: false }
  ]);
  addStyledBox(s1, 42, 90, 500, 20, null, null, 0, false, [
    { text: "POWERING THE AGENT DEVELOPMENT LIFECYCLE", font: FONT_HEADING, size: 9, color: "#8AB4F8", bold: true }
  ]);
  addStyledBox(s1, 42, 112, 636, 105, null, null, 0, false, [
    { text: "Every agent framework.", font: FONT_DISPLAY, size: 34, color: "#FFFFFF", bold: true },
    { text: "One production lifecycle.", font: FONT_DISPLAY, size: 34, color: "#8AB4F8", bold: true }
  ]);
  addStyledBox(s1, 42, 225, 580, 55, null, null, 0, false, [
    { text: "Running LangChain, LangGraph, and custom enterprise governance policies natively on Google Cloud with the Agents CLI Extension System.", font: FONT_BODY, size: 12.5, color: "#BDC1C6", bold: false }
  ]);
  addRect(s1, 42, 348, 636, 1, "#2D3343", null, 0, false);
  addStyledBox(s1, 42, 358, 340, 24, "#1F2430", "#2D3343", 1, true, [
    { text: "github.com/sanketbisne/scalfod-langgraph-agentscli", font: FONT_MONO, size: 8.5, color: "#FFFFFF", bold: false }
  ]);

  // =========================================================================
  // SLIDE 02: By The Numbers (Dark Stage #0E1015)
  // =========================================================================
  var s2 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupHeaderAndFooter(
    s2, true, "By The Numbers", "#8AB4F8",
    "Decoupling the lifecycle from the runtime.",
    "Out of 24 CLI commands, 18 are framework-agnostic and only 6 touch the agent runtime.",
    "02 / 10",
    "Available starting in Agents CLI v1.5+ (Extension System) & v1.8+ (LangChain Template)",
    "google/agents-cli", "#8AB4F8"
  );
  addStyledBox(s2, 36, 98, 206, 255, "#161922", "#2D3343", 1, true, [
    { text: "18+", font: FONT_DISPLAY, size: 38, color: "#8AB4F8", bold: true },
    { text: "Framework-Agnostic Commands", font: FONT_HEADING, size: 11, color: "#FFFFFF", bold: true },
    { text: "deploy, eval grade, eval compare, infra, scaffold, lint, and login work unchanged across ADK, LangChain, and LangGraph.", font: FONT_BODY, size: 9, color: "#9AA0A6", bold: false }
  ]);
  addStyledBox(s2, 257, 98, 206, 255, "#161922", "#2D3343", 1, true, [
    { text: "6", font: FONT_DISPLAY, size: 38, color: "#81C995", bold: true },
    { text: "Runtime Overrides", font: FONT_HEADING, size: 11, color: "#FFFFFF", bold: true },
    { text: "run, playground, and eval.generate hot-swap via a single agents-cli-extension.yaml manifest.", font: FONT_BODY, size: 9, color: "#9AA0A6", bold: false }
  ]);
  addStyledBox(s2, 478, 98, 206, 255, "#161922", "#2D3343", 1, true, [
    { text: "0%", font: FONT_DISPLAY, size: 38, color: "#FDD663", bold: true },
    { text: "Framework Lock-In", font: FONT_HEADING, size: 11, color: "#FFFFFF", bold: true },
    { text: "Zero google-adk dependency required in pyproject.toml. Pure LangChain and LangGraph code in production.", font: FONT_BODY, size: 9, color: "#9AA0A6", bold: false }
  ]);

  // =========================================================================
  // SLIDE 03: The Framework Lock-In Problem (Light Stage #FFFFFF)
  // =========================================================================
  var s3 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupHeaderAndFooter(
    s3, false, "The Framework Lock-In Problem", "#1A73E8",
    "Ending the tradeoff between velocity and choice.",
    "How teams previously adapted opinionated agent toolchains vs. the Agents CLI Extension System:",
    "03 / 10",
    "Distributed directly via Git repositories with zero external registry required",
    "schema: agents-cli-extension/v1alpha1", "#5F6368"
  );
  addStyledBox(s3, 36, 98, 206, 255, "#F8F9FA", "#DADCE0", 1, true, [
    { text: "LEGACY PATH 1", font: FONT_HEADING, size: 8, color: "#C5221F", bold: true },
    { text: "Forking the CLI", font: FONT_HEADING, size: 13, color: "#202124", bold: true },
    { text: "Maintain a divergent internal copy and manually rebase on every upstream release.\n\nResult: Permanent maintenance tax", font: FONT_BODY, size: 9, color: "#5F6368", bold: false }
  ]);
  addStyledBox(s3, 257, 98, 206, 255, "#F8F9FA", "#DADCE0", 1, true, [
    { text: "LEGACY PATH 2", font: FONT_HEADING, size: 8, color: "#B06000", bold: true },
    { text: "Custom Wrapper Scripts", font: FONT_HEADING, size: 13, color: "#202124", bold: true },
    { text: "Build parallel shell scripts around the CLI. Developers and coding agents call native CLI directly.\n\nResult: Bypassed governance gates", font: FONT_BODY, size: 9, color: "#5F6368", bold: false }
  ]);
  addStyledBox(s3, 478, 98, 206, 255, "#E8F0FE", "#1A73E8", 2, true, [
    { text: "CLOUD NEXT '27 STANDARD", font: FONT_HEADING, size: 8, color: "#1A73E8", bold: true },
    { text: "Agents CLI Extensions", font: FONT_HEADING, size: 13, color: "#202124", bold: true },
    { text: "Declarative agents-cli-extension.yaml overrides commands in-place, pinned by Git commit SHA.\n\nResult: Zero fork + 100% enforcement", font: FONT_BODY, size: 9, color: "#202124", bold: false }
  ]);

  // =========================================================================
  // SLIDE 04: 3-Layer Stack Cake - 6 vs 18 Split (Light Stage #FFFFFF)
  // =========================================================================
  var s4 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupHeaderAndFooter(
    s4, false, "Inside the Command Surface (6 vs. 18 Split)", "#137333",
    "One unified command surface across the stack.",
    "A single agents-cli-extension.yaml swaps only the 6 runtime commands and keeps the 18 production commands intact.",
    "04 / 10",
    "Same Dockerfile CMD & FastAPI A2A contract across every framework",
    "app.fast_api_app:app", "#5F6368"
  );
  addStyledBox(s4, 36, 94, 648, 66, "#F8F9FA", "#DADCE0", 1, true, [
    { text: "1. AGENT AUTHORING LAYER (BRING YOUR OWN FRAMEWORK)", font: FONT_HEADING, size: 8, color: "#5F6368", bold: true },
    { text: "[ LangChain 1.0+ ]     [ LangGraph StateGraph ]     [ Deep Agents ]     [ Google ADK (Python / Go) ]", font: FONT_HEADING, size: 10, color: "#1967D2", bold: true }
  ]);
  addStyledBox(s4, 36, 168, 318, 112, "#F8FAFF", "#4285F4", 2, true, [
    { text: "6 Overridden Runtime Commands  [↑ langchain]", font: FONT_HEADING, size: 10, color: "#1967D2", bold: true },
    { text: "• run -> uv run python scripts/run.py\n• playground -> uv run langgraph dev --port 8080\n• eval.generate -> uv run python scripts/eval_generate.py\n• publish.gemini-enterprise & eval.dataset / optimize", font: FONT_MONO, size: 8, color: "#3C4043", bold: false }
  ]);
  addStyledBox(s4, 366, 168, 318, 112, "#F6FEF8", "#34A853", 2, true, [
    { text: "18+ Native Production Commands  [Built-In]", font: FONT_HEADING, size: 10, color: "#137333", bold: true },
    { text: "• deploy (Cloud Run / GKE via FastAPI A2A)\n• eval grade / eval compare / eval analyze (Vertex AI)\n• infra (Terraform) & scaffold create / enhance\n• extension add / list & install / info / lint / login", font: FONT_MONO, size: 8, color: "#3C4043", bold: false }
  ]);
  addStyledBox(s4, 36, 288, 648, 68, "#202124", "#202124", 1, true, [
    { text: "3. GOOGLE CLOUD PRODUCTION FOUNDATION", font: FONT_HEADING, size: 8, color: "#8AB4F8", bold: true },
    { text: "[ Cloud Run (FastAPI A2A) ]    [ Vertex AI Eval Service ]    [ Gemini on Vertex AI ]    [ Cloud Trace & Logging ]", font: FONT_MONO, size: 9, color: "#FFFFFF", bold: false }
  ]);

  // =========================================================================
  // SLIDE 05: Live Demo Act 1 - Scaffolding (Dark Stage #0E1015)
  // =========================================================================
  var s5 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupHeaderAndFooter(
    s5, true, "Live Demo  •  Act 1", "#8AB4F8",
    "Scaffold a pure LangGraph project in one command.",
    "Scaffolding and extension installation happen together. Nothing needs to be installed globally.",
    "05 / 10",
    "Auto-loaded via ./agents-cli-extension.yaml at project root",
    "Zero ADK Dependency Verified", "#81C995"
  );
  addStyledBox(s5, 36, 98, 648, 255, "#131314", "#3C4043", 1, true, [
    { text: "# 1. Scaffold directly from the first-party LangChain template", font: FONT_MONO, size: 9, color: "#8AB4F8", bold: false },
    { text: "$ agents-cli create scalfod-langgraph-agentscli \\\n    --agent google/agents-cli/extensions/langchain/template@v1.8.0 \\\n    -d cloud_run\n\n$ cd scalfod-langgraph-agentscli && agents-cli install", font: FONT_MONO, size: 9, color: "#E8EAED", bold: false },
    { text: "Agents CLI v1.8.0 • Fetching remote template: google/agents-cli/extensions/langchain/template@v1.8.0\n> ✓ Connected to project: your-project • Your agent project is ready.", font: FONT_MONO, size: 9, color: "#81C995", bold: false },
    { text: "\n# 2. Prove zero google-adk dependency in pyproject.toml and app/", font: FONT_MONO, size: 9, color: "#8AB4F8", bold: false },
    { text: "$ grep -r \"google.adk\\|google-adk\" pyproject.toml app/ ; echo \"exit: $?\"", font: FONT_MONO, size: 9, color: "#E8EAED", bold: false },
    { text: "exit: 1   # Verified: Zero google-adk dependency!", font: FONT_MONO, size: 9, color: "#FDD663", bold: true }
  ]);

  // =========================================================================
  // SLIDE 06: Project Structure & CompiledStateGraph (Light Stage #FFFFFF)
  // =========================================================================
  var s6 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupHeaderAndFooter(
    s6, false, "Codebase Architecture", "#B06000",
    "One graph representation: CompiledStateGraph",
    "In LangChain 1.0+, create_agent compiles directly into a LangGraph CompiledStateGraph.",
    "06 / 10",
    "Authenticates automatically via Application Default Credentials (ADC) on Vertex AI",
    "GOOGLE_GENAI_USE_VERTEXAI=True", "#5F6368"
  );
  addStyledBox(s6, 36, 98, 318, 255, "#131314", "#3C4043", 1, true, [
    { text: "Project Tree", font: FONT_HEADING, size: 9, color: "#8AB4F8", bold: true },
    { text: "scalfod-langgraph-agentscli/\n├── agents-cli-extension.yaml  # Overrides\n├── agents-cli-manifest.yaml   # cloud_run\n├── langgraph.json             # Studio\n├── pyproject.toml             # Zero ADK\n├── Dockerfile                 # FastAPI :8080\n├── app/\n│   ├── agent.py               # StateGraph\n│   ├── tools.py               # DeepCite\n│   ├── fast_api_app.py        # A2A server\n│   └── app_utils/a2a.py       # agent.json\n└── extensions/sbom-deploy/    # SBOM gate", font: FONT_MONO, size: 8.5, color: "#E8EAED", bold: false }
  ]);
  addStyledBox(s6, 366, 98, 318, 255, "#131314", "#3C4043", 1, true, [
    { text: "app/agent.py", font: FONT_HEADING, size: 9, color: "#81C995", bold: true },
    { text: "from langchain.agents import create_agent\nfrom langchain_google_genai import ChatGoogleGenerativeAI\nfrom langgraph.graph.state import CompiledStateGraph\n\nllm = ChatGoogleGenerativeAI(\n    model=\"gemini-2.5-flash\", temperature=0\n)\n\nroot_agent: CompiledStateGraph = create_agent(\n    model=llm,\n    tools=[create_research_plan, search_curated_kb,\n           search_arxiv_papers, critique_research_draft],\n    system_prompt=SYSTEM_PROMPT,\n)", font: FONT_MONO, size: 8.5, color: "#E8EAED", bold: false }
  ]);

  // =========================================================================
  // SLIDE 07: DeepCite Research & Critique Loop (Light Stage #FFFFFF)
  // =========================================================================
  var s7 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupHeaderAndFooter(
    s7, false, "DeepCite Reference Workload", "#1A73E8",
    "Iterative Research & Self-Critique Loop",
    "Grounded retrieval and mandatory citation verification before generating the final technical report:",
    "07 / 10",
    "Deterministic offline fallbacks guarantee reproducible runs in CI/CD and sandboxed environments",
    "app/tools.py", "#1A73E8"
  );
  var stages = [
    { k: "01 • PLAN", col: "#1A73E8", bar: "#4285F4", fn: "create_research_plan", d: "Decomposes complex prompts into structured sub-questions and targeted search queries." },
    { k: "02 • SEARCH", col: "#B06000", bar: "#FBBC04", fn: "search_curated_kb", d: "Retrieves evidence with explicit IDs ([KB-...], [ARXIV-...], [WIKI-...]) and offline fallbacks." },
    { k: "03 • CRITIQUE", col: "#C5221F", bar: "#EA4335", fn: "critique_research_draft", d: "Audits draft claims for >= 2 distinct citations and depth; triggers revision if incomplete." },
    { k: "04 • REPORT", col: "#137333", bar: "#34A853", fn: "research-report CLI", d: "Outputs Markdown with inline [SOURCE_ID] citations and a verified ## References section." }
  ];
  for (var idx = 0; idx < 4; idx++) {
    var st = stages[idx];
    var sx = 36 + idx * 165;
    addStyledBox(s7, sx, 98, 153, 255, "#F8F9FA", "#DADCE0", 1, true, [
      { text: st.k, font: FONT_HEADING, size: 8.5, color: st.col, bold: true },
      { text: st.fn, font: FONT_MONO, size: 8.5, color: "#202124", bold: true },
      { text: "\n" + st.d, font: FONT_BODY, size: 8.5, color: "#5F6368", bold: false }
    ]);
    addRect(s7, sx + 2, 98, 149, 5, st.bar, null, 0, false);
  }

  // =========================================================================
  // SLIDE 08: LangGraph Studio & Vertex AI Evaluations (Dark Stage #0E1015)
  // =========================================================================
  var s8 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupHeaderAndFooter(
    s8, true, "Live Demo  •  Act 2 & Act 3", "#81C995",
    "LangGraph Studio & Vertex AI Evaluations.",
    "Boot LangGraph Studio via agents-cli playground and grade traces with Vertex AI Eval Service.",
    "08 / 10",
    "Unsupported ADK-simulator commands (eval dataset) exit cleanly with an explanation",
    "Standard EvaluationDataset Schema", "#81C995"
  );
  addStyledBox(s8, 36, 98, 318, 255, "#131314", "#3C4043", 1, true, [
    { text: "1. RUN & INSPECT IN LANGGRAPH STUDIO", font: FONT_HEADING, size: 8.5, color: "#8AB4F8", bold: true },
    { text: "$ agents-cli --help | grep -E \"playground|run \"\n  playground  Start LangGraph server. [↑ langchain]\n  run         Run compiled graph.     [↑ langchain]\n\n$ agents-cli run \"How do extensions work?\"", font: FONT_MONO, size: 8, color: "#E8EAED", bold: false },
    { text: "WARNING:root:agents-cli: applying 6 extension command(s)", font: FONT_MONO, size: 8, color: "#FDD663", bold: false },
    { text: "\n$ agents-cli playground\n> Boots LangGraph Studio on http://localhost:8080", font: FONT_MONO, size: 8, color: "#81C995", bold: true }
  ]);
  addStyledBox(s8, 366, 98, 318, 255, "#131314", "#3C4043", 1, true, [
    { text: "2. OVERRIDDEN GENERATE + NATIVE GRADE", font: FONT_HEADING, size: 8.5, color: "#81C995", bold: true },
    { text: "# Overridden: Drives LangGraph CompiledStateGraph", font: FONT_MONO, size: 8, color: "#8AB4F8", bold: false },
    { text: "$ agents-cli eval generate \\\n    --dataset tests/eval/datasets/basic-dataset.json \\\n    -o tests/eval/output/", font: FONT_MONO, size: 8, color: "#E8EAED", bold: false },
    { text: "\n# Native: Scores traces via Vertex AI Eval Service", font: FONT_MONO, size: 8, color: "#81C995", bold: false },
    { text: "$ agents-cli eval grade \\\n    --traces tests/eval/output/basic-dataset.json \\\n    --config tests/eval/eval_config.yaml", font: FONT_MONO, size: 8, color: "#E8EAED", bold: false }
  ]);

  // =========================================================================
  // SLIDE 09: Custom Enterprise Governance Extension (Dark Stage #0E1015)
  // =========================================================================
  var s9 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupHeaderAndFooter(
    s9, true, "Live Demo  •  Act 4", "#F28B82",
    "Policy-as-Code: Custom sbom-deploy Gate",
    "AGENTS_CLI_DISABLE_OVERRIDES=1 lets wrapper scripts run Syft + Grype checks and call native deploy without recursion.",
    "09 / 10",
    "$ agents-cli extension add local@./extensions/sbom-deploy --yes",
    "AGENTS_CLI_DISABLE_OVERRIDES=1", "#81C995"
  );
  addStyledBox(s9, 36, 98, 318, 255, "#131314", "#3C4043", 1, true, [
    { text: "AGENTS-CLI-EXTENSION.YAML", font: FONT_HEADING, size: 8.5, color: "#FDD663", bold: true },
    { text: "schema: agents-cli-extension/v1alpha1\nname: sbom-deploy\ndescription: Scan project SBOM, then run native deploy.\nrequires:\n  agents_cli: \">=1.5,<2\"\n  on_incompatible: warn\n\ncommands:\n  override:\n    deploy:\n      run: [\"bash\", \"scripts/sbom_then_deploy.sh\"]\n  add:\n    sbom-report:\n      run: [\"bash\", \"scripts/sbom_report.sh\"]", font: FONT_MONO, size: 8, color: "#E8EAED", bold: false }
  ]);
  addStyledBox(s9, 366, 98, 318, 255, "#131314", "#3C4043", 1, true, [
    { text: "SCRIPTS/SBOM_THEN_DEPLOY.SH", font: FONT_HEADING, size: 8.5, color: "#81C995", bold: true },
    { text: "#!/usr/bin/env bash\nset -euo pipefail\n\necho \"[sbom-deploy] Generating CycloneDX SBOM...\"\nsyft dir:. -o cyclonedx-json > /tmp/sbom.cdx.json\n\necho \"[sbom-deploy] Scanning for critical CVEs...\"\ngrype sbom:/tmp/sbom.cdx.json --fail-on critical", font: FONT_MONO, size: 8, color: "#E8EAED", bold: false },
    { text: "\n# Loader sets AGENTS_CLI_DISABLE_OVERRIDES=1\n# Delegates to built-in deploy with zero recursion!", font: FONT_MONO, size: 8, color: "#8AB4F8", bold: true },
    { text: "exec agents-cli deploy \"$@\"", font: FONT_MONO, size: 8, color: "#81C995", bold: true }
  ]);

  // =========================================================================
  // SLIDE 10: Closing Bento Grid Summary + Bottom CTA Bar (Dark Stage #0E1015)
  // =========================================================================
  var s10 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  setupHeaderAndFooter(
    s10, true, "Google Cloud Next '27 Summary", "#8AB4F8",
    "The Open Agent Development Lifecycle",
    "",
    "10 / 10",
    null, null, null
  );
  var tiles = [
    { x: 36, y: 74, k: "01 • OPEN FRAMEWORKS", col: "#8AB4F8", h: "LangChain & LangGraph", d: "First-party template with zero google-adk dependency and unified CompiledStateGraph." },
    { x: 257, y: 74, k: "02 • LOCAL DEVELOPER EXPERIENCE", col: "#81C995", h: "LangGraph Studio", d: "agents-cli playground boots LangGraph dev server on port 8080 for visual graph inspection." },
    { x: 478, y: 74, k: "03 • QUALITY FLYWHEEL", col: "#FDD663", h: "Vertex AI Evaluations", d: "Overridden eval generate pairs seamlessly with native eval grade and eval compare." },
    { x: 36, y: 194, k: "04 • ENTERPRISE GOVERNANCE", col: "#F28B82", h: "SBOM Pre-Deploy Gates", d: "Wrap deploy with Syft + Grype checks and delegate safely via AGENTS_CLI_DISABLE_OVERRIDES=1." },
    { x: 257, y: 194, k: "05 • SUPPLY-CHAIN SECURITY", col: "#8AB4F8", h: "SHA Lockfile Discipline", d: "Pinned commit SHAs in agents-cli-extensions.yaml ensure bit-for-bit reproducible CI builds." },
    { x: 478, y: 194, k: "06 • SERVERLESS PRODUCTION", col: "#81C995", h: "Cloud Run + A2A Protocol", d: "Exposes /.well-known/agent.json and /a2a/tasks/send over FastAPI on port 8080." }
  ];
  for (var tIdx = 0; tIdx < tiles.length; tIdx++) {
    var tl = tiles[tIdx];
    addStyledBox(s10, tl.x, tl.y, 206, 108, "#161922", "#2D3343", 1, true, [
      { text: tl.k, font: FONT_MONO, size: 7.5, color: tl.col, bold: true },
      { text: tl.h, font: FONT_DISPLAY, size: 12, color: "#FFFFFF", bold: true },
      { text: tl.d, font: FONT_BODY, size: 8, color: "#9AA0A6", bold: false }
    ]);
  }
  addStyledBox(s10, 36, 316, 648, 56, "#131C31", "#4285F4", 1.5, true, [
    { text: "GET STARTED TODAY", font: FONT_HEADING, size: 8, color: "#8AB4F8", bold: true },
    { text: "https://github.com/sanketbisne/scalfod-langgraph-agentscli     |     uvx google-agents-cli setup", font: FONT_MONO, size: 10.5, color: "#FFFFFF", bold: true }
  ]);

  if (existingSlides.length === 1) {
    try { existingSlides[0].remove(); } catch (e) {}
  }
  Logger.log("Updated Google Slides Deck: " + deck.getUrl());
}
