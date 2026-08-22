#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="$REPO_ROOT/dist"
OUTPUT_FILE="$OUTPUT_DIR/SherpaHandoffs.zip"

mkdir -p "$OUTPUT_DIR"
rm -f "$OUTPUT_FILE"

cd "$REPO_ROOT/handoffs"
zip -q "$OUTPUT_FILE" README.md ./*.sherpa.md

echo "$OUTPUT_FILE"

