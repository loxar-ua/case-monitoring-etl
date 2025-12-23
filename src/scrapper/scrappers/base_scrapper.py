from bs4 import BeautifulSoup

from abc import ABC, abstractmethod
from datetime import datetime
from src.scrapper.scrappers import ArticleInfo

from src.database.models.media import Media
from src.database.get_response import get_response


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

    def _get_element(self, article_soup: BeautifulSoup, cfg: dict):
        """Universal element extractor."""

        tag_name = cfg.get("tag_name")
        if not tag_name:
            return None

        element = article_soup.find(name=tag_name, attrs=cfg.get("tag_attrs", {}))
        if not element:
            return None

        if tag_name == "lastmod":
            return cfg["formatter"](element)

        value = element['content'] if element.has_attr("content") else element
        return cfg["formatter"](value)

    def _get_article_soup(self, link: str) -> BeautifulSoup:
        """Takes link of article and returns the content of articles as BeautifulSoup object."""

        article_response = get_response(link)
        if not article_response:
            return None

        article_soup = BeautifulSoup(article_response.content, "html.parser")

        return article_soup


    def parse_article(self, link: str) -> ArticleInfo | None:
        """Collects all elements of article using functions above
        and returns a dictionary of the data. Returns None if parsing fails."""

        soup = self._get_article_soup(link)
        if not soup:
            return None

        extracted = {}

        for key, cfg in self.elements_cfg.items():
            extracted[key] = self._get_element(soup, cfg)

        content = extracted.get("content")
        print(content)
        published_at = extracted.get("published_at")
        if not content or not published_at:
            return None
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