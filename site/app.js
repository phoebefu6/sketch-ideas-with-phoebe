/* Worth a thousand words - justified-row gallery. Reads GALLERY from data/works.js. */

(function () {
  "use strict";

  const data = typeof GALLERY !== "undefined" ? GALLERY : { taxonomy: { formats: {} }, works: [] };
  const works = data.works;
  const formatsInfo = (data.taxonomy && data.taxonomy.formats) || {};
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const state = { format: "all", topic: "all", style: "all", tool: "all" };
  let visible = [];
  let lightboxIndex = -1;

  const toolLabels = { midjourney: "Midjourney", chatgpt: "ChatGPT image", "nano-banana": "Nano Banana" };
  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"];

  function formatLabel(key) {
    return (formatsInfo[key] && formatsInfo[key].label) || key;
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  /* ---------- hero stats (count up) ---------- */

  const styleCount = new Set(works.filter(w => w.style).map(w => w.style)).size;

  function countUp(el, target) {
    if (!el) return;
    if (reducedMotion || target === 0) { el.textContent = target; return; }
    const duration = 1100;
    const start = performance.now();
    function tick(now) {
      const p = Math.min((now - start) / duration, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
    setTimeout(() => { el.textContent = target; }, duration + 250);
  }

  countUp(document.getElementById("stat-works"), works.length);
  countUp(document.getElementById("stat-styles"), styleCount);

  /* ---------- filters ---------- */

  function buildChips(containerId, key, values, labelFn) {
    const box = document.getElementById(containerId);
    box.innerHTML = "";
    const all = document.createElement("button");
    all.className = "chip active";
    all.textContent = "All";
    all.dataset.value = "all";
    box.appendChild(all);
    values.forEach(value => {
      const chip = document.createElement("button");
      chip.className = "chip";
      chip.textContent = labelFn(value);
      chip.dataset.value = value;
      box.appendChild(chip);
    });
    box.addEventListener("click", event => {
      const chip = event.target.closest(".chip");
      if (!chip) return;
      state[key] = chip.dataset.value;
      box.querySelectorAll(".chip").forEach(c => c.classList.toggle("active", c === chip));
      render();
    });
  }

  const formatKeys = Object.keys(formatsInfo).filter(k => works.some(w => w.format === k));
  works.forEach(w => { if (w.format && !formatKeys.includes(w.format)) formatKeys.push(w.format); });
  const topicKeys = [...new Set(works.flatMap(w => w.topic || []))].sort();
  const styleKeys = [...new Set(works.filter(w => w.style).map(w => w.style))].sort();
  const toolKeys = [...new Set(works.map(w => w.tool))].sort();

  buildChips("chips-format", "format", formatKeys, formatLabel);
  buildChips("chips-topic", "topic", topicKeys, t => t);
  buildChips("chips-style", "style", styleKeys, s => s);
  buildChips("chips-tool", "tool", toolKeys, t => toolLabels[t] || t);

  /* ---------- justified wall ---------- */

  const wall = document.getElementById("wall");
  const empty = document.getElementById("empty");
  const GAP = 8;

  function targetRowHeight() {
    const w = wall.clientWidth;
    if (w < 560) return 170;
    if (w < 960) return 220;
    return 260;
  }

  function monthKey(dateStr) {
    return String(dateStr).slice(0, 7);
  }

  function monthTitle(key) {
    const parts = key.split("-");
    const monthIndex = parseInt(parts[1], 10) - 1;
    return (monthNames[monthIndex] || parts[1]) + " " + parts[0];
  }

  function buildTile(work, index, height) {
    const ratio = work.w && work.h ? work.w / work.h : 1;
    const tile = document.createElement("figure");
    tile.className = "tile";
    tile.tabIndex = 0;
    tile.setAttribute("role", "button");
    tile.setAttribute("aria-label", work.title);
    tile.style.width = Math.round(height * ratio) + "px";
    tile.style.height = Math.round(height) + "px";
    tile.innerHTML =
      '<img loading="lazy" src="' + work.thumb + '" alt="' + escapeHtml(work.title) + '">' +
      (work.featured ? '<span class="star" aria-hidden="true"></span>' : "") +
      '<figcaption class="wash"><span class="wash-take">' +
      escapeHtml(work.takeaway || work.title) +
      '</span><span class="wash-meta">' + escapeHtml(formatLabel(work.format)) + " · " +
      escapeHtml(toolLabels[work.tool] || work.tool) + "</span></figcaption>";
    tile.addEventListener("click", () => openLightbox(index));
    tile.addEventListener("keydown", e => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openLightbox(index); }
    });
    return tile;
  }

  function layoutRows(groupWorks, startIndex, container) {
    const containerW = wall.clientWidth;
    const targetH = targetRowHeight();
    let row = [];
    let rowRatio = 0;

    function flush(isLast) {
      if (!row.length) return;
      const gaps = GAP * (row.length - 1);
      let height = (containerW - gaps) / rowRatio;
      if (isLast && height > targetH) height = targetH;
      const rowEl = document.createElement("div");
      rowEl.className = "row";
      row.forEach(item => rowEl.appendChild(buildTile(item.work, item.index, height)));
      container.appendChild(rowEl);
      row = [];
      rowRatio = 0;
    }

    groupWorks.forEach((work, i) => {
      const ratio = work.w && work.h ? work.w / work.h : 1;
      row.push({ work, index: startIndex + i });
      rowRatio += ratio;
      if ((containerW - GAP * (row.length - 1)) / rowRatio <= targetH) flush(false);
    });
    flush(true);
  }

  function render() {
    visible = works.filter(w =>
      (state.format === "all" || w.format === state.format) &&
      (state.topic === "all" || (w.topic || []).includes(state.topic)) &&
      (state.style === "all" || w.style === state.style) &&
      (state.tool === "all" || w.tool === state.tool)
    );
    wall.innerHTML = "";
    empty.hidden = visible.length > 0;

    let index = 0;
    let currentMonth = null;
    let group = [];

    function flushGroup() {
      if (!group.length) return;
      const divider = document.createElement("p");
      divider.className = "month";
      divider.textContent = monthTitle(currentMonth);
      wall.appendChild(divider);
      layoutRows(group, index - group.length, wall);
      group = [];
    }

    visible.forEach(work => {
      const key = monthKey(work.date);
      if (key !== currentMonth) { flushGroup(); currentMonth = key; }
      group.push(work);
      index += 1;
    });
    flushGroup();

    if (!reducedMotion) {
      const tiles = wall.querySelectorAll(".tile");
      tiles.forEach((tile, i) => {
        tile.classList.add("enter");
        setTimeout(() => tile.classList.add("shown"), Math.min(i, 12) * 45);
      });
      setTimeout(() => tiles.forEach(t => t.classList.add("shown")), 900);
    }
  }

  render();

  window.__gallery = { state: state, works: works, render: render, visibleCount: function () { return visible.length; } };

  let resizeTimer = null;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(render, 150);
  });

  /* ---------- lightbox ---------- */

  const lightbox = document.getElementById("lightbox");
  const lbImg = document.getElementById("lb-img");
  const lbCopy = document.getElementById("lb-copy");

  function openLightbox(index) {
    lightboxIndex = index;
    const work = visible[index];
    if (!work) return;
    lbImg.src = work.full;
    lbImg.alt = work.title;
    document.getElementById("lb-series").textContent =
      formatLabel(work.format) + " · " + work.date + (work.style ? " · " + work.style : "");
    document.getElementById("lb-title").textContent = work.title;
    const takeawayEl = document.getElementById("lb-takeaway");
    takeawayEl.textContent = work.takeaway || "";
    takeawayEl.style.display = work.takeaway ? "" : "none";
    const meta = document.getElementById("lb-meta");
    meta.innerHTML = "";
    [toolLabels[work.tool] || work.tool].concat(work.topic || []).forEach(tag => {
      const span = document.createElement("span");
      span.textContent = tag;
      meta.appendChild(span);
    });
    if (work.inspired_by) {
      const span = document.createElement("span");
      span.textContent = "inspired by " + work.inspired_by;
      meta.appendChild(span);
    }
    document.getElementById("lb-prompt").textContent = work.prompt || "(prompt lost to history)";
    lbCopy.textContent = "Copy prompt";
    lbCopy.classList.remove("copied");
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
  }

  function closeLightbox() {
    lightbox.hidden = true;
    document.body.style.overflow = "";
  }

  function step(delta) {
    if (visible.length === 0) return;
    openLightbox((lightboxIndex + delta + visible.length) % visible.length);
  }

  document.getElementById("lb-close").addEventListener("click", closeLightbox);
  document.getElementById("lb-prev").addEventListener("click", () => step(-1));
  document.getElementById("lb-next").addEventListener("click", () => step(1));
  lightbox.addEventListener("click", e => { if (e.target === lightbox) closeLightbox(); });
  document.addEventListener("keydown", e => {
    if (lightbox.hidden) return;
    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowLeft") step(-1);
    if (e.key === "ArrowRight") step(1);
  });

  /* copy prompt + click spark */
  lbCopy.addEventListener("click", event => {
    const work = visible[lightboxIndex];
    if (!work) return;
    navigator.clipboard.writeText(work.prompt || "").then(() => {
      lbCopy.textContent = "Copied - go make something";
      lbCopy.classList.add("copied");
    });
    if (!reducedMotion) spark(event.clientX, event.clientY);
  });

  function spark(x, y) {
    for (let i = 0; i < 8; i++) {
      const dot = document.createElement("div");
      dot.className = "spark";
      dot.style.left = x + "px";
      dot.style.top = y + "px";
      document.body.appendChild(dot);
      const angle = (Math.PI * 2 * i) / 8;
      const distance = 26 + Math.random() * 14;
      dot.animate(
        [
          { transform: "translate(0,0) scale(1)", opacity: 1 },
          { transform: "translate(" + Math.cos(angle) * distance + "px," + Math.sin(angle) * distance + "px) scale(0.3)", opacity: 0 }
        ],
        { duration: 450, easing: "cubic-bezier(0.22,1,0.36,1)" }
      ).onfinish = () => dot.remove();
    }
  }
})();
