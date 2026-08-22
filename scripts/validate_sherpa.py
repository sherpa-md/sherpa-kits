#!/usr/bin/env python3
"""Validate SherpaMD v0.1.0 front matter and common secret patterns."""

import os
import re
import sys

import yaml


REQUIRED_FIELDS = (
    "schema_version",
    "id",
    "title",
    "domain",
    "version",
    "status",
    "verification_state",
    "last_verified",
    "confidentiality",
    "provenance",
)
ALLOWED_STATUSES = {"draft", "active", "deprecated", "archived"}
ALLOWED_VERIFICATION_STATES = {"verified", "unverified", "needs-retest", "contradiction"}
ALLOWED_CONFIDENTIALITY = {"private", "internal", "restricted", "public"}
SECRET_PATTERNS = (
    r"ghp_[A-Za-z0-9_]{36}",
    r"github_pat_[A-Za-z0-9_]+",
    r"sk-[A-Za-z0-9_]{20,}",
    r"AIza[0-9A-Za-z-_]{35}",
    r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
)


def validate_sherpa_file(filepath):
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"

    with open(filepath, "r", encoding="utf-8") as handle:
        content = handle.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return False, "Missing or invalid YAML front matter"

    frontmatter_raw, body_raw = match.groups()
    try:
        data = yaml.safe_load(frontmatter_raw)
    except Exception as exc:
        return False, f"YAML parsing error: {exc}"

    if not isinstance(data, dict):
        return False, "Front matter must be a mapping"

    for field in REQUIRED_FIELDS:
        if field not in data:
            return False, f"Missing required field: {field}"

    if str(data["schema_version"]) != "0.1.0":
        return False, "Unsupported schema_version"
    if not re.fullmatch(r"[a-z0-9-]+", str(data["id"])):
        return False, "id must be kebab-case"
    if not re.fullmatch(r"[a-z0-9-]+", str(data["domain"])):
        return False, "domain must be kebab-case"
    if data["status"] not in ALLOWED_STATUSES:
        return False, "Invalid status"
    if data["verification_state"] not in ALLOWED_VERIFICATION_STATES:
        return False, "Invalid verification_state"
    if data["confidentiality"] not in ALLOWED_CONFIDENTIALITY:
        return False, "Invalid confidentiality"

    provenance = data["provenance"]
    if not isinstance(provenance, dict) or not provenance.get("author_alias"):
        return False, "provenance.author_alias is required"

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, content):
            return False, "Potential secret or private key detected"

    if not body_raw.strip():
        return False, "Markdown body is empty"

    return True, "Valid SherpaMD v0.1.0 document"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate_sherpa.py <file> [file ...]")
        raise SystemExit(1)

    passed = True
    for path in sys.argv[1:]:
        ok, message = validate_sherpa_file(path)
        print(f"[{'PASS' if ok else 'FAIL'}] {path}: {message}")
        passed = passed and ok

    raise SystemExit(0 if passed else 1)

