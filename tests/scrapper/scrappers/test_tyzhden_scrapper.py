import unittest
from unittest.mock import patch

from datetime import datetime, timezone, timedelta

from src.scrapper.scrappers.base_scrapper import ArticleInfo
from src.scrapper.scrappers.tyzhden_scrapper import TyzhdenScrapper
from src.database.models.media import Media
from src.database.models.article import Article
from tests.helpers import create_mock_response, URL_TO_FIXTURE_MAP, FIXTURE_PATH

TEST_URL_1="https://tyzhden.ua/v-tyshi-lopotinnia-praporiv/"
TEST_URL_2="https://tyzhden.ua/svidchennia-1933-ho/"

class TestTyzhdenScrapper(unittest.TestCase):
    def setUp(self):
        media_orm = Media(
            name="Tyzhden",
            sitemap_index_url="https://tyzhden.ua/wp-sitemap.xml",
            is_active=True
        )

        self.scrapper = TyzhdenScrapper(media_orm)

    @patch('src.utils.get_response.requests.get')
    @patch('src.utils.get_response.random.uniform')
    def test_get_links(self, mock_uniform, mock_get):
        """Test get_links returns correct links for start_date and end_date.
        When start_date is in end of previous sitemap
        and end_date is at the start of next sitemap."""

        mock_get.side_effect = create_mock_response
        mock_uniform.return_value = 0

        start_date = datetime(2025, 11, 22, 21, 51, tzinfo=timezone(timedelta(hours=2)))
        end_date = datetime(2025, 11, 23, 1, 46, tzinfo=timezone(timedelta(hours=2)))

        retrieved = self.scrapper.get_links(start_date, end_date)

        self.assertEqual(len(retrieved), 2)
        self.assertEqual(retrieved[0], TEST_URL_1)
        self.assertEqual(retrieved[1], TEST_URL_2)

    @patch('src.utils.get_response.requests.get')
    @patch('src.utils.get_response.random.uniform')
    def test_parse_article(self, mock_uniform, mock_get):
        """Test parse_article returns correct article.
        Using all other _get_element functions"""

        mock_get.side_effect = create_mock_response
        mock_uniform.return_value = 0

        retrieved = self.scrapper.parse_article(TEST_URL_1)

        self.assertIsInstance(retrieved, ArticleInfo)

        self.assertEqual(retrieved.link, TEST_URL_1)

        self.assertEqual(retrieved.title, ("В тиші лопотіння прапорів | Український тиждень"))

        self.assertEqual(retrieved.featured_image_url, "https://tyzhden.ua/wp-content/uploads/2025/04/petrenko-on.jpg")

        self.assertEqual(retrieved.published_at, datetime(2025, 11, 3, 14, 1, 26, tzinfo=timezone(timedelta(hours=2))))


if __name__ == '__main__':
    unittest.main()




