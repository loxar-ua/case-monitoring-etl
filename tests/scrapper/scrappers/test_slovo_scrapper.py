import unittest
from datetime import datetime, timezone, timedelta
from src.scrapper.scrappers.all_scrappers import SlovoScrapper
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase

TEST_URL_1 = "https://www.slovoidilo.ua/2025/11/25/novyna/polityka/komandi-trampa-rozpochalasya-pryxovana-borotba-cherez-myrnyj-plan-shhodo-ukrayiny-zmi"
TEST_URL_2 ="https://www.slovoidilo.ua/2025/11/25/novyna/polityka/sud-zalyshyv-vartoyu-fihurantku-spravy-midas-ustymenko"

class TestSlovoScrapper(CommonScrapperTestCase, unittest.TestCase,):
    scrapper_class = SlovoScrapper

    media_data = {
        "name": "Слово і Діло",
        "sitemap_index_url": "https://www.slovoidilo.ua/sitemap_index_uk.xml"
    }

    get_links_data = {
        "start_date": datetime(2025, 11, 25, 12, 25, 19,  tzinfo=timezone.utc),
        "end_date": datetime(2025, 11, 25, 12, 25, 57,   tzinfo=timezone.utc),
        "expected_links": [TEST_URL_1, TEST_URL_2]
    }

    parse_article_data = {
        "link": TEST_URL_1,
        "title": "У команді Трампа розпочалася прихована боротьба через мирний план щодо України – ЗМІ",
        "featured_image_url": "https://media.slovoidilo.ua/media/scimage/229/228526-uk.png",
        "author": None,
        "published_at": datetime(2025, 11, 25, 12, 25, 19)
    }

if __name__ == '__main__':
    unittest.main()
