import unittest
from datetime import datetime, timezone
from src.scrapper.scrappers.bihus_info_scrapper import BihusInfoScrapper
from tests.scrapper.scrappers.common_scrapper_test import CommonScrapperTestCase

TEST_URL_1 = "https://bihus.info/rosijski-vijskovi-na-sumshhyni-zahopyly-zhytlovyj-budynok-a-potim-rozstrilyaly-jogo-iz-kulemeta/"
TEST_URL_2 = "https://bihus.info/ne-bulo-ni-zvuku-ni-svystu-vidrazu-pidnyalas-velyka-pylyuka-potim-des-za-2-sekundy-posypalys-vikna-na-zhytomyrshhyni-rosijska-krylata-raketa-rozbyla-shkolu/"


class TestBihusInfoScrapper(CommonScrapperTestCase, unittest.TestCase,):
    scrapper_class = BihusInfoScrapper

    media_data = {
        "name": "Bihus.Info",
        "sitemap_index_url": "https://bihus.info/sitemap_index.xml"
    }

    get_links_data = {
        "start_date": datetime(2022, 5, 4, 15, 15, tzinfo=timezone.utc),
        "end_date": datetime(2022, 5, 4, 15, 19, tzinfo=timezone.utc),
        "expected_links": [TEST_URL_1, TEST_URL_2]
    }

    parse_article_data = {
        "link": TEST_URL_1,
        "title": "На Херсонщині ворог вбиває людей, нищить населені пункти, краде авто та використовує заборонені види озброєння проти цивільних - Bihus.Info",
        "featured_image_url": "https://bihus.info/wp-content/uploads/2022/04/prevyu.jpg",
        "author": "bihus.info",
        "published_at": datetime(2022, 4, 19, 14, 52, 43, tzinfo=timezone.utc)

    }

if __name__ == '__main__':
    unittest.main()