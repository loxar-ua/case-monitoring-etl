from bs4 import BeautifulSoup

from abc import ABC, abstractmethod
from datetime import datetime
from src.scrapper.scrappers import ArticleInfo

from src.database.models.media import Media
from src.utils.get_response import get_response


class BaseScrapper(ABC):
    def __init__(self, media_orm: Media, **kwargs):
        super().__init__(**kwargs)

        self.elements_cfg = None
        self.media_orm = media_orm

    @abstractmethod
    def get_links(self, start_date: datetime, end_date: datetime) -> list[str]:
        """Takes starting and ending date for scraping articles from sitemap_index.xml.
        Returns a list of links."""
        pass

    def _get_element(self, article_soup: BeautifulSoup, cfg: dict) -> str | None:
        """Unified method that takes html code of article,
        name and attributes of tag to find it and then makes some formatting"""

        element = article_soup.find(
            name=cfg["tag_name"],
            attrs=cfg["tag_attrs"]
        )

        if not element:
            return None

        if element.has_attr("content"):
            value = element['content']
        else:
            value = element

        return cfg["formatter"](value)

    def _get_article_soup(self, link: str) -> BeautifulSoup:
        """Takes link of article and returns the content of articles as BeautifulSoup object."""

        article_response = get_response(link)
        article_soup = BeautifulSoup(article_response.content, "html.parser")

        return article_soup


    def parse_article(self, link: str) -> ArticleInfo:
        """Collects all elements of article using functions above
        and returns a dictionary of the data. Returns None if parsing fails."""

        soup = self._get_article_soup(link)

        extracted = {}

        for key, cfg in self.elements_cfg.items():
            extracted[key] = self._get_element(soup, cfg)

        article_data = ArticleInfo(
            link,
            extracted["title"],
            extracted["featured_image_url"],
            extracted["author"],
            extracted["published_at"],
            extracted["content"],
            self.media_orm.id
        )

        return article_data
