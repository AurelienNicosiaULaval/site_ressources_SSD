"""Build the static catalogue and the downloadable template using stdlib only."""
from pathlib import Path
from html import escape
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
resources = json.loads((ROOT / "assets/ressources.json").read_text())
assert len({r["id"] for r in resources}) == len(resources), "Duplicate resource ID"
rows = ['<div id="resource-list">']
for r in resources:
    r = {key: escape(value, quote=True) for key, value in r.items()}
    rows.append(f"""
<article class="resource-row" data-category="{r['category']}" data-keywords="{r['keywords']}" aria-labelledby="resource-{r['id']}">
  <div class="resource-category">{r['label']}</div>
  <div><h2 id="resource-{r['id']}">{r['title']}</h2><p>{r['description']}</p><p class="resource-meta">{r['meta']}</p></div>
  <a class="text-link" href="{r['href']}">Voir la fiche<span class="visually-hidden"> : {r['title']}</span><span class="arrow" aria-hidden="true"></span></a>
</article>""")
rows.append("</div>")
(ROOT / "_includes").mkdir(exist_ok=True)
(ROOT / "_includes/catalogue.html").write_text("\n".join(rows) + "\n")
# The default count stays derived from the same source even without JavaScript.
page = ROOT / "ressources.qmd"
import re
text = page.read_text()
text = re.sub(r'(aria-atomic="true">)\d+ ressources', rf'\g<1>{len(resources)} ressources', text)
page.write_text(text)

# Fixed ZIP metadata makes repeated renders byte-for-byte reproducible.
target = ROOT / "downloads/site-cours-quarto.zip"
with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
    for file in sorted((ROOT / "quarto-site-template/skeleton").rglob("*")):
        if file.is_file() and not any(part.startswith(".") for part in file.relative_to(ROOT / "quarto-site-template/skeleton").parts):
            name = "site-cours-quarto/" + file.relative_to(ROOT / "quarto-site-template/skeleton").as_posix()
            item = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o644 << 16
            bundle.writestr(item, file.read_bytes())
print(f"Prepared {len(resources)} resources and the site template.")
