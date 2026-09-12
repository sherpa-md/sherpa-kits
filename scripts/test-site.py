#!/usr/bin/env python3
"""Parity and safety checks for the portable SherpaMD build."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def main() -> None:
    manifest_path = DIST / "index.json"
    if not manifest_path.exists():
        fail("dist/index.json is missing; run scripts/build-site.py first")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    items = manifest.get("items", [])
    source_paths = [item["source_path"] for item in items]

    expected = sorted(
        path.relative_to(ROOT).as_posix()
        for folder in ("handoffs", "kits", "candidates")
        for path in (ROOT / folder).rglob("*.sherpa.md")
    )
    if sorted(source_paths) != expected:
        fail(f"source/build mismatch: expected {len(expected)}, found {len(source_paths)}")
    if len(source_paths) != len(set(source_paths)):
        fail("duplicate source paths in index")
    if manifest.get("count") != len(expected):
        fail("manifest count does not match public source inventory")

    for item in items:
        source = ROOT / item["source_path"]
        raw = DIST / item["raw_url"].lstrip("/")
        detail = DIST / item["route"].strip("/") / "index.html"
        if not raw.exists() or not detail.exists():
            fail(f"missing raw or detail output for {item['source_path']}")
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        if source_hash != item["sha256"] or source.read_bytes() != raw.read_bytes():
            fail(f"hash/copy mismatch for {item['source_path']}")

    with zipfile.ZipFile(DIST / "all-sherpas.zip") as archive:
        if sorted(archive.namelist()) != expected:
            fail("all-sherpas.zip inventory mismatch")
    with zipfile.ZipFile(DIST / "sherpamd-portable-site.zip") as archive:
        names = set(archive.namelist())
        required = (
            "index.html",
            "index.json",
            "llms.txt",
            "ratings.json",
            "sitemap.xml",
            "REHOSTING.md",
            "assets/site.css",
            "assets/site.js",
            "all-sherpas.zip",
        )
        for name in required:
            if name not in names:
                fail(f"portable site archive is missing {name}")
        expected_site_files = {
            path.relative_to(DIST).as_posix()
            for path in DIST.rglob("*")
            if path.is_file() and path.name != "sherpamd-portable-site.zip"
        }
        if names != expected_site_files:
            fail("portable site archive does not exactly match the generated site")

        for item in items:
            raw_name = item["raw_url"].lstrip("/")
            detail_name = item["route"].strip("/") + "/index.html"
            if raw_name not in names or detail_name not in names:
                fail(f"portable site archive cannot serve {item['source_path']}")

    script = (DIST / "assets" / "site.js").read_text(encoding="utf-8")
    if "innerHTML" in script or "visually update anyway" in script:
        fail("unsafe or misleading client rendering pattern detected")
    if "button.disabled = true" not in script:
        fail("rating controls must be disabled without a real backend")
    if 'navigator.clipboard?.writeText' not in script or 'document.execCommand("copy")' not in script:
        fail("Use with AI must support secure and portable clipboard paths")
    if 'if (!copied) throw new Error("clipboard unavailable")' not in script:
        fail("Use with AI must not report an unconfirmed copy")
    ratings = json.loads((DIST / "ratings.json").read_text(encoding="utf-8"))
    if ratings.get("submit_url") != "https://github.com/sherpa-md/sherpa-kits/issues/new?template=rate-sherpa.yml":
        fail("official ratings snapshot must use the moderated GitHub issue form")
    for rating_contract in (
        'candidate.protocol === "https:"',
        'link.textContent = "Rate on GitHub"',
        'url.searchParams.set("title"',
        'link.setAttribute("aria-label"',
    ):
        if rating_contract not in script:
            fail(f"rating submission contract is missing: {rating_contract}")
    rating_template = (ROOT / ".github" / "ISSUE_TEMPLATE" / "rate-sherpa.yml").read_text(encoding="utf-8")
    for template_contract in (
        "5 — Built or used it successfully",
        "1 — Not usable for the stated outcome",
        "ratings do not promote a Sherpa",
        "employer data",
    ):
        if template_contract not in rating_template:
            fail(f"rating issue form contract is missing: {template_contract}")
    stylesheet = (DIST / "assets" / "site.css").read_text(encoding="utf-8")
    if ".rating-link" not in stylesheet or "min-height: 44px" not in stylesheet:
        fail("rating submission link must keep a mobile-safe touch target")
    for reader_contract in (
        "SpeechSynthesisUtterance",
        "speechEngine.pause()",
        "speechEngine.resume()",
        "speechEngine?.cancel()",
        "Code example omitted.",
    ):
        if reader_contract not in script:
            fail(f"reader contract is missing: {reader_contract}")
    index_html = (DIST / "index.html").read_text(encoding="utf-8")
    for reader_control in ("reader-player", "reader-toggle", "reader-rate", "reader-stop"):
        if f'id="{reader_control}"' not in index_html:
            fail(f"reader control is missing: {reader_control}")

    print(f"[PASS] source/build/download parity: {len(expected)}/{len(expected)}")
    print("[PASS] unique repository-relative raw paths and SHA-256 hashes")
    print("[PASS] complete site and all-Sherpas archives")
    print("[PASS] rehost archive exactly matches every generated route and download")
    print("[PASS] Use with AI has confirmed modern and static-host clipboard paths")
    print("[PASS] browser-native reader has pause, resume, stop, and speed controls")
    print("[PASS] ratings fail closed locally and submit through a moderated HTTPS form")
    print("[PASS] repository data uses DOM-safe rendering")


if __name__ == "__main__":
    main()
