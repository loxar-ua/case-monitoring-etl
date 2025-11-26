import unittest
from src.scrapper.scrappers.nashi_groshi_scrapper import NashiGroshiScrapper
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase
from datetime import datetime, timezone

TEST_URL_1 = "https://nashigroshi.org/2025/11/03/enerhoatom-za-19-mil-yoniv-zastrakhuvav-nahliadovu-radu-na-vypadok-areshtiv/"
TEST_URL_2 = "https://nashigroshi.org/2025/11/03/politsiia-upershe-zamovyla-broneshchyty-velmet-z-likhtariamy-odrazu-na-53-mil-yony/"


class TestNashiGroshiScrapper(CommonScrapperTestCase, unittest.TestCase,):
    scrapper_class = NashiGroshiScrapper

    media_data = {
        "name": "НАШІ ГРОШІ",
        "sitemap_index_url": "https://nashigroshi.org/sitemap.xml"
    }

    get_links_data = {
        "start_date": datetime(2025, 10, 31, 13, 21, tzinfo=timezone.utc),
        "end_date": datetime(2025, 10, 31, 13, 28, tzinfo=timezone.utc),
        "expected_links": [TEST_URL_1, TEST_URL_2]
    }

    parse_article_data = {
        "link": TEST_URL_1,
        "title": "«Енергоатом» за 19 мільйонів застрахував наглядову раду на випадок арештів",
        "author": "Анна Сорока, «Наші гроші»",
        "featured_image_url": "https://nashigroshi.org/wp-content/uploads/2025/10/enerhoatom-nahliadova-300x215.png",
        "published_at":  datetime(2025, 11, 3, 0, 0, tzinfo=timezone.utc)
    }

if __name__ == '__main__':
    unittest.main()