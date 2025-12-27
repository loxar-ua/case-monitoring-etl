import unittest
from abc import ABC, abstractmethod
from unittest.mock import patch

from src.database.models.media import Media
from src.database.models.article import Article
from src.scrapper.scrappers import ArticleInfo
from tests.helpers import create_mock_response


class CommonScrapperTestCase(ABC):
    """ A generic test class that holds the logic for testing any scraper.
    Subclasses must define the configuration properties below."""

    @property
    @abstractmethod
    def scrapper_class(self):
        """The class of the scraper to test (e.g. BihusInfoScrapper)"""
        pass

    @property
    @abstractmethod
    def media_data(self):
        """Dict with 'name' and 'sitemap_index_url'"""
        pass

    @property
    @abstractmethod
    def get_links_data(self):
        """Dict with 'start_date', 'end_date', and 'expected_links' (list)"""
        pass

    @property
    @abstractmethod
    def parse_article_data(self):
        """Dict with 'url' to parse and 'expected' dictionary of values"""
        pass

    def setUp(self):
        media_orm = Media(
            name=self.media_data['name'],
            sitemap_index_url=self.media_data['sitemap_index_url'],
            is_active=True
        )

        self.scrapper = self.scrapper_class(media_orm)

    @patch('src.database.get_response.requests.get')
    @patch('src.database.get_response.random.uniform')
    def test_get_links(self, mock_uniform, mock_get):
        """Test get_links returns correct links for start_date and end_date.
        When start_date is in end of previous sitemap
        and end_date is at the start of next sitemap."""

        mock_get.side_effect = create_mock_response
        mock_uniform.return_value = 0

        data = self.get_links_data

        retrieved = self.scrapper.get_links(data['start_date'], data['end_date'])

        self.assertEqual(len(retrieved), len(data['expected_links']))
        self.assertEqual(retrieved, data['expected_links'])

    @patch('src.database.get_response.requests.get')
    @patch('src.database.get_response.random.uniform')
    def test_parse_article(self, mock_uniform, mock_get):
        """Test parse_article returns correct article.
        Using all other _get_element functions"""

        mock_get.side_effect = create_mock_response
        mock_uniform.return_value = 0

        data = self.parse_article_data

        retrieved = self.scrapper.parse_article(data["link"])

        self.assertEqual(retrieved["link"], data["link"])
        self.assertEqual(retrieved["title"], data["title"])
        self.assertEqual(retrieved["featured_image_url"], data["featured_image_url"])
        self.assertEqual(retrieved["author"], data["author"])
        self.assertEqual(retrieved["published_at"], data["published_at"])