"""Check generated pages, fragments and downloadable files without dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs"

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag in ("a", "img", "script", "link"):
            url = attrs.get("href") or attrs.get("src")
            if url:
                self.links.append(url)

pages = {p: Page(p) for p in SITE.rglob("*.html")}
errors = []
checked = 0
for file, page in pages.items():
    for url in page.links:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc:
            continue
        checked += 1
        target = (file.parent / unquote(parts.path)).resolve() if parts.path else file
        if target.is_dir():
            target /= "index.html"
        if not target.exists():
            errors.append(f"{file.relative_to(SITE)}: missing {url}")
        elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
            errors.append(f"{file.relative_to(SITE)}: missing fragment {url}")

resources = json.loads((ROOT / "assets/ressources.json").read_text())
assert len({r["id"] for r in resources}) == len(resources)
assert all(r["category"] in {"supports", "activites", "donnees", "diffusion"} for r in resources)
for r in resources:
    assert f'id="resource-{r["id"]}"' in (SITE / "ressources.html").read_text()

archive = SITE / "downloads/site-cours-quarto.zip"
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    assert "site-cours-quarto/_quarto.yml" in bundle.namelist()
    assert "site-cours-quarto/index.qmd" in bundle.namelist()
    assert not any("/docs/" in name or "/.quarto/" in name for name in bundle.namelist())
assert (SITE / "downloads/fiche-activite.qmd").read_text().startswith("---")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(pages)} pages, {checked} internal links/assets, {len(resources)} resources, 2 downloads.")

