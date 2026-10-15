import re
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from unittest.mock import patch

import update_feed as feed


class FeedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.images = self.root / "docs" / "articles" / "assets" / "img"
        self.images.mkdir(parents=True)
        self.image = self.images / "cover.webp"
        self.image.write_bytes(b"test-image")
        self.patch = patch.object(feed, "ROOT", self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.article = {
            "date": datetime(2029, 3, 1),
            "title": "A & B ]]> C",
            "description": "Description",
            "link": f"{feed.ARTICLES_BASE}2029_03_01_article.html?a=1&b=2",
            "hero": f"{feed.ARTICLES_BASE}assets/img/cover.webp?a=1&b=2",
            "content": "<p>A &amp; B</p>",
        }

    def test_future_articles_keep_publication_dates_not_build_dates(self) -> None:
        built_at = datetime(2026, 10, 12, 17, 30, tzinfo=timezone.utc)
        channel = ET.fromstring(feed.build_feed([self.article], built_at)).find("channel")
        self.assertEqual(parsedate_to_datetime(channel.findtext("lastBuildDate")), built_at)
        self.assertEqual(parsedate_to_datetime(channel.findtext("item/pubDate")).year, 2029)
        self.assertEqual(channel.findtext("item/title"), self.article["title"])
        self.assertEqual(channel.findtext("item/link"), self.article["link"])

    def test_enclosure_has_real_size_mime_and_escaped_url(self) -> None:
        item = ET.fromstring(feed.build_feed([self.article])).find("channel/item")
        enclosure = item.find("enclosure")
        self.assertEqual(enclosure.get("length"), str(self.image.stat().st_size))
        self.assertEqual(enclosure.get("type"), "image/webp")
        self.assertEqual(enclosure.get("url"), self.article["hero"])
        self.assertEqual(item.find("{http://search.yahoo.com/mrss/}content").get("fileSize"),
                         enclosure.get("length"))

    def test_empty_feed_is_valid(self) -> None:
        channel = ET.fromstring(feed.build_feed([])).find("channel")
        self.assertEqual(channel.findall("item"), [])
        self.assertIsNotNone(parsedate_to_datetime(channel.findtext("lastBuildDate")).tzinfo)

    def test_without_build_date_ignores_only_volatile_timestamp(self) -> None:
        first = feed.build_feed(
            [self.article], datetime(2026, 10, 12, 17, 30, tzinfo=timezone.utc)
        )
        second = feed.build_feed(
            [self.article], datetime(2026, 10, 14, 22, 0, tzinfo=timezone.utc)
        )
        self.assertEqual(feed.without_build_date(first), feed.without_build_date(second))

        changed = {**self.article, "description": "Updated description"}
        third = feed.build_feed(
            [changed], datetime(2026, 10, 14, 22, 0, tzinfo=timezone.utc)
        )
        self.assertNotEqual(feed.without_build_date(first), feed.without_build_date(third))

    def test_without_build_date_rejects_missing_timestamp(self) -> None:
        with self.assertRaises(ValueError):
            feed.without_build_date("<rss><channel></channel></rss>")

    def test_without_build_date_rejects_invalid_timestamp(self) -> None:
        invalid = feed.build_feed([])
        invalid = re.sub(
            r"(<lastBuildDate>).*?(</lastBuildDate>)",
            r"\1not-a-date\2",
            invalid,
            count=1,
            flags=re.S,
        )
        with self.assertRaises(ValueError):
            feed.without_build_date(invalid)

    def test_check_mode_leaves_feed_unchanged_and_detects_stale_content(self) -> None:
        target = self.root / "docs" / "feed.xml"
        empty_articles = self.root / "empty-articles"
        empty_articles.mkdir()
        previous = feed.build_feed(
            [], datetime(2026, 10, 12, 17, 30, tzinfo=timezone.utc)
        )
        target.write_text(previous, encoding="utf-8")

        with patch.object(feed, "FEED_PATH", target), \
             patch.object(feed, "ARTICLES_DIR", empty_articles):
            feed.main(check=True)
            self.assertEqual(target.read_text(encoding="utf-8"), previous)

            stale = feed.build_feed(
                [self.article],
                datetime(2026, 10, 12, 17, 30, tzinfo=timezone.utc),
            )
            target.write_text(stale, encoding="utf-8")
            with self.assertRaises(SystemExit):
                feed.main(check=True)

    def test_rfc822_preserves_time_and_timezone(self) -> None:
        value = datetime(2026, 10, 12, 14, 35, 42, tzinfo=timezone.utc)
        self.assertEqual(parsedate_to_datetime(feed.rfc822(value)), value)

    def test_missing_image_fails(self) -> None:
        self.image.unlink()
        with self.assertRaises(FileNotFoundError):
            feed.render_item(self.article)

    def test_empty_image_fails(self) -> None:
        self.image.write_bytes(b"")
        with self.assertRaises(ValueError):
            feed.render_item(self.article)

    def test_external_or_traversing_image_fails(self) -> None:
        for url in ("https://example.com/cover.webp",
                    f"{feed.SITE}/%2e%2e/cover.webp"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                feed.hero_size(url)

    def test_invalid_xml_does_not_overwrite_previous_feed(self) -> None:
        target = self.root / "docs" / "feed.xml"
        target.write_text("previous-feed", encoding="utf-8")
        with patch.object(feed, "ARTICLES_DIR", self.root / "empty"), \
             patch.object(feed, "FEED_PATH", target), \
             patch.object(feed, "build_feed", return_value="<invalid"):
            with self.assertRaises(ET.ParseError):
                feed.main()
        self.assertEqual(target.read_text(encoding="utf-8"), "previous-feed")

    def test_absolutize_links_preserves_fragments_and_external_urls(self) -> None:
        markup = '<a href="2026_10_12_article.html">Article</a><a href="#terms">Terms</a>'
        fixed = feed.absolutize_html(markup)
        self.assertIn(f'href="{feed.ARTICLES_BASE}2026_10_12_article.html"', fixed)
        self.assertIn('href="#terms"', fixed)

    def test_code_samples_are_not_rewritten_as_resource_urls(self) -> None:
        markup = '<pre><code>&lt;source src="{video_path}"&gt;</code></pre>'
        self.assertEqual(feed.absolutize_html(markup), markup)

    def test_attribute_with_greater_than_sign_is_preserved(self) -> None:
        markup = '<img alt="A > B" src="assets/img/cover.webp">'
        self.assertEqual(feed.absolutize_html(markup),
                         f'<img alt="A > B" src="{feed.ARTICLES_BASE}assets/img/cover.webp">')


if __name__ == "__main__":
    unittest.main()
