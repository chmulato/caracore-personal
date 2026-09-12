"""Gera docs/sitemap.xml a partir da home, articles.html e docs/articles/.

Datas de <lastmod> vem do prefixo AAAA_MM_DD do nome do arquivo do artigo.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARTICLES_DIR = ROOT / "docs" / "articles"
SITEMAP_PATH = ROOT / "docs" / "sitemap.xml"

SITE = "https://personal.caracore.com.br"
SKIP_NAMES = {"README.html"}
DATE_PREFIX = re.compile(r"^(\d{4})_(\d{2})_(\d{2})_")


def render_url(loc: str, lastmod: date, changefreq: str, priority: str) -> str:
    return "\n".join(
        [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{lastmod.isoformat()}</lastmod>",
            f"    <changefreq>{changefreq}</changefreq>",
            f"    <priority>{priority}</priority>",
            "  </url>",
        ]
    )


def main() -> None:
    today = date.today()
    entries = [
        render_url(f"{SITE}/", today, "daily", "1.0"),
        render_url(f"{SITE}/articles.html", today, "daily", "0.8"),
    ]

    for path in sorted(ARTICLES_DIR.glob("*.html")):
        if path.name in SKIP_NAMES:
            continue
        match = DATE_PREFIX.match(path.name)
        if not match:
            continue
        article_date = date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        entries.append(render_url(f"{SITE}/articles/{path.name}", article_date, "monthly", "0.6"))

    body = "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            "\n".join(entries),
            "</urlset>",
            "",
        ]
    )
    SITEMAP_PATH.write_text(body, encoding="utf-8", newline="\n")
    print(f"URLs gravadas: {len(entries)}")
    print(f"gravado: {SITEMAP_PATH}")


if __name__ == "__main__":
    main()
