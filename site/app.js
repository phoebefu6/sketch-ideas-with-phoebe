/* Worth a thousand words - gallery app. Reads GALLERY from data/works.js. */

(function () {
  "use strict";

  const data = typeof GALLERY !== "undefined" ? GALLERY : { series: {}, works: [] };
  const works = data.works;
  const seriesInfo = data.series || {};
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const state = { series: "all", style: "all", tool: "all" };
  let visible = [];
  let lightboxIndex = -1;

  /* ---------- hero stats (count up) ---------- */

  const styleCount = new Set(works.filter(w => w.style).map(w => w.style)).size;

  function countUp(el, target) {
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

  const toolLabels = { midjourney: "Midjourney", chatgpt: "ChatGPT image", "nano-banana": "Nano Banana" };

  function seriesLabel(key) {
    if (key === "playground") return "Playground";
    return (seriesInfo[key] && seriesInfo[key].label) || key;
  }

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

  const seriesKeys = Object.keys(seriesInfo).filter(k => works.some(w => w.series === k));
  if (works.some(w => w.series === "playground")) seriesKeys.push("playground");
  const styleKeys = [...new Set(works.filter(w => w.style).map(w => w.style))].sort();
  const toolKeys = [...new Set(works.map(w => w.tool))].sort();

  buildChips("chips-series", "series", seriesKeys, seriesLabel);
  buildChips("chips-style", "style", styleKeys, s => s);
  buildChips("chips-tool", "tool", toolKeys, t => toolLabels[t] || t);

  /* ---------- grid ---------- */

  const grid = document.getElementById("grid");
  const empty = document.getElementById("empty");
  let tileObserver = null;

  function render() {
    visible = works.filter(w =>
      (state.series === "all" || w.series === state.series) &&
      (state.style === "all" || w.style === state.style) &&
      (state.tool === "all" || w.tool === state.tool)
    );
    if (tileObserver) tileObserver.disconnect();
    grid.innerHTML = "";
    empty.hidden = visible.length > 0;

    visible.forEach((work, index) => {
      const tile = document.createElement("figure");
      tile.className = "tile";
      tile.tabIndex = 0;
      tile.setAttribute("role", "button");
      tile.setAttribute("aria-label", work.title);
      const ratio = work.h && work.w ? work.h / work.w : 1;
      tile.innerHTML =
        '<img loading="lazy" src="' + work.thumb + '" alt="' + escapeHtml(work.title) +
        '" width="' + work.w + '" height="' + work.h + '">' +
        (work.featured ? '<span class="star">featured</span>' : "") +
        '<figcaption class="cap"><span class="t">' + escapeHtml(work.title) +
        '</span><span class="tool">' + escapeHtml(toolLabels[work.tool] || work.tool) + "</span></figcaption>";
      tile.style.minHeight = Math.round(120 * ratio) + "px";
      tile.addEventListener("click", () => openLightbox(index));
      tile.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openLightbox(index); } });
      grid.appendChild(tile);
    });

    if (reducedMotion) {
      grid.querySelectorAll(".tile").forEach(t => t.classList.add("shown"));
    } else {
      tileObserver = new IntersectionObserver(entries => {
        entries.forEach((entry, i) => {
          if (entry.isIntersecting) {
            setTimeout(() => entry.target.classList.add("shown"), (i % 6) * 70);
            tileObserver.unobserve(entry.target);
          }
        });
      }, { rootMargin: "0px 0px -5% 0px" });
      grid.querySelectorAll(".tile").forEach(t => tileObserver.observe(t));
      setTimeout(() => grid.querySelectorAll(".tile:not(.shown)").forEach(t => t.classList.add("shown")), 1800);
    }
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  render();

  /* ---------- scroll reveal for hero/filters ---------- */

  if (reducedMotion) {
    document.querySelectorAll(".reveal").forEach(el => el.classList.add("shown"));
  } else {
    document.querySelectorAll(".reveal").forEach((el, i) => {
      setTimeout(() => el.classList.add("shown"), 150 + i * 120);
    });
  }

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
      seriesLabel(work.series) + " · " + work.date + (work.style ? " · " + work.style : "");
    document.getElementById("lb-title").textContent = work.title;
    document.getElementById("lb-takeaway").textContent = work.takeaway || "";
    document.getElementById("lb-takeaway").style.display = work.takeaway ? "" : "none";
    const meta = document.getElementById("lb-meta");
    meta.innerHTML = "";
    [toolLabels[work.tool] || work.tool].concat(work.tags || []).forEach(tag => {
      const span = document.createElement("span");
      span.textContent = tag;
      meta.appendChild(span);
    });
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
