from datetime import datetime

from .base_scrapper import BaseScrapper
from .sitemap_search import get_links_from_sitemap
from ...database.models.media import Media
from src.scrapper.configs import CHESNO_CFG

class ChesnoScrapper(BaseScrapper):

    def __init__(self, media_orm: Media, **kwargs):
        super().__init__(media_orm, **kwargs)

        self.elements_cfg = CHESNO_CFG

    def get_links(self, start_date: datetime, end_date: datetime) -> list[str] | None:
        """Takes starting and ending date for scraping articles from sitemap_index.xml."""

        links = get_links_from_sitemap(
            sitemap_index_url=self.media_orm.sitemap_index_url,
            sub_sitemaps_pattern=r"https://www.chesno.org/sitemap-posts.xml",
            start_date=start_date,
            end_date=end_date,
        )

        return links
