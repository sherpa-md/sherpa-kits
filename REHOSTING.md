# Rehost SherpaMD

The portable site is static: it needs no database, application server, or secret. GitHub remains the source of truth for the Markdown. A portable copy is a read-only snapshot of one validated commit.

## Download

For the latest permanent GitHub snapshot:

1. Download the [`portable-site` branch ZIP](https://github.com/sherpa-md/sherpa-kits/archive/refs/heads/portable-site.zip), or clone that branch.
2. Extract the download. Its top-level folder contains the complete generated site.

For an exact 90-day build artifact:

1. Open a successful **Validate Sherpa Kits** run in GitHub Actions.
2. Download the `sherpamd-portable-<commit>` artifact.
3. Extract `sherpamd-portable-site.zip`.

The same artifact includes `all-sherpas.zip` if you only want the Markdown files.

The `portable-site` branch is updated only after the repository validator and site parity tests succeed on `main`. It is an auditable generated snapshot, not a second source of truth. Submit changes to `main`; do not edit the snapshot branch by hand.

## Check locally

From the extracted site folder, run:

```bash
python3 -m http.server 8080
```

Open `http://localhost:8080/`. Do not open `index.html` directly with a `file://` URL because browsers restrict the local fetches used by Preview and Use with AI.

## Publish

Upload the extracted contents—not the outer ZIP—to the document root of any static host, including GitHub Pages, Cloudflare Pages, Netlify, nginx, Apache, or object storage configured for website hosting.

The host must:

- serve `index.html` at `/`;
- preserve the included directory structure and case;
- serve `.md`, `.json`, `.txt`, `.xml`, `.css`, `.js`, and `.zip` files;
- keep HTTPS enabled for public use.

No server-side rewrite rules are required because each Sherpa detail route contains its own `index.html`.

## Verify the copy

After publishing, check:

1. `/index.json` loads and its `count` matches the number shown by the catalog.
2. Its `source_commit` identifies the validated `main` commit used for the snapshot.
3. A Sherpa can be previewed and downloaded.
4. `/all-sherpas.zip` downloads successfully.
5. Search and the type and verification filters work on a phone-sized screen.
6. The verification labels still match `index.json`.

Ratings are snapshots. A portable copy deliberately disables voting unless the host adds an authenticated, rate-limited, moderated, and durable ratings service.

## Update later

Rebuild from the desired `sherpa-md/sherpa-kits` commit, rerun validation, and replace the hosted files as one complete release. Do not hand-edit the generated site or copy individual Markdown files into it; those approaches break source/build parity.
