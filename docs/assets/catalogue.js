/* The complete catalogue remains readable without JavaScript. */
(() => {
  "use strict";
  const search = document.querySelector("#resource-search");
  if (!search) return;
  const buttons = Array.from(document.querySelectorAll("[data-filter]"));
  const rows = Array.from(document.querySelectorAll(".resource-row"));
  const count = document.querySelector("#resource-count");
  const reset = document.querySelector("#resource-reset");
  const normalize = (text) => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const validFilters = new Set(buttons.map((button) => button.dataset.filter));
  const searchable = new Map(rows.map((row) => [row, normalize(row.textContent + " " + row.dataset.keywords)]));
  let filter = "tout";
  function update(writeUrl = true) {
    const words = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    let visible = 0;
    rows.forEach((row) => {
      const matches = (filter === "tout" || row.dataset.category === filter)
        && words.every((word) => searchable.get(row).includes(word));
      row.hidden = !matches;
      if (matches) visible++;
    });
    buttons.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.filter === filter)));
    count.textContent = visible + (visible === 1 ? " ressource" : " ressources");
    document.querySelector("#resource-empty").hidden = visible !== 0;
    if (writeUrl) {
      const url = new URL(window.location.href);
      if (filter === "tout") url.searchParams.delete("besoin");
      else url.searchParams.set("besoin", filter);
      if (search.value.trim()) url.searchParams.set("recherche", search.value.trim());
      else url.searchParams.delete("recherche");
      window.history.replaceState(null, "", url);
    }
  }
  function readUrl() {
    const params = new URLSearchParams(window.location.search);
    const requested = params.get("besoin");
    filter = validFilters.has(requested) ? requested : "tout";
    search.value = params.get("recherche") || "";
    update(false);
  }
  search.addEventListener("input", () => update());
  buttons.forEach((button) => button.addEventListener("click", () => {
    filter = button.dataset.filter;
    update();
  }));
  reset.addEventListener("click", () => {
    filter = "tout"; search.value = ""; update(); search.focus();
  });
  window.addEventListener("popstate", readUrl);
  readUrl();
  document.querySelector("#catalogue-controls").hidden = false;
  reset.hidden = false;
})();
