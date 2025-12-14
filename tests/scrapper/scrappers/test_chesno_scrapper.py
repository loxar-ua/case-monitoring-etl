import unittest
from datetime import datetime, timezone, timedelta
from src.scrapper.scrappers.all_scrappers import ChesnoScrapper
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase

TEST_URL_1 = "https://www.chesno.org/post/6645/"

class TestChesnoScrapper(CommonScrapperTestCase, unittest.TestCase,):
    scrapper_class = ChesnoScrapper

    media_data = {
        "name": "Chesno",
        "sitemap_index_url": "https://www.chesno.org/sitemap.xml"
    }

    get_links_data = {
        "start_date": datetime(2025, 11, 20, 15, 15, tzinfo=timezone.utc),
        "end_date": datetime(2025, 11, 21, 0, 0, tzinfo=timezone.utc),
        "expected_links": [TEST_URL_1]
    }

    parse_article_data = {
        "link": TEST_URL_1,
        "title": "“Кравчучка” та продуктові набори: як депутати “турбуються” про людей похилого віку",
        "featured_image_url": "https://cdn.chesno.org/web/media/thumbs/posts/2025/11/21/jdv_7TGxlG15.jpg",
        "author": "Юлія Олещенко",
        "published_at": datetime(datetime.now().year, 11, 21, 10, 26,
                            tzinfo=timezone(timedelta(hours=2)))
    }

if __name__ == '__main__':
    unittest.main()