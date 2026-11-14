import json
import os
import subprocess
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path
from unittest.mock import patch

import linkedin_rss_auto as linkedin


class ChangedArticleTests(unittest.TestCase):
    def test_assets_and_non_articles_are_not_published(self) -> None:
        article = "docs/articles/2026_10_12_article.html"
        markdown = "docs/articles/new_article.md"
        changed = "\n".join([
            article, markdown,
            "docs/articles/assets/img/README.html",
            "docs/articles/assets/help.md",
            "docs/articles/assets/img/cover.webp",
            "docs/feed.xml",
            "docs/articles/2026_10_12_draft.txt",
        ])
        result = subprocess.CompletedProcess(args=["git"], returncode=0, stdout=changed)
        with patch.object(linkedin, "POSTS_DIRECTORY", Path("docs/articles")), \
             patch.object(linkedin.subprocess, "run", return_value=result), \
             patch.object(linkedin.requests, "post") as post:
            self.assertEqual(linkedin.git_changed_files(), [Path(article), Path(markdown)])
            post.assert_not_called()


class ScheduledArticleTests(unittest.TestCase):
    def test_selects_only_articles_due_today_in_the_schedule_window(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            articles_dir = Path(temp_dir)
            for name in (
                "2026_11_16_due.html",
                "2026_11_19_future.html",
                "2026_11_16_draft.txt",
            ):
                (articles_dir / name).write_text("", encoding="utf-8")
            assets = articles_dir / "assets"
            assets.mkdir()
            (assets / "2026_11_16_image.html").write_text("", encoding="utf-8")

            with patch.object(linkedin, "POSTS_DIRECTORY", articles_dir):
                self.assertEqual(
                    linkedin.scheduled_articles(date(2026, 11, 16)),
                    [articles_dir / "2026_11_16_due.html"],
                )

    def test_schedule_does_not_select_outside_the_2026_window(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            articles_dir = Path(temp_dir)
            (articles_dir / "2027_01_05_future.html").write_text("", encoding="utf-8")
            with patch.object(linkedin, "POSTS_DIRECTORY", articles_dir):
                self.assertEqual(linkedin.scheduled_articles(date(2027, 1, 5)), [])

    def test_pushes_exclude_all_future_dated_articles(self) -> None:
        scheduled_2026 = Path("docs/articles/2026_11_16_due.html")
        dated_2027 = Path("docs/articles/2027_04_20_future.html")
        today = Path("docs/articles/2026_11_14_current.html")
        undated = Path("docs/articles/new_article.html")
        self.assertEqual(
            linkedin.push_articles(
                [scheduled_2026, dated_2027, today, undated],
                today=date(2026, 11, 14),
            ),
            [today, undated],
        )


class RepublicationTests(unittest.TestCase):
    def test_republicacoes_do_dia_le_o_registro_da_data(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            registro = Path(temp_dir) / "linkedin_republicacoes.json"
            registro.write_text(
                json.dumps({"2027-04-20": ["docs/articles/a.html"]}),
                encoding="utf-8",
            )
            with patch.object(linkedin, "REPUBLICACOES_PATH", registro):
                self.assertEqual(
                    linkedin.republicacoes_do_dia(date(2027, 4, 20)),
                    [Path("docs/articles/a.html")],
                )
                self.assertEqual(linkedin.republicacoes_do_dia(date(2027, 4, 21)), [])

    def test_registro_real_aponta_para_artigos_existentes(self) -> None:
        registro = json.loads(linkedin.REPUBLICACOES_PATH.read_text(encoding="utf-8"))
        for caminho in [item for caminhos in registro.values() for item in caminhos]:
            self.assertTrue((linkedin.REPOSITORY_ROOT / caminho).exists(), caminho)

    def test_relancamento_do_dia_publica_mesmo_ja_estando_no_ledger(self) -> None:
        hoje = datetime.now(linkedin.SCHEDULE_TIMEZONE).date()
        with tempfile.TemporaryDirectory() as temp_dir:
            artigo = Path(temp_dir) / "docs" / "articles" / "artigo.html"
            artigo.parent.mkdir(parents=True)
            artigo.write_text(
                "<html><head><title>Artigo</title></head><body></body></html>",
                encoding="utf-8",
            )
            registro = Path(temp_dir) / "linkedin_republicacoes.json"
            registro.write_text(
                json.dumps({hoje.isoformat(): [artigo.as_posix()]}),
                encoding="utf-8",
            )
            ledger = Path(temp_dir) / "ledger.json"
            ledger.write_text(
                json.dumps({artigo.as_posix(): "2026-11-14T22:55:41Z"}),
                encoding="utf-8",
            )
            with patch.object(linkedin, "REPUBLICACOES_PATH", registro), \
                 patch.object(linkedin, "PUBLISHED_LEDGER_PATH", ledger), \
                 patch.object(linkedin, "scheduled_articles", return_value=[]), \
                 patch.object(linkedin, "publish") as publish, \
                 patch.dict(os.environ, {"PUBLISH_DUE_TODAY": "true"}):
                self.assertEqual(linkedin.main(), 0)
            publish.assert_called_once()


if __name__ == "__main__":
    unittest.main()
