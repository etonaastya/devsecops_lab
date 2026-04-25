#!/bin/bash
set -euo pipefail

UNIFIED_DIR="./unified-report"
mkdir -p "$UNIFIED_DIR"

# Копируем отчёты в unified
cp -f ./dependency-check-report/dependency-check-report.json "$UNIFIED_DIR/sca.json" 2>/dev/null || echo "[!] SCA report missing"
cp -f ../sast/semgrep-report.json "$UNIFIED_DIR/semgrep.json" 2>/dev/null || echo "[!] Semgrep report missing"
cp -f ../sast/checkov-report.json "$UNIFIED_DIR/checkov.json" 2>/dev/null || echo "[!] Checkov report missing"

# Генерируем сводку
cat > "$UNIFIED_DIR/summary.json" <<EOF
{
  "timestamp": "$(date -Iseconds)",
  "counts": {
    "semgrep": $(jq '.results | length' "$UNIFIED_DIR/semgrep.json" 2>/dev/null || echo 0),
    "checkov": $(jq '.results.failed_checks | length' "$UNIFIED_DIR/checkov.json" 2>/dev/null || echo 0),
    "sca": $(jq '[.dependencies[].vulnerabilities[]?] | length' "$UNIFIED_DIR/sca.json" 2>/dev/null || echo 0)
  },
  "status": "OK"
}
EOF

echo "✅ Unified report generated in: $UNIFIED_DIR"
cat "$UNIFIED_DIR/summary.json"
