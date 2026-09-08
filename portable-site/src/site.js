(() => {
  "use strict";

  const records = JSON.parse(document.getElementById("sherpa-data").textContent);
  const prefix = window.SHERPA_ASSET_PREFIX || "./";
  const ratings = new Map();
  let activeRecord = null;
  let toastTimer = null;

  const byId = (id) => document.getElementById(id);
  const routeHref = (route) => prefix + route.replace(/^\//, "") + "index.html";
  const rawHref = (rawUrl) => prefix + rawUrl.replace(/^\//, "");

  function toast(message) {
    const node = byId("toast");
    if (!node) return;
    window.clearTimeout(toastTimer);
    node.textContent = message;
    node.hidden = false;
    toastTimer = window.setTimeout(() => { node.hidden = true; }, 2600);
  }

  async function loadRatings() {
    try {
      const response = await fetch(prefix + "ratings.json", { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const snapshot = await response.json();
      Object.entries(snapshot.ratings || {}).forEach(([key, value]) => ratings.set(key, value));
      document.dispatchEvent(new CustomEvent("ratings-ready"));
    } catch (_error) {
      toast("Ratings are unavailable; no vote was recorded.");
    }
  }

  function ratingFragment(record) {
    const row = document.createElement("div");
    row.className = "rating-row";
    const rating = ratings.get(record.key);
    if (rating && rating.version === record.version && Number(rating.count) > 0) {
      const rounded = Math.max(0, Math.min(5, Math.round(Number(rating.average))));
      const stars = document.createElement("span");
      stars.className = "stars";
      stars.setAttribute("aria-label", `${rating.average} out of 5 stars`);
      stars.textContent = "★".repeat(rounded) + "☆".repeat(5 - rounded);
      const count = document.createElement("span");
      count.textContent = `${Number(rating.average).toFixed(1)} · ${rating.count} rating${rating.count === 1 ? "" : "s"}`;
      row.append(stars, count);
      return row;
    }
    const label = document.createElement("span");
    label.textContent = "Not rated";
    row.append(label);
    for (let value = 1; value <= 5; value += 1) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "rating-button";
      button.disabled = true;
      button.textContent = "☆";
      button.setAttribute("aria-label", `Rate ${value} out of 5`);
      button.title = "Community rating submissions are not enabled in this portable copy.";
      row.append(button);
    }
    return row;
  }

  function badge(value, extraClass = "") {
    const node = document.createElement("span");
    node.className = `badge ${extraClass}`.trim();
    node.textContent = value;
    return node;
  }

  function button(label, className = "button") {
    const node = document.createElement("button");
    node.type = "button";
    node.className = className;
    node.textContent = label;
    return node;
  }

  async function rawText(record) {
    const response = await fetch(rawHref(record.raw_url));
    if (!response.ok) throw new Error(`Unable to load ${record.source_path}`);
    return response.text();
  }

  async function writeClipboard(text) {
    if (navigator.clipboard?.writeText) {
      try {
        await navigator.clipboard.writeText(text);
        return true;
      } catch (_error) {
        // Static mirrors served over plain HTTP may not expose the Clipboard API.
      }
    }

    const field = document.createElement("textarea");
    const previousFocus = document.activeElement;
    field.value = text;
    field.readOnly = true;
    field.setAttribute("aria-hidden", "true");
    field.style.position = "fixed";
    field.style.inset = "0 auto auto -9999px";
    document.body.append(field);
    try {
      field.focus();
      field.select();
      field.setSelectionRange(0, field.value.length);
      return document.execCommand("copy");
    } catch (_error) {
      return false;
    } finally {
      field.remove();
      if (previousFocus instanceof HTMLElement) previousFocus.focus();
    }
  }

  async function copyForAI(record) {
    try {
      const raw = await rawText(record);
      const instruction = "Read the Sherpa below, inspect my environment, implement the requested outcome safely, run its validation checks, and report evidence. Do not claim completion without proof.\n\n";
      const copied = await writeClipboard(instruction + raw);
      if (!copied) throw new Error("clipboard unavailable");
      toast("Sherpa and execution instruction copied.");
    } catch (_error) {
      toast("Copy failed. Download the Markdown file instead.");
    }
  }

  async function preview(record) {
    const dialog = byId("preview-dialog");
    try {
      activeRecord = record;
      byId("preview-title").textContent = record.title;
      byId("preview-content").textContent = await rawText(record);
      byId("dialog-download").href = rawHref(record.raw_url);
      dialog.showModal();
      byId("dialog-close").focus();
    } catch (_error) {
      toast("Preview unavailable. Open the source or download the file.");
    }
  }

  function actions(record) {
    const row = document.createElement("div");
    row.className = "card-actions";
    const previewButton = button("Preview");
    previewButton.addEventListener("click", () => preview(record));
    const copyButton = button("Use with AI", "button button--primary");
    copyButton.addEventListener("click", () => copyForAI(record));
    const download = document.createElement("a");
    download.className = "button";
    download.href = rawHref(record.raw_url);
    download.download = "";
    download.textContent = "Download .md";
    const source = document.createElement("a");
    source.className = "button";
    source.href = record.source_url;
    source.target = "_blank";
    source.rel = "noopener";
    source.textContent = "GitHub";
    row.append(previewButton, copyButton, download, source);
    return row;
  }

  function card(record) {
    const article = document.createElement("article");
    article.className = "sherpa-card";
    article.dataset.kind = record.kind;
    const heading = document.createElement("h2");
    const link = document.createElement("a");
    link.href = routeHref(record.route);
    link.textContent = record.title;
    heading.append(link);
    const badges = document.createElement("div");
    badges.className = "badges";
    badges.append(badge(record.kind), badge(record.verification_state, `badge--${record.verification_state}`), badge(record.status, `badge--${record.status}`));
    const summary = document.createElement("p");
    summary.textContent = record.summary;
    article.append(heading, badges, summary, actions(record), ratingFragment(record));
    return article;
  }

  function renderCatalog() {
    const grid = byId("catalog-grid");
    if (!grid) return;
    const query = byId("search").value.trim().toLocaleLowerCase();
    const kind = byId("kind-filter").value;
    const verification = byId("verification-filter").value;
    const filtered = records.filter((record) => {
      const haystack = `${record.title} ${record.summary} ${record.domain} ${record.source_path}`.toLocaleLowerCase();
      return (!query || haystack.includes(query)) && (!kind || record.kind === kind) && (!verification || record.verification_state === verification);
    });
    grid.replaceChildren(...filtered.map(card));
    byId("results-summary").textContent = `${filtered.length} of ${records.length} Sherpa files`;
    byId("empty-state").hidden = filtered.length !== 0;
  }

  function renderDetail(record) {
    const root = byId("detail-root");
    if (!root) return;
    const back = document.createElement("a");
    back.className = "detail-back";
    back.href = routeHref("/");
    back.textContent = "← Browse all Sherpas";
    const article = document.createElement("article");
    article.className = "detail-card";
    const eyebrow = document.createElement("p");
    eyebrow.className = "eyebrow";
    eyebrow.textContent = `${record.kind} · ${record.domain}`;
    const title = document.createElement("h1");
    title.textContent = record.title;
    const summary = document.createElement("p");
    summary.className = "summary";
    summary.textContent = record.summary;
    const badges = document.createElement("div");
    badges.className = "badges";
    badges.append(badge(record.verification_state, `badge--${record.verification_state}`), badge(record.status, `badge--${record.status}`), badge(`v${record.version}`));
    const path = document.createElement("p");
    path.className = "source-path";
    path.textContent = record.source_path;
    article.append(eyebrow, title, summary, badges, actions(record), ratingFragment(record), path);
    root.replaceChildren(back, article);
  }

  byId("dialog-close")?.addEventListener("click", () => byId("preview-dialog").close());
  byId("preview-dialog")?.addEventListener("click", (event) => {
    if (event.target === byId("preview-dialog")) byId("preview-dialog").close();
  });
  byId("dialog-copy")?.addEventListener("click", () => activeRecord && copyForAI(activeRecord));

  if (byId("catalog-grid")) {
    ["search", "kind-filter", "verification-filter"].forEach((id) => byId(id).addEventListener(id === "search" ? "input" : "change", renderCatalog));
    document.addEventListener("ratings-ready", renderCatalog);
    renderCatalog();
  }
  if (window.SHERPA_DETAIL_KEY) {
    const record = records.find((item) => item.key === window.SHERPA_DETAIL_KEY);
    if (record) renderDetail(record);
    document.addEventListener("ratings-ready", () => record && renderDetail(record));
  }
  loadRatings();
})();
