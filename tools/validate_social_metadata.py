from __future__ import annotations

import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = "https://personal.caracore.com.br/"
WEBSITE_ID = SITE + "#website"
BLOG_ID = SITE + "#blog"
PERSON_ID = SITE + "editorial/sobre-o-autor.html#person"
SITEMAP = DOCS / "sitemap.xml"
TAG = re.compile(r"<meta\b[^>]*>|<link\b[^>]*>", re.I | re.S)
SCRIPT = re.compile(
    r'<script\b(?=[^>]*type=["\']application/ld\+json["\'])[^>]*>(.*?)</script>',
    re.I | re.S,
)
ATTR = re.compile(r"""([\w:-]+)\s*=\s*(["'])(.*?)\2""", re.I | re.S)
TITLE = re.compile(r"<title\b[^>]*>(.*?)</title>", re.I | re.S)
LANGUAGE = re.compile(r"<html\b[^>]*\blang\s*=\s*['\"]([^'\"]+)['\"]", re.I)
META = [
    ("description", "name"), ("author", "name"), ("og:title", "property"),
    ("og:description", "property"), ("og:type", "property"), ("og:url", "property"),
    ("og:image", "property"), ("og:image:width", "property"),
    ("og:image:height", "property"), ("og:site_name", "property"),
    ("twitter:card", "name"), ("twitter:title", "name"),
    ("twitter:description", "name"), ("twitter:image", "name"),
]
REFERENCE_FIELDS = (
    "author", "publisher", "isPartOf", "mainEntity", "mainEntityOfPage",
)


def attrs(tag: str) -> dict[str, str]:
    return {key.lower(): value for key, _, value in ATTR.findall(tag)}


def sitemap_pages() -> list[tuple[Path, str]]:
    try:
        tree = ET.parse(SITEMAP)
    except (OSError, ET.ParseError) as error:
        raise SystemExit(f"Sitemap inválido: {error}") from error

    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [
        node.text or ""
        for node in tree.getroot().findall("sm:url/sm:loc", namespace)
    ]
    if not urls or len(urls) != len(set(urls)):
        raise SystemExit("Sitemap vazio ou com URLs duplicadas.")

    pages = []
    for url in urls:
        if not url.startswith(SITE):
            raise SystemExit(f"URL fora do host canônico: {url}")
        relative = urlparse(url).path.lstrip("/")
        path = DOCS / relative if relative else DOCS / "index.html"
        try:
            path.resolve().relative_to(DOCS.resolve())
        except ValueError as error:
            raise SystemExit(f"URL fora da pasta docs: {url}") from error
        if not path.is_file():
            raise SystemExit(f"URL do sitemap sem arquivo local: {url}")
        pages.append((path, url))
    return pages


def node_has_type(node: dict, expected: str) -> bool:
    value = node.get("@type")
    return value == expected or isinstance(value, list) and expected in value


def references(value) -> list[str]:
    if isinstance(value, dict):
        identity = value.get("@id")
        return [identity] if isinstance(identity, str) else []
    if isinstance(value, list):
        return [identity for item in value for identity in references(item)]
    return []


def main() -> None:
    failures: list[str] = []
    pages = sitemap_pages()
    declared_ids: dict[str, str] = {}
    id_references: list[tuple[str, str]] = []
    page_count = article_count = editorial_count = 0

    robots_path = DOCS / "robots.txt"
    if not robots_path.is_file():
        failures.append("robots.txt ausente")
    else:
        robots_lines = {
            line.strip().lower()
            for line in robots_path.read_text(encoding="utf-8-sig").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        if "user-agent: *" not in robots_lines:
            failures.append("robots.txt: User-agent: *")
        if "allow: /" not in robots_lines:
            failures.append("robots.txt: Allow: /")
        if f"sitemap: {SITE}sitemap.xml".lower() not in robots_lines:
            failures.append("robots.txt: Sitemap canônico")

    for path, canonical in pages:
        source = path.read_text(encoding="utf-8-sig")
        tags = [attrs(tag) for tag in TAG.findall(source)]
        meta = [tag for tag in tags if tag.get("name") or tag.get("property")]
        canonicals = [
            tag.get("href")
            for tag in tags
            if tag.get("rel", "").lower() == "canonical"
        ]
        if canonicals != [canonical]:
            failures.append(f"{path.name}: canonical")

        descriptions = [
            tag.get("content", "")
            for tag in meta
            if tag.get("name", "").lower() == "description"
        ]
        if len(descriptions) != 1 or not descriptions[0].strip():
            failures.append(f"{path.name}: meta description")
            description = ""
        else:
            description = html.unescape(descriptions[0]).strip()

        if any(
            tag.get("name", "").lower() in {"robots", "googlebot"}
            and re.search(r"\bnoindex\b", tag.get("content", ""), re.I)
            for tag in meta
        ):
            failures.append(f"{path.name}: noindex está no sitemap")
        if any(
            tag.get("http-equiv", "").lower() == "refresh"
            for tag in meta
        ):
            failures.append(f"{path.name}: redirecionamento está no sitemap")

        title_match = TITLE.search(source)
        if not title_match:
            failures.append(f"{path.name}: title")
            title = ""
        else:
            title = html.unescape(re.sub(r"<[^>]+>", "", title_match.group(1))).strip()
        language_match = LANGUAGE.search(source)
        if not language_match:
            failures.append(f"{path.name}: html lang")
            language = ""
        else:
            language = language_match.group(1)

        scripts = SCRIPT.findall(source)
        if len(scripts) != 1:
            failures.append(f"{path.name}: esperado exatamente um JSON-LD")
            continue
        try:
            schema = json.loads(scripts[0])
        except json.JSONDecodeError:
            failures.append(f"{path.name}: JSON-LD inválido")
            continue
        graph = schema.get("@graph")
        if schema.get("@context") != "https://schema.org" or not isinstance(graph, list):
            failures.append(f"{path.name}: JSON-LD sem @graph schema.org")
            continue
        if not all(isinstance(node, dict) for node in graph):
            failures.append(f"{path.name}: nó JSON-LD inválido")
            continue

        for node in graph:
            if "@context" in node:
                failures.append(f"{path.name}: @context deve ficar no nível do grafo")
            identity = node.get("@id")
            if identity:
                if identity in declared_ids:
                    failures.append(f"{path.name}: @id duplicado em {declared_ids[identity]}")
                else:
                    declared_ids[identity] = path.name
            for field in REFERENCE_FIELDS:
                id_references.extend(
                    (reference, path.name)
                    for reference in references(node.get(field))
                )

        web_pages = [node for node in graph if node_has_type(node, "WebPage")]
        if len(web_pages) != 1:
            failures.append(f"{path.name}: esperado um nó WebPage")
        else:
            page_count += 1
            page_node = web_pages[0]
            expected_page = {
                "@id": canonical + "#webpage",
                "url": canonical,
                "name": title,
                "description": description,
                "inLanguage": language,
                "isPartOf": {"@id": WEBSITE_ID},
                "publisher": {"@id": PERSON_ID},
            }
            if any(page_node.get(key) != value for key, value in expected_page.items()):
                failures.append(f"{path.name}: nó WebPage não acompanha canonical/title/description")

        is_home = path == DOCS / "index.html"
        is_article = path.parent == DOCS / "articles"
        if is_home or is_article:
            for key, attribute in META:
                if sum(tag.get(attribute) == key for tag in tags) != 1:
                    failures.append(f"{path.name}: meta {key}")
            if not description or not 150 <= len(description) <= 250:
                failures.append(f"{path.name}: description length")
            og_images = [
                tag.get("content")
                for tag in meta
                if tag.get("property", "").lower() == "og:image"
            ]
            if len(og_images) == 1 and og_images[0]:
                image_url = og_images[0]
                if not image_url.startswith(SITE):
                    failures.append(f"{path.name}: og:image fora do host")
                else:
                    image_path = DOCS / urlparse(image_url).path.lstrip("/")
                    if not image_path.is_file():
                        failures.append(f"{path.name}: og:image ausente no disco")

        if is_home:
            websites = [node for node in graph if node_has_type(node, "WebSite")]
            blogs = [node for node in graph if node_has_type(node, "Blog")]
            if len(websites) != 1 or len(blogs) != 1:
                failures.append("index.html: esperado um WebSite e um Blog")
            else:
                website = websites[0]
                blog = blogs[0]
                if website.get("@id") != WEBSITE_ID or website.get("url") != SITE:
                    failures.append("index.html: identidade WebSite")
                if website.get("name") != title or website.get("description") != description:
                    failures.append("index.html: conteúdo WebSite")
                if website.get("inLanguage") != language:
                    failures.append("index.html: idioma WebSite")
                if blog.get("@id") != BLOG_ID or blog.get("url") != canonical:
                    failures.append("index.html: identidade Blog")
                if blog.get("description") != description:
                    failures.append("index.html: descrição Blog")
                if blog.get("author") != {"@id": PERSON_ID}:
                    failures.append("index.html: author do Blog")
                if blog.get("publisher") != {"@id": PERSON_ID}:
                    failures.append("index.html: publisher do Blog")
                if blog.get("isPartOf") != {"@id": WEBSITE_ID}:
                    failures.append("index.html: isPartOf do Blog")
                if website.get("publisher") != {"@id": PERSON_ID}:
                    failures.append("index.html: publisher do WebSite")

        elif is_article:
            article_count += 1
            postings = [node for node in graph if node_has_type(node, "BlogPosting")]
            if len(postings) != 1:
                failures.append(f"{path.name}: esperado um BlogPosting")
                continue
            posting = postings[0]
            expected_date = "_".join(path.name.split("_")[:3]).replace("_", "-")
            published = [
                tag.get("content", "")
                for tag in meta
                if tag.get("property", "").lower() == "article:published_time"
            ]
            if len(published) != 1 or published[0] != expected_date:
                failures.append(f"{path.name}: article:published_time")
            if posting.get("@id") != canonical + "#blogposting" or posting.get("url") != canonical:
                failures.append(f"{path.name}: identidade BlogPosting")
            if posting.get("datePublished") != expected_date:
                failures.append(f"{path.name}: datePublished")
            if posting.get("name") != posting.get("headline"):
                failures.append(f"{path.name}: name do BlogPosting")
            if posting.get("description") != description:
                failures.append(f"{path.name}: descrição BlogPosting")
            if posting.get("mainEntityOfPage") != {"@id": canonical + "#webpage"}:
                failures.append(f"{path.name}: mainEntityOfPage")
            if posting.get("author") != {"@id": PERSON_ID}:
                failures.append(f"{path.name}: author")
            if posting.get("publisher") != {"@id": PERSON_ID}:
                failures.append(f"{path.name}: publisher")
            if posting.get("isPartOf") != {"@id": WEBSITE_ID}:
                failures.append(f"{path.name}: isPartOf")
            if posting.get("image") != next(iter(og_images), None):
                failures.append(f"{path.name}: imagem BlogPosting")

        else:
            editorial_count += 1

        if path == DOCS / "editorial" / "sobre-o-autor.html":
            people = [node for node in graph if node_has_type(node, "Person")]
            if len(people) != 1:
                failures.append("sobre-o-autor.html: esperado um nó Person")
            elif (
                people[0].get("@id") != PERSON_ID
                or people[0].get("name") != "Christian Mulato"
                or people[0].get("url") != canonical
            ):
                failures.append("sobre-o-autor.html: identidade Person")
            elif web_pages and web_pages[0].get("mainEntity") != {"@id": PERSON_ID}:
                failures.append("sobre-o-autor.html: mainEntity")

    for identity, path_name in id_references:
        if identity not in declared_ids:
            failures.append(f"{path_name}: referência @id sem nó correspondente ({identity})")

    social_default = DOCS / "articles" / "assets" / "img" / "social-default.png"
    try:
        if Image.open(social_default).size != (1200, 630):
            failures.append("social-default.png: dimensions")
    except OSError:
        failures.append("social-default.png: imagem ausente ou inválida")

    if failures:
        raise SystemExit("\n".join(failures))
    print(
        f"OK: {len(pages)} URLs; {page_count} WebPage; {article_count} BlogPosting; "
        f"{editorial_count} páginas editoriais; canonicals, metadados sociais e referências JSON-LD válidos."
    )


if __name__ == "__main__":
    main()
