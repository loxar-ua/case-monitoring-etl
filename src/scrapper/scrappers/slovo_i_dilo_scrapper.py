from datetime import datetime

from .base_scrapper import BaseScrapper
from .yoast_sitemap_tyzhden import get_links_yoast
from ...database.models.media import Media
from src.scrapper.configs import SLOVO_CFG

class SlovoScrapper(BaseScrapper):

        def __init__(self, media_orm: Media, **kwargs):
            super().__init__(media_orm, **kwargs)

            self.elements_cfg = SLOVO_CFG

        def get_links(self, start_date: datetime, end_date: datetime) -> list[str] | None:
            """Takes starting and ending date for scraping articles from sitemap_index.xml."""

            links = get_links_yoast(
                sitemap_index_url=self.media_orm.sitemap_index_url,
                sub_sitemaps_pattern=r"https://www\.slovoidilo\.ua/sitemap/monthly_(202[5-9]|20[3-9]\d|\d{4})-\d{2}_uk\.xml",
                start_date=start_date,
                end_date=end_date,

            )

            return links
