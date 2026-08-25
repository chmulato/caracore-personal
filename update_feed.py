"""Gera docs/feed.xml a partir dos artigos em docs/articles/.

Regras (AGENTS.md): URLs absolutas, enclosure + media:content, dc:creator,
pubDate RFC-822, CDATA em description e content:encoded.
"""
from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent
ARTICLES_DIR = ROOT / "docs" / "articles"
FEED_PATH = ROOT / "docs" / "feed.xml"

SITE = "https://personal.caracore.com.br"
ARTICLES_BASE = f"{SITE}/articles/"
FALLBACK_HERO = f"{ARTICLES_BASE}assets/img/foto_chri.jpg"

SKIP_NAMES = {"README.html"}
DATE_PREFIX = re.compile(r"^(\d{4})_(\d{2})_(\d{2})_")
ATTR_URL = re.compile(
    r"""(?P<attr>src|href|poster|data-src)\s*=\s*(?P<q>['"])(?P<url>.*?)(?P=q)""",
    re.I,
)
SCRIPT_BLOCK = re.compile(r"<script\b[^>]*>.*?</script>", re.I | re.S)
STYLE_BLOCK = re.compile(r"<style\b[^>]*>.*?</style>", re.I | re.S)
META_DESC = re.compile(
    r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
    re.I | re.S,
)
OG_TITLE = re.compile(
    r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']',
    re.I | re.S,
)
OG_IMAGE = re.compile(
    r'<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']',
    re.I | re.S,
)
DOC_TITLE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
POST_TITLE = re.compile(
    r'<h1[^>]*class=["\'][^"\']*post-title[^"\']*["\'][^>]*>(.*?)</h1>',
    re.I | re.S,
)
HERO_IMG = re.compile(
    r'<img[^>]*class=["\'][^"\']*hero-image[^"\']*["\'][^>]*>',
    re.I | re.S,
)
IMG_SRC = re.compile(r"""src\s*=\s*['"]([^'"]+)['"]""", re.I)
IMG_ALT = re.compile(r"""alt\s*=\s*['"]([^'"]*)['"]""", re.I)

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def rfc822(dt: datetime) -> str:
    return (
        f"{WEEKDAYS[dt.weekday()]}, {dt.day:02d} "
        f"{MONTHS[dt.month - 1]} {dt.year} 00:00:00 +0000"
    )


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def cdata(text: str) -> str:
    return f"<![CDATA[{(text or '').replace(']]>', ']]]]><![CDATA[>')}]]>"


def extract_div_inner(markup: str, class_name: str) -> str:
    pattern = rf'<div[^>]*class="[^"]*\b{re.escape(class_name)}\b[^"]*"[^>]*>'
    match = re.search(pattern, markup, re.I)
    if not match:
        return ""
    start = match.end()
    depth = 1
    token = re.compile(r"</?div\b[^>]*>", re.I)
    pos = start
    while pos < len(markup) and depth:
        found = token.search(markup, pos)
        if not found:
            return markup[start:].rstrip()
        chunk = found.group(0)
        if chunk.startswith("</"):
            depth -= 1
            if depth == 0:
                return markup[start:found.start()].strip()
        elif not chunk.endswith("/>"):
            depth += 1
        pos = found.end()
    return markup[start:].strip()


def absolutize_url(url: str) -> str:
    url = html.unescape((url or "").strip())
    if not url or url.startswith(("#", "mailto:", "javascript:", "data:")):
        return url
    if url.startswith("//"):
        return "https:" + url
    return urljoin(ARTICLES_BASE, url)


def absolutize_html(markup: str) -> str:
    def repl(match: re.Match) -> str:
        url = match.group("url")
        fixed = absolutize_url(url)
        return f'{match.group("attr")}={match.group("q")}{fixed}{match.group("q")}'

    return ATTR_URL.sub(repl, markup)


def mime_for(url: str) -> str:
    lower = url.lower().split("?", 1)[0]
    if lower.endswith(".jpg") or lower.endswith(".jpeg"):
        return "image/jpeg"
    if lower.endswith(".webp"):
        return "image/webp"
    if lower.endswith(".gif"):
        return "image/gif"
    if lower.endswith(".svg"):
        return "image/svg+xml"
    return "image/png"


def pick_title(raw: str) -> str:
    og = OG_TITLE.search(raw)
    if og:
        title = strip_tags(og.group(1))
        if title:
            return title
    doc = DOC_TITLE.search(raw)
    if doc:
        title = strip_tags(doc.group(1))
        for suffix in (" - Christian Mulato Dev Blog", " — Christian Mulato Dev Blog"):
            if title.endswith(suffix):
                title = title[: -len(suffix)].rstrip()
        if title and title != "Christian Mulato Dev Blog":
            return title
    post = POST_TITLE.search(raw)
    if post:
        title = strip_tags(post.group(1))
        if title:
            return title
    return "Christian Mulato Dev Blog"


def pick_description(raw: str) -> str:
    meta = META_DESC.search(raw)
    if meta:
        desc = strip_tags(meta.group(1))
        if desc:
            return desc
    return ""


def pick_hero(raw: str, content: str) -> tuple[str, str]:
    hero = HERO_IMG.search(raw)
    if hero:
        src = IMG_SRC.search(hero.group(0))
        alt = IMG_ALT.search(hero.group(0))
        if src:
            return absolutize_url(src.group(1)), (alt.group(1) if alt else "")
    og = OG_IMAGE.search(raw)
    if og:
        return absolutize_url(og.group(1)), ""
    first = re.search(r"<img[^>]+>", content, re.I)
    if first:
        src = IMG_SRC.search(first.group(0))
        alt = IMG_ALT.search(first.group(0))
        if src:
            return absolutize_url(src.group(1)), (alt.group(1) if alt else "")
    return FALLBACK_HERO, "Christian Mulato"


def clean_content(markup: str) -> str:
    markup = SCRIPT_BLOCK.sub("", markup)
    markup = STYLE_BLOCK.sub("", markup)
    markup = re.sub(r"<!--.*?-->", "", markup, flags=re.S)
    markup = absolutize_html(markup)
    markup = re.sub(r"\n{3,}", "\n\n", markup).strip()
    return markup


def parse_article(path: Path) -> dict | None:
    match = DATE_PREFIX.match(path.name)
    if not match:
        return None
    dt = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    raw = path.read_text(encoding="utf-8", errors="replace")
    content = clean_content(extract_div_inner(raw, "post-content"))
    title = pick_title(raw)
    description = pick_description(raw) or title
    hero_url, hero_alt = pick_hero(raw, content)
    link = f"{ARTICLES_BASE}{path.name}"
    if not content:
        content = f"<p>{html.escape(description)}</p>"
    if hero_url and "hero-image" not in content:
        alt = html.escape(hero_alt or title)
        content = (
            f'<figure class="hero-image-frame">'
            f'<img src="{hero_url}" alt="{alt}" class="hero-image" />'
            f"</figure>\n{content}"
        )
    return {
        "file": path.name,
        "date": dt,
        "title": title,
        "description": description,
        "link": link,
        "hero": hero_url,
        "content": content,
    }


def render_item(article: dict) -> str:
    hero = article["hero"]
    mime = mime_for(hero)
    return "\n".join(
        [
            "    <item>",
            f"      <title>{cdata(article['title'])}</title>",
            f"      <link>{article['link']}</link>",
            "      <dc:creator><![CDATA[Christian Mulato]]></dc:creator>",
            f"      <description>{cdata(article['description'])}</description>",
            f'      <enclosure url="{hero}" length="0" type="{mime}" />',
            f'      <media:content url="{hero}" medium="image" />',
            f'      <guid isPermaLink="true">{article["link"]}</guid>',
            f"      <pubDate>{rfc822(article['date'])}</pubDate>",
            f"      <content:encoded>{cdata(article['content'])}</content:encoded>",
            "    </item>",
        ]
    )


def build_feed(articles: list[dict]) -> str:
    newest = articles[0]["date"]
    items = "\n\n".join(render_item(article) for article in articles)
    return "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" '
            'xmlns:content="http://purl.org/rss/1.0/modules/content/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:media="http://search.yahoo.com/mrss/">',
            "  <channel>",
            "    <title><![CDATA[Christian Mulato Dev Blog]]></title>",
            f"    <link>{SITE}/</link>",
            "    <description><![CDATA[Artigos técnicos sobre desenvolvimento Java, "
            "arquitetura de software e tecnologia.]]></description>",
            "    <language>pt-BR</language>",
            f"    <lastBuildDate>{rfc822(newest)}</lastBuildDate>",
            f'    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml" />',
            "    <generator>Cara Core RSS generator</generator>",
            "",
            items,
            "  </channel>",
            "</rss>",
            "",
        ]
    )


def main() -> None:
    paths = sorted(
        p for p in ARTICLES_DIR.glob("*.html") if p.name not in SKIP_NAMES
    )
    articles = []
    skipped = []
    for path in paths:
        parsed = parse_article(path)
        if parsed is None:
            skipped.append(path.name)
            continue
        articles.append(parsed)
    articles.sort(key=lambda a: (a["date"], a["file"]), reverse=True)

    relative_attr = re.compile(
        r"""(?:src|href|poster)=['"](?!https?:|mailto:|#|javascript:|data:)"""
    )
    relative = [a["file"] for a in articles if relative_attr.search(a["content"])]
    empty = [a["file"] for a in articles if not a["content"].strip()]

    FEED_PATH.write_text(build_feed(articles), encoding="utf-8", newline="\n")

    print(f"artigos lidos: {len(paths)}")
    print(f"itens gerados: {len(articles)}")
    print(f"gravado: {FEED_PATH}")
    print(f"primeiro: {articles[0]['date'].date()} {articles[0]['file']}")
    print(f"ultimo: {articles[-1]['date'].date()} {articles[-1]['file']}")
    if skipped:
        print("ignorados sem data no nome:")
        for name in skipped:
            print(f"  {name}")
    if empty:
        print("content vazio:")
        for name in empty:
            print(f"  {name}")
    if relative:
        print("ainda com URL relativa:")
        for name in relative:
            print(f"  {name}")


if __name__ == "__main__":
    main()
