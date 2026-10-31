#!/usr/bin/env python3
"""Parity and safety checks for the portable SherpaMD build."""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def json_ld(document: str, label: str) -> dict:
    matches = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', document, re.DOTALL
    )
    if len(matches) != 1:
        fail(f"{label} must contain exactly one JSON-LD block")
    try:
        parsed = json.loads(matches[0])
    except json.JSONDecodeError as error:
        fail(f"{label} contains invalid JSON-LD: {error}")
    if not isinstance(parsed, dict):
        fail(f"{label} JSON-LD must be an object")
    return parsed


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

    all_tags: set[str] = set()
    for item in items:
        source_text = (ROOT / item["source_path"]).read_text(encoding="utf-8")
        frontmatter = re.match(r"^---\s*\n(.*?)\n---\s*\n", source_text, re.DOTALL)
        metadata = yaml.safe_load(frontmatter.group(1)) if frontmatter else {}
        expected_tags = sorted(metadata.get("tags", [])) if isinstance(metadata, dict) else []
        if item.get("tags") != expected_tags:
            fail(f"tag discovery mismatch for {item['source_path']}")
        expected_last_verified = metadata.get("last_verified") if isinstance(metadata, dict) else None
        if item.get("last_verified") != expected_last_verified:
            fail(f"assessment date mismatch for {item['source_path']}")
        if len(item["tags"]) != len(set(item["tags"])):
            fail(f"duplicate tags in {item['source_path']}")
        all_tags.update(item["tags"])

    projects = json.loads((DIST / "projects.json").read_text(encoding="utf-8"))
    expected_families = sorted(
        path.name for path in (ROOT / "projects").iterdir() if path.is_dir() and (path / "README.md").is_file()
    )
    actual_families = sorted(family["slug"] for family in projects.get("families", []))
    if actual_families != expected_families or projects.get("family_count") != len(expected_families):
        fail("community project family discovery mismatch")
    expected_builds = sorted(
        (family.name, build.name)
        for family in (ROOT / "projects").iterdir()
        if family.is_dir()
        for build in family.iterdir()
        if build.is_dir() and (build / "README.md").is_file()
    )
    actual_builds = sorted(
        (family["slug"], build["slug"])
        for family in projects["families"]
        for build in family["builds"]
    )
    if actual_builds != expected_builds or projects.get("build_count") != len(expected_builds):
        fail("community project build discovery mismatch")
    projects_html = (DIST / "projects" / "index.html").read_text(encoding="utf-8")
    if "Community projects are not official verified releases." not in projects_html:
        fail("community project page must preserve the verification boundary")
    if "share-community-project.yml" not in projects_html or "PROJECT_TEMPLATE.md" not in projects_html:
        fail("community project page must expose both guided and pull-request contribution paths")
    expected_project_entries = [
        {
            "@type": "ListItem",
            "position": position,
            "url": family["source_url"],
            "name": family["title"],
        }
        for position, family in enumerate(projects["families"], start=1)
    ]
    expected_projects_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": "https://sherpamd.org/projects/",
        "url": "https://sherpamd.org/projects/",
        "name": "Community Projects — SherpaMD",
        "description": "Working community implementations built from Sherpa Kits.",
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(expected_project_entries),
            "itemListElement": expected_project_entries,
        },
    }
    if json_ld(projects_html, "community projects page") != expected_projects_schema:
        fail("community project JSON-LD does not match public project metadata")
    if '<link rel="describedby" href="../llms.txt">' not in projects_html:
        fail("community project page must identify its covering llms.txt")
    if '<link rel="alternate" type="text/markdown"' in projects_html:
        fail("community project page must not claim a nonexistent Markdown twin")
    if '<a href="../LICENSE">MIT license</a>' not in projects_html:
        fail("community project page must link to the portable license")

    catalog_html = (DIST / "index.html").read_text(encoding="utf-8")
    expected_catalog_entries = [
        {
            "@type": "ListItem",
            "position": position,
            "url": f"https://sherpamd.org{item['route']}",
            "name": item["title"],
        }
        for position, item in enumerate(items, start=1)
    ]
    expected_catalog_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": "https://sherpamd.org/",
        "url": "https://sherpamd.org/",
        "name": "Browse Sherpas — SherpaMD",
        "description": "Find a guide, give it to your AI, and build something useful.",
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(expected_catalog_entries),
            "itemListElement": expected_catalog_entries,
        },
    }
    if json_ld(catalog_html, "catalog page") != expected_catalog_schema:
        fail("catalog JSON-LD does not match the complete Sherpa manifest")
    if '<link rel="describedby" href="llms.txt">' not in catalog_html:
        fail("catalog page must identify its covering llms.txt")
    if '<link rel="alternate" type="text/markdown"' in catalog_html:
        fail("catalog page must not claim a nonexistent Markdown twin")
    if '<a href="LICENSE">MIT license</a>' not in catalog_html:
        fail("catalog page must link to the portable license")

    llms_text = (DIST / "llms.txt").read_text(encoding="utf-8")
    if not llms_text.startswith(
        f"# SherpaMD\n\n> {len(items)} public Sherpa files. GitHub Markdown is the source of truth.\n"
    ):
        fail("llms.txt must identify the complete GitHub-sourced catalog")
    for boundary in (
        "Use each lifecycle and verification label exactly as written.",
        "not a guarantee for every environment",
        "protect private data",
        "require tests",
    ):
        if boundary not in llms_text:
            fail(f"llms.txt safety boundary is missing: {boundary}")
    expected_states = sorted({item["verification_state"] for item in items})
    actual_states = re.findall(r"^## Verification state: (.+)$", llms_text, re.MULTILINE)
    if actual_states != expected_states:
        fail("llms.txt verification-state sections do not match the manifest")
    for item in items:
        assessed = item["last_verified"] or "not recorded"
        expected_entry = (
            f"- [{item['title']}]({item['raw_url']}): "
            f"Stable ID `{item['key']}`; version `{item['version']}`; "
            f"lifecycle `{item['status']}`; last assessed `{assessed}`; "
            f"SHA-256 `{item['sha256']}`. {item['summary']}"
        )
        if llms_text.count(expected_entry) != 1:
            fail(f"llms.txt agent metadata mismatch for {item['source_path']}")

    robots_text = (DIST / "robots.txt").read_text(encoding="utf-8")
    if robots_text != (
        "User-agent: *\n"
        "Allow: /\n"
        "Sitemap: https://sherpamd.org/sitemap.xml\n"
    ):
        fail("robots.txt must allow the public catalog and identify the canonical sitemap")

    for item in items:
        source = ROOT / item["source_path"]
        raw = DIST / item["raw_url"].lstrip("/")
        detail = DIST / item["route"].strip("/") / "index.html"
        if not raw.exists() or not detail.exists():
            fail(f"missing raw or detail output for {item['source_path']}")
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        if source_hash != item["sha256"] or source.read_bytes() != raw.read_bytes():
            fail(f"hash/copy mismatch for {item['source_path']}")
        detail_html = detail.read_text(encoding="utf-8")
        social_title = html.escape(f"{item['title']} — SherpaMD", quote=True)
        social_description = html.escape(item["summary"], quote=True)
        canonical_url = f"https://sherpamd.org{item['route']}"
        for social_contract in (
            '<meta property="og:site_name" content="SherpaMD">',
            '<meta property="og:type" content="article">',
            f'<meta property="og:title" content="{social_title}">',
            f'<meta property="og:description" content="{social_description}">',
            f'<meta property="og:url" content="{canonical_url}">',
            '<meta name="twitter:card" content="summary">',
            f'<meta name="twitter:title" content="{social_title}">',
            f'<meta name="twitter:description" content="{social_description}">',
        ):
            if social_contract not in detail_html:
                fail(f"social preview metadata mismatch for {item['source_path']}")
        route_depth = len(item["route"].strip("/").split("/"))
        relative_root = "../" * route_depth
        for agent_discovery_contract in (
            f'<link rel="describedby" href="{relative_root}llms.txt">',
            '<link rel="alternate" type="text/markdown" '
            f'href="{relative_root}{item["raw_url"].lstrip("/")}">',
        ):
            if agent_discovery_contract not in detail_html:
                fail(f"agent discovery link mismatch for {item['source_path']}")
        if f'<a href="{relative_root}LICENSE">MIT license</a>' not in detail_html:
            fail(f"portable license link mismatch for {item['source_path']}")
        expected_detail_schema = {
            "@context": "https://schema.org",
            "@type": "Guide",
            "@id": canonical_url,
            "url": canonical_url,
            "name": item["title"],
            "description": item["summary"],
            "identifier": item["key"],
            "version": item["version"],
            "creativeWorkStatus": item["status"],
            "keywords": item["tags"],
            "isBasedOn": item["source_url"],
            "mainEntityOfPage": canonical_url,
            "about": {
                "@type": "DefinedTerm",
                "name": item["verification_state"],
                "termCode": item["verification_state"],
                "inDefinedTermSet": {
                    "@type": "DefinedTermSet",
                    "name": "SherpaMD verification states",
                    "url": "https://github.com/sherpa-md/sherpa-kits/blob/main/CONTRIBUTING.md",
                },
            },
            "encoding": {
                "@type": "MediaObject",
                "contentUrl": f"https://sherpamd.org{item['raw_url']}",
                "encodingFormat": "text/markdown",
                "sha256": item["sha256"],
            },
        }
        if json_ld(detail_html, item["source_path"]) != expected_detail_schema:
            fail(f"structured discovery metadata mismatch for {item['source_path']}")
        for agent_guide_contract in (
            '<details class="agent-guide">',
            "Check its state.",
            "Select Use with AI.",
            "approved AI environment",
            "tests and evidence",
        ):
            if agent_guide_contract not in detail_html:
                fail(f"AI agent usage guide is missing for {item['source_path']}")

    with zipfile.ZipFile(DIST / "all-sherpas.zip") as archive:
        if sorted(archive.namelist()) != expected:
            fail("all-sherpas.zip inventory mismatch")
    if (DIST / "LICENSE").read_bytes() != (ROOT / "LICENSE").read_bytes():
        fail("portable site must preserve the repository license exactly")
    with zipfile.ZipFile(DIST / "sherpamd-portable-site.zip") as archive:
        names = set(archive.namelist())
        required = (
            "index.html",
            "index.json",
            "llms.txt",
            "ratings.json",
            "projects.json",
            "projects/index.html",
            "robots.txt",
            "sitemap.xml",
            "LICENSE",
            "REHOSTING.md",
            "update-rehost.py",
            "verify-rehost.py",
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
    for handoff_contract in (
        "function agentHandoff(record, raw)",
        "Stable ID: ${record.key}",
        "Verification state: ${record.verification_state}",
        "Status: ${record.status}",
        "Version: ${record.version}",
        "SHA-256: ${record.sha256}",
        "Canonical source: ${record.source_url}",
        "Treat the verification state exactly as written.",
        "Draft or unverified content is not validated.",
        "agentHandoff(record, raw)",
    ):
        if handoff_contract not in script:
            fail(f"traceable AI handoff contract is missing: {handoff_contract}")
    for share_contract in (
        "navigator.share",
        'error?.name === "AbortError"',
        "writeClipboard(url)",
        'button("Share")',
        'url.pathname.replace(/index\\.html$/, "")',
    ):
        if share_contract not in script:
            fail(f"mobile share contract is missing: {share_contract}")
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
    if ".card-actions .button { min-height: 44px" not in stylesheet:
        fail("Sherpa actions must keep mobile-safe touch targets")
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
    for explainer_contract in (
        'aria-labelledby="how-sherpas-work"',
        'id="how-sherpas-work"',
        "A Sherpa is readable Markdown—not an app by itself.",
        "Choose and check.",
        "Give it to your AI.",
        "Build safely and verify.",
        "approved AI environment",
    ):
        if explainer_contract not in index_html:
            fail(f"Sherpa usage explainer is missing: {explainer_contract}")
    if 'id="topic-filter"' not in index_html:
        fail("topic filter is missing from the catalog")
    for tag in all_tags:
        if f'<option value="{tag}">{tag}</option>' not in index_html:
            fail(f"topic filter is missing tag: {tag}")
    for topic_contract in ('record.tags.join(" ")', 'record.tags.includes(topic)', '"topic-filter"'):
        if topic_contract not in script:
            fail(f"topic discovery contract is missing: {topic_contract}")
    for topic_link_contract in (
        "function topicHref(tag)",
        'url.searchParams.set("topic", tag)',
        'node.className = "tag tag--link"',
        "Browse Sherpas about ${tag}",
    ):
        if topic_link_contract not in script:
            fail(f"clickable topic discovery contract is missing: {topic_link_contract}")
    if ".tag--link" not in stylesheet or "min-height: 44px" not in stylesheet:
        fail("clickable topic labels must keep a mobile-safe touch target")
    for sort_option in (
        '<option value="verified-first">Verified first</option>',
        '<option value="assessed">Recently assessed</option>',
        '<option value="title">Title A–Z</option>',
    ):
        if sort_option not in index_html:
            fail(f"catalog sort option is missing: {sort_option}")
    for sort_contract in (
        "function compareRecords(",
        'right.verification_state === "verified"',
        '(right.last_verified || "").localeCompare(left.last_verified || "")',
        '"sort-order"',
    ):
        if sort_contract not in script:
            fail(f"catalog sorting contract is missing: {sort_contract}")
    for view_contract in (
        'id="copy-view-link"',
        'id="clear-filters"',
        'function restoreCatalogView()',
        'function saveCatalogView()',
        'function resetCatalogView()',
        'url.searchParams.set(key, value)',
        'window.history.replaceState(null, "", url.toString())',
        'writeClipboard(window.location.href)',
    ):
        if view_contract not in index_html and view_contract not in script:
            fail(f"shareable catalog view contract is missing: {view_contract}")
    if 'id="catalog-label-guide"' not in index_html:
        fail("catalog verification label guide mount is missing")
    for label_guide_contract in (
        "function labelGuide()",
        "What the labels mean",
        "Validation evidence exists for the stated scope.",
        "No completed validation claim is recorded.",
        "Earlier evidence exists, but the current version or environment still needs validation.",
        "this status does not itself mean verified.",
        "do not treat it as production-ready.",
        "Labels describe repository evidence—not approval for your environment.",
        'byId("catalog-label-guide")?.replaceChildren(labelGuide())',
        "badges, labelGuide(), assessmentFragment(record)",
    ):
        if label_guide_contract not in script:
            fail(f"verification label guide contract is missing: {label_guide_contract}")
    for label_guide_style in (".label-guide", ".label-guide summary", ".label-guide__list", ".label-guide__item"):
        if label_guide_style not in stylesheet:
            fail(f"verification label guide style is missing: {label_guide_style}")
    for integrity_contract in (
        "function integrityFragment(record)",
        'section.setAttribute("aria-labelledby", "file-integrity-title")',
        'heading.textContent = "File integrity"',
        '["Stable ID", record.key]',
        '["Version", record.version]',
        '["SHA-256", record.sha256]',
        'button("Copy SHA-256")',
        "writeClipboard(record.sha256)",
        'toast(copied ? "SHA-256 copied."',
        "it does not make the Sherpa verified for your environment.",
        "integrityFragment(record)",
    ):
        if integrity_contract not in script:
            fail(f"download integrity contract is missing: {integrity_contract}")
    for integrity_style in (".integrity-panel", ".integrity-panel__facts", ".integrity-panel__note", "overflow-wrap: anywhere"):
        if integrity_style not in stylesheet:
            fail(f"download integrity style is missing: {integrity_style}")
    for inline_reader_contract in (
        "function inlineReader(record)",
        'summary.textContent = "Read full Sherpa Markdown"',
        'actions.className = "inline-reader__actions"',
        'button("Copy full Markdown")',
        'content.setAttribute("aria-label", `Full Markdown for ${record.title}`)',
        'content.textContent = "Loading Markdown…"',
        "markdownPromise = rawText(record)",
        "writeClipboard(await loadMarkdown())",
        'toast(copied ? "Full Markdown copied."',
        "content.textContent = await loadMarkdown()",
        'content.textContent = "Markdown unavailable. Use Download .md or GitHub instead."',
        "details.dataset.loaded",
        "details.append(summary, actions, content)",
        "integrityFragment(record), inlineReader(record), relatedFragment(record)",
    ):
        if inline_reader_contract not in script:
            fail(f"inline Sherpa reader contract is missing: {inline_reader_contract}")
    for inline_reader_style in (".inline-reader", ".inline-reader summary", ".inline-reader__actions", ".inline-reader__content", "white-space: pre-wrap"):
        if inline_reader_style not in stylesheet:
            fail(f"inline Sherpa reader style is missing: {inline_reader_style}")
    for assessment_contract in (
        "function assessmentFragment(",
        'row.append("Last assessed: ")',
        'row.append("not recorded")',
        "assessmentFragment(record)",
    ):
        if assessment_contract not in script:
            fail(f"assessment date contract is missing: {assessment_contract}")
    for related_contract in (
        "function relatedRecords(record, limit = 3)",
        "candidate.key !== record.key",
        "right.sharedTopics.length - left.sharedTopics.length",
        'right.candidate.verification_state === "verified"',
        "function relatedFragment(record)",
        "Related by public topics and domain—not verification or endorsement.",
        "relatedFragment(record)",
    ):
        if related_contract not in script:
            fail(f"related Sherpa discovery contract is missing: {related_contract}")
    for related_style in (".related-sherpas", ".related-list", ".related-card"):
        if related_style not in stylesheet:
            fail(f"related Sherpa layout is missing: {related_style}")
    for reader_control in ("reader-player", "reader-toggle", "reader-rate", "reader-stop"):
        if f'id="{reader_control}"' not in index_html:
            fail(f"reader control is missing: {reader_control}")

    with tempfile.TemporaryDirectory(prefix="sherpamd-rehost-test-") as temporary:
        mirror = Path(temporary) / "mirror"
        updater = DIST / "update-rehost.py"
        archive = DIST / "sherpamd-portable-site.zip"
        command = [sys.executable, str(updater), "--archive", str(archive), "--root", str(mirror)]
        dry_run = subprocess.run(command + ["--dry-run"], capture_output=True, text=True)
        if dry_run.returncode or "no files changed" not in dry_run.stdout:
            fail(f"rehost updater dry-run failed: {dry_run.stderr or dry_run.stdout}")
        install = subprocess.run(command, capture_output=True, text=True)
        if install.returncode or not (mirror / "current").is_symlink():
            fail(f"rehost updater install failed: {install.stderr or install.stdout}")
        current_manifest = json.loads((mirror / "current" / "index.json").read_text(encoding="utf-8"))
        if current_manifest.get("source_commit") != manifest.get("source_commit"):
            fail("rehost updater activated the wrong source commit")
        repeat = subprocess.run(command, capture_output=True, text=True)
        if repeat.returncode or "already installed" not in repeat.stdout:
            fail(f"rehost updater repeat run is not idempotent: {repeat.stderr or repeat.stdout}")
        previous_target = (mirror / "current").readlink()
        rejected = subprocess.run(
            command + ["--expect-source-commit", "0" * 40], capture_output=True, text=True
        )
        if rejected.returncode == 0 or "expected source commit" not in rejected.stderr:
            fail("rehost updater did not reject an unexpected source commit")
        if (mirror / "current").readlink() != previous_target:
            fail("a rejected rehost update changed the active release")

        verifier = DIST / "verify-rehost.py"
        verify = subprocess.run(
            [
                sys.executable,
                str(verifier),
                "--site-dir",
                str(DIST),
                "--canonical-index",
                str(DIST / "index.json"),
            ],
            capture_output=True,
            text=True,
        )
        if verify.returncode or f"{len(expected)}/{len(expected)} Sherpa identities" not in verify.stdout:
            fail(f"rehost verifier rejected the canonical build: {verify.stderr or verify.stdout}")
        stale = subprocess.run(
            [
                sys.executable,
                str(verifier),
                "--site-dir",
                str(DIST),
                "--canonical-index",
                str(DIST / "index.json"),
                "--expect-source-commit",
                "0" * 40,
            ],
            capture_output=True,
            text=True,
        )
        if stale.returncode == 0 or "expected source commit" not in stale.stderr:
            fail("rehost verifier did not reject an unexpected source commit")

        altered_site = Path(temporary) / "altered-site"
        shutil.copytree(DIST, altered_site)
        altered_raw = altered_site / items[0]["raw_url"].lstrip("/")
        altered_raw.write_bytes(altered_raw.read_bytes() + b"\nchanged\n")
        altered = subprocess.run(
            [
                sys.executable,
                str(verifier),
                "--site-dir",
                str(altered_site),
                "--canonical-index",
                str(DIST / "index.json"),
            ],
            capture_output=True,
            text=True,
        )
        if altered.returncode == 0 or "raw file hash mismatch" not in altered.stderr:
            fail("rehost verifier did not reject altered Sherpa content")

        missing_discovery = Path(temporary) / "missing-discovery"
        shutil.copytree(DIST, missing_discovery)
        (missing_discovery / "robots.txt").unlink()
        missing_discovery_check = subprocess.run(
            [
                sys.executable,
                str(verifier),
                "--site-dir",
                str(missing_discovery),
                "--canonical-index",
                str(DIST / "index.json"),
            ],
            capture_output=True,
            text=True,
        )
        if (
            missing_discovery_check.returncode == 0
            or "robots.txt" not in missing_discovery_check.stderr
        ):
            fail("rehost verifier did not reject a mirror missing robots.txt")

        missing_discovery_archive = Path(temporary) / "missing-discovery.zip"
        with zipfile.ZipFile(archive) as source_archive, zipfile.ZipFile(
            missing_discovery_archive, "w", zipfile.ZIP_DEFLATED
        ) as incomplete_archive:
            for name in source_archive.namelist():
                if name != "robots.txt":
                    incomplete_archive.writestr(name, source_archive.read(name))
        incomplete_update = subprocess.run(
            [
                sys.executable,
                str(updater),
                "--archive",
                str(missing_discovery_archive),
                "--root",
                str(mirror),
                "--dry-run",
            ],
            capture_output=True,
            text=True,
        )
        if incomplete_update.returncode == 0 or "robots.txt" not in incomplete_update.stderr:
            fail("rehost updater did not reject a snapshot missing robots.txt")

        missing_license = Path(temporary) / "missing-license"
        shutil.copytree(DIST, missing_license)
        (missing_license / "LICENSE").unlink()
        missing_license_check = subprocess.run(
            [
                sys.executable,
                str(verifier),
                "--site-dir",
                str(missing_license),
                "--canonical-index",
                str(DIST / "index.json"),
            ],
            capture_output=True,
            text=True,
        )
        if missing_license_check.returncode == 0 or "LICENSE" not in missing_license_check.stderr:
            fail("rehost verifier did not reject a mirror missing the license")

        missing_license_archive = Path(temporary) / "missing-license.zip"
        with zipfile.ZipFile(archive) as source_archive, zipfile.ZipFile(
            missing_license_archive, "w", zipfile.ZIP_DEFLATED
        ) as incomplete_archive:
            for name in source_archive.namelist():
                if name != "LICENSE":
                    incomplete_archive.writestr(name, source_archive.read(name))
        incomplete_license_update = subprocess.run(
            [
                sys.executable,
                str(updater),
                "--archive",
                str(missing_license_archive),
                "--root",
                str(mirror),
                "--dry-run",
            ],
            capture_output=True,
            text=True,
        )
        if incomplete_license_update.returncode == 0 or "LICENSE" not in incomplete_license_update.stderr:
            fail("rehost updater did not reject a snapshot missing the license")

    print(f"[PASS] source/build/download parity: {len(expected)}/{len(expected)}")
    print("[PASS] unique repository-relative raw paths and SHA-256 hashes")
    print("[PASS] complete site and all-Sherpas archives")
    print("[PASS] portable site preserves the exact repository license")
    print("[PASS] rehost archive exactly matches every generated route and download")
    print("[PASS] Use with AI has confirmed modern and static-host clipboard paths")
    print("[PASS] AI handoffs include source, identity, version, hash, and verification context")
    print("[PASS] detail routes expose copyable SHA-256 integrity metadata without changing verification")
    print("[PASS] catalog and detail routes explain verification and lifecycle labels")
    print("[PASS] detail routes safely expose complete Sherpa Markdown inline")
    print("[PASS] mobile sharing uses a native share sheet with a confirmed stable-link fallback")
    print("[PASS] every Sherpa detail route has escaped Open Graph and social-card metadata")
    print("[PASS] Schema.org JSON-LD matches the catalog, projects, and all Sherpa metadata")
    print("[PASS] catalog and detail routes explain safe, evidence-bound AI agent use")
    print("[PASS] browser-native reader has pause, resume, stop, and speed controls")
    print("[PASS] ratings fail closed locally and submit through a moderated HTTPS form")
    print(f"[PASS] tag-aware search and topic filtering: {len(all_tags)} topics")
    print(f"[PASS] community project discovery: {len(expected_families)} families / {len(expected_builds)} builds")
    print("[PASS] repository data uses DOM-safe rendering")
    print("[PASS] rehost updater verifies, installs atomically, reruns idempotently, and fails closed")
    print("[PASS] independent rehost verifier proves live parity and rejects stale commits")


if __name__ == "__main__":
    main()
