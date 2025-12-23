import unittest
from datetime import datetime, timezone, timedelta
from src.scrapper.scrappers.all_scrappers import SuspilneScrapper
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase

TEST_URL_1 = "https://suspilne.media/1164184-ssa-skasuvali-sankcii-zaprovadzeni-proti-proektu-aes-v-ugorsini-aku-budue-rosijskij-rosatom/"
TEST_URL_2 = "https://suspilne.media/1164200-kudrickij-pro-korupcijnu-spravu-v-energetici-ta-comu-vin-bi-ne-hotiv-ocoliti-minenergo/"

class TestSuspilneScrapper(CommonScrapperTestCase, unittest.TestCase):
    scrapper_class = SuspilneScrapper

    media_data = {
        "name": "Suspilne",
        "sitemap_index_url": "https://suspilne.media/suspilne/sitemap/sitemap.xml",
    }

    get_links_data = {
        "start_date": datetime(2025, 11, 14, 0, 20, tzinfo=timezone.utc),
        "end_date": datetime(2025, 11, 14, 2, 24, tzinfo=timezone.utc),
        "expected_links": [TEST_URL_2],
    }

    parse_article_data = {
        "link": TEST_URL_2,
        "title": "Кудрицький про корупцію в енергетиці й чому не повернеться в держсектор",
        "featured_image_url": "https://cdn4.suspilne.media/images/resize/600x1.78/7cef7f0f4f2df7f3.jpg",
        "author": "Юлія Кузьменко",
        "published_at": datetime(2025, 11, 14, 0, 22, 12, tzinfo=timezone(timedelta(hours=2)))
    }

if __name__ == '__main__':
    unittest.main()
