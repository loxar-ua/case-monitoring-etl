from datetime import datetime

from src.scrapper.scrappers.base_scrapper import BaseScrapper
from src.scrapper.scrappers.sitemap_search import get_links_from_sitemap
from src.database.models.media import Media
from src.scrapper.configs import GROSHI_CFG

class NashiGroshiScrapper(BaseScrapper):

    def __init__(self, media_orm: Media, **kwargs):
        super().__init__(media_orm, **kwargs)

        self.elements_cfg = GROSHI_CFG

    def get_links(self, start_date: datetime, end_date: datetime) -> list[str] | None:
        """Takes starting and ending date for scraping articles from sitemap_index.xml."""

        links = get_links_from_sitemap(
            sitemap_index_url=self.media_orm.sitemap_index_url,
            sub_sitemaps_pattern=r"https://nashigroshi\.org/sitemap-pt-post-(202[5-9]|20[3-9]\d)-\d{2}\.xml",
            start_date=start_date,
            end_date=end_date,
        )

        return links