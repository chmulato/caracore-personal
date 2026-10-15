from datetime import date
import unittest
import xml.etree.ElementTree as ET

import update_sitemap as sitemap


class SitemapTests(unittest.TestCase):
    def make_sitemap(self, home_date: date, article_date: date) -> str:
        entries = [
            sitemap.render_url(f"{sitemap.SITE}/", home_date, "daily", "1.0"),
            sitemap.render_url(
                f"{sitemap.SITE}/articles.html", home_date, "daily", "0.8"
            ),
            sitemap.render_url(
                f"{sitemap.SITE}/articles/2026_10_12_article.html",
                article_date,
                "monthly",
                "0.6",
            ),
        ]
        return "\n".join(
            [
                '<?xml version="1.0" encoding="UTF-8"?>',
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
                "\n".join(entries),
                "</urlset>",
                "",
            ]
        )

    def test_without_daily_lastmod_ignores_only_index_dates(self) -> None:
        first = self.make_sitemap(date(2026, 10, 14), date(2026, 10, 12))
        second = self.make_sitemap(date(2026, 10, 15), date(2026, 10, 12))
        self.assertEqual(
            sitemap.without_daily_lastmod(first),
            sitemap.without_daily_lastmod(second),
        )

        changed_article = self.make_sitemap(date(2026, 10, 15), date(2026, 10, 13))
        self.assertNotEqual(
            sitemap.without_daily_lastmod(first),
            sitemap.without_daily_lastmod(changed_article),
        )

    def test_without_daily_lastmod_rejects_invalid_xml(self) -> None:
        with self.assertRaises(ET.ParseError):
            sitemap.without_daily_lastmod("<urlset")

    def test_without_daily_lastmod_rejects_invalid_index_date(self) -> None:
        invalid = self.make_sitemap(date(2026, 10, 14), date(2026, 10, 12))
        invalid = invalid.replace("2026-10-14", "not-a-date", 1)
        with self.assertRaises(ValueError):
            sitemap.without_daily_lastmod(invalid)


if __name__ == "__main__":
    unittest.main()
