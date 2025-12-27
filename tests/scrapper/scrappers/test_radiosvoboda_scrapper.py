import unittest
from datetime import datetime, timezone, timedelta
from src.scrapper.scrappers.all_scrappers import RadioSvobodaScrapper
from tests.base_test import BaseTestCase
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase

TEST_URL_1 = "https://www.radiosvoboda.org/a/news-rosia-ataka-droniv/33629716.html"

class TestRadioSvobodaScrapper(CommonScrapperTestCase, BaseTestCase):
    scrapper_class = RadioSvobodaScrapper

    media_data = {
        "name": "Radio Svoboda",
        "sitemap_index_url": "https://www.radiosvoboda.org/sitemap.xml",
    }

    get_links_data = {
        "start_date": datetime(2025, 12, 22, 5, 48,53, tzinfo=timezone.utc),
        "end_date": datetime(2025, 12, 22, 5, 49, tzinfo=timezone.utc),
        "expected_links": [TEST_URL_1]
    }

    parse_article_data = {
        "link": TEST_URL_1,
        "title": "У РФ заявили про пошкодження двох причалів, двох суден і трубопроводу через атаку дронів",
        "featured_image_url": "https://gdb.rferl.org/01000000-0aff-0242-6226-08db4bb992b5_cx19_cy18_cw73_w1200_h630.jpg",
        "author": None,
        "published_at": datetime(2025, 12, 22, 7, 48, 53,  tzinfo=timezone(timedelta(hours=2)))
    }

if __name__ == '__main__':
    unittest.main()
