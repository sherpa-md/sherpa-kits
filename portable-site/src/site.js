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

  function labelGuide() {
    const details = document.createElement("details");
    details.className = "label-guide";
    const summary = document.createElement("summary");
    summary.textContent = "What the labels mean";
    const list = document.createElement("dl");
    list.className = "label-guide__list";
    const definitions = [
      ["verified", "Validation evidence exists for the stated scope. It is not a guarantee for every environment."],
      ["unverified", "No completed validation claim is recorded. Inspect and test before relying on it."],
      ["needs-retest", "Earlier evidence exists, but the current version or environment still needs validation."],
      ["active", "Maintained and intended for use; this status does not itself mean verified."],
      ["draft", "Incomplete or awaiting testing; do not treat it as production-ready."],
    ];
    definitions.forEach(([label, meaning]) => {
      const item = document.createElement("div");
      item.className = "label-guide__item";
      const term = document.createElement("dt");
      term.append(badge(label, `badge--${label}`));
      const description = document.createElement("dd");
      description.textContent = meaning;
      item.append(term, description);
      list.append(item);
    });
    const note = document.createElement("p");
    note.className = "label-guide__note";
    note.textContent = "Labels describe repository evidence—not approval for your environment. Inspect the target, protect private data, and require tests.";
    details.append(summary, list, note);
    return details;
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

  function agentHandoff(record, raw) {
    return [
      "SherpaMD AI handoff",
      `Title: ${record.title}`,
      `Stable ID: ${record.key}`,
      `Kind: ${record.kind}`,
      `Status: ${record.status}`,
      `Verification state: ${record.verification_state}`,
      `Version: ${record.version}`,
      `SHA-256: ${record.sha256}`,
      `Canonical source: ${record.source_url}`,
      `Catalog page: ${shareHref(record)}`,
      "",
      "Instructions:",
      "1. Treat the verification state exactly as written. Draft or unverified content is not validated.",
      "2. Inspect the actual environment before changing it; do not assume the Sherpa matches the target.",
      "3. Implement the requested outcome safely, run the stated validation checks, and report evidence.",
      "4. Do not claim completion without proof or silently alter the Sherpa's verification status.",
      "",
      "--- Begin Sherpa Markdown ---",
      raw,
      "--- End Sherpa Markdown ---",
    ].join("\n");
  }

  async function copyForAI(record) {
    try {
      const raw = await rawText(record);
      const copied = await writeClipboard(agentHandoff(record, raw));
      if (!copied) throw new Error("clipboard unavailable");
      toast("AI handoff copied with source and verification context.");
    } catch (_error) {
      toast("Copy failed. Download the Markdown file instead.");
    }
  }

  function shareHref(record) {
    const url = new URL(routeHref(record.route), window.location.href);
    url.pathname = url.pathname.replace(/index\.html$/, "");
    return url.toString();
  }

  function topicHref(tag) {
    const url = new URL(routeHref("/"), window.location.href);
    url.searchParams.set("topic", tag);
    return url.toString();
  }

  async function shareRecord(record) {
    const url = shareHref(record);
    if (navigator.share) {
      try {
        await navigator.share({
          title: `${record.title} — SherpaMD`,
          text: record.summary,
          url,
        });
        return;
      } catch (error) {
        if (error?.name === "AbortError") return;
        // Unsupported or blocked share sheets fall back to copying the stable link.
      }
    }
    const copied = await writeClipboard(url);
    toast(copied ? "Sherpa link copied." : "Share failed. Copy the page address instead.");
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
    const shareButton = button("Share");
    shareButton.title = "Share this Sherpa or copy its stable link";
    shareButton.addEventListener("click", () => shareRecord(record));
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
    row.append(previewButton, listenButton, copyButton, shareButton, download, source);
    return row;
  }

  function tagFragment(record, limit = 4) {
    if (!record.tags.length) return document.createDocumentFragment();
    const row = document.createElement("div");
    row.className = "tag-list";
    row.setAttribute("aria-label", "Topics");
    row.setAttribute("role", "list");
    record.tags.slice(0, limit).forEach((tag) => {
      const node = document.createElement("a");
      node.className = "tag tag--link";
      node.setAttribute("role", "listitem");
      node.setAttribute("aria-label", `Browse Sherpas about ${tag}`);
      node.href = topicHref(tag);
      node.textContent = `#${tag}`;
      row.append(node);
    });
    if (record.tags.length > limit) {
      const more = document.createElement("span");
      more.className = "tag tag--more";
      more.setAttribute("role", "listitem");
      more.textContent = `+${record.tags.length - limit} more`;
      more.title = record.tags.slice(limit).join(", ");
      row.append(more);
    }
    return row;
  }

  function integrityFragment(record) {
    const section = document.createElement("section");
    section.className = "integrity-panel";
    section.setAttribute("aria-labelledby", "file-integrity-title");
    const heading = document.createElement("h2");
    heading.id = "file-integrity-title";
    heading.textContent = "File integrity";
    const facts = document.createElement("dl");
    facts.className = "integrity-panel__facts";
    [
      ["Stable ID", record.key],
      ["Version", record.version],
      ["SHA-256", record.sha256],
    ].forEach(([label, value]) => {
      const term = document.createElement("dt");
      term.textContent = label;
      const description = document.createElement("dd");
      const code = document.createElement("code");
      code.textContent = value;
      description.append(code);
      facts.append(term, description);
    });
    const copyButton = button("Copy SHA-256");
    copyButton.addEventListener("click", async () => {
      const copied = await writeClipboard(record.sha256);
      toast(copied ? "SHA-256 copied." : "Copy failed. Select the checksum instead.");
    });
    const note = document.createElement("p");
    note.className = "integrity-panel__note";
    note.textContent = "The checksum confirms downloaded bytes match this catalog record; it does not make the Sherpa verified for your environment.";
    section.append(heading, facts, copyButton, note);
    return section;
  }

  function inlineReader(record) {
    const details = document.createElement("details");
    details.className = "inline-reader";
    const summary = document.createElement("summary");
    summary.textContent = "Read full Sherpa Markdown";
    const actions = document.createElement("div");
    actions.className = "inline-reader__actions";
    const copyButton = button("Copy full Markdown");
    const content = document.createElement("pre");
    content.className = "inline-reader__content";
    content.tabIndex = 0;
    content.setAttribute("aria-label", `Full Markdown for ${record.title}`);
    content.textContent = "Open this section to load the Markdown.";
    let markdownPromise = null;
    const loadMarkdown = () => {
      if (!markdownPromise) {
        markdownPromise = rawText(record).catch((error) => {
          markdownPromise = null;
          throw error;
        });
      }
      return markdownPromise;
    };
    copyButton.addEventListener("click", async () => {
      copyButton.disabled = true;
      try {
        const copied = await writeClipboard(await loadMarkdown());
        toast(copied ? "Full Markdown copied." : "Copy failed. Use Download .md instead.");
      } catch (_error) {
        toast("Full Markdown could not be loaded. Use Download .md instead.");
      } finally {
        copyButton.disabled = false;
      }
    });
    actions.append(copyButton);
    details.addEventListener("toggle", async () => {
      if (!details.open || details.dataset.loaded) return;
      details.dataset.loaded = "loading";
      content.textContent = "Loading Markdown…";
      try {
        content.textContent = await loadMarkdown();
        details.dataset.loaded = "true";
      } catch (_error) {
        delete details.dataset.loaded;
        content.textContent = "Markdown unavailable. Use Download .md or GitHub instead.";
        toast("Full Markdown could not be loaded.");
      }
    });
    details.append(summary, actions, content);
    return details;
  }

  function assessmentFragment(record) {
    const row = document.createElement("p");
    row.className = "assessment-date";
    row.append("Last assessed: ");
    if (!record.last_verified) {
      row.append("not recorded");
      return row;
    }
    const assessedAt = new Date(record.last_verified);
    const time = document.createElement("time");
    time.dateTime = record.last_verified;
    time.textContent = Number.isNaN(assessedAt.valueOf())
      ? record.last_verified
      : new Intl.DateTimeFormat(undefined, { year: "numeric", month: "short", day: "numeric", timeZone: "UTC" }).format(assessedAt);
    row.append(time);
    return row;
  }

  function relatedRecords(record, limit = 3) {
    return records
      .filter((candidate) => candidate.key !== record.key)
      .map((candidate) => {
        const sharedTopics = candidate.tags.filter((tag) => record.tags.includes(tag));
        const sameDomain = candidate.domain === record.domain;
        return { candidate, sharedTopics, sameDomain };
      })
      .filter((match) => match.sharedTopics.length || match.sameDomain)
      .sort((left, right) =>
        right.sharedTopics.length - left.sharedTopics.length
        || Number(right.sameDomain) - Number(left.sameDomain)
        || Number(right.candidate.verification_state === "verified") - Number(left.candidate.verification_state === "verified")
        || left.candidate.title.localeCompare(right.candidate.title, undefined, { sensitivity: "base" })
      )
      .slice(0, limit);
  }

  function relatedFragment(record) {
    const matches = relatedRecords(record);
    if (!matches.length) return document.createDocumentFragment();
    const section = document.createElement("section");
    section.className = "related-sherpas";
    section.setAttribute("aria-labelledby", "related-sherpas-title");
    const heading = document.createElement("h2");
    heading.id = "related-sherpas-title";
    heading.textContent = "Related Sherpas";
    const note = document.createElement("p");
    note.className = "related-note";
    note.textContent = "Related by public topics and domain—not verification or endorsement.";
    const list = document.createElement("ul");
    list.className = "related-list";
    matches.forEach(({ candidate, sharedTopics }) => {
      const item = document.createElement("li");
      item.className = "related-card";
      const link = document.createElement("a");
      link.href = routeHref(candidate.route);
      link.textContent = candidate.title;
      const reason = document.createElement("p");
      reason.textContent = sharedTopics.length
        ? `Shared topic${sharedTopics.length === 1 ? "" : "s"}: ${sharedTopics.join(", ")}`
        : `Same domain: ${candidate.domain}`;
      const badges = document.createElement("div");
      badges.className = "badges";
      badges.append(badge(candidate.kind), badge(candidate.verification_state, `badge--${candidate.verification_state}`));
      item.append(link, reason, badges);
      list.append(item);
    });
    section.append(heading, note, list);
    return section;
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
    article.append(heading, badges, assessmentFragment(record), summary, tagFragment(record), actions(record), ratingFragment(record));
    return article;
  }

  function compareRecords(left, right, order) {
    const byTitle = left.title.localeCompare(right.title, undefined, { sensitivity: "base" });
    if (order === "title") return byTitle;
    if (order === "assessed") return (right.last_verified || "").localeCompare(left.last_verified || "") || byTitle;
    const verifiedDifference = Number(right.verification_state === "verified") - Number(left.verification_state === "verified");
    return verifiedDifference || byTitle;
  }

  function setCatalogControl(id, value, fallback = "") {
    const control = byId(id);
    if (!control) return;
    if (control.tagName === "SELECT") {
      const allowed = Array.from(control.options).some((option) => option.value === value);
      control.value = allowed ? value : fallback;
      return;
    }
    control.value = value;
  }

  function restoreCatalogView() {
    const params = new URL(window.location.href).searchParams;
    setCatalogControl("search", params.get("q") || "");
    setCatalogControl("kind-filter", params.get("kind") || "");
    setCatalogControl("verification-filter", params.get("verification") || "");
    setCatalogControl("topic-filter", params.get("topic") || "");
    setCatalogControl("sort-order", params.get("sort") || "verified-first", "verified-first");
  }

  function saveCatalogView() {
    const url = new URL(window.location.href);
    const values = {
      q: byId("search").value.trim(),
      kind: byId("kind-filter").value,
      verification: byId("verification-filter").value,
      topic: byId("topic-filter").value,
      sort: byId("sort-order").value === "verified-first" ? "" : byId("sort-order").value,
    };
    Object.entries(values).forEach(([key, value]) => {
      if (value) url.searchParams.set(key, value);
      else url.searchParams.delete(key);
    });
    window.history.replaceState(null, "", url.toString());
  }

  function resetCatalogView() {
    setCatalogControl("search", "");
    setCatalogControl("kind-filter", "");
    setCatalogControl("verification-filter", "");
    setCatalogControl("topic-filter", "");
    setCatalogControl("sort-order", "verified-first", "verified-first");
    renderCatalog();
    byId("search").focus();
    toast("Catalog filters reset.");
  }

  async function copyCatalogView() {
    saveCatalogView();
    const copied = await writeClipboard(window.location.href);
    toast(copied ? "Catalog view link copied." : "Copy failed. Copy the page address instead.");
  }

  function renderCatalog() {
    const grid = byId("catalog-grid");
    if (!grid) return;
    const query = byId("search").value.trim().toLocaleLowerCase();
    const kind = byId("kind-filter").value;
    const verification = byId("verification-filter").value;
    const topic = byId("topic-filter").value;
    const sortOrder = byId("sort-order").value;
    const filtered = records.filter((record) => {
      const haystack = `${record.title} ${record.summary} ${record.domain} ${record.source_path} ${record.tags.join(" ")}`.toLocaleLowerCase();
      return (!query || haystack.includes(query)) && (!kind || record.kind === kind) && (!verification || record.verification_state === verification) && (!topic || record.tags.includes(topic));
    }).sort((left, right) => compareRecords(left, right, sortOrder));
    grid.replaceChildren(...filtered.map(card));
    byId("results-summary").textContent = `${filtered.length} of ${records.length} Sherpa files`;
    byId("empty-state").hidden = filtered.length !== 0;
    saveCatalogView();
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
    article.append(eyebrow, title, summary, badges, labelGuide(), assessmentFragment(record), tagFragment(record, record.tags.length), actions(record), ratingFragment(record), path, integrityFragment(record), inlineReader(record), relatedFragment(record));
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
    byId("catalog-label-guide")?.replaceChildren(labelGuide());
    restoreCatalogView();
    ["search", "kind-filter", "verification-filter", "topic-filter", "sort-order"].forEach((id) => byId(id).addEventListener(id === "search" ? "input" : "change", renderCatalog));
    byId("clear-filters").addEventListener("click", resetCatalogView);
    byId("copy-view-link").addEventListener("click", copyCatalogView);
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
