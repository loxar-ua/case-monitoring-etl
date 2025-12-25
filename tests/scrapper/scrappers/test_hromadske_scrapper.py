import unittest
from datetime import datetime, timezone, timedelta
from src.scrapper.scrappers.all_scrappers import HromadskeScrapper
from tests.base_test import BaseTestCase
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase

TEST_URL_1 = "https://hromadske.ua/svit/255883-v-universyteti-ssha-ziavytsia-tsilyy-kurs-pro-muzychnu-karyeru-k-pop-artysta"

class TestChesnoScrapper(CommonScrapperTestCase, BaseTestCase):
    scrapper_class = HromadskeScrapper

    media_data = {
        "name": "Громадське",
        "sitemap_index_url": "https://hromadske.ua/sitemap.xml"
    }

    get_links_data = {
        "start_date": datetime(2025, 12, 5, 17, 49,  tzinfo=timezone.utc),
        "end_date": datetime(2025, 12, 5, 17, 50, tzinfo=timezone.utc),
        "expected_links": [TEST_URL_1]
    }

    parse_article_data = {
        "link": TEST_URL_1,
        "title": "В\xa0університеті США з’явиться цілий курс про музичну кар’єру K-Pop-артиста",
        "featured_image_url": "https://hromadske.ua/static/content/thumbs/1200x630/0/a3/u5dh4a---c1200x630x50px50p--2038869e878180227889d2860ec6da30.jpg",
        "author": "Ірина Сітнікова",
        "published_at": datetime(2025, 12, 5, 17, 48,
                            tzinfo=timezone(timedelta(hours=2)))
    }
if __name__ == '__main__':
    unittest.main()