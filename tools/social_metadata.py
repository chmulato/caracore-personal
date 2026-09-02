"""Normaliza metadados SEO e de compartilhamento das paginas estaticas."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ARTICLES = DOCS / "articles"
IMAGE_DIR = ARTICLES / "assets" / "img"
SITE = "https://personal.caracore.com.br"
AUTHOR = "Christian Mulato"
SITE_NAME = "Christian Mulato Dev Blog"
DEFAULT_IMAGE = f"{SITE}/articles/assets/img/social-default.png"
DEFAULT_DESCRIPTION = (
    "Ensaios de Christian Mulato sobre engenharia de software, arquitetura de sistemas, "
    "Java, inteligencia artificial, soberania digital e tecnologia aplicada ao mundo real."
)
TARGET_META = {
    "description": "name",
    "author": "name",
    "og:title": "property",
    "og:description": "property",
    "og:type": "property",
    "og:url": "property",
    "og:image": "property",
    "og:image:width": "property",
    "og:image:height": "property",
    "og:site_name": "property",
    "twitter:card": "name",
    "twitter:title": "name",
    "twitter:description": "name",
    "twitter:image": "name",
}
TAG_RE = re.compile(r"<meta\b[^>]*>|<link\b[^>]*>", re.I | re.S)
ATTR_RE = re.compile(r"([\w:-]+)\s*=\s*([\"'])(.*?)\2", re.I | re.S)
TITLE_RE = re.compile(r"<title\b[^>]*>(.*?)</title>", re.I | re.S)
POST_TITLE_RE = re.compile(
    r'<h1\b[^>]*class=["\'][^"\']*\bpost-title\b[^"\']*["\'][^>]*>(.*?)</h1>',
    re.I | re.S,
)
DESC_RE = re.compile(
    r'<meta\b[^>]*\bname=["\']description["\'][^>]*\bcontent=["\'](.*?)["\']',
    re.I | re.S,
)
TAG_STRIP_RE = re.compile(r"<[^>]+>")
DATE_RE = re.compile(r"^(\d{4}_\d{2}_\d{2})_")


def attrs(tag: str) -> dict[str, str]:
    return {name.lower(): value for name, _, value in ATTR_RE.findall(tag)}


def text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(TAG_STRIP_RE.sub(" ", value))).strip()


def existing_value(source: str, key: str) -> str:
    for tag in TAG_RE.findall(source):
        values = attrs(tag)
        if values.get(TARGET_META[key]) == key and values.get("content"):
            return html.unescape(values["content"])
    return ""


def page_title(source: str, is_home: bool) -> str:
    if is_home:
        return SITE_NAME
    match = POST_TITLE_RE.search(source)
    if match:
        return text(match.group(1))
    match = TITLE_RE.search(source)
    title = text(match.group(1)) if match else SITE_NAME
    return re.sub(r"\s+[—-]\s+Christian Mulato Dev Blog$", "", title).strip()


def page_description(source: str, title: str, is_home: bool) -> str:
    current = text(existing_value(source, "description"))
    if is_home:
        return DEFAULT_DESCRIPTION
    if len(current) >= 150:
        return current[:250].rstrip(" ,.;:")
    expanded = (
        f"{current.rstrip('.')} Este artigo de Christian Mulato apresenta contexto, "
        f"decisoes e aprendizados praticos sobre {title}, conectando engenharia de software "
        "a problemas concretos de tecnologia e negocio."
    )
    if len(expanded) < 150:
        expanded += " A leitura combina fundamentos, experiencia e criterio para apoiar decisoes tecnicas."
    return expanded[:250].rstrip(" ,.;:")


def image_for(path: Path, is_home: bool) -> tuple[str, int, int]:
    if is_home:
        image = IMAGE_DIR / "social-default.png"
    else:
        prefix = DATE_RE.match(path.stem)
        image = IMAGE_DIR / f"{prefix.group(1)}_IMAGE_001.png" if prefix else IMAGE_DIR / "social-default.png"
        if not image.exists():
            image = IMAGE_DIR / "social-default.png"
    width, height = 1200, 630
    try:
        from PIL import Image

        with Image.open(image) as opened:
            width, height = opened.size
    except (ImportError, OSError):
        pass
    return f"{SITE}/articles/assets/img/{image.name}", width, height


def remove_target_tags(source: str) -> str:
    def keep(tag: str) -> str:
        values = attrs(tag)
        if values.get("rel", "").lower() == "canonical":
            return ""
        for key, attribute in TARGET_META.items():
            if values.get(attribute) == key:
                return ""
        return tag

    return TAG_RE.sub(lambda match: keep(match.group(0)), source)


def metadata_block(title: str, description: str, url: str, image: str, width: int, height: int, is_home: bool, date: str | None) -> str:
    page_type = "website" if is_home else "article"
    lines = [
        f'    <meta name="description" content="{html.escape(description, quote=True)}">',
        f'    <meta name="author" content="{AUTHOR}">',
        f'    <meta property="og:title" content="{html.escape(title, quote=True)}">',
        f'    <meta property="og:description" content="{html.escape(description, quote=True)}">',
        f'    <meta property="og:type" content="{page_type}">',
        f'    <meta property="og:url" content="{url}">',
        f'    <meta property="og:image" content="{image}">',
        f'    <meta property="og:image:width" content="{width}">',
        f'    <meta property="og:image:height" content="{height}">',
        f'    <meta property="og:site_name" content="{SITE_NAME}">',
        '    <meta name="twitter:card" content="summary_large_image">',
        f'    <meta name="twitter:title" content="{html.escape(title, quote=True)}">',
        f'    <meta name="twitter:description" content="{html.escape(description, quote=True)}">',
        f'    <meta name="twitter:image" content="{image}">',
        f'    <link rel="canonical" href="{url}">',
    ]
    if date:
        lines.append(f'    <meta property="article:published_time" content="{date}">')
    schema = {
        "@context": "https://schema.org",
        "@type": "Blog" if is_home else "BlogPosting",
        "name": SITE_NAME,
        "headline": title,
        "description": description,
        "image": image,
        "author": {"@type": "Person", "name": AUTHOR},
    }
    if not is_home:
        schema["datePublished"] = date
        schema["mainEntityOfPage"] = {"@type": "WebPage", "@id": url}
    import json

    lines.extend([
        '    <script type="application/ld+json">',
        "    " + json.dumps(schema, ensure_ascii=False, indent=4),
        "    </script>",
    ])
    return "\n".join(lines)


def normalize(path: Path, is_home: bool) -> None:
    raw = path.read_bytes()
    try:
        source = raw.decode("utf-8")
    except UnicodeDecodeError:
        try:
            source = raw.decode("cp1252")
        except UnicodeDecodeError:
            source = raw.decode("iso-8859-1")
    title = page_title(source, is_home)
    description = page_description(source, title, is_home)
    url = f"{SITE}/" if is_home else f"{SITE}/articles/{path.name}"
    date = DATE_RE.match(path.stem).group(1).replace("_", "-") if not is_home and DATE_RE.match(path.stem) else None
    image, width, height = image_for(path, is_home)
    cleaned = remove_target_tags(source)
    block = metadata_block(title, description, url, image, width, height, is_home, date)
    head_match = re.search(r"<head\b[^>]*>", cleaned, re.I)
    if not head_match:
        raise ValueError(f"<head> ausente: {path}")
    viewport = re.search(r'''<meta\b[^>]*\bname=["']viewport["'][^>]*>''', cleaned[head_match.end():], re.I)
    insert_at = head_match.end() + viewport.end() if viewport else head_match.end()
    updated = cleaned[:insert_at] + "\n" + block + cleaned[insert_at:]
    path.write_text(updated, encoding="utf-8", newline="")


def main() -> None:
    files = [DOCS / "index.html"] + sorted(ARTICLES.glob("*.html"))
    for path in files:
        if path.name == "README.html":
            continue
        normalize(path, path == DOCS / "index.html")
    print(f"Normalizadas {len(files) - 1} paginas de artigo e a home.")


if __name__ == "__main__":
    main()