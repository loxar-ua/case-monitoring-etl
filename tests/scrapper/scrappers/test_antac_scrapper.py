import unittest
from unittest.mock import patch

from datetime import datetime, timezone

from src.scrapper.scrappers.base_scrapper import ArticleInfo
from src.scrapper.scrappers.antac_scrapper import AntacScrapper
from src.database.models.media import Media
from src.database.models.article import Article
from tests.helpers import create_mock_response

TEST_URL_1 = "https://antac.org.ua/en/news/how-avakov-venediktova-and-pechersk-court-rescue-the-agrobaron-bakhmatyuk-and-his-property/"
TEST_URL_2 = "https://antac.org.ua/news/shans-dlia-realnoi-sudovoi-reformy-rada-pidtrymala-ochyshchennia-vyshchoi-rady-pravosuddia/"

class TestBihusInfoScrapper(unittest.TestCase):
    def setUp(self):
        media_orm = Media(
            name="Antac",
            sitemap_index_url="https://antac.org.ua/sitemap_index.xml",
            is_active=True
        )

        self.scrapper = AntacScrapper(media_orm)

    @patch('src.utils.get_response.requests.get')
    @patch('src.utils.get_response.random.uniform')
    def test_get_links(self, mock_uniform, mock_get):
        """Test get_links returns correct links for start_date and end_date.
        When start_date is in end of previous sitemap
        and end_date is at the start of next sitemap."""

        mock_get.side_effect = create_mock_response
        mock_uniform.return_value = 0

        start_date = datetime(2021, 7, 13, 11, 0, tzinfo=timezone.utc)
        end_date = datetime(2021, 7, 14, 11, 0, tzinfo=timezone.utc)

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

        retrieved = self.scrapper.parse_article(TEST_URL_2)

        self.assertIsInstance(retrieved, ArticleInfo)

        self.assertEqual(retrieved.link, TEST_URL_2)

        self.assertEqual(retrieved.title, ("Шанс для реальної судової реформи: "
                                           "Рада підтримала очищення Вищої ради правосуддя - "
                                           "Центр Протидії Корупції"))

        self.assertEqual(retrieved.featured_image_url, "https://antac.org.ua/wp-content/uploads/2020/10/Zelenskyy-venetsyanka.jpg")

        self.assertEqual(retrieved.author, None)

        self.assertEqual(retrieved.published_at, datetime(2021, 7, 19, 10, 48, 38, tzinfo=timezone.utc))


if __name__ == '__main__':
    unittest.main()




