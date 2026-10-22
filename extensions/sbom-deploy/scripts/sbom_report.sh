#!/usr/bin/env bash
# extensions/sbom-deploy/scripts/sbom_report.sh
set -euo pipefail

echo "============================================================"
echo "  [sbom-deploy] Supply-Chain & SBOM Report"
echo "============================================================"
if command -v syft >/dev/null 2>&1; then
  syft dir:. -o table
else
  echo "Project dependencies declared in pyproject.toml:"
  grep -A 15 "dependencies = \[" pyproject.toml || true
  echo ""
  echo "Tip: Install 'syft' and 'grype' for full CycloneDX container/directory scanning."
fi
