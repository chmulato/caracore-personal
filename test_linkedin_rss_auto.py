import subprocess
import unittest
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


if __name__ == "__main__":
    unittest.main()
