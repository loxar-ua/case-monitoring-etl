import unittest
from datetime import datetime, timezone
from src.scrapper.scrappers.antac_scrapper import AntacScrapper
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase

TEST_URL_1 = "https://antac.org.ua/en/news/how-avakov-venediktova-and-pechersk-court-rescue-the-agrobaron-bakhmatyuk-and-his-property/"
TEST_URL_2 = "https://antac.org.ua/news/shans-dlia-realnoi-sudovoi-reformy-rada-pidtrymala-ochyshchennia-vyshchoi-rady-pravosuddia/"

class TestBihusInfoScrapper(CommonScrapperTestCase, unittest.TestCase,):
    scrapper_class = AntacScrapper

    media_data = {
        "name": "Antac",
        "sitemap_index_url": "https://antac.org.ua/sitemap_index.xml"
    }

    get_links_data = {
        "start_date": datetime(2021, 7, 13, 11, 0, tzinfo=timezone.utc),
        "end_date": datetime(2021, 7, 14, 11, 0, tzinfo=timezone.utc),
        "expected_links": [TEST_URL_1, TEST_URL_2]
    }

    parse_article_data = {
        "link": TEST_URL_2,
        "title": "Шанс для реальної судової реформи: Рада підтримала очищення Вищої ради правосуддя - Центр Протидії Корупції",
        "featured_image_url": "https://antac.org.ua/wp-content/uploads/2020/10/Zelenskyy-venetsyanka.jpg",
        "author": None,
        "published_at": datetime(2021, 7, 19, 10, 48, 38, tzinfo=timezone.utc)
    }

if __name__ == '__main__':
    unittest.main()

