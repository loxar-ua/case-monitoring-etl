import unittest
from unittest.mock import patch

from datetime import datetime, timezone

from src.scrapper.scrappers.base_scrapper import ArticleInfo
from src.scrapper.scrappers.nashi_groshi_scrapper import NashiGroshiScrapper
from src.database.models.media import Media
from src.database.models.article import Article
from tests.helpers import create_mock_response

TEST_URL_1 = "https://nashigroshi.org/2025/11/03/enerhoatom-za-19-mil-yoniv-zastrakhuvav-nahliadovu-radu-na-vypadok-areshtiv/"
TEST_URL_2 = "https://nashigroshi.org/2025/11/03/politsiia-upershe-zamovyla-broneshchyty-velmet-z-likhtariamy-odrazu-na-53-mil-yony/"
class TestNashiGroshiScrapper(unittest.TestCase):
    def setUp(self):
        media_orm = Media(
            name="НАШІ ГРОШІ",
            sitemap_index_url="https://nashigroshi.org/sitemap.xml",
            is_active=True
        )

        self.scrapper = NashiGroshiScrapper(media_orm)

    @patch('src.utils.get_response.requests.get')
    @patch('src.utils.get_response.random.uniform')
    def test_get_links(self, mock_uniform, mock_get):
        """Test get_links returns correct links for start_date and end_date.
        When start_date is in end of previous sitemap
        and end_date is at the start of next sitemap."""

        mock_get.side_effect = create_mock_response
        mock_uniform.return_value = 0

        start_date = datetime(2025, 10, 31, 13, 21, tzinfo=timezone.utc)
        end_date = datetime(2025, 10, 31, 13, 28, tzinfo=timezone.utc)

        retrieved = self.scrapper.get_links(start_date, end_date)

        self.assertEqual(len(retrieved), 2)
        self.assertEqual(retrieved[0], TEST_URL_2)
        self.assertEqual(retrieved[1], TEST_URL_1)


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

        self.assertEqual(retrieved.title, ("«Енергоатом» за 19 мільйонів застрахував наглядову раду на випадок арештів"))

        self.assertEqual(retrieved.author, "Анна Сорока, «Наші гроші»")
        print(retrieved.featured_image_url)

        self.assertEqual(retrieved.published_at, datetime(2025, 11, 3, 0, 0, tzinfo=timezone.utc))



if __name__ == '__main__':
    unittest.main()



