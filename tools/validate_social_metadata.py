from __future__ import annotations

import html
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "docs" / "index.html"] + sorted((ROOT / "docs" / "articles").glob("*.html"))
META = [
    ("description", "name"), ("author", "name"), ("og:title", "property"),
    ("og:description", "property"), ("og:type", "property"), ("og:url", "property"),
    ("og:image", "property"), ("og:image:width", "property"),
    ("og:image:height", "property"), ("og:site_name", "property"),
    ("twitter:card", "name"), ("twitter:title", "name"),
    ("twitter:description", "name"), ("twitter:image", "name"),
]
TAG = re.compile(r"<meta\b[^>]*>|<link\b[^>]*>", re.I | re.S)
SCRIPT = re.compile(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
ATTR = re.compile(r"([\w:-]+)\s*=\s*([\"'])(.*?)\2", re.I | re.S)


def attrs(tag: str) -> dict[str, str]:
    return {key.lower(): value for key, _, value in ATTR.findall(tag)}


def main() -> None:
    failures: list[str] = []
    for path in PAGES:
        source = path.read_text(encoding="utf-8")
        tags = [attrs(tag) for tag in TAG.findall(source)]
        for key, attribute in META:
            if sum(values.get(attribute) == key for values in tags) != 1:
                failures.append(f"{path.name}: meta {key}")
        descriptions = [values.get("content", "") for values in tags if values.get("name") == "description"]
        if not descriptions or not 150 <= len(html.unescape(descriptions[0])) <= 250:
            failures.append(f"{path.name}: description length")
        canonicals = [values.get("href") for values in tags if values.get("rel", "").lower() == "canonical"]
        expected = "https://personal.caracore.com.br/" if path.name == "index.html" else f"https://personal.caracore.com.br/articles/{path.name}"
        if canonicals != [expected]:
            failures.append(f"{path.name}: canonical")
        scripts = SCRIPT.findall(source)
        try:
            schema = json.loads(scripts[0])
        except (IndexError, json.JSONDecodeError):
            schema = {}
        expected_type = "Blog" if path.name == "index.html" else "BlogPosting"
        if schema.get("@type") != expected_type or schema.get("author", {}).get("name") != "Christian Mulato":
            failures.append(f"{path.name}: JSON-LD")
        if path.name != "index.html" and not schema.get("datePublished"):
            failures.append(f"{path.name}: datePublished")
    social = ROOT / "docs" / "articles" / "assets" / "img" / "social-default.png"
    if not social.exists() or Image.open(social).size != (1200, 630):
        failures.append("social-default.png: dimensions")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"OK: {len(PAGES)} paginas, metadados sociais e JSON-LD validos.")


if __name__ == "__main__":
    main()