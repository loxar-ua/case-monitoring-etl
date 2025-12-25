import unittest
from datetime import datetime, timezone, timedelta
from src.scrapper.scrappers.all_scrappers import BabelScrapper
from tests.base_test import BaseTestCase
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase

TEST_URL_1 = "https://babel.ua/news/122971-turechchina-pidtverdila-zagibel-20-viyskovih-pid-chas-avariji-litaka-c-130"

class TestBabelScrapper(CommonScrapperTestCase, BaseTestCase):
    scrapper_class = BabelScrapper

    media_data = {
        "name": "Бабель",
        "sitemap_index_url": "https://babel.ua/sitemap_full.xml"
    }

    get_links_data = {
        "start_date": datetime(2025, 11, 12, 8, 22,33, tzinfo=timezone.utc),
        "end_date": datetime(2025, 11, 12, 8, 30, tzinfo=timezone.utc),
        "expected_links": [TEST_URL_1]
    }

    parse_article_data = {
        "link": TEST_URL_1,
        "title": "Туреччина підтвердила загибель 20 військових під час аварії літака C-130",
        "featured_image_url": "https://babel.ua/static/content/frtlki9g/thumbs/1200x630/a/46/580b5f2bca66d366242f14db9841046a.jpg?v=5275",
        "author": "Ольга Березюк",
        "published_at": datetime(2025, 11, 12, 7, 28,34, tzinfo=timezone(timedelta(hours=2)))
    }

if __name__ == '__main__':
    unittest.main()

