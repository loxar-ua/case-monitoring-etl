from datetime import datetime

from .base_scrapper import BaseScrapper
from .sitemap_search import get_links_from_sitemap
from ...database.models.media import Media
from src.scrapper.configs import BABEL_CFG

class BabelScrapper(BaseScrapper):

    def __init__(self, media_orm: Media, **kwargs):
        super().__init__(media_orm, **kwargs)

        self.elements_cfg = BABEL_CFG

    def get_links(self, start_date: datetime, end_date: datetime) -> list[str] | None:
        """Takes starting and ending date for scraping articles from sitemap_index.xml."""

        links = get_links_from_sitemap(
            sitemap_index_url=self.media_orm.sitemap_index_url,
            sub_sitemaps_pattern=r"https://babel\.ua/ukrainian/default/2025/(0[1-9]|1[0-1])-(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])\.xml",
            start_date=start_date,
            end_date=end_date,
        )

        return links