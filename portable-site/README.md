# SherpaMD Portable Site

This folder contains the authored assets for a self-contained, read-only catalog. The public Markdown in `handoffs/`, `kits/`, and `candidates/` remains the source of truth.

## Build

```bash
python3 -m pip install -r requirements-site.txt
python3 scripts/build-site.py
python3 scripts/test-site.py
```

Serve `dist/` with any static file server, GitHub Pages, Cloudflare Pages, Netlify, nginx, Apache, or an object-storage website host. `dist/sherpamd-portable-site.zip` contains the complete generated catalog, and `dist/all-sherpas.zip` contains every public `.sherpa.md` source file with its repository-relative path preserved.

Every successful GitHub Actions run also publishes both ZIPs as a 90-day `sherpamd-portable-<commit>` artifact. Open the run, download the artifact, then follow `REHOSTING.md` inside the site ZIP. The workflow checks that the archive contains every generated detail page and raw Markdown download before publishing it.

After validation succeeds on `main`, the same generated output is committed to the permanent [`portable-site` snapshot branch](https://github.com/sherpa-md/sherpa-kits/tree/portable-site). Download that branch as a [complete site ZIP](https://github.com/sherpa-md/sherpa-kits/archive/refs/heads/portable-site.zip), or clone it when a rehost needs update history. The branch is generated output; contribute source changes through `main` instead of editing the snapshot.

See [REHOSTING.md](REHOSTING.md) for local preview and hosting instructions.

The snapshot publisher does not replace the production site automatically. Production adoption requires a separate reviewed deployment.

The **Use with AI** action tries the modern Clipboard API first and falls back to a temporary text selection for static mirrors that do not provide the secure-context clipboard permission. It reports success only when the browser confirms that one of those methods copied the instruction and Markdown.

The **Listen** action uses the browser's Web Speech API to read public Sherpa narrative text aloud. It skips fenced code blocks, divides long files into smaller reliable speech chunks, and provides play/pause, stop, and speed controls in a mobile-safe player. SherpaMD does not operate a speech backend; voice availability and processing depend on the visitor's browser and operating system.

## Ratings contract

`data/ratings.json` is a portable, read-only snapshot:

```json
{
  "schema_version": "1",
  "generated_at": "2026-09-06T12:00:00Z",
  "submit_url": "https://github.com/sherpa-md/sherpa-kits/issues/new?template=rate-sherpa.yml",
  "ratings": {
    "kit:token-piggy-bank": {
      "version": "1.0.0",
      "average": 4.8,
      "count": 24
    }
  }
}
```

Keys are type-qualified stable Sherpa IDs so a handoff and its supporting kit cannot overwrite each other. A rating record must include the rated Sherpa version, average from 1 through 5, and a non-negative count. Portable copies show the snapshot but keep inline star controls disabled unless a host deliberately adds authentication, rate limiting, moderation, and a durable backend. The interface never claims a vote was saved when no backend exists.

The official snapshot links to the repository's **Rate a Sherpa** issue form. GitHub supplies authentication, durable submissions, and maintainer moderation. The form records the specific Sherpa/version, a 1–5 score, the submitter's hands-on experience, and optional sanitized evidence. Ratings measure community usefulness only; they never alter `status` or `verification_state`. A maintainer must review valid submissions and update this version-bound snapshot through a normal pull request before an aggregate appears on the site.
