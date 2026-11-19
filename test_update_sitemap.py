from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import update_sitemap as sitemap


class SitemapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.docs = self.root / "docs"
        self.articles = self.docs / "articles"
        self.editorial = self.docs / "editorial"
        self.articles.mkdir(parents=True)
        self.editorial.mkdir()
        self.write_page(self.docs / "index.html", f"{sitemap.SITE}/")
        self.write_page(self.editorial / "sobre.html", f"{sitemap.SITE}/editorial/sobre.html")
        self.future = self.articles / "2099_01_01_futuro.html"
        self.write_page(self.future, f"{sitemap.SITE}/articles/{self.future.name}")
        for name in sitemap.SKIP_NAMES:
            (self.articles / name).write_text('<meta name="robots" content="noindex">', encoding="utf-8")
        self.sitemap_path = self.docs / "sitemap.xml"

    def write_page(self, path: Path, url: str, extra: str = "") -> None:
        path.write_text(f'<link href="{url}" rel="canonical">{extra}', encoding="utf-8")

    def test_includes_index_editorial_and_future_articles_without_lastmod(self) -> None:
        root = ET.fromstring(sitemap.build_sitemap(self.docs))
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locations = [entry.findtext(f"{namespace}loc") for entry in root]
        self.assertEqual(locations, [
            f"{sitemap.SITE}/",
            f"{sitemap.SITE}/editorial/sobre.html",
            f"{sitemap.SITE}/articles/{self.future.name}",
        ])
        self.assertEqual(len(locations), len(set(locations)))
        self.assertFalse(root.findall(f".//{namespace}lastmod"))
        self.assertNotIn(f"{sitemap.SITE}/articles.html", locations)

    def test_rejects_invalid_article_date(self) -> None:
        (self.articles / "2099_13_01_invalido.html").write_text("", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Data inválida"):
            sitemap.build_sitemap(self.docs)

    def test_rejects_noindex_redirect_and_wrong_canonical(self) -> None:
        url = f"{sitemap.SITE}/articles/{self.future.name}"
        for canonical, extra in [
            (url, '<meta content="noindex, follow" name="robots">'),
            (url, '<meta content="0; url=/" http-equiv="refresh">'),
            (f"{sitemap.SITE}/", ""),
        ]:
            with self.subTest(canonical=canonical, extra=extra):
                self.write_page(self.future, canonical, extra)
                with self.assertRaises(ValueError):
                    sitemap.build_sitemap(self.docs)

    def test_check_detects_missing_stale_and_duplicate_entries(self) -> None:
        body = sitemap.build_sitemap(self.docs)
        with patch.object(sitemap, "ROOT", self.root), patch.object(sitemap, "SITEMAP_PATH", self.sitemap_path):
            with self.assertRaises(SystemExit):
                sitemap.main(check=True)
            self.sitemap_path.write_text(body, encoding="utf-8")
            sitemap.main(check=True)
            for changed in [
                body.replace(f"{sitemap.SITE}/articles/{self.future.name}", f"{sitemap.SITE}/articles/old.html"),
                body.replace("</urlset>", f"  <url><loc>{sitemap.SITE}/</loc></url>\n</urlset>"),
                "<urlset",
            ]:
                with self.subTest(changed=changed):
                    self.sitemap_path.write_text(changed, encoding="utf-8")
                    with self.assertRaises(SystemExit):
                        sitemap.main(check=True)


if __name__ == "__main__":
    unittest.main()
