import unittest
from datetime import datetime, timezone, timedelta
from src.scrapper.scrappers.pravda_scrapper import PravdaScrapper
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase

TEST_URL_1 = "https://www.pravda.com.ua/news/2025/12/01/8009697/"


class TestPravdaScrapper(CommonScrapperTestCase, unittest.TestCase,):
    scrapper_class = PravdaScrapper

    media_data = {
        "name": "Українська Правда",
        "sitemap_index_url": "https://www.pravda.com.ua/sitemap/sitemap-archive.xml"
    }

    get_links_data = {
        "start_date": datetime(2025, 12, 1, 0, 8,  tzinfo=timezone.utc),
        "end_date": datetime(2025, 12, 1, 0, 8,  tzinfo=timezone.utc),
        "expected_links": [TEST_URL_1]
    }

    parse_article_data = {
        "link": TEST_URL_1,
        "title": "Трамп заявив про \"деякі складні проблеми\" в України і \"хороший шанс\" для \"мирної угоди\"",
        "featured_image_url": "https://uimg.pravda.com.ua/buckets/upstatic/images/doc/6/a/724555/6aaa17a160e16e81770c0626b62e23cf.jpeg?w=1200&q=85&stamp=1764540527",
        "author": "Ольга Глущенко",
        "published_at": datetime(datetime.now().year, 12, 1, 0, 8,
                            tzinfo=timezone(timedelta(hours=2)))
    }

if __name__ == '__main__':
    unittest.main()