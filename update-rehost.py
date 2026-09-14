#!/usr/bin/env python3
"""Safely update a SherpaMD static mirror from the validated GitHub snapshot."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath


DEFAULT_SOURCE = "https://github.com/sherpa-md/sherpa-kits/archive/refs/heads/portable-site.zip"
EXPECTED_REPOSITORY = "sherpa-md/sherpa-kits"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_FILES = (
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


class UpdateError(RuntimeError):
    """Raised when a candidate snapshot is unsafe or invalid."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify and atomically install the latest validated SherpaMD snapshot."
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--source",
        default=DEFAULT_SOURCE,
        help="HTTPS snapshot ZIP URL (default: the permanent portable-site branch)",
    )
    source.add_argument(
        "--archive", type=Path, help="Use a local snapshot ZIP instead of downloading"
    )
    parser.add_argument(
        "--root", type=Path, required=True, help="Mirror root containing releases/ and current"
    )
    parser.add_argument("--expect-source-commit", help="Refuse a snapshot from any other 40-character commit")
    parser.add_argument(
        "--keep", type=int, default=3, help="Number of validated releases to retain (default: 3)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Download and verify without changing the mirror"
    )
    return parser.parse_args()


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and ".." not in path.parts and "\\" not in name


def extract_safely(archive_path: Path, destination: Path) -> None:
    try:
        with zipfile.ZipFile(archive_path) as archive:
            for member in archive.infolist():
                if not safe_member(member.filename):
                    raise UpdateError(f"unsafe ZIP member: {member.filename!r}")
                mode = member.external_attr >> 16
                if stat.S_ISLNK(mode):
                    raise UpdateError(f"snapshot ZIP must not contain symlinks: {member.filename}")
            archive.extractall(destination)
    except zipfile.BadZipFile as exc:
        raise UpdateError("snapshot is not a valid ZIP archive") from exc


def payload_root(extracted: Path) -> Path:
    if (extracted / "index.json").is_file():
        return extracted
    candidates = [
        path
        for path in extracted.iterdir()
        if path.is_dir() and (path / "index.json").is_file()
    ]
    if len(candidates) != 1:
        raise UpdateError("snapshot must contain one site root with index.json")
    return candidates[0]


def local_path(root: Path, web_path: object, label: str) -> Path:
    if not isinstance(web_path, str) or not web_path.startswith("/"):
        raise UpdateError(f"{label} must be a root-relative path")
    relative = PurePosixPath(web_path.lstrip("/"))
    if not relative.parts or ".." in relative.parts or "\\" in web_path:
        raise UpdateError(f"unsafe {label}: {web_path!r}")
    return root.joinpath(*relative.parts)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_payload(root: Path, expected_commit: str | None = None) -> str:
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            raise UpdateError(f"snapshot is missing {relative}")

    try:
        manifest = json.loads((root / "index.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UpdateError("index.json is unreadable or invalid") from exc

    if manifest.get("schema_version") != "1":
        raise UpdateError("unsupported index.json schema")
    if manifest.get("source_repository") != EXPECTED_REPOSITORY:
        raise UpdateError("snapshot does not identify the canonical SherpaMD repository")
    commit = manifest.get("source_commit")
    if not isinstance(commit, str) or not COMMIT_RE.fullmatch(commit):
        raise UpdateError("snapshot source_commit is not a full Git commit SHA")
    if expected_commit and commit != expected_commit:
        raise UpdateError(f"expected source commit {expected_commit}, received {commit}")

    items = manifest.get("items")
    if not isinstance(items, list) or not items or manifest.get("count") != len(items):
        raise UpdateError("snapshot count does not match its non-empty item list")

    identities: set[tuple[object, object]] = set()
    source_paths: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            raise UpdateError("snapshot item is not an object")
        identity = (item.get("kind"), item.get("id"))
        if not all(isinstance(value, str) and value for value in identity) or identity in identities:
            raise UpdateError("snapshot contains a missing or duplicate type-qualified ID")
        identities.add(identity)

        source_path = item.get("source_path")
        if not isinstance(source_path, str) or not safe_member(source_path):
            raise UpdateError(f"unsafe source_path for {identity[0]}:{identity[1]}")
        source_paths.append(source_path)

        raw = local_path(root, item.get("raw_url"), "raw_url")
        route = local_path(root, item.get("route"), "route") / "index.html"
        if item.get("raw_url") != f"/raw/{source_path}":
            raise UpdateError(f"raw URL does not preserve source_path for {identity[0]}:{identity[1]}")
        if not raw.is_file() or not route.is_file():
            raise UpdateError(f"snapshot is missing a route or raw file for {identity[0]}:{identity[1]}")
        expected_hash = item.get("sha256")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            raise UpdateError(f"invalid SHA-256 for {identity[0]}:{identity[1]}")
        if sha256(raw) != expected_hash:
            raise UpdateError(f"raw file hash mismatch for {identity[0]}:{identity[1]}")

    try:
        with zipfile.ZipFile(root / "all-sherpas.zip") as archive:
            if sorted(archive.namelist()) != sorted(source_paths):
                raise UpdateError("all-sherpas.zip inventory does not match index.json")
            for item in items:
                raw = local_path(root, item["raw_url"], "raw_url")
                if archive.read(item["source_path"]) != raw.read_bytes():
                    raise UpdateError(f"all-sherpas.zip mismatch for {item['source_path']}")
    except zipfile.BadZipFile as exc:
        raise UpdateError("all-sherpas.zip is invalid") from exc
    return commit


def acquire_archive(args: argparse.Namespace, temporary: Path) -> Path:
    if args.archive:
        archive = args.archive.expanduser().resolve()
        if not archive.is_file():
            raise UpdateError(f"local archive does not exist: {archive}")
        return archive
    if not args.source.startswith("https://"):
        raise UpdateError("remote snapshot source must use HTTPS")
    archive = temporary / "snapshot.zip"
    request = urllib.request.Request(
        args.source, headers={"User-Agent": "SherpaMD-Rehost-Updater/1"}
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response, archive.open("wb") as output:
            shutil.copyfileobj(response, output)
    except OSError as exc:
        raise UpdateError(f"could not download snapshot: {exc}") from exc
    return archive


def activate(root: Path, payload: Path, commit: str, keep: int) -> str:
    root.mkdir(parents=True, exist_ok=True)
    with (root / ".update.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        releases = root / "releases"
        releases.mkdir(exist_ok=True)
        current = root / "current"
        if current.exists() and not current.is_symlink():
            raise UpdateError(f"refusing to replace non-symlink path: {current}")

        release = releases / commit
        if release.exists():
            if not release.is_dir() or validate_payload(release) != commit:
                raise UpdateError(f"existing release is not the expected validated snapshot: {release}")
            result = "already installed"
        else:
            staging = releases / f".{commit}-{os.getpid()}"
            if staging.exists():
                shutil.rmtree(staging)
            shutil.copytree(payload, staging)
            validate_payload(staging, commit)
            os.replace(staging, release)
            result = "installed"

        temporary_link = root / f".current-{os.getpid()}"
        if temporary_link.exists() or temporary_link.is_symlink():
            temporary_link.unlink()
        temporary_link.symlink_to(Path("releases") / commit, target_is_directory=True)
        os.replace(temporary_link, current)

        candidates = sorted(
            (path for path in releases.iterdir() if path.is_dir() and COMMIT_RE.fullmatch(path.name)),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        retained = {commit, *(path.name for path in candidates[:keep])}
        for old_release in candidates:
            if old_release.name not in retained:
                shutil.rmtree(old_release)
        return result


def main() -> int:
    args = parse_args()
    if args.keep < 1:
        raise UpdateError("--keep must be at least 1")
    if args.expect_source_commit and not COMMIT_RE.fullmatch(args.expect_source_commit):
        raise UpdateError("--expect-source-commit must be a lowercase 40-character SHA")

    with tempfile.TemporaryDirectory(prefix="sherpamd-update-") as temporary_name:
        temporary = Path(temporary_name)
        archive = acquire_archive(args, temporary)
        extracted = temporary / "extracted"
        extracted.mkdir()
        extract_safely(archive, extracted)
        payload = payload_root(extracted)
        commit = validate_payload(payload, args.expect_source_commit)
        if args.dry_run:
            print(f"Verified SherpaMD snapshot {commit}; no files changed.")
            return 0
        result = activate(args.root.expanduser().resolve(), payload, commit, args.keep)
        print(f"SherpaMD snapshot {commit} {result}; current switched atomically.")
        return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except UpdateError as exc:
        print(f"ERROR: {exc}", file=__import__("sys").stderr)
        raise SystemExit(1)
