#!/usr/bin/env bash
set -euo pipefail
echo "=== Validating sherpa-kits ==="

FAIL=0

# 1. Check catalog.json
if [ -f "catalog.json" ]; then
  if jq . catalog.json > /dev/null 2>&1; then
    echo "[OK] catalog.json is valid JSON."
  else
    echo "[FAIL] catalog.json is invalid JSON."
    FAIL=1
  fi
else
  echo "[FAIL] catalog.json missing."
  FAIL=1
fi

# 2. Validate all SHERPA.md files
for f in $(find domains -name "SHERPA.md" | sort); do
  if [ ! -f "$f" ]; then
    continue
  fi
  echo "Checking $f..."
  if ! head -n 1 "$f" | grep -q "^---$"; then
    echo "  [FAIL] $f missing YAML front matter."
    FAIL=1
  else
    echo "  [OK] $f front matter present."
  fi

  # Check for sensitive paths
  if grep -nE "(/home/[a-zA-Z0-9_-]+|/Users/[a-zA-Z0-9_-]+|[a-zA-Z]:\\\\Users\\\\[a-zA-Z0-9_-]+)" "$f" > /dev/null 2>&1; then
    echo "  [FAIL] $f contains hardcoded user home path!"
    FAIL=1
  fi

  # Check for private markers in public release
  if grep -n "confidentiality:[[:space:]]*\"private\"" "$f" > /dev/null 2>&1; then
    echo "  [FAIL] $f marked as confidentiality: private."
    FAIL=1
  fi
done

# 3. Check for standard repo documents
for doc in README.md LICENSE CONTRIBUTING.md SECURITY.md .gitignore; do
  if [ -f "$doc" ]; then
    echo "[OK] $doc present."
  else
    echo "[FAIL] $doc missing."
    FAIL=1
  fi
done

# 4. Check for forbidden private wording across the repository
PATTERN_PRIV="confidentiality:[[:space:]]*\"private\""
if grep -rnE "$PATTERN_PRIV" domains/ catalog.json > /dev/null 2>&1; then
  echo "[FAIL] Stale private confidentiality detected."
  FAIL=1
fi

if [ "$FAIL" -eq 1 ]; then
  echo "=== Validation FAILED ==="
  exit 1
fi

echo "=== All validations PASSED ==="
exit 0
