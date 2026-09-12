(() => {
  "use strict";

  const records = JSON.parse(document.getElementById("sherpa-data").textContent);
  const prefix = window.SHERPA_ASSET_PREFIX || "./";
  const ratings = new Map();
  const speechEngine = window.speechSynthesis || null;
  const speechAvailable = Boolean(speechEngine && window.SpeechSynthesisUtterance);
  const reader = { record: null, chunks: [], index: 0, utterance: null, paused: false, token: 0 };
  let activeRecord = null;
  let ratingsSubmitUrl = null;
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
      if (typeof snapshot.submit_url === "string" && snapshot.submit_url.trim()) {
        const candidate = new URL(snapshot.submit_url, window.location.href);
        if (candidate.protocol === "https:") ratingsSubmitUrl = candidate.toString();
      }
      document.dispatchEvent(new CustomEvent("ratings-ready"));
    } catch (_error) {
      toast("Ratings are unavailable; no vote was recorded.");
    }
  }

  function ratingFragment(record) {
    const row = document.createElement("div");
    row.className = "rating-row";
    const appendSubmissionLink = () => {
      if (!ratingsSubmitUrl) return;
      const url = new URL(ratingsSubmitUrl);
      url.searchParams.set("title", `[Rating]: ${record.title} (${record.key}, v${record.version})`);
      const link = document.createElement("a");
      link.className = "rating-link";
      link.href = url.toString();
      link.target = "_blank";
      link.rel = "noopener";
      link.textContent = "Rate on GitHub";
      link.setAttribute("aria-label", `Rate ${record.title} on GitHub`);
      row.append(link);
    };
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
      appendSubmissionLink();
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
      button.title = ratingsSubmitUrl
        ? "Use Rate on GitHub to submit a moderated community rating."
        : "Community rating submissions are not enabled in this portable copy.";
      row.append(button);
    }
    appendSubmissionLink();
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

  function speechText(markdown) {
    return markdown
      .replace(/^---\s*\n[\s\S]*?\n---\s*\n/, "")
      .replace(/```[\s\S]*?```/g, "\nCode example omitted.\n")
      .replace(/!\[([^\]]*)\]\([^)]*\)/g, "$1")
      .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
      .replace(/<[^>]+>/g, " ")
      .replace(/^#{1,6}\s+/gm, "")
      .replace(/^>\s?/gm, "")
      .replace(/^[-*+]\s+/gm, "")
      .replace(/^\d+\.\s+/gm, "")
      .replace(/[*_~`|]/g, " ")
      .replace(/[ \t]+/g, " ")
      .replace(/\n{2,}/g, "\n")
      .trim();
  }

  function splitForSpeech(text, limit = 1200) {
    const chunks = [];
    const add = (piece) => {
      const clean = piece.trim();
      if (!clean) return;
      if (clean.length <= limit) {
        chunks.push(clean);
        return;
      }
      const sentences = clean.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [clean];
      let current = "";
      sentences.forEach((sentence) => {
        const next = `${current} ${sentence.trim()}`.trim();
        if (next.length <= limit) {
          current = next;
          return;
        }
        if (current) chunks.push(current);
        if (sentence.length <= limit) {
          current = sentence.trim();
          return;
        }
        const words = sentence.trim().split(/\s+/);
        current = "";
        words.forEach((word) => {
          const wordNext = `${current} ${word}`.trim();
          if (current && wordNext.length > limit) {
            chunks.push(current);
            current = word;
          } else {
            current = wordNext;
          }
        });
      });
      if (current) chunks.push(current);
    };
    text.split(/\n+/).forEach(add);
    return chunks;
  }

  function updateReader() {
    const player = byId("reader-player");
    if (!player || !reader.record) return;
    player.hidden = false;
    document.body.classList.add("reader-active");
    byId("reader-title").textContent = reader.record.title;
    byId("reader-progress").textContent = `Part ${reader.index + 1} of ${reader.chunks.length}`;
    byId("reader-toggle").textContent = reader.paused ? "Resume" : "Pause";
    byId("reader-toggle").setAttribute("aria-pressed", String(reader.paused));
  }

  function stopReader({ announce = false } = {}) {
    reader.token += 1;
    speechEngine?.cancel();
    reader.record = null;
    reader.chunks = [];
    reader.index = 0;
    reader.utterance = null;
    reader.paused = false;
    byId("reader-player").hidden = true;
    document.body.classList.remove("reader-active");
    if (announce) toast("Reader stopped.");
  }

  function speakReaderPart() {
    if (!reader.record || reader.index >= reader.chunks.length) {
      stopReader();
      toast("Finished reading this Sherpa.");
      return;
    }
    const token = ++reader.token;
    const utterance = new SpeechSynthesisUtterance(reader.chunks[reader.index]);
    utterance.rate = Number(byId("reader-rate").value);
    utterance.onend = () => {
      if (token !== reader.token) return;
      reader.index += 1;
      speakReaderPart();
    };
    utterance.onerror = (event) => {
      if (token !== reader.token || event.error === "canceled" || event.error === "interrupted") return;
      stopReader();
      toast("The browser reader stopped unexpectedly.");
    };
    reader.utterance = utterance;
    reader.paused = false;
    updateReader();
    speechEngine.speak(utterance);
  }

  async function listen(record) {
    if (!speechAvailable) {
      toast("This browser does not provide a speech reader.");
      return;
    }
    try {
      const chunks = splitForSpeech(speechText(await rawText(record)));
      if (!chunks.length) throw new Error("nothing to read");
      stopReader();
      reader.record = record;
      reader.chunks = chunks;
      reader.index = 0;
      updateReader();
      speakReaderPart();
    } catch (_error) {
      stopReader();
      toast("Reader could not load this Sherpa.");
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
    const listenButton = button("Listen");
    listenButton.disabled = !speechAvailable;
    listenButton.title = speechAvailable ? "Read this Sherpa aloud" : "Speech is not supported by this browser";
    listenButton.addEventListener("click", () => listen(record));
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
    row.append(previewButton, listenButton, copyButton, download, source);
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
  byId("reader-toggle")?.addEventListener("click", () => {
    if (!reader.record) return;
    if (reader.paused) {
      speechEngine.resume();
      reader.paused = false;
    } else {
      speechEngine.pause();
      reader.paused = true;
    }
    updateReader();
  });
  byId("reader-stop")?.addEventListener("click", () => stopReader({ announce: true }));
  byId("reader-rate")?.addEventListener("change", () => {
    if (!reader.record) return;
    speechEngine.cancel();
    reader.token += 1;
    speakReaderPart();
    toast(`Reading speed set to ${byId("reader-rate").value}×.`);
  });
  window.addEventListener("beforeunload", () => speechEngine?.cancel());

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
