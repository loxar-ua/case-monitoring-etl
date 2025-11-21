import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup

from datetime import datetime, timezone

from src.scrapper.scrappers.base_scrapper import ArticleInfo
from src.scrapper.scrappers.bihus_info_scrapper import BihusInfoScrapper
from src.database.models.media import Media
from src.database.models.article import Article
from tests.helpers import create_mock_response, URL_TO_FIXTURE_MAP, FIXTURE_PATH

TEST_URL_1 = "https://bihus.info/rosijski-vijskovi-na-sumshhyni-zahopyly-zhytlovyj-budynok-a-potim-rozstrilyaly-jogo-iz-kulemeta/"
TEST_URL_2 = "https://bihus.info/ne-bulo-ni-zvuku-ni-svystu-vidrazu-pidnyalas-velyka-pylyuka-potim-des-za-2-sekundy-posypalys-vikna-na-zhytomyrshhyni-rosijska-krylata-raketa-rozbyla-shkolu/"

class TestBihusInfoScrapper(unittest.TestCase):
    def setUp(self):
        media_orm = Media(
            name="Bihus.Info",
            sitemap_index_url="https://bihus.info/sitemap_index.xml",
            is_active=True
        )

        self.scrapper = BihusInfoScrapper(media_orm)

    @patch('src.utils.get_response.requests.get')
    @patch('src.utils.get_response.random.uniform')
    def test_get_links(self, mock_uniform, mock_get):
        """Test get_links returns correct links for start_date and end_date.
        When start_date is in end of previous sitemap
        and end_date is at the start of next sitemap."""

        mock_get.side_effect = create_mock_response
        mock_uniform.return_value = 0

        start_date = datetime(2022, 5, 4, 15, 15, tzinfo=timezone.utc)
        end_date = datetime(2022, 5, 4, 15, 19, tzinfo=timezone.utc)

        retrieved = self.scrapper.get_links(start_date, end_date)

        self.assertEqual(len(retrieved), 2)
        self.assertEqual(retrieved[0], TEST_URL_1)
        self.assertEqual(retrieved[1], TEST_URL_2)


if __name__ == '__main__':
    unittest.main()




