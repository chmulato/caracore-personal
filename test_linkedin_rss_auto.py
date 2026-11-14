import subprocess
import tempfile
import unittest
from datetime import date
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

    def test_pushes_do_not_publish_articles_with_scheduled_dates_early(self) -> None:
        scheduled = Path("docs/articles/2026_11_16_due.html")
        unscheduled = Path("docs/articles/2026_11_14_existing.html")
        self.assertEqual(linkedin.push_articles([scheduled, unscheduled]), [unscheduled])


if __name__ == "__main__":
    unittest.main()
