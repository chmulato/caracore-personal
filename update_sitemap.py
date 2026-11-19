"""Gera e verifica o sitemap das páginas canônicas do blog."""
from __future__ import annotations

import argparse
from datetime import date
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SITEMAP_PATH = ROOT / "docs" / "sitemap.xml"
SITE = "https://personal.caracore.com.br"
SKIP_NAMES = {
    "README.html",
    "2027_04_20_serie_engenharia_urgencia_chamada.html",
    "2027_04_26_serie_engenharia_urgencia_ep01.html",
    "2027_05_06_serie_engenharia_urgencia_ep02.html",
    "2027_05_16_serie_engenharia_urgencia_ep03.html",
}
DATE_PREFIX = re.compile(r"^(\d{4})_(\d{2})_(\d{2})_")


class SitemapPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.canonicals: list[str] = []
        self.noindex = False
        self.redirect = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "link" and "canonical" in (attributes.get("rel") or "").lower().split():
            self.canonicals.append(attributes.get("href") or "")
        if tag == "meta":
            name = (attributes.get("name") or "").lower()
            content = (attributes.get("content") or "").lower()
            if name in {"robots", "googlebot"} and re.search(r"\bnoindex\b", content):
                self.noindex = True
            if (attributes.get("http-equiv") or "").lower() == "refresh":
                self.redirect = True


def build_sitemap(docs: Path) -> str:
    pages = [(docs / "index.html", f"{SITE}/")]
    pages.extend(
        (path, f"{SITE}/editorial/{path.name}")
        for path in sorted((docs / "editorial").glob("*.html"))
    )
    for path in sorted((docs / "articles").glob("*.html")):
        match = DATE_PREFIX.match(path.name)
        if path.name in SKIP_NAMES or not match:
            continue
        try:
            date(*(int(part) for part in match.groups()))
        except ValueError as error:
            raise ValueError(f"Data inválida no nome do artigo: {path}") from error
        pages.append((path, f"{SITE}/articles/{path.name}"))

    for path, url in pages:
        page = SitemapPageParser()
        page.feed(path.read_text(encoding="utf-8-sig"))
        page.close()
        if page.canonicals != [url] or page.noindex or page.redirect:
            raise ValueError(f"Página não canônica ou não indexável: {path}")

    entries = [f"  <url><loc>{escape(url)}</loc></url>" for _, url in pages]
    return "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        *entries,
        "</urlset>",
        "",
    ])


def main(check: bool = False) -> None:
    try:
        body = build_sitemap(ROOT / "docs")
        ET.fromstring(body)
        if check:
            current = SITEMAP_PATH.read_text(encoding="utf-8")
            ET.fromstring(current)
            if current != body:
                raise SystemExit("docs/sitemap.xml desatualizado; execute python update_sitemap.py")
            print("docs/sitemap.xml atualizado.")
            return
    except (OSError, UnicodeError, ValueError, ET.ParseError) as error:
        raise SystemExit(f"Sitemap inválido: {error}") from error

    SITEMAP_PATH.write_text(body, encoding="utf-8", newline="\n")
    print(f"URLs gravadas: {len(ET.fromstring(body))}")
    print(f"gravado: {SITEMAP_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="valida o sitemap sem gravar",
    )
    main(check=parser.parse_args().check)
