#!/usr/bin/env python3
"""Build the self-contained, read-only SherpaMD portable catalog."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path, PurePosixPath

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOTS = ("handoffs", "kits", "candidates")
PORTABLE_ROOT = REPO_ROOT / "portable-site"
ASSET_ROOT = PORTABLE_ROOT / "src"
RATINGS_SNAPSHOT = PORTABLE_ROOT / "data" / "ratings.json"
PRODUCTION_ORIGIN = "https://sherpamd.org"
GITHUB_BLOB = "https://github.com/sherpa-md/sherpa-kits/blob/main"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=REPO_ROOT / "dist")
    return parser.parse_args()


def frontmatter(text: str) -> tuple[dict, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not match:
        return {}, text
    parsed = yaml.safe_load(match.group(1))
    if not isinstance(parsed, dict):
        raise ValueError("front matter must be a mapping")
    return parsed, match.group(2)


def kebab(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value)
    value = re.sub(r"[^A-Za-z0-9]+", "-", value)
    return value.strip("-").lower()


def first_heading(body: str, fallback: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def first_summary(body: str, fallback: str) -> str:
    paragraphs: list[str] = []
    current: list[str] = []
    in_code = False
    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.startswith(("#", ">", "|", "- ", "* ")) or re.match(r"^\d+\.\s", line):
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        if line:
            current.append(line)
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    for paragraph in paragraphs:
        cleaned = re.sub(r"[`*_\[\]()]", "", paragraph).strip()
        if len(cleaned) >= 35:
            return cleaned[:237] + ("…" if len(cleaned) > 237 else "")
    return fallback


def load_catalog() -> tuple[dict[str, dict], dict[str, dict]]:
    catalog = json.loads((REPO_ROOT / "catalog.json").read_text(encoding="utf-8"))
    by_path: dict[str, dict] = {}
    by_share_path: dict[str, dict] = {}
    for item in catalog.get("kits", []):
        if item.get("path"):
            by_path[item["path"]] = item
        if item.get("share_path"):
            by_share_path[item["share_path"]] = item
    return by_path, by_share_path


def route_for(relative_path: str) -> str:
    path = PurePosixPath(relative_path)
    kind = path.parts[0]
    if kind == "handoffs":
        return f"/handoffs/{path.name.removesuffix('.sherpa.md')}/"
    return f"/{kind}/{path.parent.name}/"


def source_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def discover() -> list[dict]:
    catalog_by_path, catalog_by_share = load_catalog()
    records: list[dict] = []
    seen_paths: set[str] = set()
    seen_keys: set[str] = set()

    for root_name in SOURCE_ROOTS:
        root = REPO_ROOT / root_name
        for path in sorted(root.rglob("*.sherpa.md")):
            relative_path = path.relative_to(REPO_ROOT).as_posix()
            if relative_path in seen_paths:
                raise ValueError(f"duplicate source path: {relative_path}")
            seen_paths.add(relative_path)

            raw = path.read_text(encoding="utf-8")
            metadata, body = frontmatter(raw)
            catalog_item = catalog_by_path.get(relative_path) or catalog_by_share.get(relative_path) or {}
            confidentiality = metadata.get("confidentiality", catalog_item.get("confidentiality"))
            if confidentiality and confidentiality != "public":
                continue
            if not metadata and root_name != "handoffs":
                raise ValueError(f"missing front matter outside handoffs: {relative_path}")

            derived_id = kebab(path.name.removesuffix(".sherpa.md"))
            item_id = str(metadata.get("id") or catalog_item.get("id") or derived_id)
            kind = root_name.removesuffix("s")
            key = f"{kind}:{item_id}"
            if key in seen_keys:
                raise ValueError(f"duplicate portable key: {key}")
            seen_keys.add(key)

            title = str(metadata.get("title") or first_heading(body, path.stem))
            domain = str(metadata.get("domain") or catalog_item.get("domain") or "general")
            status = str(metadata.get("status") or catalog_item.get("status") or "draft")
            verification = str(
                metadata.get("verification_state")
                or catalog_item.get("verification_state")
                or "unverified"
            )
            version = str(metadata.get("version") or catalog_item.get("version") or "unversioned")
            summary = str(
                metadata.get("summary")
                or metadata.get("description")
                or first_summary(body, f"Open {title} to review the complete Sherpa instructions.")
            )
            raw_url = "/raw/" + relative_path
            route = route_for(relative_path)
            records.append(
                {
                    "key": key,
                    "id": item_id,
                    "kind": kind,
                    "title": title,
                    "summary": summary,
                    "domain": domain,
                    "version": version,
                    "status": status,
                    "verification_state": verification,
                    "source_path": relative_path,
                    "source_url": f"{GITHUB_BLOB}/{relative_path}",
                    "raw_url": raw_url,
                    "route": route,
                    "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                    "raw": raw,
                }
            )

    return sorted(records, key=lambda item: (item["kind"], item["title"].casefold(), item["source_path"]))


def safe_json(data: object) -> str:
    return (
        json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def relative_from(route: str, target: str) -> str:
    route_dir = route.strip("/")
    target_path = target.lstrip("/") or "."
    relative = os.path.relpath(target_path, route_dir or ".").replace(os.sep, "/")
    if target == "/":
        return "./" if relative == "." else relative.rstrip("/") + "/"
    return relative


def shell(records: list[dict], *, detail: dict | None = None) -> str:
    payload = [{key: value for key, value in record.items() if key != "raw"} for record in records]
    detail_title = detail["title"] if detail else "Browse Sherpas"
    description = detail["summary"] if detail else "Find a guide, give it to your AI, and build something useful."
    route = detail["route"] if detail else "/"
    asset_prefix = relative_from(route, "/assets/site.css")
    home_prefix = relative_from(route, "/index.html")
    body_class = "detail-page" if detail else "catalog-page"
    detail_key = detail["key"] if detail else ""
    canonical = PRODUCTION_ORIGIN + route
    content = (
        '<main id="main" class="page"><section class="detail-shell" id="detail-root" '
        f'data-detail-key="{html.escape(detail_key, quote=True)}"></section></main>'
        if detail
        else """<main id="main" class="page">
  <section class="catalog-intro" aria-labelledby="catalog-title">
    <div><p class="eyebrow">MD means Markdown</p><h1 id="catalog-title">Find a Sherpa. Build the outcome.</h1><p>Portable guides that people can read and capable AI agents can execute.</p></div>
    <div class="bundle-actions" aria-label="Download options">
      <a class="button button--primary" href="all-sherpas.zip" download>Download all Sherpas</a>
      <a class="button" href="sherpamd-portable-site.zip" download>Download this site</a>
    </div>
  </section>
  <section class="catalog-tools" aria-label="Find Sherpas">
    <label class="search-field"><span>Search</span><input id="search" type="search" placeholder="Try photos, private data, Discord…" autocomplete="off"></label>
    <label><span>Type</span><select id="kind-filter"><option value="">All types</option><option value="handoff">Handoffs</option><option value="kit">Kits</option><option value="candidate">Candidates</option></select></label>
    <label><span>Verification</span><select id="verification-filter"><option value="">All states</option><option value="verified">Verified</option><option value="unverified">Unverified</option><option value="needs-retest">Needs retest</option></select></label>
  </section>
  <p class="results-summary" id="results-summary" aria-live="polite"></p>
  <section class="card-grid" id="catalog-grid" aria-label="Sherpa catalog"></section>
  <section class="empty-state" id="empty-state" hidden><h2>No Sherpas match</h2><p>Clear a filter or try a broader search.</p></section>
</main>"""
    )
    return f"""<!doctype html>
<html lang="en" data-route="{html.escape(route, quote=True)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>{html.escape(detail_title)} — SherpaMD</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <link rel="canonical" href="{html.escape(canonical, quote=True)}">
  <link rel="stylesheet" href="{asset_prefix}">
</head>
<body class="{body_class}">
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="site-header__inner">
  <a class="brand" href="{home_prefix}" aria-label="SherpaMD home"><span class="brand-mark" aria-hidden="true">SM</span><span>SherpaMD<small>MD = Markdown</small></span></a>
  <nav aria-label="Primary"><a href="{home_prefix}">Browse</a><a href="https://github.com/sherpa-md/sherpa-kits/tree/main/projects">Projects</a><a href="https://github.com/sherpa-md/sherpa-kits/blob/main/CONTRIBUTING.md">Contribute</a><a href="https://github.com/sherpa-md">GitHub</a></nav>
</div></header>
{content}
<dialog id="preview-dialog" aria-labelledby="preview-title"><div class="dialog-head"><h2 id="preview-title">Sherpa preview</h2><button id="dialog-close" class="icon-button" aria-label="Close preview">×</button></div><pre id="preview-content" tabindex="0"></pre><div class="dialog-actions"><button id="dialog-copy" class="button button--primary">Use with AI</button><a id="dialog-download" class="button" download>Download .md</a></div></dialog>
<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>
<footer><div><strong>SherpaMD</strong><span>Readable by people. Followable by AI.</span></div><div><a href="{relative_from(route, '/index.json')}">index.json</a><a href="{relative_from(route, '/llms.txt')}">llms.txt</a><a href="{relative_from(route, '/ratings.json')}">ratings snapshot</a></div></footer>
<script id="sherpa-data" type="application/json">{safe_json(payload)}</script>
<script>window.SHERPA_DETAIL_KEY={safe_json(detail_key)};window.SHERPA_ASSET_PREFIX={safe_json(relative_from(route, '/'))};</script>
<script src="{relative_from(route, '/assets/site.js')}" defer></script>
</body>
</html>"""


def load_ratings(records: list[dict]) -> dict:
    if not RATINGS_SNAPSHOT.exists():
        return {"schema_version": "1", "generated_at": None, "submit_url": None, "ratings": {}}
    data = json.loads(RATINGS_SNAPSHOT.read_text(encoding="utf-8"))
    if not isinstance(data.get("ratings"), dict):
        raise ValueError("ratings snapshot must contain a ratings mapping")
    current = {record["key"]: record for record in records}
    for key, rating in data["ratings"].items():
        if key not in current:
            raise ValueError(f"rating references an unknown Sherpa key: {key}")
        if not isinstance(rating, dict):
            raise ValueError(f"rating must be a mapping: {key}")
        average = rating.get("average")
        count = rating.get("count")
        if not isinstance(average, (int, float)) or not 1 <= average <= 5:
            raise ValueError(f"rating average must be between 1 and 5: {key}")
        if not isinstance(count, int) or count < 0:
            raise ValueError(f"rating count must be a non-negative integer: {key}")
        if str(rating.get("version")) != current[key]["version"]:
            raise ValueError(f"rating version does not match the Sherpa version: {key}")
    return data


def build(output: Path) -> list[dict]:
    records = discover()
    if not records:
        raise ValueError("no public Sherpa files discovered")

    output = output.resolve()
    if output == REPO_ROOT or REPO_ROOT not in output.parents:
        raise ValueError("output must be a directory inside the repository")
    if output.exists():
        shutil.rmtree(output)
    (output / "assets").mkdir(parents=True)
    shutil.copy2(ASSET_ROOT / "site.css", output / "assets" / "site.css")
    shutil.copy2(ASSET_ROOT / "site.js", output / "assets" / "site.js")
    shutil.copy2(PORTABLE_ROOT / "REHOSTING.md", output / "REHOSTING.md")

    for record in records:
        raw_destination = output / "raw" / record["source_path"]
        raw_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / record["source_path"], raw_destination)
        page_destination = output / record["route"].strip("/") / "index.html"
        page_destination.parent.mkdir(parents=True, exist_ok=True)
        page_destination.write_text(shell(records, detail=record), encoding="utf-8")

    manifest = {
        "schema_version": "1",
        "source_repository": "sherpa-md/sherpa-kits",
        "source_commit": source_sha(),
        "count": len(records),
        "items": [{key: value for key, value in record.items() if key != "raw"} for record in records],
    }
    (output / "index.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    ratings = load_ratings(records)
    (output / "ratings.json").write_text(json.dumps(ratings, indent=2) + "\n", encoding="utf-8")
    (output / "index.html").write_text(shell(records), encoding="utf-8")

    llms_lines = ["# SherpaMD", "", f"> {len(records)} public Sherpa files. Markdown is the source of truth.", ""]
    for record in records:
        llms_lines.append(f"- [{record['title']}]({record['raw_url']}): {record['summary']}")
    (output / "llms.txt").write_text("\n".join(llms_lines) + "\n", encoding="utf-8")

    sitemap_root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for route in ["/"] + [record["route"] for record in records]:
        url = ET.SubElement(sitemap_root, "url")
        ET.SubElement(url, "loc").text = PRODUCTION_ORIGIN + route
    ET.ElementTree(sitemap_root).write(output / "sitemap.xml", encoding="utf-8", xml_declaration=True)

    with zipfile.ZipFile(output / "all-sherpas.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for record in records:
            archive.write(REPO_ROOT / record["source_path"], record["source_path"])

    with zipfile.ZipFile(output / "sherpamd-portable-site.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(output.rglob("*")):
            if path.is_file() and path.name != "sherpamd-portable-site.zip":
                archive.write(path, path.relative_to(output).as_posix())

    print(f"Discovered: {len(records)}, built: {len(records)}, downloadable: {len(records)}")
    return records


if __name__ == "__main__":
    build(parse_args().output)
