#!/usr/bin/env python3
"""Publica o artigo adicionado ou alterado no commit atual no LinkedIn.

Funciona com posts Markdown com frontmatter YAML e com os artigos HTML atuais.
"""

from __future__ import annotations

import hashlib
import logging
import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote

import requests


REPOSITORY_ROOT = Path(__file__).resolve().parent
POSTS_DIRECTORY = Path(os.getenv("POSTS_DIRECTORY", "docs/articles"))
PUBLIC_ARTICLES_PATH = os.getenv("PUBLIC_ARTICLES_PATH", "articles").strip("/")
BLOG_BASE_URL = os.getenv("BLOG_BASE_URL", "https://personal.caracore.com.br").rstrip("/")
LINKEDIN_API_URL = "https://api.linkedin.com/rest/posts"
LINKEDIN_VERSION = os.getenv("LINKEDIN_VERSION", "202601")
REQUEST_TIMEOUT_SECONDS = 30
MAX_ATTEMPTS = 3
MAX_POST_LENGTH = 3000


class _HTMLTextExtractor(HTMLParser):
    """Extrai texto visivel de um trecho HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return " ".join(" ".join(self.parts).split())


class _HTMLMetadataExtractor(HTMLParser):
    """Encontra o primeiro titulo sem depender de um parser externo."""

    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.in_h1 = False
        self.title_parts: list[str] = []
        self.h1_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.in_title |= tag.lower() == "title"
        self.in_h1 |= tag.lower() == "h1"

    def handle_endtag(self, tag: str) -> None:
        self.in_title &= tag.lower() != "title"
        self.in_h1 &= tag.lower() != "h1"

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_h1:
            self.h1_parts.append(data)

    def title(self) -> str:
        return " ".join(" ".join(self.title_parts).split()) or " ".join(
            " ".join(self.h1_parts).split()
        )


def required_environment(name: str) -> str:
    """Retorna uma variavel obrigatoria sem registrar seu valor."""
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"A variavel de ambiente {name} nao foi configurada")
    return value


def git_changed_files() -> list[Path]:
    """Lista posts adicionados ou modificados no push recebido pelo workflow."""
    commit_sha = os.getenv("GITHUB_SHA", "HEAD")
    previous_sha = os.getenv("GITHUB_BEFORE", "")

    if previous_sha and set(previous_sha) != {"0"}:
        command = ["git", "diff", "--name-only", "--diff-filter=AM", previous_sha, commit_sha]
    else:
        command = [
            "git",
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "--diff-filter=AM",
            "-r",
            commit_sha,
        ]

    result = subprocess.run(
        command,
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    posts_prefix = POSTS_DIRECTORY.as_posix().rstrip("/") + "/"
    allowed_suffixes = {".md", ".markdown", ".html"}
    changed = {
        Path(line.strip())
        for line in result.stdout.splitlines()
        if line.strip()
        and Path(line.strip()).suffix.lower() in allowed_suffixes
        and Path(line.strip()).as_posix().startswith(posts_prefix)
    }
    return sorted(changed)


def extract_markdown_title(content: str) -> str:
    """Extrai title do frontmatter YAML simples, sem exigir PyYAML."""
    frontmatter = re.match(
        r"^---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", content, re.DOTALL
    )
    if not frontmatter:
        return ""
    match = re.search(r"^title\s*:\s*(.+?)\s*$", frontmatter.group(1), re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip("'\"")


def extract_title(path: Path, content: str) -> str:
    """Extrai o titulo do Markdown ou do HTML do acervo atual."""
    markdown_title = extract_markdown_title(content)
    if markdown_title:
        return markdown_title

    parser = _HTMLMetadataExtractor()
    parser.feed(content)
    title = parser.title()
    if " - Christian Mulato Dev Blog" in title:
        title = title.split(" - Christian Mulato Dev Blog", 1)[0].rstrip()
    if title:
        return title
    raise RuntimeError(f"Nao foi possivel extrair o titulo de {path}")


def extract_summary(content: str, title: str) -> str:
    """Monta um resumo curto para acompanhar o link no LinkedIn."""
    body = re.sub(r"^---.*?---\s*", "", content, count=1, flags=re.DOTALL)
    body = re.sub(r"!\[[^]]*\]\([^)]*\)", "", body)
    body = re.sub(r"[#>*_`~-]", " ", body)
    text = _HTMLTextExtractor()
    text.feed(body)
    summary = text.text()
    if summary.lower().startswith(title.lower()):
        summary = summary[len(title) :].strip(" .:-")
    return summary[:500].rstrip()


def post_url(path: Path) -> str:
    """Converte o caminho do arquivo em URL publica do artigo."""
    filename = path.name
    if filename.endswith(".md") or filename.endswith(".markdown"):
        filename = filename.rsplit(".", 1)[0] + ".html"
    relative_path = f"{PUBLIC_ARTICLES_PATH}/{filename}"
    encoded_path = quote(relative_path, safe="/_-.~")
    return f"{BLOG_BASE_URL}/{encoded_path}"


def build_post_text(title: str, summary: str, url: str) -> str:
    """Monta o texto respeitando o limite pratico do LinkedIn."""
    prefix = f"{title}\n\n"
    suffix = f"\n\n{url}"
    available = MAX_POST_LENGTH - len(prefix) - len(suffix)
    if available <= 0:
        return (title[: MAX_POST_LENGTH - len(url) - 2] + "\n\n" + url)[:MAX_POST_LENGTH]
    shortened_summary = summary[:available].rstrip()
    if len(shortened_summary) < len(summary):
        shortened_summary = shortened_summary.rstrip(" .,;") + "..."
    return f"{prefix}{shortened_summary}{suffix}"


def publish(title: str, summary: str, url: str) -> None:
    """Publica um artigo usando a API REST atual de posts do LinkedIn."""
    access_token = required_environment("LINKEDIN_ACCESS_TOKEN")
    person_urn = required_environment("PERSON_URN")
    if not person_urn.startswith("urn:li:person:"):
        raise RuntimeError("PERSON_URN deve estar no formato urn:li:person:ID")

    commit_key = os.getenv("GITHUB_SHA", url)
    idempotency_key = hashlib.sha256(f"{commit_key}:{url}".encode()).hexdigest()
    payload = {
        "author": person_urn,
        "commentary": build_post_text(title, summary, url),
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "content": {"article": {"source": url, "title": title}},
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": LINKEDIN_VERSION,
        "X-Restli-Protocol-Version": "2.0.0",
        "X-RestLi-Idempotency-Key": idempotency_key,
    }

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.post(
                LINKEDIN_API_URL,
                headers=headers,
                json=payload,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.RequestException as exc:
            if attempt == MAX_ATTEMPTS:
                raise RuntimeError("Falha de rede ao publicar no LinkedIn") from exc
            logging.warning("Falha de rede; nova tentativa %d/%d", attempt + 1, MAX_ATTEMPTS)
            continue

        if 200 <= response.status_code < 300:
            logging.info("Artigo publicado no LinkedIn: %s", url)
            return
        if response.status_code in {400, 401, 403} or response.status_code < 500:
            raise RuntimeError(
                f"LinkedIn respondeu HTTP {response.status_code}: {response.text[:500]}"
            )
        if attempt < MAX_ATTEMPTS:
            logging.warning("LinkedIn respondeu HTTP %d; nova tentativa", response.status_code)

    raise RuntimeError("LinkedIn nao publicou o artigo apos as tentativas")


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        changed_files = git_changed_files()
        if not changed_files:
            logging.info("Nenhum artigo adicionado ou alterado neste commit")
            return 0

        # O nome do arquivo normalmente contem a data; o ultimo por ordem de
        # caminho representa o artigo mais recente dentro do push.
        path = changed_files[-1]
        content = (REPOSITORY_ROOT / path).read_text(encoding="utf-8")
        title = extract_title(path, content)
        url = post_url(path)
        publish(title, extract_summary(content, title), url)
        return 0
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        logging.error("Publicacao interrompida: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
