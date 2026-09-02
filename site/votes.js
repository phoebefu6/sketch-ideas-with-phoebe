/* Crowd-favourites voting. Counts live in a Google Sheet behind a Google Apps
   Script web app. ENDPOINT empty = voting UI hidden, shelf falls back to newest 5.
   Deploy guide: private/voting/README.md (repo-private). */

window.VOTES = (function () {
  "use strict";

  var ENDPOINT = ""; /* paste the Apps Script /exec URL here, then rebuild */

  var counts = {};

  function load() {
    if (!ENDPOINT) return Promise.resolve(counts);
    return fetch(ENDPOINT, { method: "GET" })
      .then(function (r) { return r.json(); })
      .then(function (c) { counts = c && typeof c === "object" ? c : {}; return counts; })
      .catch(function () { return counts; });
  }

  function vote(id) {
    counts[id] = (counts[id] || 0) + 1;
    if (!ENDPOINT) return;
    /* text/plain body avoids a CORS preflight, which Apps Script cannot answer */
    fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "text/plain" },
      body: JSON.stringify({ id: id })
    }).catch(function () {});
  }

  function count(id) { return counts[id] || 0; }
  function any() {
    for (var k in counts) { if (counts[k] > 0) return true; }
    return false;
  }

  return { load: load, vote: vote, count: count, any: any, enabled: !!ENDPOINT };
})();
