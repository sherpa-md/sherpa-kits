#!/usr/bin/env python3
"""Verify that a SherpaMD mirror matches the canonical portable snapshot."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath


DEFAULT_CANONICAL_INDEX = (
    "https://raw.githubusercontent.com/sherpa-md/sherpa-kits/portable-site/index.json"
)
EXPECTED_REPOSITORY = "sherpa-md/sherpa-kits"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_FILES = (
    "index.html",
    "index.json",
    "llms.txt",
    "ratings.json",
    "sitemap.xml",
    "REHOSTING.md",
    "update-rehost.py",
    "verify-rehost.py",
    "assets/site.css",
    "assets/site.js",
    "all-sherpas.zip",
    "sherpamd-portable-site.zip",
)
MAX_DOWNLOAD_BYTES = 100 * 1024 * 1024


class VerificationError(RuntimeError):
    """Raised when a mirror is incomplete, altered, or stale."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a deployed or extracted SherpaMD portable site."
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument(
        "--base-url", help="HTTPS origin to verify, for example https://sherpamd.org"
    )
    target.add_argument(
        "--site-dir", type=Path, help="Extracted portable-site directory to verify offline"
    )
    parser.add_argument(
        "--canonical-index",
        default=DEFAULT_CANONICAL_INDEX,
        help="Canonical index.json URL or local file (default: portable-site branch)",
    )
    parser.add_argument(
        "--expect-source-commit",
        help="Also require this lowercase 40-character source commit",
    )
    parser.add_argument(
        "--allow-http",
        action="store_true",
        help="Permit plain HTTP for a private development mirror",
    )
    return parser.parse_args()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_relative(path: str) -> bool:
    candidate = PurePosixPath(path)
    return (
        bool(path)
        and not candidate.is_absolute()
        and ".." not in candidate.parts
        and "\\" not in path
    )


def read_url(url: str) -> bytes:
    request = urllib.request.Request(
        url, headers={"User-Agent": "SherpaMD-Rehost-Verifier/1"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read(MAX_DOWNLOAD_BYTES + 1)
    except (OSError, urllib.error.HTTPError) as exc:
        raise VerificationError(f"could not fetch {url}: {exc}") from exc
    if len(data) > MAX_DOWNLOAD_BYTES:
        raise VerificationError(f"response exceeds 100 MiB safety limit: {url}")
    return data


def read_locator(locator: str) -> bytes:
    parsed = urllib.parse.urlparse(locator)
    if parsed.scheme in {"http", "https"}:
        return read_url(locator)
    if parsed.scheme:
        raise VerificationError(f"unsupported canonical index scheme: {parsed.scheme}")
    path = Path(locator).expanduser()
    try:
        return path.read_bytes()
    except OSError as exc:
        raise VerificationError(f"could not read canonical index {path}: {exc}") from exc


class SiteReader:
    def __init__(self, base_url: str | None, site_dir: Path | None, allow_http: bool):
        self.base_url = base_url.rstrip("/") + "/" if base_url else None
        self.site_dir = site_dir.expanduser().resolve() if site_dir else None
        self.cache: dict[str, bytes] = {}
        if self.base_url:
            parsed = urllib.parse.urlparse(self.base_url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise VerificationError("--base-url must be an absolute HTTP(S) URL")
            if parsed.scheme != "https" and not allow_http:
                raise VerificationError("public mirrors must use HTTPS (or pass --allow-http)")
        elif not self.site_dir or not self.site_dir.is_dir():
            raise VerificationError("--site-dir must identify an extracted site directory")

    def read(self, relative: str) -> bytes:
        if not safe_relative(relative):
            raise VerificationError(f"unsafe site path: {relative!r}")
        if relative in self.cache:
            return self.cache[relative]
        if self.base_url:
            data = read_url(urllib.parse.urljoin(self.base_url, relative))
        else:
            assert self.site_dir is not None
            path = self.site_dir.joinpath(*PurePosixPath(relative).parts)
            try:
                data = path.read_bytes()
            except OSError as exc:
                raise VerificationError(f"could not read {relative}: {exc}") from exc
        self.cache[relative] = data
        return data


def parse_manifest(data: bytes, label: str) -> dict:
    try:
        manifest = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"{label} is not valid UTF-8 JSON") from exc
    if not isinstance(manifest, dict):
        raise VerificationError(f"{label} must be a JSON object")
    if manifest.get("schema_version") != "1":
        raise VerificationError(f"{label} uses an unsupported schema")
    if manifest.get("source_repository") != EXPECTED_REPOSITORY:
        raise VerificationError(f"{label} does not identify the canonical repository")
    commit = manifest.get("source_commit")
    if not isinstance(commit, str) or not COMMIT_RE.fullmatch(commit):
        raise VerificationError(f"{label} has an invalid source_commit")
    items = manifest.get("items")
    if not isinstance(items, list) or not items or manifest.get("count") != len(items):
        raise VerificationError(f"{label} count does not match its non-empty items list")
    return manifest


def validate_items(manifest: dict) -> tuple[list[dict], list[str], set[str]]:
    items = manifest["items"]
    identities: set[tuple[str, str]] = set()
    source_paths: list[str] = []
    required_routes = set(REQUIRED_FILES)
    for item in items:
        if not isinstance(item, dict):
            raise VerificationError("index.json contains a non-object item")
        kind, item_id = item.get("kind"), item.get("id")
        if not isinstance(kind, str) or not kind or not isinstance(item_id, str) or not item_id:
            raise VerificationError("index.json contains a missing type-qualified ID")
        identity = (kind, item_id)
        if identity in identities:
            raise VerificationError(f"duplicate type-qualified ID: {kind}:{item_id}")
        identities.add(identity)

        source_path = item.get("source_path")
        raw_url = item.get("raw_url")
        route = item.get("route")
        expected_hash = item.get("sha256")
        if not isinstance(source_path, str) or not safe_relative(source_path):
            raise VerificationError(f"unsafe source_path for {kind}:{item_id}")
        if raw_url != f"/raw/{source_path}":
            raise VerificationError(f"raw URL does not preserve source_path for {kind}:{item_id}")
        if not isinstance(route, str) or not route.startswith("/") or ".." in route:
            raise VerificationError(f"unsafe route for {kind}:{item_id}")
        if not isinstance(expected_hash, str) or not HASH_RE.fullmatch(expected_hash):
            raise VerificationError(f"invalid SHA-256 for {kind}:{item_id}")
        source_paths.append(source_path)
        required_routes.add(raw_url.lstrip("/"))
        required_routes.add(route.strip("/") + "/index.html")
    return items, source_paths, required_routes


def verify_archive(data: bytes, items: list[dict], source_paths: list[str]) -> None:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            if sorted(archive.namelist()) != sorted(source_paths):
                raise VerificationError("all-sherpas.zip inventory does not match index.json")
            for item in items:
                if sha256(archive.read(item["source_path"])) != item["sha256"]:
                    raise VerificationError(
                        f"all-sherpas.zip hash mismatch for {item['source_path']}"
                    )
    except zipfile.BadZipFile as exc:
        raise VerificationError("all-sherpas.zip is not a valid ZIP archive") from exc


def verify_site_archive(data: bytes, required_routes: set[str]) -> None:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            names = set(archive.namelist())
    except zipfile.BadZipFile as exc:
        raise VerificationError("sherpamd-portable-site.zip is not a valid ZIP archive") from exc
    expected = required_routes - {"sherpamd-portable-site.zip"}
    if names != expected:
        missing = sorted(expected - names)
        extra = sorted(names - expected)
        detail = f"missing {missing[0]}" if missing else f"unexpected {extra[0]}"
        raise VerificationError(
            f"portable site ZIP inventory differs from the snapshot: {detail}"
        )


def main() -> int:
    args = parse_args()
    if args.expect_source_commit and not COMMIT_RE.fullmatch(args.expect_source_commit):
        raise VerificationError(
            "--expect-source-commit must be a lowercase 40-character SHA"
        )

    canonical = parse_manifest(read_locator(args.canonical_index), "canonical index.json")
    reader = SiteReader(args.base_url, args.site_dir, args.allow_http)
    deployed = parse_manifest(reader.read("index.json"), "deployed index.json")
    if deployed != canonical:
        if deployed.get("source_commit") != canonical.get("source_commit"):
            raise VerificationError(
                "mirror is stale: deployed source commit "
                f"{deployed.get('source_commit')} != canonical {canonical.get('source_commit')}"
            )
        raise VerificationError("deployed index.json differs from the canonical snapshot")
    commit = deployed["source_commit"]
    if args.expect_source_commit and commit != args.expect_source_commit:
        raise VerificationError(
            f"expected source commit {args.expect_source_commit}, received {commit}"
        )

    items, source_paths, required_routes = validate_items(deployed)
    for relative in sorted(required_routes):
        data = reader.read(relative)
        if not data:
            raise VerificationError(f"mirror returned an empty file: {relative}")
    for item in items:
        raw = reader.read(item["raw_url"].lstrip("/"))
        if sha256(raw) != item["sha256"]:
            raise VerificationError(f"raw file hash mismatch for {item['source_path']}")

    verify_archive(reader.read("all-sherpas.zip"), items, source_paths)
    verify_site_archive(reader.read("sherpamd-portable-site.zip"), required_routes)

    print(f"[PASS] mirror matches canonical source commit {commit}")
    print(f"[PASS] {len(items)}/{len(items)} Sherpa identities, routes, and SHA-256 hashes")
    print("[PASS] required assets and both download archives are complete")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"ERROR: {exc}", file=__import__("sys").stderr)
        raise SystemExit(1)
