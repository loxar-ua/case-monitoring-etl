import unittest
from src.scrapper.scrappers.all_scrappers import TyzhdenScrapper
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase
from datetime import datetime, timezone, timedelta

TEST_URL_1="https://tyzhden.ua/svidchennia-1933-ho/"
TEST_URL_2="https://tyzhden.ua/v-tyshi-lopotinnia-praporiv/"

class TestTyzhdenScrapper(CommonScrapperTestCase, unittest.TestCase,):
    scrapper_class = TyzhdenScrapper

    media_data = {
        "name": "Український тиждень",
        "sitemap_index_url": "https://tyzhden.ua/wp-sitemap.xml"
    }

    get_links_data = {
        "start_date": datetime(2025, 11, 22, 21, 51, tzinfo=timezone(timedelta(hours=2))),
        "end_date": datetime(2025, 11, 23, 1, 46, tzinfo=timezone(timedelta(hours=2))),
        "expected_links": [TEST_URL_1, TEST_URL_2]
    }

    parse_article_data = {
        "link": TEST_URL_2,
        "title": "В тиші лопотіння прапорів | Український тиждень",
        "featured_image_url": "https://tyzhden.ua/wp-content/uploads/2025/04/petrenko-on.jpg",
        "author": "Ольга Петренко-Цеунова",
        "published_at": datetime(2025, 11, 3, 14, 1, 26, tzinfo=timezone(timedelta(hours=2)))
    }

if __name__ == '__main__':
    unittest.main()
