import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup

from datetime import datetime, timezone

from src.scrapper.scrappers.base_scrapper import ArticleInfo
from src.scrapper.scrappers.bihus_info_scrapper import BihusInfoScrapper
from src.database.models.media import Media
from src.database.models.article import Article
from tests.helpers import create_mock_response, URL_TO_FIXTURE_MAP, FIXTURE_PATH

TEST_URL = "https://bihus.info/rosijski-vijskovi-na-sumshhyni-zahopyly-zhytlovyj-budynok-a-potim-rozstrilyaly-jogo-iz-kulemeta/"

class TestBaseScrapper(unittest.TestCase):
    def setUp(self):
        media_orm = Media(
            name="Bihus.Info",
            sitemap_index_url="https://bihus.info/sitemap_index.xml",
            is_active=True
        )

        self.scrapper = BihusInfoScrapper(media_orm)

    @patch('src.utils.get_response.requests.get')
    @patch('src.utils.get_response.random.uniform')
    def test__get_article_soup(self, mock_uniform, mock_get):
        """Test _get_soup return correct """

        mock_get.side_effect = create_mock_response
        mock_uniform.return_value = 0

        retrieved = self.scrapper._get_article_soup(TEST_URL)

        article_path = FIXTURE_PATH / URL_TO_FIXTURE_MAP[TEST_URL]

        with open(article_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        self.assertIsInstance(retrieved, BeautifulSoup)
        self.assertEqual(retrieved.prettify(), soup.prettify())

    @patch('src.utils.get_response.requests.get')
    @patch('src.utils.get_response.random.uniform')
    def test_parse_article(self, mock_uniform, mock_get):
        """Test parse_article returns correct article.
        Using all other _get_element functions"""

        mock_get.side_effect = create_mock_response
        mock_uniform.return_value = 0

        retrieved = self.scrapper.parse_article(TEST_URL)

        self.assertIsInstance(retrieved, ArticleInfo)

        self.assertEqual(retrieved.link, TEST_URL)

        self.assertEqual(retrieved.title, ("На Херсонщині ворог вбиває людей, нищить "
                                           "населені пункти, краде авто та використовує заборонені "
                                           "види озброєння проти цивільних - Bihus.Info"))

        self.assertEqual(retrieved.featured_image_url, "https://bihus.info/wp-content/uploads/2022/04/prevyu.jpg")

        self.assertEqual(retrieved.author, "bihus.info")

        self.assertEqual(retrieved.published_at, datetime(2022, 4, 19, 14, 52, 43, tzinfo=timezone.utc))


if __name__ == '__main__':
    unittest.main()