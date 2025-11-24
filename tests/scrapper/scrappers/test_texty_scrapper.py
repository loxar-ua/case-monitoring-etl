import unittest
from datetime import datetime, timezone, timedelta
from src.scrapper.scrappers.texty_scrapper import TextyScrapper
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase

TEST_URL_1 = "https://texty.org.ua/articles/116355/korupcijni-nebesa-hrushevskoho-9a-istoriya-skandalnoho-budivnyctva-j-meshkanciv/"

class TestTextyScrapper(CommonScrapperTestCase, unittest.TestCase,):
    scrapper_class = TextyScrapper

    media_data = {
        "name": "Texty",
        "sitemap_index_url": "https://texty.org.ua/sitemap.xml"
    }

    get_links_data = {
        "start_date": datetime(2025, 11, 23, 15, 15, tzinfo=timezone.utc),
        "end_date": datetime(2025, 11, 25, 0, 0, tzinfo=timezone.utc),
        "expected_links": [TEST_URL_1]
    }

    parse_article_data = {
        "link": TEST_URL_1,
        "title": "Корупційні небеса.  Хто ще живе і як зводився будинок, у якому НАБУ слухало Міндіча",
        "featured_image_url": "https://texty.org.ua/media/images/Zagalniy_vid_0.2e16d0ba.fill-1200x630.jpg",
        "author": "Ірина Касьянова",
        "published_at": datetime(2025, 11, 24, 10, 52,
                            tzinfo=timezone.utc)
    }

if __name__ == '__main__':
    unittest.main()