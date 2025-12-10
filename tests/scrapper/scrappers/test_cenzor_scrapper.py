import unittest
from datetime import datetime, timezone, timedelta
from src.scrapper.scrappers.cenzor_scrapper import CenzorScrapper
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase

TEST_URL_1 = "https://censor.net/biz/resonance/3589375/skilky-ukrayina-vytratyla-na-zahyst-energetyky"

class TestCenzorScrapper(CommonScrapperTestCase, unittest.TestCase):
    scrapper_class = CenzorScrapper

    media_data = {
        "name": "Цензор",
        "sitemap_index_url": "https://assets.censor.net/sitemap/censor.net/sitemap_uk.xml",
    }

    get_links_data = {
        "start_date": datetime(2025, 12, 10, 9, 43, 13,  tzinfo=timezone.utc),
        "end_date": datetime(2025, 12, 10, 9, 45, tzinfo=timezone.utc),
        "expected_links": [TEST_URL_1]
    }

    parse_article_data = {
        "link": TEST_URL_1,
        "title": "Скільки грошей Україна витрачає на захист енергетики і чому він (не) працює?",
        "featured_image_url": "https://images.cnscdn.com/8/5/4/8/85484964e831bdf367baddbbbccb345c/1200x630.jpg",
        "author": "Михайло Орлюк",
        "published_at": datetime(2025, 12, 9, 9, 30, 1, tzinfo=timezone(timedelta(hours=2)))
    }

if __name__ == '__main__':
    unittest.main()
