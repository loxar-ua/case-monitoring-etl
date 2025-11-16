from bs4 import BeautifulSoup

from abc import ABC, abstractmethod
from datetime import datetime
from src.scrapper.scrappers import ArticleInfo

from src.database.models.media import Media

class BaseScrapper(ABC):
    def __init__(self, media_orm: Media, **kwargs):
        super().__init__(**kwargs)

        self.media_orm = media_orm

    @abstractmethod
    def get_links(self, start_date: datetime, end_date: datetime) -> list[str]:
        """Takes starting and ending date for scraping articles from sitemap_index.xml.
        Returns a list of links."""
        pass

    @abstractmethod
    def _get_article_soup(self, link: str) -> BeautifulSoup:
        """Takes link of article and returns the content of articles as BeautifulSoup object."""
        pass

    @abstractmethod
    def _get_featured_image_url(self, article_soup: BeautifulSoup) -> str:
        """Takes content of article in form of soup and returns featured image url."""
        pass

    @abstractmethod
    def _get_title(self, article_soup: BeautifulSoup) -> str:
        """Takes content of article in form of soup and returns title."""
        pass

    @abstractmethod
    def _get_author(self, article_soup: BeautifulSoup) -> str:
        """Takes content of article in form of soup and returns title."""
        pass

    @abstractmethod
    def _get_published_at(self, article_soup: BeautifulSoup) -> datetime:
        """Takes content of article in form of soup and returns published date."""
        pass

    @abstractmethod
    def _get_content(self, article_soup: BeautifulSoup) -> str:
        """Takes content of article in form of soup and returns normalised content."""
        pass

    def parse_article(self, link: str) -> ArticleInfo:
        """Collects all elements of article using functions above
        and returns a dictionary of the data. Returns None if parsing fails."""

        soup = self._get_article_soup(link)

        article_data = ArticleInfo(
            link,
            self._get_title(soup),
            self._get_featured_image_url(soup),
            self._get_author(soup),
            self._get_published_at(soup),
            self._get_content(soup),
            self.media_orm.id
        )

        return article_data
