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

See [REHOSTING.md](REHOSTING.md) for local preview and hosting instructions.

The generator does not replace the production site automatically. Production adoption requires a separate reviewed deployment.

## Ratings contract

`data/ratings.json` is a portable, read-only snapshot:

```json
{
  "schema_version": "1",
  "generated_at": "2026-09-06T12:00:00Z",
  "submit_url": null,
  "ratings": {
    "kit:token-piggy-bank": {
      "version": "1.0.0",
      "average": 4.8,
      "count": 24
    }
  }
}
```

Keys are type-qualified stable Sherpa IDs so a handoff and its supporting kit cannot overwrite each other. A rating record must include the rated Sherpa version, average from 1 through 5, and a non-negative count. Portable copies show the snapshot but keep voting disabled unless a host deliberately adds authentication, rate limiting, moderation, and a durable backend. The interface never claims a vote was saved when no backend exists.
