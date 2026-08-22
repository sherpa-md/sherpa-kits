#!/usr/bin/env bash
set -euo pipefail

echo "=== Validating sherpa-kits ==="
FAIL=0

if jq . catalog.json >/dev/null 2>&1; then
  echo "[PASS] catalog.json is valid JSON"
else
  echo "[FAIL] catalog.json is invalid JSON"
  FAIL=1
fi

if jq -e '([.kits[].id] | length) == ([.kits[].id] | unique | length)' catalog.json >/dev/null; then
  echo "[PASS] catalog kit IDs are unique"
else
  echo "[FAIL] catalog contains duplicate kit IDs"
  FAIL=1
fi

while IFS= read -r path; do
  if [[ -f "$path" ]]; then
    echo "[PASS] catalog path exists: $path"
  else
    echo "[FAIL] catalog path missing: $path"
    FAIL=1
  fi
done < <(jq -r '.kits[].path' catalog.json)

while IFS= read -r path; do
  if [[ -f "$path" ]]; then
    echo "[PASS] shareable Sherpa path exists: $path"
  else
    echo "[FAIL] shareable Sherpa path missing: $path"
    FAIL=1
  fi
done < <(jq -r '.kits[] | select(.share_path != null) | .share_path' catalog.json)

mapfile -t SHERPA_FILES < <(find kits -name SHERPA.md -type f | sort)
if python3 scripts/validate_sherpa.py "${SHERPA_FILES[@]}"; then
  echo "[PASS] SherpaMD front matter and secret checks"
else
  FAIL=1
fi

for doc in README.md LICENSE CONTRIBUTING.md SECURITY.md .gitignore; do
  if [[ -f "$doc" ]]; then
    echo "[PASS] $doc present"
  else
    echo "[FAIL] $doc missing"
    FAIL=1
  fi
done

if grep -rniE --include='*.md' 'one[- ]shot' . >/dev/null 2>&1; then
  echo "[FAIL] Deprecated help term detected; refer to the artifact as a Sherpa file"
  FAIL=1
else
  echo "[PASS] Sherpa file naming language"
fi

if grep -rnE --include='*.md' '(/home/[A-Za-z0-9_-]+|/Users/[A-Za-z0-9_-]+|[A-Za-z]:\\Users\\[A-Za-z0-9_-]+)' kits >/dev/null 2>&1; then
  echo "[FAIL] Hardcoded personal home path detected"
  FAIL=1
else
  echo "[PASS] No hardcoded personal home paths"
fi

if grep -rnE 'confidentiality:[[:space:]]*"private"' kits catalog.json >/dev/null 2>&1; then
  echo "[FAIL] Private confidentiality marker detected in public catalog"
  FAIL=1
else
  echo "[PASS] Public confidentiality markers"
fi

if [[ "$FAIL" -ne 0 ]]; then
  echo "=== Validation FAILED ==="
  exit 1
fi

echo "=== All validations PASSED ==="
