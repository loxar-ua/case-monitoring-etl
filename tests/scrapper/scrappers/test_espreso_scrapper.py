
import unittest
from datetime import datetime, timezone, timedelta
from src.scrapper.scrappers.all_scrappers import EspresoScrapper
from tests.base_test import BaseTestCase
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase

TEST_URL_2 = "https://espreso.tv/news-proekt-khochu-zhit-opublikuvav-spisok-politvyazniv-zvilnenikh-z-bilorusi"
TEST_URL_1="https://espreso.tv/news-bilorus-pogodilas-pripiniti-zapuskati-povitryani-kuli-na-litvu"

class TestEspresoScrapper(CommonScrapperTestCase,  BaseTestCase):
    scrapper_class = EspresoScrapper

    media_data = {
        "name": "Еспресо",
        "sitemap_index_url": "https://espreso.tv/sitemap.xml"
    }

    get_links_data = {
        "start_date": datetime(2025, 12, 14, 0, tzinfo=timezone.utc),
        "end_date": datetime(2025, 12, 14, 20,  tzinfo=timezone.utc),
        "expected_links": [TEST_URL_1, TEST_URL_2]
    }

    parse_article_data = {
        "link": TEST_URL_1,
        "title": "Білорусь погодилась припинити запускати повітряні кулі на Литву",
        "featured_image_url": "https://static.espreso.tv/uploads/photobank/349000_350000/349227_Lukashenko-Oleksandr.jpg?id=1765734891",
        "author": "Адріана Муллаянова",
        "published_at": datetime(2025, 12, 14, 0, 25, tzinfo=timezone.utc)
    }

if __name__ == '__main__':
    unittest.main()

